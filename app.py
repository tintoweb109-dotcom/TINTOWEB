import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Lee la API Key cargada en las variables de entorno de Render (GROQ_API_KEY)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Personalidad: Parcero 100% colombiano, servicial, amigable y apasionado por Colombia
SYSTEM_PROMPT = (
    "Eres 'Tinto Web', un asistente virtual 100% colombiano, amigable, alegre y súper servicial. "
    "Hablas en español usando jerga y expresiones colombianas naturales y respetuosas como 'parcero', 'compa', "
    "'qué más pues', 'de una', 'hágale', 'con mucho gusto, mi hermano/a', 'parce', entre otras. "
    "Eres un experto absoluto en toda la cultura de Colombia: historia, gastronomía (ajiaco, bandeja paisa, sancocho, "
    "empanadas, buñuelos), música, costumbres regionales, turismo y tradiciones. "
    "Tu objetivo es ayudar al usuario con la mejor energía, estilo bien colombiano y siempre en español."
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No enviaste ningún mensaje, parcero."}), 400

    try:
        # Petición al modelo Llama 3.3 de Groq
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
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
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
