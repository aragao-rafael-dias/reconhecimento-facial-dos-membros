# Use uma imagem base com Python
FROM python:3.9-slim

# Instale as dependências do sistema necessárias para o dlib
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libatlas-base-dev \
    && apt-get clean

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos do projeto para dentro do contêiner
COPY . .

# Instale as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta onde a aplicação será executada
EXPOSE 5000

# Comando padrão para rodar a aplicação
CMD ["python", "run.py"]
