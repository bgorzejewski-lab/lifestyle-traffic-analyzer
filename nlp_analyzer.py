import re
import spacy

# Definicje kategorii tagów dla rynku lifestyle
CATEGORIES = {
    "PORADNICTWO": {
        "lemmas": ["poradnik", "trik", "porada", "instrukcja", "sposób"],
        "stems": ["poradn", "trik", "porad", "instrukc", "sposób"],
        "phrases": [
            "jak nosić", "jak łączyć", "jak ubrać", "jak stylizować", 
            "jak dobrać", "sposób na", "jak się ubrać", "triki na", 
            "porady na", "jak wyglądać"
        ]
    },
    "EMOCJONALNY_TRIGGER": {
        "lemmas": [
            "wpadka", "błąd", "koszmar", "szok", "rewolucja", "szał", "obłędny", 
            "gwiazda", "królować", "klasa", "szyk", "elegancja", "zachwycać", 
            "odmładzać", "wyszczuplać", "postarzać", "pogrubiać", "dramat", "hit"
        ],
        "stems": [
            "wpadk", "błąd", "błęd", "koszmar", "szok", "rewolucj", "szał", "obłędn", 
            "gwiazd", "króluj", "klas", "szyk", "elegancj", "zachwyc", 
            "odmładz", "wyszczupl", "postarz", "pogrub", "dramat", "hit"
        ],
        "phrases": ["absolutny hit", "modowy koszmar", "szał ciał"]
    },
    "KOLOR": {
        "lemmas": [
            "czarny", "biały", "czerwony", "beżowy", "różowy", "zielony", "niebieski", 
            "szary", "brązowy", "żółty", "złoty", "srebrny", "pastelowy", "camel", 
            "liliowy", "fioletowy", "granatowy"
        ],
        "stems": [
            "czarn", "biał", "czerwon", "beżow", "różow", "zielon", "niebiesk", 
            "szar", "brązow", "żółt", "złot", "srebrn", "pastel", "camel", 
            "liliow", "fiolet", "granat"
        ],
        "phrases": []
    },
    "CZESC_GARDEROBY": {
        "lemmas": [
            "sukienka", "suknia", "spódnica", "but", "szpilka", "sneakersy", "mokasyny", 
            "sandał", "klapki", "czółenka", "płaszcz", "kurtka", "spodnie", "jeansy", 
            "dżinsy", "marynarka", "torebka", "sweter", "kardigan", "golf", "koszula", 
            "bluzka", "garnitur"
        ],
        "stems": [
            "sukienk", "sukni", "spódnic", "but", "szpilk", "sneakers", "mokasyn", 
            "sandał", "klapk", "czółenk", "płaszcz", "kurtk", "spodn", "jeans", 
            "dżins", "marynark", "torebk", "sweter", "swetr", "kardigan", "golf", 
            "koszul", "bluzk", "garnitur"
        ],
        "phrases": ["płaskiej podeszwie", "wysokim obcasie"]
    },
    "SEZON": {
        "lemmas": ["lato", "zima", "wiosna", "jesień", "wakacje", "urlop", "święta", "sezon"],
        "stems": ["lat", "letn", "zim", "wiosn", "wiosen", "jesien", "wakac", "urlop", "święt", "sezon"],
        "phrases": ["nowy sezon", "zimowy sezon", "letni sezon", "wiosenny sezon", "jesienny sezon"]
    },
    "TREND_ROK": {
        "lemmas": [
            "2024", "2025", "2026", "2027", "2028", "trend", "nowość", 
            "modny", "stylowy"
        ],
        "stems": [
            "2024", "2025", "2026", "2027", "2028", "trend", "nowość", 
            "modn", "stylow"
        ],
        "phrases": ["nowy trend", "najnowsze trendy"]
    },
    "MARKA": {
        "lemmas": ["zara", "h&m", "mango", "chanel", "gucci", "prada", "reserved", "nike", "adidas", "lidl", "biedronka"],
        "stems": ["zara", "h&m", "mango", "chanel", "gucci", "prada", "reserved", "nike", "adidas", "lidl", "biedronka"],
        "phrases": []
    },
    "ADRESAT": {
        "lemmas": [
            "50-latka", "60-latka", "40-latka", "kobieta", "pani", "panna", "gwiazda"
        ],
        "stems": [
            "50-latk", "60-latk", "40-latk", "50-tce", "60-tce", "40-tce", "50 lat", "60 lat", "40 lat",
            "kobiet", "pani", "pann", "gwiazd"
        ],
        "phrases": ["dojrzałe panie", "dojrzałych pań", "panna młoda", "panny młode"]
    }
}

