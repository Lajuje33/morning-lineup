import urllib.request
import json
import os
import sys

# 1. Récupération et nettoyage de la clé
raw_key = os.environ.get("GEMINI_API_KEY", "")
api_key = raw_key.strip() # Enlève les espaces invisibles

if not api_key:
    print("ERREUR : La clé GEMINI_API_KEY est vide dans GitHub Secrets.")
    sys.exit(1)

# 2. Utilisation du modèle Flash de génération actuelle (Stable en 2026)
# On utilise v1beta pour conserver l'outil de recherche Google
model_name = "gemini-2.0-flash"
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

# 3. Le Prompt
prompt = """Agis comme un journaliste sportif expert. Génère le code HTML complet (Tailwind CSS) pour 'Morning Lineup'. 
Utilise ta fonction de recherche Google pour trouver les scores réels de LA NUIT DERNIÈRE (NBA et MLB). 
OBLIGATOIRE : Inclus le lien <link rel="manifest" href="manifest.json"> et le script du Service Worker.
Réponds UNIQUEMENT avec le code HTML brut, sans balises ```."""

data = {
    "contents": [{"parts": [{"text": prompt}]}],
    "tools": [{"google_search": {}}]
}

req = urllib.request.Request(
    url, 
    data=json.dumps(data).encode('utf-8'), 
    headers={'Content-Type': 'application/json'}
)

try:
    print(f"Connexion à {model_name}...")
    with urllib.request.urlopen(req, timeout=120) as response:
        res_data = json.loads(response.read().decode('utf-8'))
        html_content = res_data['candidates'][0]['content']['parts'][0]['text']
        
        # Nettoyage automatique
        final_html = html_content.replace('```html', '').replace('```', '').strip()
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"SUCCÈS : Le journal a été mis à jour via {model_name}.")

except Exception as e:
    print(f"Échec avec {model_name} : {e}")
    if "404" in str(e):
        print("Note : Le modèle est peut-être trop récent ou le nom a encore changé.")
    sys.exit(1)
