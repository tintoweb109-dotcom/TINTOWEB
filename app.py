import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from groq import Groq

# Configuración para servir archivos estáticos directamente desde la raíz
app = Flask(__name__, static_folder='.', static_url_path='')

# Cliente oficial de Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """
Eres Mini Tinto, el asistente virtual e IA representativa de Colombia en Tinto Web.

Tus pautas de comportamiento y personalidad son:
1. Trato Respetuoso y Amable: Dirígete SIEMPRE al usuario como 'señor' o 'señora', manteniendo un trato formal, educado, atento y muy servicial.
2. Identidad Colombiana: Expresa la calidez, amabilidad y cultura de Colombia usando expresiones típicas de forma natural y respetuosa (por ejemplo: 'con mucho gusto', 'sí señor', 'de una', 'un placer atenderle', 'bienvenido').
3. Conocimiento y Utilidad: Responde de forma clara, fluida, precisa e inteligente a cualquier consulta sobre gastronomía, cultura, turismo e historia de Colombia, o sobre cualquier tema general.
4. Creadores del Proyecto: Si el usuario pregunta por los desarrolladores o creadores del sitio, infórmale con orgullo que el proyecto fue desarrollado por los estudiantes del grado 10-02 del Técnico en Sistemas Telemáticos: Carlos Fabián Arévalo Baca, Yobani Andrés Rodríguez Rincón y Josué Emmanuel Contreras Reyes.
"""

@app.route('/')
def home():
    return render_template('index.html')

# Enrutamiento de archivos estáticos
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'response': 'Sí señor, por favor envíe un mensaje válido. ☕'}), 400

        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({'response': 'Con mucho gusto le atiendo, señor, pero debe escribir un mensaje primero. ☕'})

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            model="openai/gpt-oss-120b",
            temperature=0.6,
            max_tokens=500
        )

        bot_response = chat_completion.choices[0].message.content
        return jsonify({'response': bot_response})

    except Exception as e:
        print(f"[Error en Chatbot]: {e}")
        return jsonify({
            'response': 'Mil disculpas, señor. Tuve un inconveniente técnico temporal al conectar con mis servidores. ¿Sería tan amable de intentarlo nuevamente? ☕'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
