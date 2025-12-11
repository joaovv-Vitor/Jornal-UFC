# app/services/noticia_service.py
from sqlmodel import Session, select
from fastapi import UploadFile, HTTPException
from typing import List

from app.models.noticia import Noticia, Tag
from app.models.usuario import Usuario
from app.core.utils import salvar_imagem
import re
import unicodedata

class NoticiaService:
    def __init__(self, session: Session):
        self.session = session

    def _gerar_slug(self, texto: str) -> str:
        """Método interno para gerar slug único"""
        texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
        texto = re.sub(r'[^\w\s-]', '', texto).lower()
        base_slug = re.sub(r'[-\s]+', '-', texto).strip('-')
        
        slug_final = base_slug
        contador = 1
        
        # Verifica duplicidade no banco
        while self.session.exec(select(Noticia).where(Noticia.slug == slug_final)).first():
            slug_final = f"{base_slug}-{contador}"
            contador += 1
            
        return slug_final

    def _processar_tags(self, tags_str: str) -> List[Tag]:
        """Recebe 'ufc, edital' e retorna lista de objetos Tag"""
        lista_nomes = [t.strip() for t in tags_str.split(",") if t.strip()]
        objetos_tags = []
        
        for nome_tag in lista_nomes:
            tag_db = self.session.exec(select(Tag).where(Tag.nome == nome_tag)).first()
            if not tag_db:
                slug_tag = self._gerar_slug(nome_tag) # Reusa a lógica de slug
                tag_db = Tag(nome=nome_tag, slug=slug_tag)
                self.session.add(tag_db)
                self.session.commit()
                self.session.refresh(tag_db)
            objetos_tags.append(tag_db)
            
        return objetos_tags

    def criar_noticia(self, titulo: str, conteudo: str, subtitulo: str, tags_str: str, imagem: UploadFile, autor: Usuario) -> Noticia:
        """Orquestra a criação da notícia"""
        
        # 1. Upload
        caminho_imagem = salvar_imagem(imagem)
        
        # 2. Slug
        slug = self._gerar_slug(titulo)
        
        # 3. Tags
        lista_tags = self._processar_tags(tags_str)
        
        # 4. Criar Objeto
        nova_noticia = Noticia(
            titulo=titulo,
            subtitulo=subtitulo,
            conteudo=conteudo,
            slug=slug,
            imagem_capa=caminho_imagem,
            autor_id=autor.id,
            tags=lista_tags,
            publicado=True
        )
        
        self.session.add(nova_noticia)
        self.session.commit()
        self.session.refresh(nova_noticia)
        
        return nova_noticia