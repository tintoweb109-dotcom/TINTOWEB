import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from groq import Groq

# Configuración de Flask desde la raíz
app = Flask(__name__, static_folder='.', static_url_path='')

# Cliente oficial de Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Prompt con reglas estrictas de brevedad y formato visual
SYSTEM_PROMPT = """
Eres Mini Tinto, el asistente virtual de Colombia en Tinto Web.

REGLAS OBLIGATORIAS DE RESPUESTA:
1. BREVEDAD EXTREMA: Da respuestas muy cortas (máximo 2 a 4 frases). Sé directo al punto.
2. RESPETO Y TONO: Dirígete SIEMPRE al usuario como 'señor' o 'señora'. Usa la amabilidad colombiana.
3. FORMATO LIMPIO Y VISUAL:
   - Utiliza emojis apropiados (☕, 🇨🇴, ✨, 📌, 🍽️) para decorar la respuesta.
   - Si das títulos o puntos clave, resáltalos usando negritas (**Título**).
   - JAMÁS generes tablas, cuadros, símbolos '|' ni respuestas largas.
4. CREADORES: Si preguntan por los creadores, indica brevemente que son los estudiantes del grado 10-02 de la técnica sistemas teleinformáticos: Carlos Fabián Arévalo Baca, Yobani Andrés Rodríguez Rincón y Josué Emmanuel Contreras Reyes.
"""

@app.route('/')
def home():
    return render_template('index.html')

# Ruta para la página dedicada al Chat completo
@app.route('/chat-view')
def chat_view():
    return render_template('chat.html')

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
            return jsonify({'response': 'Sí señor, envíe un mensaje válido por favor. ☕'}), 400

        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({'response': 'Con mucho gusto le atiendo, señor, ¿en qué le puedo colaborar? ☕'})

        # Petición a Groq con máximo de tokens recortado para forzar respuestas breves
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            model="gemma2-9b-it", # Tu modelo activo en Groq
            temperature=0.5,
            max_tokens=250 # Límite estricto para mantener la brevedad
        )

        bot_response = chat_completion.choices[0].message.content
        return jsonify({'response': bot_response})

    except Exception as e:
        print(f"[Error en Chatbot]: {e}")
        return jsonify({
            'response': 'Mil disculpas, señor. Ocurrió un detalle técnico. ¿Podría preguntarme de nuevo? ☕'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
