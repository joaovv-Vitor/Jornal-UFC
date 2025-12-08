# app/core/email.py
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from app.core.config import settings
from typing import List

# Configuração da biblioteca usando nossas variáveis de ambiente
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def enviar_email_simples(assunto: str, emails_destino: List[EmailStr], corpo_html: str):
    """
    Envia um e-mail assíncrono.
    """
    message = MessageSchema(
        subject=assunto,
        recipients=emails_destino,
        body=corpo_html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)