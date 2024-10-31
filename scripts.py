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
     # Patrón para resultados finales (e.g., "nombre_equipo 0-1 nombre_equipo2")
    pattern_score = r"(\w+(?:\s\w+)*)\s(\d+)-(\d+)\s(\w+(?:\s\w+)*)"
    
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
    
    match_score = re.match(pattern_score, text)
    if match_score:
        equipo1, goles1, goles2, equipo2 = match_score.groups()
        return {
            "tipo": "resultado_final",
            "equipo1": equipo1,
            "goles1": int(goles1),
            "goles2": int(goles2),
            "equipo2": equipo2
        }
    
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
        
        # Procesar cada elemento encontrado
        for element in match_elements:
            match_text = element.get_text(strip=True)  # Obtener el texto completo del elemento
            print(match_text)
            match_info = parse_match_info(match_text)  # Analizar el texto
            results.append(match_info)  # Agregar el resultado a la lista

    return jsonify(results)





if __name__ == '__main__':
    app.run(debug=True)
