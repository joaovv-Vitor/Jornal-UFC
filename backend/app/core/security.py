# app/core/security.py
from passlib.context import CryptContext

# Configura o algoritmo Bcrypt (padrão da indústria)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha em texto puro bate com o hash salvo no banco.
    Usado no Login.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Gera o hash da senha.
    Usado no Cadastro (Register).
    """
    return pwd_context.hash(password)