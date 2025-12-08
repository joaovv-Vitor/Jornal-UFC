from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .noticia import Noticia, CurtidaNoticia
    from .comentario import Comentario, CurtidaComentario
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

    #validando professor
    is_active: bool = Field(default=True)
    
    criado_em: datetime = Field(default_factory=datetime.now)

    # --- HIERARQUIA (Quem é o chefe?) ---
    # Se for Bolsista, esse campo guarda o ID do Professor
    orientador_id: int | None = Field(default=None, foreign_key="usuarios.id")

    # Relacionamento para acessar o objeto do Professor (Orientador)
    # remote_side=[id] é OBRIGATÓRIO em auto-relacionamentos no SQLModel/SQLAlchemy
    orientador: Optional["Usuario"] = Relationship(
        back_populates="bolsistas", 
        sa_relationship_kwargs={"remote_side": "Usuario.id"}
    )

    # Relacionamento para o Professor ver sua lista de alunos
    bolsistas: List["Usuario"] = Relationship(back_populates="orientador")

    # --- Relacionamentos de Conteúdo ---
    noticias: List["Noticia"] = Relationship(back_populates="autor")
    comentarios: List["Comentario"] = Relationship(back_populates="usuario")
    eventos: List["Evento"] = Relationship(back_populates="usuario")
    
    # --- Relacionamentos de Curtidas ---
    curtidas_noticias: List["CurtidaNoticia"] = Relationship(back_populates="usuario")
    curtidas_comentarios: List["CurtidaComentario"] = Relationship(back_populates="usuario")