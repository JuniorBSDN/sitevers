from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

app = Flask(__name__)
CORS(app)

# Conexão com Firebase usando variável de ambiente FIREBASE_CREDENTIALS
if not firebase_admin._apps:
    firebase_json = os.environ.get("FIREBASE_CREDENTIALS")
    if firebase_json:
        cred_dict = json.loads(firebase_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
    else:
        raise Exception("Variável de ambiente FIREBASE_CREDENTIALS não encontrada")

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
            "mensagem": dados.get("mensagem", "")
        })

        return jsonify({"mensagem": "Solicitação registrada com sucesso.", "id": doc_ref[1].id}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
