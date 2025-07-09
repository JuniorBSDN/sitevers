from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

app = Flask(__name__)
CORS(app)

# Inicialização do Firebase
try:
    if not firebase_admin._apps:
        firebase_json = os.environ.get("FIREBASE_CREDENTIALS")

        if not firebase_json:
            raise ValueError("Variável FIREBASE_CREDENTIALS não encontrada.")

        cred_dict = json.loads(firebase_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)

    db = firestore.client()
except Exception as e:
    print(f"Erro ao inicializar Firebase: {e}")
    db = None  # Garante que não quebra o app

@app.route("/api/", methods=["POST"])
def salvar_contato():
    if not db:
        return jsonify({"erro": "Banco de dados não conectado."}), 500

    try:
        dados = request.get_json(force=True)
        nome = dados.get("nome", "").strip()
        email = dados.get("email", "").strip()
        assunto = dados.get("assunto", "").strip()
        mensagem = dados.get("mensagem", "").strip()

        # Validação mínima
        if not nome or not email or not assunto:
            return jsonify({"erro": "Campos obrigatórios faltando."}), 400

        # Salvar no Firestore
        db.collection("contatos").add({
            "nome": nome,
            "email": email,
            "assunto": assunto,
            "mensagem": mensagem
        })

        return jsonify({"mensagem": "Solicitação registrada com sucesso."}), 200

    except Exception as e:
        print(f"Erro ao salvar no Firestore: {e}")
        return jsonify({"erro": "Erro interno ao salvar"}), 500
