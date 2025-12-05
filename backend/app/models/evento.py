from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

# Evita erro de importação circular
if TYPE_CHECKING:
    from .usuario import Usuario

class Evento(SQLModel, table=True):
    __tablename__ = "eventos"

    id: int | None = Field(default=None, primary_key=True)
    titulo: str
    descricao: str | None = None
    data_inicio: datetime
    data_fim: datetime
    local: str | None = None
    imagem_url: str | None = None
    destaque: bool = False
    criado_em: datetime = Field(default_factory=datetime.now)

    # Chave Estrangeira
    usuario_id: int | None = Field(default=None, foreign_key="usuarios.id")

    # Relacionamento: Uso de aspas "Usuario" para o SQLModel resolver depois
    usuario: Optional["Usuario"] = Relationship(back_populates="eventos")