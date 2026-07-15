import pandas as pd
import numpy as np
from itertools import combinations
from nlp_analyzer import LifestyleNLPAnalyzer

def detect_columns(df: pd.DataFrame) -> dict:
    """
    Automatycznie rozpoznaje, które kolumny zawierają Tytuł, Kliknięcia (Ruch) oraz URL.
    """
    title_col = None
    clicks_col = None
    url_col = None
    warnings = []
    
    # 1. Poszukiwanie kolumny z ruchem
    for col in df.columns:
        col_lower = str(col).lower()
        if any(x in col_lower for x in ["click", "klik", "odsłon", "traffic", "ruch", "pv", "pageview", "odsłony", "wyświetlenia"]):
            clicks_col = col
            break
            
    # 2. Poszukiwanie kolumny z tytułem
    for col in df.columns:
        col_lower = str(col).lower()
        if col != clicks_col:
            if any(x in col_lower for x in ["title", "tytuł", "slug", "nagłówek", "h1", "nazwa"]):
                title_col = col
                break
                
    # 3. Poszukiwanie kolumny z URL
    for col in df.columns:
        col_lower = str(col).lower()
        if col not in [clicks_col, title_col]:
            if any(x in col_lower for x in ["url", "link", "adres"]):
                url_col = col
                break
                
    # Fallbacki
    if not clicks_col:
        num_cols = df.select_dtypes(include=['number']).columns
        if len(num_cols) > 0:
            clicks_col = num_cols[0]
            warnings.append(f"Auto-wykryto ruch: '{clicks_col}' (typ numeryczny)")
        else:
            clicks_col = df.columns[0]
            warnings.append(f"Użyto pierwszej kolumny jako ruchu: '{clicks_col}'")
            
    if not title_col:
        str_cols = df.select_dtypes(include=['object']).columns
        str_cols = [c for c in str_cols if c != clicks_col]
        if len(str_cols) > 0:
            title_col = str_cols[0]
            warnings.append(f"Auto-wykryto tytuł: '{title_col}' (typ tekstowy)")
        else:
            title_col = df.columns[0]
            warnings.append(f"Użyto pierwszej kolumny jako tytułu: '{title_col}'")
            
    if not url_col:
        string_cols = df.select_dtypes(include=['object']).columns
        string_cols = [c for c in string_cols if c not in [clicks_col, title_col]]
        for col in string_cols:
            if df[col].astype(str).str.contains("http").any():
                url_col = col
                break
        if not url_col:
            url_col = title_col
            warnings.append(f"Nie znaleziono kolumny URL. Użyto tytułu: '{url_col}'")
            
    return {
        "title_col": title_col,
        "clicks_col": clicks_col,
        "url_col": url_col,
        "warnings": warnings
    }

