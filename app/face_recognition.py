import face_recognition
import numpy as np
from utils import carregar_membros  
import os

def carregar_encodings():
    membros = carregar_membros()  
    encodings = []

    for membro in membros:
        caminho_foto = membro['foto']  
        if os.path.exists(caminho_foto):  
            try:
                imagem = face_recognition.load_image_file(caminho_foto)  
                encoding = face_recognition.face_encodings(imagem)  
                if encoding:  
                    encodings.append({
                        "nome": membro['nome'],
                        "encoding": encoding[0]  
                    })
                else:
                    print(f"Atenção: Nenhum rosto encontrado na foto {caminho_foto}")
            except Exception as e:
                print(f"Erro ao processar {caminho_foto}: {e}")
        else:
            print(f"Atenção: Foto não encontrada em {caminho_foto}")
    return encodings


def gerar_embedding(imagem_path):
    try:
        imagem = face_recognition.load_image_file(imagem_path)  
        face_encoding = face_recognition.face_encodings(imagem)  

        if len(face_encoding) > 0:  
            return face_encoding[0] 
        else:
            print(f"Nenhum rosto encontrado na imagem {imagem_path}")
            return None
    except Exception as e:
        print(f"Erro ao gerar embedding: {e}")
        return None


def comparar_faces(imagem_encoding, embedding_banco):
    try:
        return face_recognition.compare_faces([embedding_banco], imagem_encoding)[0]
    except Exception as e:
        print(f"Erro ao comparar faces: {e}")
        return False
