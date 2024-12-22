from flask import Flask, jsonify, request
from scraper import scrape_bourses

app = Flask(__name__)

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
    """Recherche une bourse par nom."""
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
    """Filtre les bourses par date limite."""
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
