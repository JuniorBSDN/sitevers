from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import os

app = Flask(__name__)
CORS(app)

# Inicializar Firebase apenas uma vez
if not firebase_admin._apps:
    try:
        cred_path = os.path.join(os.path.dirname(__file__), 'FIREBASE_CREDENTIALS.json')
        cred = credentials.Certificate(cred_path)
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
        return jsonify({"erro": "Banco de dados não inicializado."}), 500

    try:
        dados = request.get_json()

        # Verificar se os campos obrigatórios existem e não estão vazios
        obrigatorios = ("nome", "email", "assunto")
        if not all(dados.get(campo) for campo in obrigatorios):
            return jsonify({"erro": "Todos os campos obrigatórios devem ser preenchidos."}), 400

        # Salvar no Firestore
        db.collection("contatos").add({
            "nome": dados["nome"],
            "email": dados["email"],
            "assunto": dados["assunto"],
            "mensagem": dados.get("mensagem", ""),
        })

        return jsonify({"mensagem": "Solicitação registrada com sucesso."}), 200

    except Exception as e:
        print(f"Erro no backend: {e}")
        return jsonify({"erro": "Erro interno no servidor."}), 500
