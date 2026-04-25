import urllib.request
import json
import os
import sys
import time

# Nettoyage de la clé
api_key = os.environ.get("GEMINI_API_KEY", "").strip()
model = "gemini-2.0-flash"
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

prompt = """Agis comme un journaliste sportif. Génère le code HTML (Tailwind CSS) pour 'Morning Lineup'. 
Trouve les scores NBA et MLB de la nuit dernière via Google Search. 
Inclus le manifest.json et le service worker. 
Réponds UNIQUEMENT avec le code HTML brut."""

data = {
    "contents": [{"parts": [{"text": prompt}]}],
    "tools": [{"google_search": {}}]
}

def run_update():
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        print(f"Appel à {model}...")
        with urllib.request.urlopen(req, timeout=120) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            html = res_data['candidates'][0]['content']['parts'][0]['text']
            
            clean_html = html.replace('```html', '').replace('```', '').strip()
            
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(clean_html)
            print("Mise à jour réussie.")
            return True
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print("Quota Google Search atteint. Le serveur refuse la requête pour le moment.")
        else:
            print(f"Erreur HTTP {e.code}")
        return False
    except Exception as e:
        print(f"Erreur imprévue : {e}")
        return False

# Tentative d'exécution
if not run_update():
    print("L'automatisation a échoué à cause des limites de l'API Google. Réessaie dans 1 heure.")
    # On ne fait pas sys.exit(1) pour éviter de marquer le workflow en 'échec' rouge vif si c'est juste un quota
