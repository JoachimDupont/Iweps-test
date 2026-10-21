from flask import Flask, jsonify, Response, render_template
import requests
import re
import os

app = Flask(__name__)
API_BASE = "https://opendata.iweps.be/api/data"
TIMEOUT = 30

THEMES = [
    ("population", "Population & démographie", "Habitants, âge, ménages, naissances, migrations"),
    ("emploi", "Emploi & marché du travail", "Emploi, chômage, activité, métiers"),
    ("economie", "Économie & revenus", "Revenus, PIB, prix, pouvoir d’achat"),
    ("logement", "Logement & immobilier", "Logements, loyers, immobilier, construction"),
    ("enseignement", "Enseignement & formation", "Écoles, diplômes, formation, compétences"),
    ("sante", "Santé & bien-être", "Santé, soins, espérance de vie, qualité de vie"),
    ("environnement", "Environnement & énergie", "Climat, énergie, déchets, ressources"),
    ("mobilite", "Mobilité & transport", "Déplacements, transports, routes"),
    ("territoire", "Territoire & communes", "Communes, provinces, territoire"),
    ("social", "Action sociale & inégalités", "Pauvreté, précarité, inégalités"),
    ("entreprises", "Entreprises & innovation", "Entreprises, activité, innovation"),
    ("gouvernance", "Société & gouvernance", "Société, institutions, participation"),
]

@app.get("/")
def index():
    return render_template("index.html", themes=THEMES)

@app.get("/health")
def health():
    return jsonify(status="ok", app="Explorateur IWEPS")

@app.get("/api/data/<fmt>/<indicator>/<path:options>")
def proxy_data(fmt, indicator, options):
    if fmt not in ("json", "csv"):
        return jsonify(error="Format non pris en charge. Utilisez json ou csv."), 400
    if not re.fullmatch(r"\d+_\d+", indicator):
        return jsonify(error="Identifiant invalide. Exemple : 833605_7"), 400
    if not re.fullmatch(r"[A-Za-z0-9_=+-]+", options):
        return jsonify(error="Options invalides."), 400

    url = f"{API_BASE}/{fmt}/{indicator}/{options}"
    try:
        r = requests.get(url, timeout=TIMEOUT)
        r.raise_for_status()
        content_type = r.headers.get(
            "Content-Type",
            "application/json; charset=utf-8" if fmt == "json" else "text/csv; charset=utf-8"
        )
        return Response(r.content, status=200, content_type=content_type)
    except requests.Timeout:
        return jsonify(error="L’API IWEPS met trop de temps à répondre. Réessayez."), 504
    except requests.RequestException as exc:
        return jsonify(error="Impossible de récupérer les données IWEPS.", details=str(exc)), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
