# app/api/deps.py
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlmodel import select

from app.core.config import settings
from app.core.database import SessionDep
from app.models.usuario import Usuario
from app.schemas.token import TokenData

# 1. Configura o Swagger para saber onde pegar o token
# O caminho deve bater com sua rota de login (/api/v1/auth/login)
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def get_current_user(
    session: SessionDep, 
    token: Annotated[str, Depends(reusable_oauth2)]
) -> Usuario:
    """
    Função que valida o Token JWT e retorna o Usuário logado.
    Se o token for inválido ou expirado, lança erro 401.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 2. Decodifica o Token JWT usando a SECRET_KEY
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
            
        token_data = TokenData(email=email)
        
    except (JWTError, ValidationError):
        raise credentials_exception

    # 3. Busca o usuário no banco de dados
    user = session.exec(select(Usuario).where(Usuario.email == token_data.email)).first()
    
    if user is None:
        raise credentials_exception
        
    # 4. Bloqueia se a conta estiver inativa (ainda não ativou o email)
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
        
    return user

# Atalho para usar nas rotas: CurrentUser
# Ao colocar isso na função da rota, o FastAPI exige login automaticamente
CurrentUser = Annotated[Usuario, Depends(get_current_user)]