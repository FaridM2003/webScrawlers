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

@app.route('/api/news/href')
def api_newshref():
    url = "https://www.lavanguardia.com/deportes/resultados"
    response = requests.get(url)
    newshref = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        newshref = ["https://www.lavanguardia.com"+ a_tag.get('href') for h2_tag in soup.find_all('h2', 'title') for a_tag in h2_tag.find_all('a', 'page-link')]
    return jsonify(newshref)

pattern_team = r"[A-Za-zÀ-ÖØ-öø-ÿ'\-\s]+"
def parse_match_time(text):
    # Expresión regular para capturar equipo1, hora y equipo2
    pattern_time = re.compile(rf'({pattern_team})\s*(\d{{1,2}}h\d{{2}})\s*({pattern_team})', re.UNICODE)
    
    # Intentar hacer coincidir el texto con el patrón de partido programado
    match_time = re.search(pattern_time, text)
    if match_time:
        equipo1, hora, equipo2 = match_time.groups()
        return {
            "tipo": "partido_programado",
            "equipo1": equipo1.strip(),
            "hora": hora,
            "equipo2": equipo2.strip()
        }
    
    return {
            "tipo":"partido_daniado",
            "text":text
            }

def parse_match_score(text):
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    # Expresión regular para partidos con resultados finales
    pattern_score = re.compile(rf'({pattern_team})\s*(\d+)\s*-\s*(\d+)\s*({pattern_team})')
    # Intentar hacer coincidir el texto con el patrón de resultado final
    match_score = re.search(pattern_score, text)
    if match_score:
        equipo1, goles1, goles2, equipo2 = match_score.groups()
        return {
            "tipo": "resultado_final",
            "equipo1": equipo1.strip(),
            "goles1": int(goles1),
            "goles2": int(goles2),
            "equipo2": equipo2.strip()
        }
    
    return {
            "tipo":"resultado_daniado",
            "text":text
            }

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







