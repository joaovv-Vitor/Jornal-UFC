from sqlmodel import SQLModel
from typing import Optional

# Base
class CategoriaBase(SQLModel):
    nome: str

# Create (O que o usuário envia)
class CategoriaCreate(CategoriaBase):
    pass

# Read (O que o usuário recebe)
class CategoriaRead(CategoriaBase):
    id: int
    slug: str