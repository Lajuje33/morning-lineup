import urllib.request
import json
import os
import sys

# 1. Vérification de la clé API (indispensable pour éviter le 404)
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("ERREUR : La variable GEMINI_API_KEY est vide. Vérifie tes 'Secrets' GitHub.")
    sys.exit(1)

# 2. Configuration du modèle 2.5 Pro (URL v1beta indispensable)
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={api_key}"

# 3. Le Prompt Expert
prompt = """Agis comme un journaliste sportif expert. Ta mission est de générer le code HTML complet et monopage (utilisant Tailwind CSS) d'un tableau de bord "Morning Lineup". 
IMPORTANT : Utilise tes capacités de recherche web pour trouver les vrais résultats sportifs de la nuit dernière (NBA, MLB).
OBLIGATOIRE : Inclus <link rel="manifest" href="manifest.json"> et le script du Service Worker.
Réponds UNIQUEMENT avec le code HTML brut, sans balises de code au début ou à la fin."""

# 4. Payload avec recherche Google activée
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
    print("Interrogation de Gemini 2.5 Pro avec recherche Google...")
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode('utf-8'))
        
        # Récupération du texte
        raw_html = res_data['candidates'][0]['content']['parts'][0]['text']
        
        # Nettoyage de sécurité
        final_html = raw_html.replace('```html', '').replace('```', '').strip()
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(final_html)
        print("SUCCÈS : index.html a été mis à jour par Gemini 2.5 Pro.")

except Exception as e:
    print(f"ÉCHEC de l'appel API : {e}")
    sys.exit(1)
