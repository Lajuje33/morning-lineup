import urllib.request
import json
import os

# 1. Configuration
api_key = os.environ.get("GEMINI_API_KEY")
# Utilisation du modèle Flash (plus rapide et évite les erreurs de quota)
url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"

# 2. Instructions
prompt = """Agis comme un journaliste sportif expert. Ta mission est de générer le code HTML complet et monopage (utilisant Tailwind CSS) d'un tableau de bord "Morning Lineup". 
IMPORTANT : Trouve les vrais résultats sportifs de la nuit dernière pour la NBA et la MLB.
OBLIGATOIRE POUR LA PWA : Inclus le lien <link rel="manifest" href="manifest.json"> dans le <head> et le script du Service Worker à la fin du <body>.
Fournis UNIQUEMENT le code HTML brut. Ne commence pas par ```html et ne termine pas par ```."""

# 3. Requête
data = {
    "contents": [{"parts": [{"text": prompt}]}]
}

req = urllib.request.Request(
    url, 
    data=json.dumps(data).encode('utf-8'), 
    headers={'Content-Type': 'application/json'}
)

try:
    print("Interrogation de Gemini 1.5 Flash...")
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        text = result['candidates'][0]['content']['parts'][0]['text']
        
        # Nettoyage
        final_html = text.replace('```html', '').replace('```', '').strip()
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(final_html)
        print("Succès ! Ton index.html est à jour.")
        
except Exception as e:
    print(f"Erreur rencontrée : {e}")
    exit(1)
