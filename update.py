import urllib.request
import json
import os

api_key = os.environ.get("GEMINI_API_KEY")
url = f"[https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key=](https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key=){api_key}"

prompt = """Agis comme un journaliste sportif expert. Ta mission est de générer le code HTML complet et monopage (utilisant Tailwind CSS) d'un tableau de bord "Morning Lineup". 
IMPORTANT : Tu dois IMPÉRATIVEMENT utiliser tes capacités de recherche sur le web pour trouver les vrais résultats sportifs de la nuit dernière, les classements à jour de ce matin, et les actualités brûlantes concernant la MLB et la NBA (et la NFL si c'est la période de draft/saison).
Structure le code exactement avec : un header, des sections par ligue (logo, highlights, actus), des cartes de scores défilables horizontalement (snap-x), une section "Enjeux à venir", et les classements intégraux. 
OBLIGATOIRE POUR LA PWA : Inclus le lien `<link rel="manifest" href="manifest.json">` et l'icône dans le `<head>`. Inclus le script du Service Worker à la fin du `<body>` (exactement comme ceci : `<script>if ('serviceWorker' in navigator) { window.addEventListener('load', () => navigator.serviceWorker.register('./sw.js')); }</script>`).
Fournis UNIQUEMENT le code HTML brut. Ne commence pas par ```html et ne termine pas par ```."""

data = {
    "contents": [{"parts": [{"text": prompt}]}],
    "tools": [{"google_search": {}}]
}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        text = result['candidates'][0]['content']['parts'][0]['text']
        
        # Nettoyage du markdown si Gemini en ajoute
        if text.startswith('
http://googleusercontent.com/immersive_entry_chip/1
http://googleusercontent.com/immersive_entry_chip/2
http://googleusercontent.com/immersive_entry_chip/3

Pour reprendre sereinement : ouvre le document et rends-toi directement à la nouvelle **Étape 5.1**. N'hésite pas à me dire dès que tu lances le premier test manuel (à l'étape 5.4) !
