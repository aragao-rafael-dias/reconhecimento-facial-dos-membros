from flask import render_template, request, jsonify
from . import create_app
from .database import salvar_embedding_no_banco, buscar_embeddings_no_banco
from .face_recognition import gerar_embedding, comparar_faces, carregar_encodings
from .utils import gerar_pdf, enviar_email
from datetime import datetime

app = create_app()

ENCODINGS = carregar_encodings()
presentes = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reconhecer', methods=['POST'])
def reconhecer_rosto():
    if 'foto' not in request.files:
        return jsonify({"mensagem": "Nenhuma foto enviada!"}), 400
    
    foto = request.files['foto']

    foto_path = f"temp/{foto.filename}"
    foto.save(foto_path)
    encoding_foto = gerar_embedding(foto_path)

    if encoding_foto is None:
        return jsonify({"mensagem": "Nenhum rosto encontrado na imagem!"}), 400

    for membro in ENCODINGS:
        if comparar_faces(encoding_foto, membro["encoding"]):
            nome_membro = membro["nome"]
            if nome_membro not in presentes:
                presentes.append({"nome": nome_membro, "hora": datetime.now().strftime("%H: %M: %S")})
            return jsonify({"mensagem": f"Rosto recohecido: {nome_membro}"}), 200
    
    return jsonify({"mensagem": "Nenhuma correspondência encontrada!"}), 404

@app.route('/gerar_pdf', methods=['GET'])
def gerar_pdf_presencas():
    if not presentes:
        return jsonify({"mensagem": "Nenhuma presença registrada"})
    
    caminho_pdf = gerar_pdf(presentes)

    envio_sucesso = enviar_email(caminho_pdf)
    if envio_sucesso:
        presentes.clear()
        return jsonify({"mensagem": f"PDF gerado e enviado para os e-mails"}), 200
    else:
        return jsonify({"mensagem": "Erro ao enviar o e-mail"}), 500
    