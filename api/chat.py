import sys, os
sys.path.insert(0, os.path.dirname(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from core.prompt_mestre import PromptMestre

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
prompt = PromptMestre()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    mensagem = data.get('mensagem', '')

    resposta = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": prompt.get_prompt()},
            {"role": "user", "content": mensagem}
        ],
    )
    
    return jsonify({"resposta": resposta.choices[0].message.content})
