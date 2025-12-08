# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr

class Settings(BaseSettings):
    PROJECT_NAME: str = "Jornal UFC API"
    API_V1_STR: str = "/api/v1"
    
    # Banco de Dados
    # Atenção: O Pydantic vai tentar ler isso do arquivo .env
    DATABASE_URL: str

    # Segurança (JWT)
    SECRET_KEY: str = "sua_chave_super_secreta_e_aleatoria_aqui"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --- CONFIGURAÇÃO CORRETA (Pydantic v2) ---
    # Removemos qualquer "class Config" e usamos apenas isto:
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore", # Ignora variáveis extras no .env que não estão listadas aqui
        case_sensitive=True
    )

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int = 587
    MAIL_SERVER: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False

settings = Settings()