from flask import Blueprint, render_template, request, jsonify
from .database import salvar_embedding_no_banco, buscar_embeddings_no_banco
from .face_recognition import gerar_embedding, comparar_faces, carregar_encodings
from .utils import gerar_pdf, enviar_email
from datetime import datetime
import os

routes = Blueprint('routes', __name__)

ENCODINGS = carregar_encodings()
presentes = []

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/reconhecer', methods=['POST'])
def reconhecer_rosto():
    if 'foto' not in request.files:
        return jsonify({"mensagem": "Nenhuma foto enviada!"}), 400
    
    foto = request.files['foto']

    os.makedirs("temp", exist_ok=True)

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

@routes.route('/lista_presencas', methods=['GET'])
def listar_presencas():
    return jsonify({"presentes": presentes})

@routes.route('/gerar_pdf', methods=['POST'])
def gerar_pdf_presencas():
    if not presentes:
        return jsonify({"mensagem": "Nenhuma presença registrada!"}), 400
    
    try:
        # Gera o PDF com a lista de presenças
        caminho_pdf = gerar_pdf(presentes)

        # Envia o PDF por e-mail
        enviar_email(caminho_pdf)

        # Limpa a lista de presenças após o envio
        presentes.clear()

        return jsonify({"mensagem": "PDF gerado e enviado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"mensagem": f"Erro ao gerar/enviar o PDF: {str(e)}"}), 500