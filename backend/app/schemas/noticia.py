# app/db/schemas/noticia.py
from sqlmodel import SQLModel
from datetime import datetime
from typing import List, Optional

# --- SCHEMAS AUXILIARES ---

class NoticiaImagemRead(SQLModel):
    id: int
    caminho: str

class TagRead(SQLModel):
    id: int
    nome: str
    slug: str

class CategoriaRead(SQLModel):
    id: int
    nome: str

class AutorRead(SQLModel):
    id: int
    nome: str
    email: str
    # avatar: Optional[str] = None (Adicione se seu usuário tiver foto)

# --- SCHEMAS DE NOTICIA ---

# 1. Base: Campos comuns a todos
class NoticiaBase(SQLModel):
    titulo: str
    subtitulo: Optional[str] = None
    conteudo: str
    categoria_id: Optional[int] = None

# 2. Create: Validação
class NoticiaCreate(NoticiaBase):
    tags: List[str] = [] 

# 3. Read: O JSON que o Front-end recebe
class NoticiaRead(NoticiaBase):
    id: int
    slug: str
    imagem_capa: Optional[str] = None
    criado_em: datetime
    atualizado_em: datetime
    publicado: bool
    
    autor_id: int
    
    # --- RELACIONAMENTOS ---
    
    # Lista de Tags
    tags: List[TagRead] = [] 
    
    # Categoria (Objeto completo, não só ID)
    categoria: Optional[CategoriaRead] = None 
    
    # Autor (Para mostrar "Por Fulano")
    autor: Optional[AutorRead] = None 

    # --- NOVA LISTA DE GALERIA ---
    # Aqui conectamos o schema que você criou no topo
    imagens_galeria: List[NoticiaImagemRead] = []