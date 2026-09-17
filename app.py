import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from groq import Groq

# Configuración para servir archivos estáticos directamente desde las carpetas raíz
app = Flask(__name__, static_folder='.', static_url_path='')

# Cliente oficial de Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """
Eres Mini Tinto, el asistente virtual e IA representativa de Colombia en Tinto Web.
Tus características son:
- Hablas con la calidez, amabilidad y jerga típica colombiana (usa expresiones como 'parcero', 'quiubo', 'de una', 'compa', 'chévere', 'con gusto').
- Respondes de forma dinámica, fluida e inteligente a cualquier pregunta sobre cultura, gastronomía, lugares turísticos, historia o cualquier duda general que te hagan.
- Si te preguntan por los creadores del proyecto, responde que son los estudiantes del grado 10-02 del Técnico en Sistemas Telemáticos: Carlos Fabián Arévalo Baca, Yobani Andrés Rodríguez Rincón y Josué Emmanuel Contreras Reyes.
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
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({'response': '¡Uy compa! Escribe un mensaje para poder responderte. ☕'})

        # Modelo oficial activo en Groq (Ultra rápido y potente)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=500
        )

        bot_response = chat_completion.choices[0].message.content
        return jsonify({'response': bot_response})

    except Exception as e:
        print(f"Error detallado en el servidor: {e}")
        return jsonify({'response': '¡Uy parcero! Tuve un problema temporal para conectar con la IA. ¡Intenta preguntarme otra vez! ☕'})

if __name__ == '__main__':
    app.run(debug=True)
