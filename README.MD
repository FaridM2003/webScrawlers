# Proyecto de Web Scraper de Resultados de Partidos

## Descripción
Este proyecto es un web scraper diseñado para recopilar información de resultados de partidos deportivos desde una fuente en línea y presentarla en una interfaz web. Usando Python con `Flask`, `BeautifulSoup`, y una pequeña API, el sistema muestra equipos, horarios de partidos y resultados finales, gestionando nombres de equipos que incluyen caracteres especiales.

## Funcionalidades
- **Extracción de información**: Utiliza `BeautifulSoup` para hacer scraping en una página de resultados deportivos y obtener datos sobre equipos, horarios y marcadores.
- **Interfaz Web**: Presenta la información en una página web construida con HTML y Bootstrap, accesible a través de una API REST creada con `Flask`.
- **Actualización periódica**: Permite actualizar los datos de los partidos cada cierto tiempo (si se implementa), para reflejar los cambios en la fuente de datos.
- **Compatibilidad Unicode**: Admite nombres de equipos que incluyen caracteres especiales y nombres compuestos, como "Beşiktaş" o "AD Ceuta FC".

## Requisitos
- **Python 3.7+**
- Librerías necesarias (instalación mediante `pip`):
  ```bash
  pip install requests beautifulsoup4 flask regex
  ```
- **Flask**: Para ejecutar el servidor web.
- **Bootstrap**: Para estilizar la página web (se incluye enlace en el HTML).

## Estructura del Proyecto
```
├── app.py              # Script principal para la API y web scraping
├── templates
│   └── index.html      # Página principal que muestra los resultados
├── static
│   └── style.css       # Archivo CSS opcional para estilizar la página
└── README.md           # Descripción del proyecto (este archivo)
```

## Instalación
1. Clona el repositorio o descarga los archivos del proyecto.
2. Navega al directorio del proyecto:
   ```bash
   cd proyecto-web-scraper
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso
1. **Ejecuta el servidor Flask**:
   ```bash
   python app.py
   ```
2. **Accede a la aplicación** en tu navegador en `http://127.0.0.1:5000`.

3. **Visualización**: La página principal mostrará los resultados de los partidos extraídos, listando equipos y resultados o tiempos de inicio, actualizándose cada cierto tiempo si se configura adecuadamente.

## Código Destacado
### Extracción de Información
El script utiliza `BeautifulSoup` para capturar el texto de los equipos y los resultados en la estructura HTML de la página fuente.

### Análisis de Datos
La función `parse_match_score` detecta y organiza partidos con resultados finales, mientras `parse_match_time` identifica partidos programados para ser jugados en el futuro. Ambas funciones utilizan expresiones regulares avanzadas para manejar nombres con caracteres especiales.

### Ejemplo de Respuesta JSON
La API devuelve un JSON con datos organizados:
```json
[
    {
        "tipo": "resultado_final",
        "equipo1": "Crvena Zvezda",
        "goles1": 1,
        "goles2": 2,
        "equipo2": "Beşiktaş"
    },
    {
        "tipo": "partido_programado",
        "equipo1": "AD Ceuta FC",
        "hora": "20h45",
        "equipo2": "Real Madrid"
    }
]
```

## Personalización
1. **Intervalo de actualización**: Puedes configurar el scraper para actualizarse cada cierto tiempo usando JavaScript en el HTML o un cron job en el servidor.
2. **Cambio de URL fuente**: Modifica la URL en `app.py` para apuntar a una fuente de datos diferente si deseas extraer información de otro sitio.

## Contribuciones
Si deseas contribuir a este proyecto, puedes hacer un fork del repositorio y enviar tus cambios mediante un pull request.

## Licencia
Este proyecto está bajo la Licencia MIT, lo que permite su libre uso, modificación y distribución para fines educativos o de aprendizaje.
