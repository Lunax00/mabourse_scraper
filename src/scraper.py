import requests
from bs4 import BeautifulSoup
import time
time.sleep(10)  # Délai de 2 secondes entre les requêtes


def scrape_bourses():
    """Scrape les bourses depuis le site maBourse."""
    url = "https://mabourse.enssup.gov.ma/bourse"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Erreur HTTP : {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all("div", class_="card")
    bourses = []

    for card in cards:
        # Nom de la bourse
        nom_tag = card.find("h4", class_="card-title")
        nom = nom_tag.text.strip() if nom_tag else "Nom indisponible"

        # Date de clôture (facultatif)
        date_tag = card.find("p", class_="card-text")
        date_cloture = (
            date_tag.text.strip().replace("Date de clôture :", "").strip()
            if date_tag
            else None
        )

        # Image du pays
        image_tag = card.find("img", class_="drapeau")
        image_url = (
            f"https://mabourse.enssup.gov.ma{image_tag['src']}" if image_tag else None
        )

        # PDF associés
        pdf_links = card.find_all("a", class_="btn")
        programmes = [
            f"https://mabourse.enssup.gov.ma{link['href']}" for link in pdf_links
        ]

        # Ajouter la bourse au tableau
        bourses.append(
            {
                "nom": nom,
                "date_limite": date_cloture,
                "image": image_url,
                "programme": programmes,
            }
        )

    return bourses
