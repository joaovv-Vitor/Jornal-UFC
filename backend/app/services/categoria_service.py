from sqlmodel import Session, select
from typing import List, Optional
import unicodedata
import re

from app.models.categoria import Categoria

class CategoriaService:
    def __init__(self, session: Session):
        self.session = session

    def _gerar_slug(self, texto: str) -> str:
        """Gera slug simples (ex: 'Ciência & Tec' -> 'ciencia-tec')"""
        texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
        texto = re.sub(r'[^\w\s-]', '', texto).lower()
        return re.sub(r'[-\s]+', '-', texto).strip('-')

    def criar_categoria(self, nome: str) -> Categoria:
        slug = self._gerar_slug(nome)
        
        # Verifica duplicidade
        existente = self.session.exec(select(Categoria).where(Categoria.slug == slug)).first()
        if existente:
            return existente # Ou raise Exception, depende da regra

        categoria = Categoria(nome=nome, slug=slug)
        self.session.add(categoria)
        self.session.commit()
        self.session.refresh(categoria)
        return categoria

    def listar_categorias(self) -> List[Categoria]:
        return self.session.exec(select(Categoria).order_by(Categoria.nome)).all()

    def deletar_categoria(self, id: int):
        categoria = self.session.get(Categoria, id)
        if categoria:
            self.session.delete(categoria)
            self.session.commit()