import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from groq import Groq

# Flask buscará por defecto en la carpeta 'templates'
app = Flask(__name__, static_folder='.', static_url_path='')

# Cliente oficial de Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Prompt ajustado para respuestas cortas, respetuosas y limpias
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

@app.route('/')
def home():
    """Ruta de la landing page principal"""
    return render_template('index.html')

@app.route('/chat-view')
def chat_view():
    """Ruta para la vista completa del chat"""
    return render_template('chat.html')

# --- RUTAS PARA ARCHIVOS ESTÁTICOS ---
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)

# --- ENDPOINT DEL CHATBOT ---
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'response': 'Sí señor, por favor envíe un mensaje válido. ☕'}), 400

        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({'response': 'Con mucho gusto le atiendo, señor, pero debe escribir un mensaje primero. ☕'})

        # Consulta a Groq con límite de tokens para garantizar brevedad
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            model="gemma2-9b-it", # O el modelo activo configurado en tu cuenta
            temperature=0.5,
            max_tokens=300
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
