import urllib.request
import json
import os

# Configuration des accès
api_key = os.environ.get("GEMINI_API_KEY")
# Utilisation du moteur de pointe Gemini 2.5 Pro
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={api_key}"

# Instructions précises pour l'IA
prompt = """Agis comme un journaliste sportif expert. Ta mission est de générer le code HTML complet et monopage (utilisant Tailwind CSS) d'un tableau de bord "Morning Lineup". 
IMPORTANT : Tu dois IMPÉRATIVEMENT utiliser tes capacités de recherche sur le web pour trouver les vrais résultats sportifs de la nuit dernière, les classements à jour de ce matin, et les actualités brûlantes concernant la MLB et la NBA.
Structure le code exactement avec : un header élégant, des sections par ligue (logo, highlights, actus), des cartes de scores défilables horizontalement (snap-x), une section "Enjeux à venir", et les classements. 
OBLIGATOIRE POUR LA PWA : Inclus le lien <link rel="manifest" href="manifest.json"> dans le <head>. Inclus le script du Service Worker à la fin du <body> (exactement comme ceci : <script>if ('serviceWorker' in navigator) { window.addEventListener('load', () => navigator.serviceWorker.register('./sw.js')); }</script>).
Fournis UNIQUEMENT le code HTML brut. Ne commence pas par ```html et ne termine pas par ```."""

# Préparation de la requête avec l'outil de recherche Google Search
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
    print("Interrogation de Gemini 2.5 Pro en cours...")
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        
        # Extraction du texte généré
        text = result['candidates'][0]['content']['parts'][0]['text']
        
        # Nettoyage rigoureux des balises de code markdown pour éviter les erreurs d'affichage
        clean_text = text.strip()
        if clean_text.startswith('```html'):
            clean_text = clean_text[7:]
        elif clean_text.startswith('```'):
            clean_text = clean_text[3:]
            
        if clean_text.endswith('
