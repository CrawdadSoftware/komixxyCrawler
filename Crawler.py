def komixxyCrawler():
    """
    komixxy Crawler, bot pobierający wszystkie obrazy ze strony komixxy.pl (ustawiony limit stron do 50 strony)
    """

    import requests, bs4, os

    url = "https://komixxy.pl/1500943" # adres początkowy
    os.makedirs("komixxy.pl/", exist_ok=True) # komiksy są przechowywane w katalogu komixxy.pl

    while not url.endswith("342875"):
        # Pobieranie strony
        print("Pobieranie strony %s..." % url)
        res = requests.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "html.parser")

        # Ustalenie adresu URL pliku obrazu komiksu
        comicElem = soup.select(".pic_image img")
        if not comicElem:
            print("Nie udało się odnaleźć pliku obrazu komiksu.")
        else:
            comicURL = "https://komixxy.pl" + comicElem[0]["src"]
            if comicURL:
                # Pobranie obrazu
                print("Pobieranie obrazu %s..." % (comicURL))
                res = requests.get(comicURL)
                res.raise_for_status()

                # Zapis obrazu w katalogu https://komixxy.pl/
                imageFile = open(os.path.join("komixxy.pl", os.path.basename(comicURL)), "wb")
                for chunk in res.iter_content(100000): # 100000 maksymalna ilość bajtów
                    imageFile.write(chunk)
                imageFile.close()

            # Pobranie adresu URL w przycisku następny komixx class="prefetch list_next_page_button"
            prevLink = soup.select(".prefetch.list_next_page_button")[0]
            url = "https://komixxy.pl" + prevLink.get("href")


    print(" ukończono proces pobierania komiksów ".center(46, "🕷"))

komixxyCrawler()