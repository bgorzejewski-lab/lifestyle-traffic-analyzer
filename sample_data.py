import pandas as pd
import random

def get_sample_data():
    """
    Zwraca listę realistycznych artykułów lifestyle dla polskiego portalu modowego,
    zbudowanych tak, aby zawierały wyraźne, powtarzalne wzorce o zróżnicowanym ruchu (clicks).
    """
    articles = [
        # Wzorzec 1: [PORADNICTWO] + [CZĘŚĆ_GARDEROBY] + [ADRESAT] (BARDZO WYSOKI RUCH)
        {"title": "Jak nosić jeansy po 50-tce? Te 3 stylizacje dla 50-latki to absolutny hit!", "clicks": 24500, "url": "https://lifestyle.pl/jak-nosic-jeansy-50-latki-stylizacje"},
        {"title": "Jak nosić sweter oversize? Modne porady dla dojrzałych kobiet", "clicks": 18200, "url": "https://lifestyle.pl/jak-nosic-sweter-oversize-dojrzale-panie"},
        {"title": "Jak nosić sneakersy do sukienki? 5 stylizacji dla 50-latki", "clicks": 21000, "url": "https://lifestyle.pl/sneakersy-do-sukienki-porady-50-latka"},
        {"title": "Jak nosić marynarkę do jeansów? Triki dla kobiet po 40-tce", "clicks": 19500, "url": "https://lifestyle.pl/jak-nosic-marynarke-jeansy-40-latki"},
        {"title": "Jak stylizować buty na płaskiej podeszwie? Poradnik dla 50-latki", "clicks": 17800, "url": "https://lifestyle.pl/buty-na-plaskiej-podeszwie-50-latki"},

        # Wzorzec 2: [EMOCJONALNY_TRIGGER] + [CZĘŚĆ_GARDEROBY] + [ADRESAT] (EKSTREMALNIE WYSOKI RUCH - clickbait/błędy)
        {"title": "Wpadka z sukienką? Te 3 poważne błędy postarzają 60-latki o dekadę!", "clicks": 38900, "url": "https://lifestyle.pl/wpadka-sukienka-bledy-postarzaja-60-latki"},
        {"title": "Stylizacyjny koszmar! Te buty pogrubiają łydkę. Unikaj ich po 50-tce", "clicks": 42000, "url": "https://lifestyle.pl/koszmarne-buty-pogrubiaja-lydke-50-latki"},
        {"title": "Najgorsze błędy z kurtką puchową. Tak dojrzałe panie dodają sobie kilogramów", "clicks": 35400, "url": "https://lifestyle.pl/bledy-kurtka-puchowa-dojrzale-panie"},
        {"title": "Modowy dramat dojrzałych kobiet. Te jeansy zniekształcają sylwetkę!", "clicks": 31200, "url": "https://lifestyle.pl/modowy-dramat-jeansy-kobiety-50"},
        {"title": "Szokująca wpadka z torebką. Te modele wyszły z mody i postarzają", "clicks": 29800, "url": "https://lifestyle.pl/wpadka-torebki-przestarzale-modele"},

        # Wzorzec 3: [KOLOR] + [CZĘŚĆ_GARDEROBY] + [SEZON] + [TREND_ROK] (ŚREDNIO-WYSOKI RUCH - sezonowe trendy)
        {"title": "Czarny płaszcz na zimę 2026. Klasa, szyk i ponadczasowa elegancja", "clicks": 14200, "url": "https://lifestyle.pl/czarny-plaszcz-zima-2026-klasa-szyk"},
        {"title": "Beżowy sweter na jesień 2026 to must-have. Jak go modnie łączyć?", "clicks": 12800, "url": "https://lifestyle.pl/bezowy-sweter-jesien-2026-must-have"},
        {"title": "Biała koszula na lato 2026. Lekki i stylowy wybór na upały", "clicks": 11500, "url": "https://lifestyle.pl/biala-koszula-lato-2026-stylizacje"},
        {"title": "Czerwona sukienka na sylwestra 2026. Będziesz królować na parkiecie", "clicks": 16100, "url": "https://lifestyle.pl/czerwona-sukienka-sylwester-2026-trendy"},
        {"title": "Zielona marynarka na wiosnę 2026. Odświeży każdą stylizację", "clicks": 9800, "url": "https://lifestyle.pl/zielona-marynarka-wiosna-2026-trendy"},

        # Wzorzec 4: [MARKA] + [CZĘŚĆ_GARDEROBY] + [SEZON]/[TREND_ROK] (ŚREDNI RUCH - zakupowy)
        {"title": "Nowości z Zara na lato 2026! Te klapki i sandały to absolutne hity", "clicks": 8200, "url": "https://lifestyle.pl/nowosci-zara-lato-2026-klapki-sandaly"},
        {"title": "Wyprzedaż w H&M na jesień. Te swetry znikają z półek w mgnieniu oka", "clicks": 7900, "url": "https://lifestyle.pl/wyprzedaz-hm-jesien-swetry-hity"},
        {"title": "Kolekcja Mango na wiosnę 2026. Wybraliśmy najpiękniejsze sukienki", "clicks": 9100, "url": "https://lifestyle.pl/mango-wiosna-2026-najpiekniejsze-sukienki"},
        {"title": "Reserved zaskakuje ofertą na zimę. Ten wełniany płaszcz to cudo", "clicks": 8500, "url": "https://lifestyle.pl/reserved-zima-welniany-plaszcz"},
        {"title": "Torebki Chanel na nowy sezon. Inwestycja w luksus i styl", "clicks": 6200, "url": "https://lifestyle.pl/torebki-chanel-luksus-styl-nowy-sezon"},

        # Wzorzec 5: [KOLOR] + [CZĘŚĆ_GARDEROBY] + [ADRESAT] (ŚREDNIO-WYSOKI RUCH - dopasowanie do wieku)
        {"title": "Beżowe spodnie dla 50-latki. Klasyczna stylizacja na każdą okazję", "clicks": 13400, "url": "https://lifestyle.pl/bezowe-spodnie-50-latka-stylizacja"},
        {"title": "Różowa bluzka odmładza! 3 propozycje dla dojrzałych kobiet", "clicks": 14900, "url": "https://lifestyle.pl/rozowa-bluzka-odmladza-dojrzale-panie"},
        {"title": "Czarna marynarka wyszczupla. Zobacz stylizacje dla 60-latki", "clicks": 12100, "url": "https://lifestyle.pl/czarna-marynarka-wyszczupla-60-latki"},
        {"title": "Szary sweter dla 50-latki. Jak nosić go z klasą?", "clicks": 11200, "url": "https://lifestyle.pl/szary-sweter-50-latki-stylizacje"},
        {"title": "Biała spódnica dla dojrzałych pań. Modne zestawy na lato", "clicks": 13900, "url": "https://lifestyle.pl/biala-spodnica-dojrzale-panie-lato"},

        # Artykuły o niskim/standardowym ruchu (do wyznaczenia tła/mediany witryny)
        {"title": "Historia mody: Jak ewoluowały damskie spodnie na przestrzeni lat?", "clicks": 1200, "url": "https://lifestyle.pl/historia-mody-damskie-spodnie"},
        {"title": "Jak dbać o skórzane buty? Praktyczne porady i konserwacja", "clicks": 2100, "url": "https://lifestyle.pl/jak-dbac-o-skorzane-buty"},
        {"title": "Organizacja szafy przed nowym sezonem. Krok po kroku", "clicks": 1800, "url": "https://lifestyle.pl/organizacja-szafy-krok-po-kroku"},
        {"title": "Szybkie fryzury do pracy. Proste i efektowne upięcia w 5 minut", "clicks": 3100, "url": "https://lifestyle.pl/szybkie-fryzury-do-pracy"},
        {"title": "Jak dobrać perfumy na prezent? Kompletny poradnik zakupowy", "clicks": 1400, "url": "https://lifestyle.pl/jak-dobrac-perfumy-prezent"},
        {"title": "Kosmetyczka minimalistki: Tylko te 5 produktów musisz mieć w torbie", "clicks": 2900, "url": "https://lifestyle.pl/kosmetyczka-minimalistki-5-produktow"},
        {"title": "Wpływ kolorów na nasz nastrój. Co mówi o Tobie czerwony?", "clicks": 800, "url": "https://lifestyle.pl/wplyw-kolorow-na-nastroj-psychologia"},
        {"title": "Klasyczny manicure francuski wraca do łask. Zobacz nowe wersje", "clicks": 1500, "url": "https://lifestyle.pl/manicure-francuski-nowoczesne-wersje"},
        {"title": "Pielęgnacja cery zimą. Ochrona przed mrozem i suchym powietrzem", "clicks": 2300, "url": "https://lifestyle.pl/pielegnacja-cery-zima-porady"},
        {"title": "Jak nosić dodatki? Mniej znaczy więcej w eleganckiej stylizacji", "clicks": 1900, "url": "https://lifestyle.pl/jak-nosic-dodatki-szyk"},
        {"title": "Przegląd okularów przeciwsłonecznych. Najpopularniejsze kształty oprawek", "clicks": 1300, "url": "https://lifestyle.pl/przeglad-okularow-przeciwslonecznych"},
        {"title": "Jak prać delikatne tkaniny? Wełna, jedwab i kaszmir bez tajemnic", "clicks": 2500, "url": "https://lifestyle.pl/jak-prac-delikatne-tkaniny"},
        {"title": "Najpopularniejsze trendy w makijażu na nadchodzące miesiące", "clicks": 2900, "url": "https://lifestyle.pl/trendy-makijaz-przeglad"},
        {"title": "Biżuteria minimalistyczna vs retro. Co wybrać do codziennej stylizacji?", "clicks": 1100, "url": "https://lifestyle.pl/bizuteria-minimalistyczna-retro"},
        {"title": "Jak optycznie wydłużyć nogi? Proste triki z wysokim stanem", "clicks": 3400, "url": "https://lifestyle.pl/optomizacja-sylwetki-wysoki-stan"},
    ]

    # Dodajmy trochę losowego szumu i dodatkowych artykułów, aby łącznie było ok. 100-150 artykułów
    random.seed(42)
    garderoba = ["sukienka", "spódnica", "buty", "płaszcz", "kurtka", "spodnie", "marynarka", "torebka", "sweter", "koszula", "bluzka", "jeansy", "szpilki", "sneakersy"]
    kolory = ["czarny", "biały", "czerwony", "beżowy", "różowy", "zielony", "niebieski", "szary"]
    sezony = ["lato", "zima", "wiosna", "jesień"]
    adresaci = ["50-latki", "60-latki", "kobiety", "dojrzałe panie"]
    triggery_pos = ["hit", "króluje", "klasa", "szyk", "zachwyca", "odmładza"]
    triggery_neg = ["wpadka", "błąd", "koszmar", "szok"]
    porady = ["Jak nosić", "Jak łączyć", "Jak stylizować", "Sposób na"]
    marki = ["Zara", "H&M", "Mango"]

    # Generowanie dodatkowych losowych artykułów dla realizmu statystycznego
    for i in range(120):
        # Losujemy typ artykułu
        typ = random.randint(1, 6)
        title = ""
        clicks = random.randint(500, 4500)  # Tło
        
        if typ == 1:
            # Losowa porada
            title = f"{random.choice(porady)} {random.choice(garderoba)}? {random.choice(triggery_pos).capitalize()} sezonu!"
            clicks = random.randint(3000, 9000)
        elif typ == 2:
            # Losowy trigger i błąd
            title = f"{random.choice(triggery_neg).capitalize()} z {random.choice(garderoba)}. Te 3 błędy popełniają {random.choice(adresaci)}!"
            clicks = random.randint(5000, 15000)
        elif typ == 3:
            # Losowa marka i garderoba
            title = f"Nowości z {random.choice(marki)} na {random.choice(sezony)}. Ten {random.choice(garderoba)} to hit!"
            clicks = random.randint(2000, 7000)
        elif typ == 4:
            # Losowy kolor i garderoba na sezon
            title = f"{random.choice(kolory).capitalize()} {random.choice(garderoba)} na {random.choice(sezony)} 2026. Jak go nosić?"
            clicks = random.randint(3500, 9500)
        elif typ == 5:
            # Losowy kolor, garderoba dla adresata
            title = f"{random.choice(kolory).capitalize()} {random.choice(garderoba)} dla {random.choice(adresaci)}. Optycznie {random.choice(['wyszczupla', 'odmładza', 'wydłuża sylwetkę'])}!"
            clicks = random.randint(4000, 11000)
        else:
            # Ogólny artykuł lifestyle
            topics = [
                "Jak pić wodę rano? Zaskakujące efekty dla skóry",
                "Najzdrowsze nawyki żywieniowe znanych modelek",
                "Jak urządzić sypialnię, by spać lepiej?",
                "Joga dla początkujących. Zobacz prosty zestaw ćwiczeń",
                "Jak dbać o rośliny doniczkowe w mieszkaniu?",
                "Podróże solo: Gdzie warto wyjechać na weekend?",
                "Kapsułowa garderoba na wyjazd. Co spakować do małej walizki?",
                "Jak radzić sobie ze stresem w pracy? Proste techniki oddechowe",
                "Domowe maseczki na twarz. Proste przepisy z kuchni",
                "Najlepsze książki na urlop. Przegląd nowości literackich"
            ]
            title = random.choice(topics) + f" (Poradnik {random.randint(2025, 2026)})"
            clicks = random.randint(300, 2000)

        slug = title.lower().replace("?", "").replace("!", "").replace(",", "").replace(".", "").replace(":", "").replace(" ", "-")
        url = f"https://lifestyle.pl/{slug}"
        articles.append({"title": title, "clicks": clicks, "url": url})

    return articles

def get_sample_dataframe():
    """
    Zwraca DataFrame z danymi testowymi.
    """
    return pd.DataFrame(get_sample_data())
