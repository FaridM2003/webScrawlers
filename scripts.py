from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import re
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/news')
def api_news():
    url = "https://www.lavanguardia.com/deportes/resultados"
    response = requests.get(url)
    news = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        news = [a_tag.get_text() for h2_tag in soup.find_all('h2','title') for a_tag in h2_tag.find_all('a','page-link')]

    
    return jsonify(news)




def parse_match_info(text):
    # Patrón para partidos programados (e.g., "nombre_equipo 10h00 nombre_equipo2")
    pattern_time = r"([A-Za-z]+)\s*(\d{1,2}h\d{2})\s*([A-Za-z]+)"
    match_time = re.match(pattern_time, text)
    if match_time:
        equipo1, hora, equipo2 = match_time.groups()
        return {
            "tipo": "partido_programado",
            "equipo1": equipo1,
            "hora": hora,
            "equipo2": equipo2
        }
    
    return {"error": "Formato no reconocido"}
def parse_match_score(text):
    # Nueva expresión regular para marcador (e.g., "Equipo1 0-1 Equipo2")
    pattern_score = r"([A-Za-z\s]+)\s*(\d+)-(\d+)\s*([A-Za-z\s]+)"
    
    # Intentar hacer coincidir el texto con el patrón de marcador
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
    
    return {"error": "Formato no reconocido"}
    return {"error": "Formato no reconocido"}

# Nueva ruta para obtener solo los datos en formato JSON
@app.route('/api/titles')
def api_titles():
    url = "https://www.lavanguardia.com/deportes/resultados"
    response = requests.get(url)
    results = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Buscar los elementos de partidos o resultados
        match_elements = soup.find_all('div', class_='tpl-match-block-teams')
        
        for element in match_elements:
            match_text = element.get_text(strip=True)
            
            # Detectar si es un partido programado o resultado final
            if "-" in match_text:
                match_info = parse_match_score(match_text)  # Usar para marcador final
            else:
                match_info = parse_match_info(match_text)   # Usar para partido programado
            
            results.append(match_info)

    return jsonify(results)





if __name__ == '__main__':
    app.run(debug=True)