class PatternClustering:
    def __init__(self, analyzer: LifestyleNLPAnalyzer):
        self.analyzer = analyzer

    def analyze_dataset(self, df: pd.DataFrame, min_articles: int = 3, 
                        title_col: str = None, clicks_col: str = None, url_col: str = None) -> tuple:
        """
        Analizuje zbiór danych, wyodrębnia tagi i wzorce dla każdego artykułu,
        a następnie klastruje je i zwraca Top 10 wzorców oraz ogólne statystyki witryny.
        """
        # 1. Klonowanie i przygotowanie danych
        df = df.copy()
        
        # Jeśli nie podano kolumn, wykonaj autodetekcję
        if not title_col or not clicks_col or not url_col:
            detected = detect_columns(df)
            title_col = title_col or detected["title_col"]
            clicks_col = clicks_col or detected["clicks_col"]
            url_col = url_col or detected["url_col"]

        # Czyszczenie i konwersja
        df[clicks_col] = pd.to_numeric(df[clicks_col], errors='coerce').fillna(0).astype(int)
        df[title_col] = df[title_col].astype(str)
        df[url_col] = df[url_col].astype(str)

        # Agregacja duplikatów (przydatne przy łączeniu danych z wielu plików)
        df = df.groupby([url_col, title_col], as_index=False)[clicks_col].sum()

        # 2. Obliczanie statystyk bazowych witryny (benchmark)
        site_median = float(df[clicks_col].median())
        site_mean = float(df[clicks_col].mean())
        site_total_clicks = int(df[clicks_col].sum())
        total_articles = len(df)

        if site_median == 0:
            site_median = 1.0  # zapobieganie dzieleniu przez zero

        # 3. Ekstrakcja tagów dla każdego artykułu
        articles_data = []
        for idx, row in df.iterrows():
            title = row[title_col]
            clicks = row[clicks_col]
            url = row[url_col]
            
            tags = self.analyzer.extract_tags(title)
            full_pattern = self.analyzer.get_pattern_string(tags)
            
            articles_data.append({
                "index": idx,
                "title": title,
                "clicks": clicks,
                "url": url,
                "tags": tags,  # format: { KATEGORIA: {"value": X, "start": pos} }
                "full_pattern": full_pattern
            })

        # 4. Generowanie i ocena kandydatów na wzorce (podwzorce kombinacji tagów)
        # Chcemy znaleźć sekwencje tagów, np. [KOLOR] + [CZĘŚĆ_GARDEROBY]
        pattern_candidates = {}

        for art in articles_data:
            tags = art["tags"]
            if not tags:
                continue
            
            # Sortujemy kategorie według ich pozycji startowej w tytule
            sorted_tags = sorted(tags.items(), key=lambda x: x[1]["start"])
            categories = [cat for cat, info in sorted_tags]
            
            # Generujemy pod-kombinacje o długości od 2 do 4 tagów, zachowując kolejność występowania
            combos = []
            for r in range(2, min(5, len(categories) + 1)):
                for combo in combinations(categories, r):
                    combos.append(" + ".join([f"[{cat}]" for cat in combo]))
            
            # Dodajemy też pojedyncze tagi o długości 1, aby sprawdzić ich ogólną skuteczność
            for cat in categories:
                combos.append(f"[{cat}]")

            # Przypisujemy artykuł do każdego wygenerowanego wzorca
            for pat in set(combos):
                if pat not in pattern_candidates:
                    pattern_candidates[pat] = []
                pattern_candidates[pat].append(art)

        # 5. Obliczanie statystyk dla każdego wzorca
        pattern_stats = []
        for pat, matched_arts in pattern_candidates.items():
            n_matched = len(matched_arts)
            if n_matched < min_articles:
                continue
                
            clicks_list = [art["clicks"] for art in matched_arts]
            pat_median = float(np.median(clicks_list))
            pat_mean = float(np.mean(clicks_list))
            pat_total = int(np.sum(clicks_list))
            
            # Wskaźnik "Mediana vs witryna"
            med_vs_site = (pat_median / site_median) * 100.0
            
            # Udział w ruchu
            traffic_share = (pat_total / site_total_clicks) * 100.0 if site_total_clicks > 0 else 0.0
            
            # Pobieramy 3 najlepsze przykłady (sortowanie po kliknięciach desc)
            sorted_matched = sorted(matched_arts, key=lambda x: x["clicks"], reverse=True)
            top_examples = []
            for art in sorted_matched[:3]:
                top_examples.append({
                    "title": art["title"],
                    "clicks": art["clicks"],
                    "url": art["url"]
                })
                
            # Zbieramy indeksy artykułów pasujących do wzorca (do celów deduplikacji)
            matched_indices = set(art["index"] for art in matched_arts)

            pattern_stats.append({
                "pattern": pat,
                "n_articles": n_matched,
                "median_clicks": pat_median,
                "avg_clicks": pat_mean,
                "total_clicks": pat_total,
                "med_vs_site": med_vs_site,
                "traffic_share": traffic_share,
                "examples": top_examples,
                "indices": matched_indices,
                "n_variables": pat.count("[")  # liczba zmiennych w szablonie
            })

        # 6. Klastrowanie i dywersyfikacja (Greedy set coverage diversity filter)
        # Chcemy wybrać Top 10 najbardziej efektywnych wzorców, zapobiegając duplikacji tych samych zestawów artykułów.
        # Sortujemy według wskaźnika "Mediana vs witryna" malejąco.
        pattern_stats_sorted = sorted(pattern_stats, key=lambda x: x["med_vs_site"], reverse=True)
        
        selected_patterns = []
        for pat in pattern_stats_sorted:
            if len(selected_patterns) >= 10:
                break
                
            # Sprawdzamy nakładanie się z już wybranymi wzorcami
            is_redundant = False
            for sel in selected_patterns:
                # Obliczamy Jaccard similarity między zestawami pasujących artykułów
                intersection = len(pat["indices"].intersection(sel["indices"]))
                union = len(pat["indices"].union(sel["indices"]))
                jaccard = intersection / union if union > 0 else 0
                
                # Jeśli udziały artykułów pokrywają się w ponad 65%, traktujemy je jako nadmiarowe
                if jaccard > 0.65:
                    # Preferujemy wzorzec o większej liczbie zmiennych (bardziej szczegółowy/świeży)
                    # chyba że ten nowy ma mniejszą szczegółowość i duży overlap, wtedy odrzucamy
                    if pat["n_variables"] <= sel["n_variables"]:
                        is_redundant = True
                        break
            
            if not is_redundant:
                selected_patterns.append(pat)

        # Usunięcie 'indices' przed zwróceniem wyników na front
        for pat in selected_patterns:
            if "indices" in pat:
                del pat["indices"]

        # 7. Zwracamy statystyki witryny i ranking Top 10
        site_stats = {
            "total_articles": total_articles,
            "site_median": site_median,
            "site_mean": site_mean,
            "site_total_clicks": site_total_clicks
        }
        
        return selected_patterns, site_stats, articles_data
