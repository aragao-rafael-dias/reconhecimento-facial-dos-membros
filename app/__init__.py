from flask import Flask
import mysql.connector
from config import Config

def create_app():
    app = Flask(__name__)

    # Configuração do Flask
    app.config.from_object(Config)

    # Inicializar a conexão com o banco de dados dentro do contexto da aplicação
    def init_db():
        # A configuração já estará carregada no app.config
        conn = mysql.connector.connect(
            host=app.config['DB_HOST'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            database=app.config['DB_NAME']
        )
        app.db = conn

    # Chama a inicialização do banco ao iniciar a aplicação
    with app.app_context():
        init_db()

    return app
