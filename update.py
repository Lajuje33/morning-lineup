import urllib.request
import json
import os
import sys

api_key = os.environ.get("GEMINI_API_KEY", "").strip()
# On utilise le modèle Flash pour être sûr que ça passe
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

# PROMPT SIMPLIFIÉ (Sans recherche web pour éviter le blocage de quota)
prompt = "Génère une page HTML simple avec Tailwind CSS. Affiche en gros 'SYSTÈME DÉBLOQUÉ' et la date d'aujourd'hui. C'est un test pour valider l'enregistrement GitHub."

data = {"contents": [{"parts": [{"text": prompt}]}]}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})

try:
    print("Tentative de déblocage...")
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode('utf-8'))
        html = res_data['candidates'][0]['content']['parts'][0]['text']
        html = html.replace('```html', '').replace('```', '').strip()
        
        # On écrit le fichier
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Fichier index.html écrit sur le disque !")
except Exception as e:
    print(f"Erreur : {e}")
    sys.exit(1) # Ici on force l'erreur si ça rate
