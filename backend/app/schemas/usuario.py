from typing import Optional
from sqlmodel import SQLModel
from pydantic import EmailStr, model_validator
from app.models.usuario import RoleEnum

# --- BASE ---
# Campos comuns que existem tanto na criação quanto na leitura
class UsuarioBase(SQLModel):
    nome: str
    email: EmailStr
    role: RoleEnum = RoleEnum.LEITOR

# --- CREATE ---
# O que o front-end envia para cadastrar
class UsuarioCreate(UsuarioBase):
    senha: str
    
    # Campo auxiliar para a regra de negócio do Bolsista (não vai pro banco direto)
    email_orientador: Optional[EmailStr] = None 

    # Validação de Regras de Negócio (US 01)
    @model_validator(mode='after')
    def validar_regras_negocio(self):
        # Regra 1: Professor deve ter email institucional
        if self.role == RoleEnum.PROFESSOR:
            if not self.email.endswith("@ufc.br"):
                raise ValueError('Professores devem utilizar um e-mail institucional (@ufc.br).')
        
        # Regra 2: Bolsista deve informar quem é o orientador
        if self.role == RoleEnum.BOLSISTA:
            if not self.email_orientador:
                raise ValueError('Alunos bolsistas devem informar o e-mail do professor orientador.')
        
        return self

# --- READ ---
# O que a API devolve para o front-end (sem senha!)
class UsuarioRead(UsuarioBase):
    id: int
    is_active: bool
    orientador_id: int | None = None


class SolicitacaoBolsa(SQLModel):
    email_orientador: EmailStr

# Input para pedir o e-mail de recuperação
class GenerateUserToken(SQLModel):
    email: EmailStr

# Input para efetivar a troca de senha
class ResetPassword(SQLModel):
    token: str
    new_password: str