import streamlit as pd_st  # using streamlit
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

from nlp_analyzer import LifestyleNLPAnalyzer
from clustering import PatternClustering
from sample_data import get_sample_dataframe

# Konfiguracja strony Streamlit
st.set_page_config(
    page_title="Digital Media Success Patterns",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Wstrzyknięcie czystego i premium stylu CSS do interfejsu
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* Główna typografia */
html, body, [class*="css"], .stMarkdown {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Stylizacja kart KPI */
.kpi-container {
    display: flex;
    gap: 16px;
    margin-bottom: 24px;
    flex-wrap: wrap;
}
.kpi-card {
    flex: 1;
    min-width: 220px;
    background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.kpi-card:hover {
    transform: translateY(-4px);
    border-color: rgba(99, 102, 241, 0.4);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 0 15px rgba(99, 102, 241, 0.15);
}
.kpi-title {
    font-size: 0.75rem;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.075em;
    font-weight: 700;
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 1.85rem;
    font-weight: 800;
    color: #F8FAFC;
    line-height: 1.2;
}
.kpi-subtitle {
    font-size: 0.8rem;
    color: #10B981;
    margin-top: 8px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 4px;
}

/* Tabela premium */
.premium-table-container {
    overflow-x: auto;
    border-radius: 16px;
    border: 1px solid rgba(148, 163, 184, 0.15);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    margin: 20px 0;
}
.premium-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    background-color: #0F172A;
}
.premium-table th {
    background-color: #1E293B;
    color: #F1F5F9;
    font-weight: 700;
    text-align: left;
    padding: 16px 20px;
    font-size: 0.85rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    border-bottom: 2px solid #334155;
}
.premium-table td {
    padding: 16px 20px;
    font-size: 0.88rem;
    color: #E2E8F0;
    border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    vertical-align: middle;
}
.premium-table tr:last-child td {
    border-bottom: none;
}
.premium-table tr:hover td {
    background-color: #1E293B;
}

/* Kolorowe Badge dla wzorców NLP */
.badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    margin: 2px;
    text-transform: uppercase;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.badge-poradnictwo { background-color: rgba(249, 115, 22, 0.15); color: #FF781F; border: 1.5px solid rgba(249, 115, 22, 0.35); }
.badge-emocjonalny_trigger { background-color: rgba(239, 68, 68, 0.15); color: #FF5A5A; border: 1.5px solid rgba(239, 68, 68, 0.35); }
.badge-kolor { background-color: rgba(168, 85, 247, 0.15); color: #B96BFF; border: 1.5px solid rgba(168, 85, 247, 0.35); }
.badge-czesc_garderoby { background-color: rgba(59, 130, 246, 0.15); color: #5097FF; border: 1.5px solid rgba(59, 130, 246, 0.35); }
.badge-sezon { background-color: rgba(16, 185, 129, 0.15); color: #1BD89A; border: 1.5px solid rgba(16, 185, 129, 0.35); }
.badge-trend_rok { background-color: rgba(234, 179, 8, 0.15); color: #F5C425; border: 1.5px solid rgba(234, 179, 8, 0.35); }
.badge-marka { background-color: rgba(236, 72, 153, 0.15); color: #FF66B6; border: 1.5px solid rgba(236, 72, 153, 0.35); }
.badge-adresat { background-color: rgba(20, 184, 166, 0.15); color: #2AD1BE; border: 1.5px solid rgba(20, 184, 166, 0.35); }
.badge-ogolny_lifestyle { background-color: rgba(148, 163, 184, 0.15); color: #94A3B8; border: 1.5px solid rgba(148, 163, 184, 0.35); }

/* Pigułki wzrostu ruchu (LIFT PILL) */
.lift-pill {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
    box-shadow: 0 2px 4px rgba(0,0,0,0.15);
}
.lift-pill-high { background-color: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.4); }
.lift-pill-med { background-color: rgba(245, 158, 11, 0.15); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.4); }
.lift-pill-low { background-color: rgba(148, 163, 184, 0.15); color: #94A3B8; border: 1px solid rgba(148, 163, 184, 0.4); }

/* Przykłady tytułów */
.example-box {
    margin-top: 6px;
    border-left: 2px solid #6366F1;
    padding-left: 10px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}
.example-item {
    font-size: 0.8rem;
    color: #94A3B8;
}
.example-link {
    color: #C084FC;
    text-decoration: none;
    font-weight: 500;
}
.example-link:hover {
    color: #A855F7;
    text-decoration: underline;
}
.example-traffic {
    color: #10B981;
    font-weight: 600;
    margin-left: 4px;
}
</style>
""", unsafe_allow_html=True)

# Inicjalizacja NLP i clusteringu
@st.cache_resource
def load_nlp_analyzer():
    return LifestyleNLPAnalyzer()

analyzer = load_nlp_analyzer()
clusterer = PatternClustering(analyzer)

# --- SIDEBAR (PANEL STEROWANIA) ---
with st.sidebar:
    st.markdown("<h2 style='color: #6366F1; margin-bottom: 0;'>⚡ Success Patterns</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; margin-top: 0; margin-bottom: 24px;'>Lifestyle Article Traffic Analyzer</p>", unsafe_allow_html=True)
    
    st.markdown("### 📥 Import Danych")
    uploaded_files = st.file_uploader(
        "Wgraj pliki z artykułami (Excel / CSV)",
        type=["csv", "xlsx"],
        accept_multiple_files=True,
        help="Możesz wgrać jeden lub więcej plików zawierających kolumny z tytułem artykułu oraz liczbą kliknięć."
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Konfiguracja Algorytmu")
    
    min_articles = st.slider(
        "Min. artykułów na wzorzec",
        min_value=2,
        max_value=8,
        value=3,
        help="Minimalna liczba artykułów przypisanych do wzorca, by był brany pod uwagę."
    )
    
    sort_by = st.selectbox(
        "Sortuj ranking według:",
        options=["Mediana vs witryna", "Średnia klikalność", "Łączny ruch"],
        index=0
    )
    
    st.markdown("---")
    # Generowanie pliku demonstracyjnego do pobrania
    sample_df = get_sample_dataframe()
    csv_buffer = BytesIO()
    sample_df.to_csv(csv_buffer, index=False, encoding='utf-8')
    csv_data = csv_buffer.getvalue()
    
    st.download_button(
        label="📥 Pobierz plik demonstracyjny (CSV)",
        data=csv_data,
        file_name="lifestyle_articles_sample.csv",
        mime="text/csv",
        help="Pobierz przykładowe dane w formacie CSV, aby przetestować wgrywanie plików."
    )

# --- GŁÓWNY PANEL ---
st.title("Lifestyle Traffic Analyzer & Pattern Generator")
st.markdown("Analizuj strukturę gramatyczno-tematyczną artykułów lifestyle za pomocą NLP i odkrywaj najbardziej dochodowe wzorce SEO.")

# Sprawdzenie wczytania danych
if uploaded_files:
    dfs = []
    loaded_names = []
    for file in uploaded_files:
        try:
            if file.name.endswith('.csv'):
                temp_df = pd.read_csv(file, encoding='utf-8')
                dfs.append(temp_df)
                loaded_names.append(f"• {file.name} ({len(temp_df)} wierszy)")
            else:
                xls = pd.ExcelFile(file)
                sheet_names = xls.sheet_names
                loaded_sheet = None
                
                for sheet in sheet_names:
                    sheet_df = pd.read_excel(xls, sheet_name=sheet)
                    if not sheet_df.empty:
                        # Sprawdzamy, czy arkusz zawiera dane URL-i
                        has_url = False
                        for col in sheet_df.columns:
                            col_lower = str(col).lower()
                            if any(x in col_lower for x in ["url", "link", "adres"]):
                                has_url = True
                                break
                        if not has_url:
                            str_cols = sheet_df.select_dtypes(include=['object']).columns
                            for col in str_cols:
                                if sheet_df[col].astype(str).str.contains("http").any():
                                    has_url = True
                                    break
                        if has_url:
                            loaded_sheet = (sheet, sheet_df)
                            break
                
                if loaded_sheet:
                    temp_df = loaded_sheet[1]
                    dfs.append(temp_df)
                    loaded_names.append(f"• {file.name} (Arkusz: '{loaded_sheet[0]}', {len(temp_df)} wierszy)")
                else:
                    # Fallback do pierwszego arkusza, jeśli żaden nie zawiera URL-i
                    temp_df = pd.read_excel(xls, sheet_name=sheet_names[0])
                    dfs.append(temp_df)
                    loaded_names.append(f"• {file.name} (Arkusz: '{sheet_names[0]}' - brak URL, {len(temp_df)} wierszy)")
        except Exception as e:
            st.sidebar.error(f"Błąd podczas wczytywania {file.name}: {e}")
            
    if dfs:
        df = pd.concat(dfs, ignore_index=True)
        st.sidebar.success(f"Załadowano {len(dfs)} plik(ów):\n" + "\n".join(loaded_names))
    else:
        st.error("Nie udało się załadować żadnego pliku. Użycie danych demo.")
        df = sample_df
else:
    # Komunikat o użyciu danych demonstracyjnych
    st.info("ℹ️ Brak wgranych plików. Aplikacja prezentuje analizę na bazie wbudowanych danych demonstracyjnych (Polski portal lifestyle).")
    df = sample_df

# Autodetekcja kolumn i prezentacja struktury użytkownikowi
from clustering import detect_columns
detected_cols = detect_columns(df)

# Panel boczny - Mapowanie wykrytych kolumn
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📊 Mapowanie Kolumn")
    st.info("💡 Automatycznie wykryliśmy strukturę danych w plikach. Jeśli chcesz, możesz zmienić przypisanie kolumn poniżej:")
    
    cols_list = list(df.columns)
    
    # Wyznaczenie domyślnych indeksów
    try:
        title_idx = cols_list.index(detected_cols["title_col"])
    except ValueError:
        title_idx = 0
        
    try:
        clicks_idx = cols_list.index(detected_cols["clicks_col"])
    except ValueError:
        clicks_idx = 0
        
    try:
        url_idx = cols_list.index(detected_cols["url_col"])
    except ValueError:
        url_idx = 0
        
    title_col_override = st.selectbox(
        "📝 Kolumna z Tytułem / Nagłówkiem",
        options=cols_list,
        index=title_idx,
        help="Kolumna zawierająca tytuły artykułów, które zostaną przeanalizowane pod kątem wzorców NLP."
    )
    
    clicks_col_override = st.selectbox(
        "📈 Kolumna z Kliknięciami / Ruchem",
        options=cols_list,
        index=clicks_idx,
        help="Kolumna numeryczna z liczbą kliknięć/odsłon, służąca do kalkulacji mediany i wskaźników sukcesu."
    )
    
    url_col_override = st.selectbox(
        "🔗 Kolumna z Adresem URL / Linkiem",
        options=cols_list,
        index=url_idx,
        help="Kolumna zawierająca linki do artykułów (wykorzystywana do generowania klikalnych przykładów)."
    )
    
    # Wyświetlanie ostrzeżeń i komunikatów autodetekcji w pasku bocznym
    if detected_cols["warnings"]:
        for warning_msg in detected_cols["warnings"]:
            st.sidebar.warning(f"⚠️ {warning_msg}")

# Uruchomienie klastrowania z uwzględnieniem mapowania kolumn
with st.spinner("Analizowanie tytułów za pomocą NLP i klastrowanie struktur..."):
    patterns, site_stats, raw_articles = clusterer.analyze_dataset(
        df, 
        min_articles=min_articles,
        title_col=title_col_override,
        clicks_col=clicks_col_override,
        url_col=url_col_override
    )

# Sortowanie wzorców na podstawie wybranej opcji
if sort_by == "Średnia klikalność":
    patterns = sorted(patterns, key=lambda x: x["avg_clicks"], reverse=True)
elif sort_by == "Łączny ruch":
    patterns = sorted(patterns, key=lambda x: x["total_clicks"], reverse=True)
else:
    patterns = sorted(patterns, key=lambda x: x["med_vs_site"], reverse=True)

# Obliczenie Pattern Lift (Średni lift top 10)
avg_lift = np.mean([p["med_vs_site"] for p in patterns]) if patterns else 100.0

# --- KPI CARDS SECTION ---
kpi_html = f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-title">Analizowane Artykuły</div>
        <div class="kpi-value">{site_stats['total_articles']}</div>
        <div class="kpi-subtitle" style="color: #6366F1;">Pełny zbiór danych</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Łączny Ruch Witryny</div>
        <div class="kpi-value">{site_stats['site_total_clicks']:,}</div>
        <div class="kpi-subtitle" style="color: #3B82F6;">Kliknięć łącznie</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Mediana Ruchu Witryny</div>
        <div class="kpi-value">{int(site_stats['site_median']):,}</div>
        <div class="kpi-subtitle" style="color: #94A3B8;">Punkt odniesienia</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Średni Lift Top 10 Wzorców</div>
        <div class="kpi-value">+{avg_lift - 100:.1f}%</div>
        <div class="kpi-subtitle" style="color: #10B981;">vs Mediana Witryny</div>
    </div>
</div>
"""
kpi_html_clean = "\n".join([line.strip() for line in kpi_html.split("\n")])
st.markdown(kpi_html_clean, unsafe_allow_html=True)

# Pomocnicza funkcja do budowania HTML wzorca (badge)
def build_pattern_html(pattern_str: str) -> str:
    if pattern_str == "[OGÓLNY_LIFESTYLE]":
        return f'<span class="badge badge-ogolny_lifestyle">[OGÓLNY LIFESTYLE]</span>'
    
    parts = pattern_str.split(" + ")
    html_badges = []
    
    # Słownik mapowania kluczy na ładne etykiety UI
    label_mapping = {
        "czesc_garderoby": "CZĘŚĆ GARDEROBY",
        "emocjonalny_trigger": "EMOCJONALNY TRIGGER",
        "trend_rok": "TREND / ROK",
        "poradnictwo": "PORADNICTWO",
        "kolor": "KOLOR",
        "sezon": "SEZON",
        "marka": "MARKA",
        "adresat": "ADRESAT"
    }
    
    for part in parts:
        clean_part = part.replace("[", "").replace("]", "").lower()
        badge_class = f"badge-{clean_part}"
        display_label = label_mapping.get(clean_part, clean_part.upper().replace("_", " "))
        html_badges.append(f'<span class="badge {badge_class}">[{display_label}]</span>')
    return " + ".join(html_badges)

# --- TABELA RANKINGOWA ---
st.subheader("🏆 Top 10 Rekomendowanych Wzorców Sukcesu")
st.markdown("Poniższa tabela przedstawia ranking unikalnych kombinacji tagów językowych, które generują ponadprzeciętny ruch.")

if not patterns:
    st.warning("Nie znaleziono wzorców spełniających kryteria. Spróbuj zmniejszyć wartość 'Min. artykułów na wzorzec' w panelu bocznym.")
else:
    # Budowanie kodu HTML tabeli rankingu
    table_rows = []
    for i, pat in enumerate(patterns):
        # Formatowanie pigułki lift
        lift = pat["med_vs_site"]
        if lift >= 200:
            lift_class = "lift-pill-high"
            lift_text = f"⚡ {lift:.0f}% witryny"
        elif lift >= 130:
            lift_class = "lift-pill-med"
            lift_text = f"↗ {lift:.0f}% witryny"
        else:
            lift_class = "lift-pill-low"
            lift_text = f"{lift:.0f}% witryny"
            
        pattern_html = build_pattern_html(pat["pattern"])
        
        # Budowanie HTML dla przykładów tytułów (ukryte pod akordeonem details/summary)
        examples_html = []
        for ex in pat["examples"]:
            examples_html.append(
                f'<div class="example-item" style="margin-bottom: 4px;">'
                f'• <a class="example-link" href="{ex["url"]}" target="_blank">{ex["title"]}</a> '
                f'<span class="example-traffic">({ex["clicks"]:,} kliknięć)</span>'
                f'</div>'
            )
        
        examples_section_html = f"""
        <details style="cursor: pointer; outline: none; margin-top: 2px;">
            <summary style="color: #C084FC; font-weight: 600; font-size: 0.8rem; outline: none; user-select: none;">
                Rozwiń przykłady ({len(pat['examples'])})
            </summary>
            <div class="example-box" style="margin-top: 6px;">{"".join(examples_html)}</div>
        </details>
        """
        
        row_html = f"""
        <tr>
            <td style="font-weight: 800; font-size: 1.05rem; text-align: center; width: 50px; color: #8B5CF6;">#{i+1}</td>
            <td style="font-weight: 600; width: 40%;">{pattern_html}</td>
            <td style="font-weight: 700; text-align: right; color: #F1F5F9; width: 130px;">{int(pat['avg_clicks']):,}</td>
            <td style="text-align: center; width: 150px;">
                <span class="lift-pill {lift_class}">{lift_text}</span>
            </td>
            <td style="font-weight: 600; text-align: right; color: #10B981; width: 110px;">{pat['traffic_share']:.2f}%</td>
            <td>{examples_section_html}</td>
        </tr>
        """
        table_rows.append(row_html)
        
    table_html = f"""
    <div class="premium-table-container">
        <table class="premium-table">
            <thead>
                <tr>
                    <th style="text-align: center; width: 50px;">Poz.</th>
                    <th style="width: 40%;">Zidentyfikowany Wzorzec Sukcesu</th>
                    <th style="text-align: right; width: 130px;">Śr. Klikalność</th>
                    <th style="text-align: center; width: 150px;">Mediana vs Witryna</th>
                    <th style="text-align: right; width: 110px;">Udział w ruchu</th>
                    <th>Najlepsze Przykłady Artykułów (Top 3)</th>
                </tr>
            </thead>
            <tbody>
                {"".join(table_rows)}
            </tbody>
        </table>
    </div>
    """
    # Usuwamy wiodące spacji z każdej linii HTML, aby zapobiec interpretowaniu ich przez Markdown jako blok kodu
    table_html_clean = "\n".join([line.strip() for line in table_html.split("\n")])
    st.markdown(table_html_clean, unsafe_allow_html=True)

st.markdown("---")

# --- WIZUALIZACJE DANYCH ---
st.subheader("📊 Analiza Wizualna Tematów i Wzorców")

if patterns:
    tab1, tab2, tab3 = st.tabs([
        "📈 Efektywność Wzorców (Mediana vs Witryna)", 
        "🔮 Portfolio Wzorców (Popularność vs Skuteczność)",
        "🌿 Mapa Tagów Językowych"
    ])
    
    with tab1:
        # Wykres słupkowy
        chart_data = pd.DataFrame(patterns)
        # Czyszczenie nazw wzorców do wykresu
        chart_data["simple_pattern"] = chart_data["pattern"].str.replace("[", "").str.replace("]", "")
        
        fig1 = px.bar(
            chart_data,
            x="med_vs_site",
            y="simple_pattern",
            orientation="h",
            color="med_vs_site",
            color_continuous_scale=["#334155", "#6366F1", "#8B5CF6"],
            labels={
                "med_vs_site": "Mediana kliknięć vs Mediana Witryny [%]",
                "simple_pattern": "Zidentyfikowany Wzorzec"
            },
            title="Skuteczność Wzorców w porównaniu do Medianu Witryny (100% = Linia bazowa witryny)"
        )
        # Linia bazowa witryny (100%)
        fig1.add_vline(x=100, line_dash="dash", line_color="#EF4444", annotation_text="Mediana Witryny")
        fig1.update_layout(
            height=450,
            template="plotly_dark",
            paper_bgcolor="#0F172A",
            plot_bgcolor="#0F172A",
            font_family="Plus Jakarta Sans",
            margin=dict(l=20, r=20, t=40, b=20),
            yaxis={'categoryorder':'total ascending'}
        )
        st.plotly_chart(fig1, width="stretch")
        
    with tab2:
        # Bubble chart (Growth-Share Matrix)
        fig2 = px.scatter(
            chart_data,
            x="n_articles",
            y="med_vs_site",
            size="traffic_share",
            color="med_vs_site",
            hover_name="simple_pattern",
            labels={
                "n_articles": "Liczba artykułów z wzorcem",
                "med_vs_site": "Mediana vs Witryna [%]",
                "traffic_share": "Udział w ruchu [%]"
            },
            title="Macierz Wzorców: Wolumen artykułów vs Efektywność (Rozmiar bąbelka = Udział w ruchu)"
        )
        fig2.add_hline(y=100, line_dash="dash", line_color="#EF4444")
        fig2.update_layout(
            height=450,
            template="plotly_dark",
            paper_bgcolor="#0F172A",
            plot_bgcolor="#0F172A",
            font_family="Plus Jakarta Sans",
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig2, width="stretch")
        
    with tab3:
        # Wykres rozkładu poszczególnych tagów i ich średnich kliknięć
        # Budujemy treemap na podstawie unikalnych tagów i ich wystąpień
        tag_occurrences = []
        for art in raw_articles:
            for cat, val_info in art["tags"].items():
                tag_occurrences.append({
                    "Kategoria": cat,
                    "Tag": val_info["value"].lower(),
                    "clicks": art["clicks"]
                })
        
        if tag_occurrences:
            tag_df = pd.DataFrame(tag_occurrences)
            tag_summary = tag_df.groupby(["Kategoria", "Tag"]).agg(
                n_articles=("clicks", "count"),
                avg_clicks=("clicks", "mean")
            ).reset_index()
            
            fig3 = px.treemap(
                tag_summary,
                path=["Kategoria", "Tag"],
                values="n_articles",
                color="avg_clicks",
                color_continuous_scale=["#334155", "#6366F1", "#10B981"],
                labels={
                    "n_articles": "Liczba wystąpień",
                    "avg_clicks": "Średnia klikalność tagu"
                },
                title="Struktura tagów: Popularność (Rozmiar pola) vs Skuteczność (Kolor)"
            )
            fig3.update_layout(
                height=500,
                template="plotly_dark",
                paper_bgcolor="#0F172A",
                plot_bgcolor="#0F172A",
                font_family="Plus Jakarta Sans",
                margin=dict(l=10, r=10, t=40, b=10)
            )
            st.plotly_chart(fig3, width="stretch")
        else:
            st.info("Brak wystarczającej liczby wyodrębnionych tagów do wygenerowania mapy.")

st.markdown("---")

# --- INTERAKTYWNY SANDBOX NLP (PLAYGROUND) ---
st.subheader("⚡ Interaktywny Sandbox NLP (Playground)")
st.markdown("Sprawdź, jak system NLP rozpozna i sklasyfikuje Twój własny tytuł lifestyle oraz jaki przypisze mu szacowany wskaźnik ruchu.")

col1, col2 = st.columns([2, 1])

with col1:
    user_title = st.text_input(
        "Wpisz testowy tytuł artykułu:",
        value="Jak nosić czerwone szpilki wiosną 2026? Absolutny hit dla 50-latki!",
        placeholder="Wpisz np. Czarny sweter na zimę za 50 zł z Zara..."
    )
    
    if user_title:
        # Analiza
        user_tags = analyzer.extract_tags(user_title)
        user_pattern = analyzer.get_pattern_string(user_tags)
        
        # Wyświetlanie sformatowanego wzorca
        st.markdown("#### Wykryty wzorzec strukturalny:")
        st.markdown(build_pattern_html(user_pattern), unsafe_allow_html=True)
        
        # Wyświetlanie szczegółowych tagów w postaci tabeli
        if user_tags:
            tag_rows = []
            for cat, info in user_tags.items():
                tag_rows.append({
                    "Kategoria": cat,
                    "Wykryte Słowo": info["value"],
                    "Pozycja w tekście": info["start"]
                })
            st.dataframe(pd.DataFrame(tag_rows), hide_index=True, width="stretch")
        else:
            st.info("System NLP nie wykrył w tytule żadnych predefiniowanych tagów lifestylowych.")

with col2:
    if user_title and user_tags:
        # Szukamy czy ten wzorzec (lub jego część) występuje w Top 10 lub bazie
        matched_db_pattern = None
        for pat in patterns:
            # Sprawdzamy pełne dopasowanie lub zawieranie się podwzorców
            if pat["pattern"] == user_pattern:
                matched_db_pattern = pat
                break
                
        st.markdown("#### Estymacja skuteczności:")
        if matched_db_pattern:
            st.markdown(f"""
            <div style="background-color: rgba(16, 185, 129, 0.15); border: 1.5px solid #10B981; border-radius: 12px; padding: 15px; text-align: center;">
                <span style="font-size: 2.2rem; font-weight: 800; color: #10B981;">{matched_db_pattern['med_vs_site']:.0f}%</span>
                <p style="margin: 5px 0 0 0; color: #F1F5F9; font-weight: 600; font-size: 0.9rem;">Wysoka zgodność z Top Wzorcem #{patterns.index(matched_db_pattern)+1}</p>
                <p style="margin: 2px 0 0 0; color: #94A3B8; font-size: 0.8rem;">Ten wzorzec generuje średnio {int(matched_db_pattern['avg_clicks']):,} kliknięć.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Sprawdzenie czy w ogóle w bazie jest ten wzorzec
            matched_anywhere = False
            for art in raw_articles:
                if art["full_pattern"] == user_pattern:
                    matched_anywhere = True
                    break
                    
            if matched_anywhere:
                st.markdown(f"""
                <div style="background-color: rgba(234, 179, 8, 0.15); border: 1.5px solid #EAB308; border-radius: 12px; padding: 15px; text-align: center;">
                    <span style="font-size: 2.0rem; font-weight: 800; color: #EAB308;">Umiarkowana</span>
                    <p style="margin: 5px 0 0 0; color: #F1F5F9; font-weight: 600; font-size: 0.9rem;">Wzorzec znany w bazie, ale poza Top 10</p>
                    <p style="margin: 2px 0 0 0; color: #94A3B8; font-size: 0.8rem;">Wzorzec został wykryty, ale ma niższy wskaźnik ruchu.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background-color: rgba(148, 163, 184, 0.15); border: 1.5px solid #94A3B8; border-radius: 12px; padding: 15px; text-align: center;">
                    <span style="font-size: 2.0rem; font-weight: 800; color: #94A3B8;">Dziewiczy Wzorzec</span>
                    <p style="margin: 5px 0 0 0; color: #F1F5F9; font-weight: 600; font-size: 0.9rem;">Całkowicie nowa struktura językowa</p>
                    <p style="margin: 2px 0 0 0; color: #94A3B8; font-size: 0.8rem;">Wzorzec nie posiada dotychczasowych danych historycznych.</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.write("Wpisz tytuł po lewej, aby otrzymać prognozę ruchu.")
