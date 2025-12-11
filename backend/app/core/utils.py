# app/core/utils.py
import shutil
import os
from uuid import uuid4
from fastapi import UploadFile

# Define onde salvar (dentro do container Docker)
UPLOAD_DIR = "static/images"

def salvar_imagem(file: UploadFile) -> str:
    """
    Recebe um arquivo de imagem, gera um nome único e salva no disco.
    Retorna a URL relativa para salvar no banco de dados.
    Ex: recebe 'minha_foto.jpg' -> retorna '/static/images/a1b2-c3d4-e5f6.jpg'
    """
    # 1. Cria a pasta se ela não existir
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # 2. Gera nome único: uuid + extensão original
    # Ex: 'foto.png' vira 'f47ac10b-58cc-4372-a567-0e02b2c3d479.png'
    filename = file.filename or "imagem_sem_nome"
    extensao = filename.split(".")[-1]
    novo_nome = f"{uuid4()}.{extensao}"
    
    caminho_completo = os.path.join(UPLOAD_DIR, novo_nome)
    
    # 3. Salva o arquivo fisicamente no disco
    with open(caminho_completo, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Retorna o caminho que o Front vai usar para acessar a imagem
    return f"/static/images/{novo_nome}"