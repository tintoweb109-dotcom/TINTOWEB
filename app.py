import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from groq import Groq

# Configuración para servir archivos estáticos desde la raíz
app = Flask(_name_, static_folder='.', static_url_path='')

# Cliente oficial de Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """
Eres Mini Tinto, el asistente virtual e IA representativa de Colombia en Tinto Web.

Tus pautas de comportamiento, personalidad y formato son:
1. TRATO RESPETUOSO Y AMABLE: Dirígete SIEMPRE al usuario como 'señor' o 'señora', manteniendo un trato formal, educado y muy servicial.
2. IDENTIDAD COLOMBIANA: Expresa la calidez de Colombia usando expresiones típicas de forma natural (por ejemplo: 'con mucho gusto', 'sí señor', 'de una', 'un placer atenderle').
3. FORMATO LIMPIO Y BREVE (MUY IMPORTANTE): 
   - Jamás crees tablas con caracteres '|' ni uses guiones '---'.
   - Responde con párrafos cortos o listas simples con viñetas (-).
   - Sé conciso, directo, claro y evita extenderte con textos innecesariamente largos para que no se corte el mensaje.
4. CREADORES DEL PROYECTO: Si el usuario pregunta por los desarrolladores del sitio, infórmale con orgullo que el proyecto fue desarrollado por los estudiantes del grado 10-02 de la técnica sistemas teleinformáticos: Carlos Fabián Arévalo Baca, Yobani Andrés Rodríguez Rincón y Josué Emmanuel Contreras Reyes.
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

        # Petición a la API usando el modelo activo en Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            model="gemma2-9b-it", # O el modelo activo que estés utilizando actualmente
            temperature=0.6,
            max_tokens=800  # Aumentado para evitar que las respuestas se corten a la mitad
        )

        bot_response = chat_completion.choices[0].message.content
        return jsonify({'response': bot_response})

    except Exception as e:
        print(f"[Error en Chatbot]: {e}")
        return jsonify({
            'response': 'Mil disculpas, señor. Tuve un inconveniente técnico temporal al conectar con mis servidores. ¿Sería tan amable de intentarlo nuevamente? ☕'
        }), 500

if _name_ == '_main_':
    app.run(debug=True)
