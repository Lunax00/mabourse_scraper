import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.studyrama.com"

def fetch_categories():
    """
    Récupère la liste des catégories avec leurs images et titres.
    """
    url = f"{BASE_URL}/formations/fiches-metiers"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    categories = []
    category_elements = soup.find_all("div", class_="item")

    for category in category_elements:
        link_element = category.find("a")
        if link_element:
            category_url = link_element["href"]
            category_url = f"{BASE_URL}{category_url}" if category_url.startswith("/") else category_url
            title = link_element["title"]
            
            image_element = category.find("img")
            card_image = image_element["src"] if image_element else None
            card_image = f"{BASE_URL}{card_image}" if card_image and card_image.startswith("/") else card_image

            categories.append({
                "title": title,
                "url": category_url,
                "card_image": card_image
            })

    return categories

def fetch_category_details(category):
    """
    Récupère les détails d'une catégorie spécifique :
    - image principale
    - description
    - liste des métiers
    """
    response = requests.get(category["url"])
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extraire l'image principale de la catégorie
    image_element = soup.find("div", class_="field--name-field-rub-image").find("img")
    main_image = image_element["src"] if image_element else None
    if main_image and main_image.startswith("/"):
        main_image = f"{BASE_URL}{main_image}"

    # Extraire la description de la catégorie
    description_element = soup.find("div", class_="field--name-description")
    description = description_element.text.strip() if description_element else "Aucune description disponible"
    
    # Extraire la liste des métiers associés
    jobs = []
    job_elements = soup.find_all("li", class_="list-group-item")
    for job in job_elements:
        job_link = job.find("a")
        if job_link:
            job_title = job_link.text.strip()
            job_url = job_link["href"]
            job_url = f"{BASE_URL}{job_url}" if job_url.startswith("/") else job_url
            
            # Extraire les détails du métier
            job_details = fetch_job_details(job_url)
            jobs.append({
                "title": job_title,
                "image": job_details["image"],
                "short_description": job_details["short_description"],
                "article": job_details["article"]
            })

    return {
        "main_image": main_image,
        "description": description,
        "jobs": jobs
}

def fetch_job_details(job_url):
    """
    Récupère les détails d'un métier spécifique :
    - image principale
    - description courte
    - texte principal (missions uniquement)
    """
    response = requests.get(job_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Extraire l'image principale du métier
    image_element = soup.find("div", class_="field--name-field-art-image").find("img")
    image = image_element["src"] if image_element else None
    if image and image.startswith("/"):
        image = f"{BASE_URL}{image}"

    # Extraire la description courte
    short_description_element = soup.find("div", class_="field--name-field-art-sous-titre")
    short_description = short_description_element.text.strip() if short_description_element else "Aucune description disponible"

    # Extraire l'article (missions uniquement)
    article_element = soup.find("div", class_="field--name-field-metier-mission")
    article = article_element.text.strip() if article_element else "Aucun article disponible"

    return {
        "image": image,
        "short_description": short_description,
        "article": article
    }

def save_to_json(data, filename):
    """
    Enregistre les données dans un fichier JSON.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    print("Fetching categories...")
    categories = fetch_categories()

    print("Limiting to 40 categories...")
    limited_categories = categories[:40]

    all_details = {}
    for category in limited_categories:
        print(f"Fetching details for category: {category['title']}")
        try:
            details = fetch_category_details(category)
            all_details[category["title"]] = {
                "card_image": category["card_image"],
                "main_image": details["main_image"],
                "description": details["description"],
                "jobs": details["jobs"]
            }
        except Exception as e:
            print(f"Error fetching details for {category['title']}: {e}")
            continue

    print("Saving to categories_with_jobs.json...")
    save_to_json(all_details, "categories_with_jobs.json")
    print("Done!")
