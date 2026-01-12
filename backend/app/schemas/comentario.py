from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional

# Schema simples para mostrar quem comentou
class AutorComentarioRead(SQLModel):
    id: int
    nome: str
    email: str
    # avatar: Optional[str] = None

# O que o usuário envia
class ComentarioCreate(SQLModel):
    conteudo: str

# O que o front recebe
class ComentarioRead(SQLModel):
    id: int
    conteudo: str
    criado_em: datetime
    usuario_id: int
    oculto: bool
    
    # Nested object: permite acessar comentario.usuario.nome no front
    usuario: AutorComentarioRead