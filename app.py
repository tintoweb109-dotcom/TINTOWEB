import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from groq import Groq

# ---------------------------------------------------------
# CONFIGURACIÓN DE RUTAS ABSOLUTAS Y FLASK
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(
    __name__,
    template_folder=TEMPLATES_DIR,
    static_folder=None  # Se gestionan las rutas estáticas de forma manual explícita
)

# ---------------------------------------------------------
# CONFIGURACIÓN DEL CLIENTE GROQ API
# ---------------------------------------------------------
groq_api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=groq_api_key) if groq_api_key else None

# ---------------------------------------------------------
# INSTRUCCIONES DEL SISTEMA (PROMPT PARA MINI TINTO)
# ---------------------------------------------------------
SYSTEM_PROMPT = """
Eres Mini Tinto, el asistente virtual e IA representativa de Colombia en Tinto Web.

Tus pautas de comportamiento, personalidad y formato son:
1. TRATO RESPETUOSO Y AMABLE: Dirígete SIEMPRE al usuario como 'señor' o 'señora', manteniendo un trato formal, educado, atento y muy servicial.
2. IDENTIDAD COLOMBIANA: Expresa la calidez de Colombia usando expresiones típicas de forma natural (por ejemplo: 'con mucho gusto', 'sí señor', 'de una', 'un placer atenderle').
3. FORMATO CORTO Y LIMPIO:
   - Responde de forma muy concisa, clara y directa (máximo 2 a 4 oraciones breves).
   - Utiliza emojis apropiados (☕, 🇨🇴, ✨, 📌, 🍽️) para decorar la respuesta.
   - Si incluyes un título o concepto importante, usa negritas (**Título**).
   - JAMÁS generes tablas, cuadros ni uses el carácter '|' o listas largas.
4. CREADORES DEL PROYECTO: Si el usuario pregunta por los desarrolladores del sitio, infórmale con orgullo que el proyecto fue desarrollado por los estudiantes del grado 10-02 de la técnica sistemas teleinformáticos: Carlos Fabián Arévalo Baca, Yobani Andrés Rodríguez Rincón y Josué Emmanuel Contreras Reyes.
"""

# ---------------------------------------------------------
# RUTAS PRINCIPALES (VISTAS HTML)
# ---------------------------------------------------------
@app.route('/')
def home():
    """Ruta para cargar el index.html desde la carpeta templates"""
    return render_template('index.html')

@app.route('/chat-view')
def chat_view():
    """Ruta dedicada para la interfaz de chat en chat.html"""
    return render_template('chat.html')

# ---------------------------------------------------------
# RUTAS DE ARCHIVOS ESTÁTICOS (CSS, JS, IMÁGENES)
# ---------------------------------------------------------
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'css'), filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'js'), filename)

@app.route('/img/<path:filename>')
def serve_img(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'img'), filename)

# ---------------------------------------------------------
# ENDPOINT PARA EL CHATBOT (POST /chat)
# ---------------------------------------------------------
@app.route('/chat', methods=['POST'])
def chat():
    if not client:
        return jsonify({
            'response': 'Mil disculpas, señor. La clave de API de Groq no se encuentra configurada en el servidor. ☕'
        }), 500

    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'response': 'Sí señor, por favor envíe un mensaje válido. ☕'
            }), 400

        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify({
                'response': 'Con mucho gusto le atiendo, señor, pero debe escribir un mensaje primero. ☕'
            })

        # Consulta a la API de Groq utilizando gemma2-9b-it
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            model="gemma2-9b-it",
            temperature=0.5,
            max_tokens=300
        )

        bot_response = chat_completion.choices[0].message.content
        return jsonify({'response': bot_response})

    except Exception as e:
        print(f"[Error en Chatbot]: {e}")
        return jsonify({
            'response': 'Mil disculpas, señor. Ocurrió un error de conexión al procesar su solicitud. ☕'
        }), 500

# ---------------------------------------------------------
# EJECUCIÓN LOCAL
# ---------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
