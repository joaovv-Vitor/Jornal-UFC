from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .usuario import Usuario
    from .noticia import Noticia

# ---Curtidas em Comentários ---
class CurtidaComentario(SQLModel, table=True):
    __tablename__ = "curtidas_comentarios"

    usuario_id: int = Field(foreign_key="usuarios.id", primary_key=True)
    comentario_id: int = Field(foreign_key="comentarios.id", primary_key=True)
    criado_em: datetime = Field(default_factory=datetime.now)

    usuario: "Usuario" = Relationship(back_populates="curtidas_comentarios")
    comentario: "Comentario" = Relationship(back_populates="curtidas")

class Comentario(SQLModel, table=True):
    __tablename__ = "comentarios"

    id: int | None = Field(default=None, primary_key=True)
    conteudo: str
    criado_em: datetime = Field(default_factory=datetime.now)
    aprovado: bool = True
    
    usuario_id: int | None = Field(default=None, foreign_key="usuarios.id")
    noticia_id: int | None = Field(default=None, foreign_key="noticias.id")

    usuario: Optional["Usuario"] = Relationship(back_populates="comentarios")
    noticia: Optional["Noticia"] = Relationship(back_populates="comentarios")

    # --- NOVO RELACIONAMENTO ---
    curtidas: list["CurtidaComentario"] = Relationship(back_populates="comentario")