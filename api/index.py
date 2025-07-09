from firebase_admin import credentials, firestore
import os
import json
import base64

app = Flask(__name__)
CORS(app)

firebase_credentials = os.environ.get("FIREBASE_CREDENTIALS")

# Firebase com variável de ambiente
if not firebase_admin._apps:
    cred_dict = json.loads(firebase_credentials)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
    try:
        firebase_json = os.environ.get("FIREBASE_CREDENTIALS")
        cred_dict = json.loads(firebase_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
    except Exception as e:
        print(f"Erro ao inicializar Firebase: {e}")
@@ -26,26 +26,22 @@
@app.route("/api/", methods=["POST"])
def salvar_contato():
    if not db:
        return jsonify({"erro": "Banco de dados não inicializado."}), 500
        return jsonify({"erro": "Banco de dados não conectado."}), 500

    try:
        dados = request.get_json()
        if not all(dados.get(k) for k in ("nome", "email", "assunto")):
            return jsonify({"erro": "Campos obrigatórios faltando."}), 400

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
            "mensagem": dados.get("mensagem", "")
        })

        return jsonify({"mensagem": "Solicitação registrada com sucesso."}), 200

    except Exception as e:
        print(f"Erro no backend: {e}")
        return jsonify({"erro": "Erro interno no servidor."}), 500
        print(f"Erro ao salvar no Firestore: {e}")
        return jsonify({"erro": "Erro interno ao salvar"}), 500
