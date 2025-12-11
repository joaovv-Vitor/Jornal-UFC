# app/db/schemas/noticia.py
from sqlmodel import SQLModel
from datetime import datetime
from typing import List, Optional

# --- SCHEMAS DE TAG ---
# Usado apenas para leitura dentro da notícia
class TagRead(SQLModel):
    id: int
    nome: str
    slug: str

# --- SCHEMAS DE NOTICIA ---

# 1. Base: Campos comuns a todos
class NoticiaBase(SQLModel):
    titulo: str
    subtitulo: Optional[str] = None
    conteudo: str
    categoria_id: Optional[int] = None

# 2. Create: Validação (embora a gente use Form no Controller, é bom ter)
class NoticiaCreate(NoticiaBase):
    tags: List[str] = [] # O front manda uma lista de strings: ["Esporte", "UFC"]

# 3. Read: O JSON que o Front-end recebe
class NoticiaRead(NoticiaBase):
    id: int
    slug: str
    imagem_capa: Optional[str] = None
    criado_em: datetime
    atualizado_em: datetime
    publicado: bool
    
    autor_id: int
    
    # Aqui está a mágica: O Pydantic converte a lista de objetos do banco 
    # para essa lista de schemas automaticamente
    tags: List[TagRead] = [] 
    
    # Dica: Se quiser retornar o nome do autor, precisaremos fazer um ajuste no controller,
    # mas por enquanto vamos manter simples.