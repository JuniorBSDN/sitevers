from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Inicializa app Flask
app = Flask(__name__)
CORS(app)

# Firebase - usa arquivo de credenciais JSON
if not firebase_admin._apps:
    cred_path = os.path.join(os.path.dirname(__file__), '..', 'firebase_config.json')
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route("/api/", methods=["POST"])
def salvar_contato():
    try:
        dados = request.get_json()

        if not all(k in dados for k in ("nome", "email", "assunto")):
            return jsonify({"erro": "Campos obrigatórios faltando."}), 400

        doc_ref = db.collection("contatos").add({
            "nome": dados["nome"],
            "email": dados["email"],
            "assunto": dados["assunto"],
            "mensagem": dados.get("mensagem", ""),
        })

        return jsonify({"mensagem": "Solicitação registrada com sucesso."}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
