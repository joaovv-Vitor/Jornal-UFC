# app/api/endpoints/auth.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from fastapi.responses import HTMLResponse

from app.core.database import SessionDep
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.models.usuario import Usuario
from app.schemas.token import Token
from datetime import timedelta
from app.models.usuario import Usuario

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    session: SessionDep, 
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    # 1. Busca usuário pelo email (O form envia 'username', mas nós usamos email)
    usuario = session.exec(
        select(Usuario).where(Usuario.email == form_data.username)
    ).first()

    # 2. Validações
    if not usuario or not verify_password(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not usuario.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo. Verifique seu e-mail ou aguarde aprovação."
        )

    # 3. Gera o Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": usuario.email, "role": usuario.role.value}, # Guardamos o Role no token!
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")

@router.get("/verificar", response_class=HTMLResponse)
def verificar_email(email: str, session: SessionDep):
    """
    Rota acessada pelo link enviado por e-mail.
    Ativa a conta do Professor.
    """
    # 1. Busca o usuário
    usuario = session.exec(select(Usuario).where(Usuario.email == email)).first()

    # 2. Se não achar, erro
    if not usuario:
        return HTMLResponse(content="<h1>Erro</h1><p>Usuário não encontrado.</p>", status_code=404)

    # 3. Se já estiver ativo
    if usuario.is_active:
        return HTMLResponse(content="""
            <h1 style="color: green;">Conta Já Ativa!</h1>
            <p>Você já pode fazer login no sistema.</p>
        """)

    # 4. ATIVA A CONTA
    usuario.is_active = True
    session.add(usuario)
    session.commit()

    # 5. Retorna página de sucesso
    return HTMLResponse(content=f"""
        <div style="font-family: sans-serif; text-align: center; padding-top: 50px;">
            <h1 style="color: #28a745;">Sucesso!</h1>
            <p>Olá, <b>{usuario.nome}</b>.</p>
            <p>Sua conta de Professor foi confirmada com sucesso.</p>
            <p>Você já pode fechar esta janela e fazer login na API.</p>
        </div>
    """)