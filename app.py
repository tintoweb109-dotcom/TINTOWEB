import os
from flask import Flask, request, jsonify, send_file, send_from_directory

app = Flask(__name__, static_folder=None)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Carga segura de Groq API
try:
    from groq import Groq
    groq_api_key = os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=groq_api_key) if groq_api_key else None
except Exception as e:
    print(f"[ADVERTENCIA] Error al cargar la librería Groq: {e}")
    client = None

# PROMPT OPTIMIZADO PARA UN FORMATO LIMPIO, ORDENADO Y ELEGANTE
SYSTEM_PROMPT = """
Eres Mini Tinto, el asistente virtual e IA representativa de Colombia en Tinto Web.

Instrucciones estrictas de formato y redacción:
1. TRATO CORDIAL: Dirígete siempre al usuario como 'señor' o 'señora', manteniendo un trato formal, educado y con la calidez de la cultura colombiana.
2. FORMATO Y ESTILO DE RESPUESTA:
   - Da respuestas breves, claras y muy comprensibles (máximo 2 a 3 oraciones por idea).
   - Para destacar nombres propios, tribus, lugares o conceptos clave, enciérralos siempre entre etiquetas HTML de negrita exacta: <b>Nombre</b>. Esto hará que aparezcan en color dorado de inmediato en la interfaz sin mostrar asteriscos extraños.
   - Organiza la información en oraciones fluidas y ordenadas. Evita acumular nombres con comas sueltas o dejar etiquetas abiertas. Explica brevemente cada punto de forma natural.
3. CREADORES DEL PROYECTO: Si preguntan por los desarrolladores o creadores del sitio, responde con orgullo que el proyecto fue desarrollado por los estudiantes del grado 10-02 de la técnica en sistemas teleinformáticos: Carlos Fabián Arévalo Baca, Yobani Andrés Rodríguez Rincón y Josué Emmanuel Contreras Reyes.
"""

def obtener_ruta_archivo(nombre_archivo):
    rutas_a_probar = [
        os.path.join(BASE_DIR, 'templates', nombre_archivo),
        os.path.join(BASE_DIR, 'templates ', nombre_archivo),
        os.path.join(BASE_DIR, nombre_archivo)
    ]
    for ruta in rutas_a_probar:
        if os.path.exists(ruta):
            return ruta
    return None

# ---------------------------------------------------------
# RUTAS DE PÁGINAS HTML
# ---------------------------------------------------------
@app.route('/')
def home():
    file_path = obtener_ruta_archivo('index.html')
    if file_path:
        return send_file(file_path)
    return "<h1>Error: No se encontró index.html</h1>", 404

@app.route('/chat-view')
def chat_view():
    file_path = obtener_ruta_archivo('chat.html')
    if file_path:
        return send_file(file_path)
    return "<h1>Error: No se encontró chat.html</h1>", 404

# ---------------------------------------------------------
# RUTAS DE ARCHIVOS ESTÁTICOS
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
# ENDPOINT DEL CHATBOT
# ---------------------------------------------------------
@app.route('/chat', methods=['POST'])
def chat():
    if not client:
        return jsonify({
            'response': 'Mil disculpas, señor. La clave de API de Groq no está configurada en el servidor. ☕'
        }), 500

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
            temperature=0.4,
            max_tokens=350
        )

        bot_response = chat_completion.choices[0].message.content
        return jsonify({'response': bot_response})

    except Exception as e:
        print(f"[Error en Chatbot]: {e}")
        return jsonify({
            'response': 'Mil disculpas, señor. Ocurrió un error al conectar con mis servidores. ☕'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
