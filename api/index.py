from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

app = Flask(__name__)
CORS(app)

# Firebase com variável de ambiente
if not firebase_admin._apps:
    try:
        firebase_json = os.environ.get("FIREDB")
        cred_dict = json.loads(firebase_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
    except Exception as e:
        print(f"Erro ao inicializar Firebase: {e}")
        db = None
else:
    db = firestore.client()


@app.route("/api/", methods=["POST"])
def salvar_contato():
    if not db:
        return jsonify({"erro": "Banco de dados não conectado."}), 500

    try:
        dados = request.get_json()
        if not all(dados.get(k) for k in ("nome", "email", "assunto")):
            return jsonify({"erro": "Campos obrigatórios faltando."}), 400

        db.collection("contatos").add({
            "nome": dados["nome"],
            "email": dados["email"],
            "assunto": dados["assunto"],
            "mensagem": dados.get("mensagem", "")
        })

        return jsonify({"mensagem": "Solicitação registrada com sucesso."}), 200

    except Exception as e:
        print(f"Erro ao salvar no Firestore: {e}")
        return jsonify({"erro": "Erro interno ao salvar"}), 500
