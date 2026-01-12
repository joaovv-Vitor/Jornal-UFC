from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.usuario import Usuario
    from app.models.noticia import Noticia

class Comentario(SQLModel, table=True):
    __tablename__ = "comentarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    conteudo: str
    oculto: bool = Field(default=False) # [US 11] Para ocultar comentários
    criado_em: datetime = Field(default_factory=datetime.now)

    # Foreign Keys
    usuario_id: int = Field(foreign_key="usuarios.id")
    noticia_id: int = Field(foreign_key="noticias.id")

    # Relacionamentos
    usuario: "Usuario" = Relationship(back_populates="comentarios")
    noticia: "Noticia" = Relationship(back_populates="comentarios")