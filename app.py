import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from groq import Groq

app = Flask(__name__)

# Configuración de la clave de Groq desde las variables de entorno de Render
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# Prompt del sistema para definir la personalidad de Tinto Web
SYSTEM_PROMPT = (
    "Eres 'Tinto Web', un asistente virtual 100% colombiano, alegre, amigable y súper servicial. "
    "Hablas en español usando jerga y expresiones colombianas naturales y respetuosas como 'parcero', 'compa', "
    "'qué más pues', 'de una', 'hágale', 'con mucho gusto, mi hermano/a', 'parce', entre otras. "
    "Eres un experto absoluto en la cultura de Colombia: historia, gastronomía, música, costumbres regionales, turismo y tradiciones. "
    "Tu objetivo es ayudar al usuario con la mejor energía, estilo bien colombiano y siempre en español."
)

@app.route("/")
def index():
    return render_template("index.html")

# Servir carpeta css ubicada en la raíz
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('css', filename)

# Servir carpeta js ubicada en la raíz
@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('js', filename)

@app.route("/chat", methods=["POST"])
def chat():
    if not client:
        return jsonify({"error": "GROQ_API_KEY no está configurada en el servidor."}), 500

    data = request.get_json() or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "No enviaste ningún mensaje, parcero."}), 400

    try:
        completion = client.chat.completions.create(
            model="gpt-oss-120b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        reply = completion.choices[0].message.content
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"error": f"Error procesando la solicitud: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
