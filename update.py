import urllib.request
import json
import os
import sys

# 1. Vérification de la clé API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("ERREUR : Clé API manquante dans les Secrets GitHub.")
    sys.exit(1)

# 2. Utilisation de Gemini 2.5 Pro (URL v1beta pour la recherche Google)
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={api_key}"

# 3. Le Prompt Dynamique (SANS DATE FIXE)
prompt = """Agis comme un journaliste sportif expert. Ta mission est de générer le code HTML complet et monopage (utilisant Tailwind CSS) d'un tableau de bord "Morning Lineup". 
IMPORTANT : Utilise ta fonction de recherche Google pour trouver les scores réels de LA NUIT DERNIÈRE (NBA et MLB). 
Inclus les classements à jour de ce matin.
OBLIGATOIRE : Inclus <link rel="manifest" href="manifest.json"> et le script du Service Worker à la fin du <body>.
Réponds UNIQUEMENT avec le code HTML brut, sans aucune balise de code ``` au début ou à la fin."""

# 4. Payload avec recherche Google
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
    print("Génération du journal de bord par Gemini 2.5 Pro...")
    # Timeout de 120s pour laisser le temps à l'IA de chercher sur le web
    with urllib.request.urlopen(req, timeout=120) as response:
        res_data = json.loads(response.read().decode('utf-8'))
        html_content = res_data['candidates'][0]['content']['parts'][0]['text']
        
        # Nettoyage automatique des balises
        final_html = html_content.replace('```html', '').replace('```', '').strip()
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(final_html)
        print("SUCCÈS : index.html a été mis à jour avec les dernières actualités.")

except Exception as e:
    print(f"Erreur lors de l'automatisation : {e}")
    sys.exit(1)
