from flask import Flask, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import regex as re
app = Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/news')
def api_news():
    url = "https://www.lavanguardia.com/deportes/resultados"
    response = requests.get(url)
    news = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        news = [a_tag.get_text() for h2_tag in soup.find_all('h2','title') for a_tag in h2_tag.find_all('a','page-link')]

    
    return jsonify(news)




def parse_match_score(text):
    # Expresión regular mejorada para capturar nombres de equipos con caracteres especiales y espacios
    pattern_score = r"([\w\s\p{L}]+)\s*(\d+)-(\d+)\s*([\w\s\p{L}]+)"
    
    # Intentar hacer coincidir el texto con el patrón de marcador
    match_score = re.search(pattern_score, text, re.UNICODE)
    if match_score:
        equipo1, goles1, goles2, equipo2 = match_score.groups()
        return {
            "tipo": "resultado_final",
            "equipo1": equipo1.strip(),
            "goles1": int(goles1),
            "goles2": int(goles2),
            "equipo2": equipo2.strip()
        }
    
    return {"error": "Formato no reconocido"}

def parse_match_time(text):
    # Nueva expresión regular para partidos programados (e.g., "Crvena Zvezda 18h30 Beşiktaş")
    pattern_time = r"([\w\s\p{L}]+)\s*(\d{1,2}h\d{2})\s*([\w\s\p{L}]+)"
    
    # Intentar hacer coincidir el texto con el patrón de partido programado
    match_time = re.search(pattern_time, text, re.UNICODE)
    if match_time:
        equipo1, hora, equipo2 = match_time.groups()
        return {
            "tipo": "partido_programado",
            "equipo1": equipo1.strip(),
            "hora": hora,
            "equipo2": equipo2.strip()
        }
    
    return {"error": "Formato no reconocido"}

@app.route('/api/titles')
def api_titles():
    url = "https://www.lavanguardia.com/deportes/resultados"
    response = requests.get(url)
    results = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        match_elements = soup.find_all('div', class_='tpl-match-block-teams')
        
        for element in match_elements:
            match_text = element.get_text(strip=True)
            
            # Detectar si es un partido programado o resultado final
            if "-" in match_text:
                match_info = parse_match_score(match_text)  # Usar para marcador final
            else:
                match_info = parse_match_time(match_text)   # Usar para partido programado
            
            results.append(match_info)

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)







