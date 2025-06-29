import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

# Inicializar Firebase com variável de ambiente segura
if not firebase_admin._apps:
    cred_dict = json.loads(os.environ.get("FIREBASE_CREDENTIALS"))
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route("/api/", methods=["POST"])
def receber_dados():
    dados = request.get_json()
    db.collection("mensagens").add(dados)
    return jsonify({"mensagem": "Dados recebidos com sucesso!"})


@app.route("/", methods=["POST"])
def salvar_formulario():
    dados = request.get_json()
    nome = dados.get("nome")
    email = dados.get("email")
    assunto = dados.get("assunto")
    mensagem = dados.get("mensagem")

    if not nome or not email:
        return jsonify({"erro": "Nome e email são obrigatórios"}), 400

    db.collection("contatos").add({
        "nome": nome,
        "email": email,
        "assunto": assunto,
        "mensagem": mensagem
    })

    return jsonify({"mensagem": "Dados recebidos com sucesso!"}), 200
