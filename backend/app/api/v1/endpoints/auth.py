# app/api/endpoints/auth.py
from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from sqlmodel import select
from jose import jwt, JWTError # type: ignore
from pydantic import ValidationError

from app.core.database import SessionDep
from app.core.security import verify_password, create_access_token, get_password_hash
from app.core.config import settings
from app.core.email import enviar_email_simples
from app.models.usuario import Usuario 
from app.schemas.token import Token
# Importe os novos schemas aqui
from app.schemas.usuario import GenerateUserToken, ResetPassword 

router = APIRouter()

# ... (Rota /login continua igual) ...
@router.post("/login", response_model=Token)
def login_access_token(
    session: SessionDep, 
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    usuario = session.exec(
        select(Usuario).where(Usuario.email == form_data.username)
    ).first()

    if not usuario or not verify_password(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not usuario.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo.")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": usuario.email, "role": usuario.role.value},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


# ... (Rota /verificar continua igual) ...
@router.get("/verificar", response_class=HTMLResponse)
def verificar_email(email: str, session: SessionDep):
    usuario = session.exec(select(Usuario).where(Usuario.email == email)).first()
    if not usuario:
        return HTMLResponse(content="<h1>Erro</h1><p>Usuário não encontrado.</p>", status_code=404)
    if usuario.is_active:
        return HTMLResponse(content="<h1>Conta já ativa!</h1>")

    usuario.is_active = True
    session.add(usuario)
    session.commit()
    return HTMLResponse(content="<h1 style='color:green'>Sucesso! Conta ativada.</h1>")


# --- NOVAS ROTAS DE REDEFINIÇÃO DE SENHA ---

@router.post("/recover-password")
def recover_password(
    input_data: GenerateUserToken,
    session: SessionDep,
    background_tasks: BackgroundTasks
):
    """
    1. Recebe o e-mail.
    2. Gera token de 10 min.
    3. Envia e-mail com o token.
    """
    usuario = session.exec(
        select(Usuario).where(Usuario.email == input_data.email)
    ).first()

    if not usuario:
        # Por segurança, não dizemos se o e-mail existe ou não, apenas retornamos sucesso.
        # Mas para debug agora, se quiser, pode retornar 404.
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Gera token curto (10 minutos)
    token_expires = timedelta(minutes=10)
    reset_token = create_access_token(
        data={"sub": usuario.email, "type": "reset"}, # 'type' diferencia de login normal
        expires_delta=token_expires
    )

    # Monta o email
    # Como não temos front-end, enviamos o Token para ser usado no Swagger
    html_content = f"""
    <h1>Recuperação de Senha</h1>
    <p>Você solicitou a troca de senha. Copie o token abaixo e use na API:</p>
    <p style="background: #eee; padding: 10px; font-family: monospace;">{reset_token}</p>
    <p><b>Este token expira em 10 minutos.</b></p>
    <p>Se você tivesse um front-end, o link seria: <br>
       <a href="http://localhost:3000/reset-password?token={reset_token}">Redefinir Senha</a>
    </p>
    """

    background_tasks.add_task(
        enviar_email_simples,
        "Recuperação de Senha - Jornal UFC",
        [usuario.email],
        html_content
    )

    return {"message": "E-mail de recuperação enviado (se o usuário existir)."}


@router.post("/reset-password")
def reset_password(
    input_data: ResetPassword,
    session: SessionDep
):
    """
    Recebe o token e a nova senha para efetivar a troca.
    """
    try:
        # 1. Decodifica e valida o token
        payload = jwt.decode(
            input_data.token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if email is None or token_type != "reset":
            raise HTTPException(status_code=400, detail="Token inválido")
            
    except (JWTError, ValidationError):
        raise HTTPException(status_code=400, detail="Token expirado ou inválido")

    # 2. Busca usuário
    usuario = session.exec(select(Usuario).where(Usuario.email == email)).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # 3. Atualiza senha
    usuario.senha_hash = get_password_hash(input_data.new_password)
    session.add(usuario)
    session.commit()

    return {"message": "Senha alterada com sucesso."}