from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    # Removemos CurtidaComentario daqui
    from .noticia import Noticia, CurtidaNoticia
    from .comentario import Comentario
    
    # IMPORTANTE: Se o arquivo app/models/evento.py não existir, 
    # comente a linha abaixo para não dar erro 500.
    from .evento import Evento 

# Definindo os papeis fixos do sistema
class RoleEnum(str, Enum):
    ADMIN = "admin"
    PROFESSOR = "professor"
    BOLSISTA = "bolsista"
    LEITOR = "leitor"

class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: int | None = Field(default=None, primary_key=True)
    nome: str
    email: str = Field(unique=True, index=True)
    senha_hash: str
    
    # Define o papel do usuário (Padrão é leitor)
    role: RoleEnum = Field(default=RoleEnum.LEITOR)

    # validando professor/usuário ativo
    is_active: bool = Field(default=True)
    
    criado_em: datetime = Field(default_factory=datetime.now)

    # --- HIERARQUIA (Orientador <-> Bolsista) ---
    orientador_id: int | None = Field(default=None, foreign_key="usuarios.id")

    orientador: Optional["Usuario"] = Relationship(
        back_populates="bolsistas", 
        sa_relationship_kwargs={"remote_side": "Usuario.id"}
    )

    bolsistas: List["Usuario"] = Relationship(back_populates="orientador")

    # --- RELACIONAMENTOS DE CONTEÚDO ---
    
    noticias: List["Noticia"] = Relationship(back_populates="autor")
    
    comentarios: List["Comentario"] = Relationship(back_populates="usuario")
    
    # Curtidas em Notícias (O que você queria)
    curtidas_noticias: List["CurtidaNoticia"] = Relationship(back_populates="usuario")

    # --- RELACIONAMENTOS FUTUROS ---
    # Se Evento já existir, mantenha. Se não, comente para evitar erro "failed to locate name".
    eventos: List["Evento"] = Relationship(back_populates="usuario")