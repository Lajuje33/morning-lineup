import urllib.request
import json
import os
import sys

# 1. Récupération et NETTOYAGE de la clé (pour éviter le 404)
raw_key = os.environ.get("GEMINI_API_KEY", "")
api_key = raw_key.strip() # Enlève les espaces ou retours à la ligne accidentels

if not api_key:
    print("ERREUR : La clé API est vide dans les secrets GitHub.")
    sys.exit(1)

# 2. URL Standardisée (v1beta est nécessaire pour la recherche Google)
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

# 3. Le Prompt sans date fixe pour l'autonomie
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
    print("Connexion à Gemini 1.5 Flash (Mode Automatique)...")
    # Timeout de 120s pour laisser le temps à la recherche Google
    with urllib.request.urlopen(req, timeout=120) as response:
        res_data = json.loads(response.read().decode('utf-8'))
        html_content = res_data['candidates'][0]['content']['parts'][0]['text']
        
        # Nettoyage du code HTML reçu
        final_html = html_content.replace('```html', '').replace('```', '').strip()
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(final_html)
        print("SUCCÈS : Le journal a été mis à jour avec les derniers scores.")

except Exception as e:
    print(f"Échec de la mise à jour : {e}")
    # Si c'est encore une 404, on affiche un petit message d'aide
    if "404" in str(e):
        print("Note : Vérifiez qu'il n'y a pas de faute de frappe dans le nom du Secret sur GitHub.")
    sys.exit(1)
