import requests
from bs4 import BeautifulSoup

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
            image_url = image_element["src"] if image_element else None
            image_url = f"{BASE_URL}{image_url}" if image_url and image_url.startswith("/") else image_url

            categories.append({
                "title": title,
                "url": category_url,
                "image": image_url
            })

    return categories


def fetch_category_details(category_url):
    """
    Récupère les détails d'une catégorie spécifique :
    - description
    - image principale
    - liste des métiers
    """
    response = requests.get(category_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extraire la description de la catégorie
    description_element = soup.find("div", class_="clearfix text-formatted field field--name-description field--type-text-long field--label-hidden field__item")
    description = description_element.text.strip() if description_element else "Aucune description disponible"
    
    # Extraire l'image principale de la catégorie
    image_div = soup.find("div", class_="field field--name-field-rub-image")
    image_element = image_div.find("img") if image_div else None
    image = image_element["src"] if image_element else None
    if image and image.startswith("/"):
        image = BASE_URL + image

    # Extraire la liste des métiers associés
    jobs = []
    job_elements = soup.find_all("div", class_="item col-6 col-md-4 col-lg-3")
    for job in job_elements:
        job_link = job.find("a")
        job_url = BASE_URL + job_link["href"] if job_link and job_link["href"].startswith("/") else job_link["href"] if job_link else None

        job_title = job.find("span").text.strip() if job.find("span") else "Titre indisponible"
        job_image_element = job.find("img")
        job_image = job_image_element["src"] if job_image_element else None
        if job_image and job_image.startswith("/"):
            job_image = BASE_URL + job_image

        jobs.append({
            "title": job_title,
            "url": job_url,
            "image": job_image,
        })

    return {
        "description": description,
        "image": image,
        "jobs": jobs
    }
