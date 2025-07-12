from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

app = Flask(__name__)
CORS(app)

# Inicialização segura do Firebase Admin com variável de ambiente
if not firebase_admin._apps:
    firebase_cred_json = os.environ.get("FIREBASE_CREDENTIALS")
    if firebase_cred_json:
        cred = credentials.Certificate(json.loads(firebase_cred_json))
        firebase_admin.initialize_app(cred)
    else:
        raise Exception("❌ A variável FIREBASE_CREDENTIALS não foi encontrada no ambiente.")

# Cliente Firestore
db = firestore.client()

@app.route("/", methods=["GET"])
def index():
    return jsonify({"mensagem": "API operando com Firestore no Vercel."})

@app.route("/api/contato", methods=["POST"])
def contato():
    try:
        data = request.get_json()

        # Campos esperados do formulário
        nome = data.get("nome")
        email = data.get("email")
        assunto = data.get("assunto")
        mensagem = data.get("mensagem")

        if not all([nome, email, assunto, mensagem]):
            return jsonify({"erro": "Todos os campos são obrigatórios."}), 400

        # Salvar no Firestore
        db.collection("contatos").add({
            "nome": nome,
            "email": email,
            "assunto": assunto,
            "mensagem": mensagem
        })

        return jsonify({"mensagem": "Contato registrado com sucesso!"}), 200

    except Exception as e:
        print(f"Erro no backend: {e}")
        return jsonify({"erro": "Erro ao registrar contato."}), 500
