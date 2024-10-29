from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Ruta principal que renderiza el HTML
@app.route('/')
def index():
    return render_template('index.html')

# Nueva ruta para obtener solo los datos en formato JSON
@app.route('/api/titles')
def api_titles():
    url = "https://www.lavanguardia.com/deportes/resultados"
    response = requests.get(url)
    titles = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = [title.get_text() for title in soup.find_all('div', 'tpl-match-block-teams')]
    
    return jsonify(titles)


@app.route('/api/news')
def api_news():
    url = "https://www.lavanguardia.com/deportes/resultados"
    response = requests.get(url)
    news = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        news = [a_tag.get_text() for h2_tag in soup.find_all('h2','title') for a_tag in h2_tag.find_all('a','page-link')]

    
    return jsonify(news)




if __name__ == '__main__':
    app.run(debug=True)
