import os
from flask import Flask, render_template, request, jsonify

# Le indicamos a Flask que busque css, img y js en la raíz '.'
app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_message = data.get('message', '')

    bot_reply = f"¡Quiubo, parcero! Recibí tu mensaje: '{user_message}'. ¿En qué te colaboro hoy sobre Colombia o el proyecto?"

    return jsonify({'response': bot_reply})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
