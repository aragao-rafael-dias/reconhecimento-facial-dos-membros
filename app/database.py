import json
import mysql.connector
import numpy as np
from .face_recognition import gerar_embedding
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("MYSQL_ROOT_PASSWORD")
DB_HOST = os.getenv("MYSQL_HOST")
DB_USER= os.getenv("MYSQL_USER")
DB_PASSWORD =  os.getenv("MYSQL_PASSWORD")
DB_NAME =  os.getenv("MYSQL_DATABASE")

def salvar_embedding_no_banco(nome, imagem_path):
    embedding = gerar_embedding(imagem_path)
    if embedding is None:
        return None
    
    embedding_str = json.dumps(embedding.tolist())
    
    conn = mysql.connector.connect(
        host = DB_HOST,
        user = DB_USER,
        password = DB_PASSWORD,
        database = DB_NAME  
    ) 
    cursor = conn.cursor()
    
    cursor.execute('''INSERT INTO membros (nome, embedding) VALUES (%s, %s)''', (nome, embedding_str))
    
    conn.commit()
    cursor.close()
    conn.close()

def buscar_embeddings_no_banco():
    conn = mysql.connector.connect(
        host = DB_HOST,
        user = DB_USER,
        password = DB_PASSWORD,
        database = DB_NAME 
    )
    cursor = conn.cursor()

    cursor.execute('SELECT id, nome, embedding FROM membros')
    membros = cursor.fetchall()

    cursor.close()
    conn.close()

    return membros