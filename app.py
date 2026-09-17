import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Conexión con la API de Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Instrucciones para la inteligencia artificial de Mini Tinto
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

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({'response': '¡Uy compa! Escribe un mensaje para poder responderte. ☕'})

        # Petición a la IA de Groq para respuesta dinámica
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            model="openai/gpt-oss-120b",
            temperature=0.7,
            max_tokens=500
        )

        bot_response = chat_completion.choices[0].message.content
        return jsonify({'response': bot_response})

    except Exception as e:
        print(f"Error en el servidor: {e}")
        return jsonify({'response': '¡Uy parcero! Tuve un problema temporal para conectar con mi cerebro de IA. ¡Intenta preguntarme otra vez! ☕'})

if __name__ == '__main__':
    app.run(debug=True)
