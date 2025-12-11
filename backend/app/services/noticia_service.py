# app/services/noticia_service.py
from sqlmodel import Session, select
from fastapi import UploadFile
from typing import List, Optional
import os
from datetime import datetime # Importante para marcar a hora da exclusão

# Ajuste os imports conforme a estrutura real do seu projeto (app.db.models ou app.models)
from app.models.noticia import Noticia, Tag
from app.models.usuario import Usuario
from app.core.utils import salvar_imagem
import re
import unicodedata

class NoticiaService:
    def __init__(self, session: Session):
        self.session = session

    def _gerar_slug(self, texto: str) -> str:
        """Gera URL amigável única"""
        texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
        texto = re.sub(r'[^\w\s-]', '', texto).lower()
        base_slug = re.sub(r'[-\s]+', '-', texto).strip('-')
        
        slug_final = base_slug
        contador = 1
        
        # Verifica se existe algum slug igual (mesmo que deletado, para evitar colisão futura)
        while self.session.exec(select(Noticia).where(Noticia.slug == slug_final)).first():
            slug_final = f"{base_slug}-{contador}"
            contador += 1
            
        return slug_final

    def _processar_tags(self, tags_str: str) -> List[Tag]:
        """Processa string de tags e retorna objetos"""
        lista_nomes = [t.strip() for t in tags_str.split(",") if t.strip()]
        objetos_tags = []
        
        for nome_tag in lista_nomes:
            tag_db = self.session.exec(select(Tag).where(Tag.nome == nome_tag)).first()
            if not tag_db:
                slug_tag = self._gerar_slug(nome_tag)
                tag_db = Tag(nome=nome_tag, slug=slug_tag)
                self.session.add(tag_db)
                self.session.commit()
                self.session.refresh(tag_db)
            objetos_tags.append(tag_db)
            
        return objetos_tags

    def criar_noticia(self, titulo: str, conteudo: str, subtitulo: str, tags_str: str, imagem: UploadFile, autor: Usuario) -> Noticia:
        """Cria notícia nova"""
        caminho_imagem = salvar_imagem(imagem)
        slug = self._gerar_slug(titulo)
        lista_tags = self._processar_tags(tags_str)
        
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

    # --- [US 03] MÉTODOS DE LEITURA (COM SOFT DELETE) ---

    def listar_noticias(self, skip: int = 0, limit: int = 10) -> List[Noticia]:
        """Retorna lista paginada de notícias ATIVAS (não deletadas)"""
        return self.session.exec(
            select(Noticia)
            .where(Noticia.deleted_at == None) # <--- FILTRO DE SOFT DELETE
            .offset(skip)
            .limit(limit)
            .order_by(Noticia.criado_em.desc())
        ).all()

    def buscar_por_slug(self, slug: str) -> Optional[Noticia]:
        """Busca notícia ativa pelo link amigável"""
        return self.session.exec(
            select(Noticia)
            .where(Noticia.slug == slug)
            .where(Noticia.deleted_at == None) # <--- Garante que não traz deletada
        ).first()

    def buscar_por_id(self, id: int) -> Optional[Noticia]:
        """Busca notícia ativa pelo ID"""
        # Trocamos session.get por select para poder filtrar deleted_at
        return self.session.exec(
            select(Noticia)
            .where(Noticia.id == id)
            .where(Noticia.deleted_at == None)
        ).first()

    # --- [US 06] SOFT DELETE ---
    
    def deletar_noticia(self, noticia: Noticia):
        """
        Apenas marca a data de exclusão.
        NÃO remove a imagem do disco (para permitir restauração futura).
        """
        noticia.deleted_at = datetime.now() # <--- "Carimba" a saída
        
        self.session.add(noticia)
        self.session.commit()
        self.session.refresh(noticia)

    # --- [US 05] UPDATE ---

    def atualizar_noticia(
        self, 
        noticia_db: Noticia, 
        titulo: Optional[str], 
        conteudo: Optional[str], 
        subtitulo: Optional[str],
        tags_str: Optional[str], 
        imagem: Optional[UploadFile]
    ) -> Noticia:
        
        if titulo:
            noticia_db.titulo = titulo
        if conteudo:
            noticia_db.conteudo = conteudo
        if subtitulo is not None:
            noticia_db.subtitulo = subtitulo

        if tags_str is not None:
            noticia_db.tags = self._processar_tags(tags_str)

        if imagem:
            # Aqui mantemos a lógica de apagar a imagem velha pois é uma SUBSTITUIÇÃO,
            # não uma exclusão da notícia.
            if noticia_db.imagem_capa:
                try:
                    old_path = noticia_db.imagem_capa.lstrip("/")
                    if os.path.exists(old_path):
                        os.remove(old_path)
                except Exception:
                    pass 
            
            noticia_db.imagem_capa = salvar_imagem(imagem)

        self.session.add(noticia_db)
        self.session.commit()
        self.session.refresh(noticia_db)
        return noticia_db