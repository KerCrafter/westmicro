# West Micro — Site statique

Ce dépôt contient un générateur simple pour créer un site statique administrable via fichiers JSON. Le site cible "West Micro" (réparation informatique — Vannes et environs).

Principes:
- Le contenu (pages, services, coordonnées) est stocké dans `content/*.json`.
- Le script Python `scripts/generate.py` lit ces JSON et rend destemplates Jinja2 dans `site/`.
- Le formulaire de contact du site utilise Formspree.

Pré-requis
- Python 3.8+

Installation (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```


Générer le site
```powershell
python scripts\generate.py --content content --templates templates --output build
```

Générer puis servir localement (optionnel)
```powershell
python -m http.server 8000 --directory build
# puis ouvrir http://localhost:8000
```


Remplir le contenu
- Modifiez `content/site.json` et `content/services.json` avec le texte et les adresses. Puis relancez le generateur.