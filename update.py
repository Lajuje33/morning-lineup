import urllib.request
import json
import os

# 1. Configuration des accès
api_key = os.environ.get("GEMINI_API_KEY")
# Utilisation du moteur de pointe Gemini 2.5 Pro
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={api_key}"

# 2. Instructions détaillées pour l'IA
prompt = """Agis comme un journaliste sportif expert. Ta mission est de générer le code HTML complet et monopage (utilisant Tailwind CSS) d'un tableau de bord "Morning Lineup". 
IMPORTANT : Tu dois IMPÉRATIVEMENT utiliser tes capacités de recherche sur le web pour trouver les vrais résultats sportifs de la nuit dernière, les classements à jour de ce matin, et les actualités brûlantes concernant la MLB et la NBA.
Structure le code avec : un header, des sections par ligue, des cartes de scores et les classements. 
OBLIGATOIRE POUR LA PWA : Inclus le lien <link rel="manifest" href="manifest.json"> dans le <head> et le script du Service Worker à la fin du <body>.
Fournis UNIQUEMENT le code HTML brut. Ne commence pas par ```html et ne termine pas par ```."""

# 3. Préparation de la requête avec l'outil de recherche Google
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
        result = json.loads(response.read().decode('utf-8'))
        
        # Extraction du texte
        text = result['candidates'][0]['content']['parts'][0]['text']
        
        # Nettoyage automatique du code (supprime les balises ``` si l'IA en ajoute)
        html_propre = text.replace('```html', '').replace('```', '').strip()
        
        # Sauvegarde dans le fichier final
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_propre)
            
    print("Succès : index.html a été mis à jour avec les scores de la nuit.")

except Exception as e:
    print(f"Erreur lors de l'exécution : {e}")
    exit(1)
