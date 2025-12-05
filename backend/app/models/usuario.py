from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

# Importação condicional para evitar ciclo
if TYPE_CHECKING:
    from .noticia import Noticia, CurtidaNoticia # Importar CurtidaNoticia
    from .comentario import Comentario, CurtidaComentario # Importar CurtidaComentario
    from .evento import Evento
    
class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: int | None = Field(default=None, primary_key=True)
    nome: str
    email: str = Field(unique=True, index=True)
    senha_hash: str
    role: str = Field(default="leitor")
    criado_em: datetime = Field(default_factory=datetime.now)

    # Note as aspas em "Noticia", "Comentario", etc.
    noticias: list["Noticia"] = Relationship(back_populates="autor")
    comentarios: list["Comentario"] = Relationship(back_populates="usuario")
    eventos: list["Evento"] = Relationship(back_populates="usuario")

    curtidas_noticias: list["CurtidaNoticia"] = Relationship(back_populates="usuario")
    curtidas_comentarios: list["CurtidaComentario"] = Relationship(back_populates="usuario")
