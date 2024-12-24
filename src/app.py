from flask import Flask, jsonify, request
from flask_cors import CORS
from scraperMetier import fetch_categories, fetch_category_details
from scraper import scrape_bourses

app = Flask(__name__)
CORS(app)

# Endpoint pour récupérer toutes les catégories avec l'image et URL associées
@app.route('/categories', methods=['GET'])
def get_categories():
    try:
        data = fetch_categories()
        categories = [
            {
                "name": category["title"],
                "image": category.get("image", ""),
                "category_url": category.get("url", "")
            }
            for category in data
        ]
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint pour récupérer les détails d'une catégorie spécifique
@app.route('/categories/<category_name>', methods=['GET'])
def get_category_details(category_name):
    try:
        data = fetch_categories()
        category = next(
            (cat for cat in data if cat["title"].lower() == category_name.lower()),
            None
        )
        if not category:
            return jsonify({"error": "Catégorie introuvable"}), 404

        category_details = fetch_category_details(category["url"])
        response = {
            "title": category["title"],
            "image": category.get("image", ""),
            "description": category_details["description"],
            "jobs": category_details["jobs"]
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint pour récupérer toutes les bourses
@app.route('/bourses', methods=['GET'])
def get_bourses():
    try:
        bourses = scrape_bourses()
        return jsonify(bourses), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint pour la recherche par nom
@app.route('/bourses/search', methods=['GET'])
def search_bourse():
    nom = request.args.get("nom")
    if not nom:
        return jsonify({"error": "Veuillez fournir un paramètre 'nom'"}), 400
    try:
        bourses = scrape_bourses()
        result = [bourse for bourse in bourses if nom.lower() in bourse["nom"].lower()]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint pour le filtrage par date limite
@app.route('/bourses/filter', methods=['GET'])
def filter_bourses():
    date_limite = request.args.get("date_limite")
    if not date_limite:
        return jsonify({"error": "Veuillez fournir un paramètre 'date_limite'"}), 400
    try:
        bourses = scrape_bourses()
        result = [
            bourse for bourse in bourses
            if bourse["date_limite"] and bourse["date_limite"] <= date_limite
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
