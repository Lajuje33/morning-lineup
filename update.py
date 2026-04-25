import urllib.request
import json
import os
import sys

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("ERREUR : Clé API manquante.")
    sys.exit(1)

# On passe sur 1.5 Flash pour une fiabilité totale (fini les erreurs 429)
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

prompt = """Agis comme un journaliste sportif expert. Génère le code HTML complet (Tailwind CSS) pour 'Morning Lineup'. 
Utilise ta fonction de recherche Google pour trouver les scores réels de LA NUIT DERNIÈRE (NBA et MLB). 
OBLIGATOIRE : Inclus <link rel="manifest" href="manifest.json"> et le script du Service Worker.
Réponds UNIQUEMENT avec le code HTML brut, sans balises ```."""

data = {
    "contents": [{"parts": [{"text": prompt}]}],
    "tools": [{"google_search": {}}]
}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})

try:
    print("Mise à jour en cours avec Gemini 1.5 Flash (Modèle Stable)...")
    with urllib.request.urlopen(req, timeout=120) as response:
        res_data = json.loads(response.read().decode('utf-8'))
        html_content = res_data['candidates'][0]['content']['parts'][0]['text']
        
        final_html = html_content.replace('```html', '').replace('```', '').strip()
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(final_html)
        print("SUCCÈS : Ton journal est prêt !")
except Exception as e:
    print(f"Erreur : {e}")
    sys.exit(1)