class LifestyleNLPAnalyzer:
    def __init__(self):
        self.nlp = None
        self.use_fallback = True
        
        # Próba załadowania modelu polskiego spaCy
        try:
            self.nlp = spacy.load("pl_core_news_sm")
            self.use_fallback = False
            print("Pomyślnie załadowano model spaCy: pl_core_news_sm")
        except Exception:
            print("Model spaCy 'pl_core_news_sm' nie jest dostępny. Próba pobrania...")
            try:
                spacy.cli.download("pl_core_news_sm")
                self.nlp = spacy.load("pl_core_news_sm")
                self.use_fallback = False
                print("Pomyślnie pobrano i załadowano model spaCy: pl_core_news_sm")
            except Exception as e:
                print(f"Nie udało się pobrać spaCy pl_core_news_sm: {e}. Uruchomiono tryb fallback (wyrażenia regularne + lematyzacja słownikowa).")
                self.use_fallback = True

    def clean_text(self, text: str) -> str:
        """Czyszczenie tekstu z nadmiarowych znaków interpunkcyjnych."""
        return text.replace("?", "").replace("!", "").replace(",", "").replace(".", "").replace(":", "")

    def extract_tags(self, text: str) -> dict:
        """
        Ekstrahuje tagi z tytułu. Zwraca słownik postaci:
        { KATEGORIA: {"value": dopasowane_słowo, "start": start_char_index} }
        """
        text_lower = text.lower()
        cleaned_text = self.clean_text(text_lower)
        extracted = {}

        # 1. Najpierw dopasowujemy frazy wielowyrazowe (aby zapobiec dzieleniu ich na pojedyncze słowa)
        for category, rules in CATEGORIES.items():
            for phrase in rules.get("phrases", []):
                match = re.search(r'\b' + re.escape(phrase) + r'\b', cleaned_text)
                if match:
                    extracted[category] = {
                        "value": phrase.upper(),
                        "start": match.start()
                    }

        # 2. Następnie przetwarzamy pojedyncze słowa
        if not self.use_fallback and self.nlp:
            # Użycie spaCy do lematyzacji i tagowania POS
            doc = self.nlp(text_lower)
            for token in doc:
                lemma = token.lemma_
                # Pomijamy słowa, które są już dopasowane w frazach
                for category, rules in CATEGORIES.items():
                    if category in extracted:
                        continue
                    
                    # Sprawdzamy czy lemma pasuje do słownika
                    if lemma in rules["lemmas"] or token.text in rules["lemmas"]:
                        # Sprawdzamy czy nie nakłada się na już istniejący początek
                        start_idx = text_lower.find(token.text)
                        extracted[category] = {
                            "value": token.text.upper(),
                            "start": start_idx if start_idx != -1 else token.idx
                        }
                        break
        
        # 3. Dodatkowo (lub w trybie fallback) dopasowujemy słowa za pomocą rdzeni wyrazowych (stems)
        words = cleaned_text.split()
        for word in words:
            for category, rules in CATEGORIES.items():
                if category in extracted:
                    continue
                
                # Sprawdzanie rdzeni
                for stem in rules["stems"]:
                    # Zabezpieczenie przed zbyt krótkimi dopasowaniami (np. 'lat' jako lato, a to część 'latach')
                    if len(stem) >= 3 and word.startswith(stem):
                        start_idx = text_lower.find(word)
                        extracted[category] = {
                            "value": word.upper(),
                            "start": start_idx if start_idx != -1 else 0
                        }
                        break
                    elif len(stem) < 3 and word == stem:
                        start_idx = text_lower.find(word)
                        extracted[category] = {
                            "value": word.upper(),
                            "start": start_idx if start_idx != -1 else 0
                        }
                        break

        return extracted

    def get_pattern_string(self, extracted_tags: dict) -> str:
        """
        Tworzy ładnie sformatowany wzorzec z wyodrębnionych tagów,
        sortując je po kolejności występowania w oryginalnym tekście.
        Przykład: [PORADNICTWO] + [KOLOR] + [CZĘŚĆ_GARDEROBY]
        """
        if not extracted_tags:
            return "[OGÓLNY_LIFESTYLE]"
        
        # Sortowanie według pozycji startowej w tytule
        sorted_categories = sorted(extracted_tags.items(), key=lambda item: item[1]["start"])
        
        pattern_elements = [f"[{cat}]" for cat, info in sorted_categories]
        return " + ".join(pattern_elements)

# Test modułu
if __name__ == "__main__":
    analyzer = LifestyleNLPAnalyzer()
    test_titles = [
        "Jak nosić czarny płaszcz zimą 2026? Te 3 stylizacje dla 50-latki to hit!",
        "Wpadka z sukienką? Te błędy postarzają 60-latki",
        "Nowości z Zara na lato! Te buty to absolutny hit"
    ]
    for title in test_titles:
        tags = analyzer.extract_tags(title)
        pattern = analyzer.get_pattern_string(tags)
        print(f"Tytuł: {title}")
        print(f"Tagi: {tags}")
        print(f"Wzorzec: {pattern}")
        print("-" * 40)
