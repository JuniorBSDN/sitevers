from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

app = Flask(__name__)
CORS(app)  # 👉 Habilita CORS para todas as origens (ou defina a origem do seu front)

# 🔐 Inicializar Firebase (usando variável de ambiente segura)
if not firebase_admin._apps:
    try:
        cred_dict = json.loads(os.environ.get("FIREBASE_CREDENTIALS"))
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        print("Firebase inicializado com sucesso!")
    except Exception as e:
        print("Erro ao inicializar Firebase:", e)

# 🔧 Conectar ao Firestore
db = firestore.client()

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


    except Exception as e:
        print("❌ Erro na API:", e)
        return jsonify({"erro": "Erro interno no servidor."}), 500


@app.route("/contatos", methods=["GET"])
def listar_contatos():
    try:
        contatos_ref = db.collection("contatos").stream()
        contatos = []

        for doc in contatos_ref:
            contato = doc.to_dict()
            contato["id"] = doc.id
            contatos.append(contato)

        return jsonify(contatos), 200
    except Exception as e:
        print("❌ Erro ao listar contatos:", e)
        return jsonify({"erro": "Erro ao listar contatos"}), 500
