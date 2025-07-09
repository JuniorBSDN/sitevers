@app.route("/api/", methods=["POST"])
def salvar_contato():
    if not db:
        return jsonify({"erro": "Banco de dados não conectado."}), 500

    try:
        dados = request.get_json()
        if not all(dados.get(k) for k in ("nome", "email", "assunto")):
            return jsonify({"erro": "Campos obrigatórios faltando."}), 400

        db.collection("FIREDB").add({  # <- Aqui é onde foi alterado
            "nome": dados["nome"],
            "email": dados["email"],
            "assunto": dados["assunto"],
            "mensagem": dados.get("mensagem", "")
        })

        return jsonify({"mensagem": "Solicitação registrada com sucesso."}), 200

    except Exception as e:
        print(f"Erro ao salvar no Firestore: {e}")
        return jsonify({"erro": "Erro interno ao salvar"}), 500
