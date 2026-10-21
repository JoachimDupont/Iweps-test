# Explorateur IWEPS — déploiement en ligne

Ce projet est un point de départ déployable d'une application Flask. Il sert l'interface web et relaie les appels vers l'API Open Data IWEPS côté serveur.

## Déploiement le plus simple avec Render + GitHub

1. Crée un compte sur GitHub et Render.
2. Sur GitHub, crée un nouveau dépôt, par exemple `explorateur-iweps`.
3. Téléverse tous les fichiers de ce dossier en conservant la structure :
   - `app.py`
   - `requirements.txt`
   - `render.yaml`
   - `templates/index.html`
4. Dans Render, choisis **New > Web Service**, puis connecte le dépôt GitHub.
5. Paramètres :
   - Runtime / Language : Python
   - Build command : `pip install -r requirements.txt`
   - Start command : `gunicorn app:app`
6. Lance le déploiement. Render donnera une URL publique `https://...onrender.com`.

`render.yaml` contient aussi ces paramètres si Render choisit de lire la configuration du dépôt.

## Tester après déploiement

- Ouvre la racine de l'URL Render : l'interface doit apparaître.
- Ouvre `/health` à la fin de l'URL : doit renvoyer `{"status":"ok","app":"Explorateur IWEPS"}`.
- Dans l'interface, charge l'identifiant `833605_7` pour tester l'API IWEPS.
- Essaie ensuite les boutons CSV et JSON.

## Limites importantes

Ceci est une version de démarrage, pas encore l'agrégateur exhaustif final :
- Les thèmes sont éditoriaux ; ils ne sont pas encore reliés à un catalogue complet d'indicateurs.
- L'export CSV/JSON télécharge la réponse de l'API pour l'indicateur saisi.
- L'export Excel .xlsx du catalogue et des valeurs n'est pas encore implémenté.
- Le format exact de la réponse API doit être validé sur plusieurs indicateurs.
- Le service public relaie des requêtes vers l'API ; pour un usage partagé plus large, ajouter une limitation de débit et une validation supplémentaire.

## Sources
- https://walstat.iweps.be/
- https://www.iweps.be/outils/open-data/
- https://www.iweps.be/donnees-et-indicateurs/
