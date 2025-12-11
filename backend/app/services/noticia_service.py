import os
import re
import unicodedata
from datetime import datetime
from typing import List, Optional

from fastapi import UploadFile
from sqlmodel import Session, select

# --- IMPORTAÇÕES CORRETAS (MODELOS SEPARADOS) ---
# Importamos cada entidade do seu respectivo arquivo para evitar erros de ciclo/duplicação
from app.models.noticia import Noticia
from app.models.tag import Tag
from app.models.imagem import NoticiaImagem
from app.models.usuario import Usuario

from app.core.utils import salvar_imagem

class NoticiaService:
    def __init__(self, session: Session):
        self.session = session

    def _gerar_slug(self, texto: str) -> str:
        """Gera URL amigável única baseada no título."""
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
        """
        Recebe string "Futebol, Esporte" e retorna objetos Tag.
        Cria a tag no banco se ela não existir.
        """
        if not tags_str:
            return []
            
        lista_nomes = [t.strip() for t in tags_str.split(",") if t.strip()]
        objetos_tags = []
        
        for nome_tag in lista_nomes:
            # Busca na tabela de Tags
            tag_db = self.session.exec(select(Tag).where(Tag.nome == nome_tag)).first()
            
            if not tag_db:
                slug_tag = self._gerar_slug(nome_tag)
                tag_db = Tag(nome=nome_tag, slug=slug_tag)
                self.session.add(tag_db)
                self.session.commit()
                self.session.refresh(tag_db)
            
            objetos_tags.append(tag_db)
            
        return objetos_tags

    def criar_noticia(
        self, 
        titulo: str, 
        conteudo: str, 
        subtitulo: str, 
        tags_str: str, 
        imagem_capa: UploadFile, 
        autor: Usuario,
        categoria_id: Optional[int] = None,
        galeria: List[UploadFile] = [] # Lista de imagens extras
    ) -> Noticia:
        """
        Cria a notícia, salva a capa e processa a galeria de imagens.
        """
        # 1. Salva a imagem principal (Capa)
        caminho_capa = salvar_imagem(imagem_capa)
        
        # 2. Gera dados auxiliares
        slug = self._gerar_slug(titulo)
        lista_tags = self._processar_tags(tags_str)
        
        # 3. Cria o objeto Noticia (Tabela Principal)
        nova_noticia = Noticia(
            titulo=titulo, 
            subtitulo=subtitulo, 
            conteudo=conteudo, 
            slug=slug,
            imagem_capa=caminho_capa, 
            autor_id=autor.id, 
            tags=lista_tags, 
            publicado=True,
            categoria_id=categoria_id
        )
        
        self.session.add(nova_noticia)
        self.session.commit()
        self.session.refresh(nova_noticia) # Importante: recupera o ID gerado

        # 4. Processa a Galeria (Tabela NoticiaImagem)
        if galeria:
            for foto in galeria:
                # O UploadFile pode vir vazio se o campo for opcional no form
                if foto.filename:
                    caminho_foto = salvar_imagem(foto)
                    
                    # Cria o registro na tabela separada vinculando pelo ID
                    nova_imagem = NoticiaImagem(
                        caminho=caminho_foto,
                        noticia_id=nova_noticia.id
                    )
                    self.session.add(nova_imagem)
            
            self.session.commit()
            self.session.refresh(nova_noticia) # Atualiza para trazer a lista populada

        return nova_noticia

    # --- MÉTODOS DE LEITURA (CONSIDERANDO SOFT DELETE) ---

    def listar_noticias(self, skip: int = 0, limit: int = 10) -> List[Noticia]:
        return self.session.exec(
            select(Noticia)
            .where(Noticia.deleted_at == None)
            .offset(skip)
            .limit(limit)
            .order_by(Noticia.criado_em.desc())
        ).all()

    def buscar_por_slug(self, slug: str) -> Optional[Noticia]:
        return self.session.exec(
            select(Noticia)
            .where(Noticia.slug == slug)
            .where(Noticia.deleted_at == None)
        ).first()

    def buscar_por_id(self, id: int) -> Optional[Noticia]:
        return self.session.exec(
            select(Noticia)
            .where(Noticia.id == id)
            .where(Noticia.deleted_at == None)
        ).first()

    # --- UPDATE ---

    def atualizar_noticia(
        self, 
        noticia_db: Noticia, 
        titulo: Optional[str], 
        conteudo: Optional[str], 
        subtitulo: Optional[str],
        tags_str: Optional[str], 
        categoria_id: Optional[int],
        imagem_capa: Optional[UploadFile],
        galeria: List[UploadFile] = []
    ) -> Noticia:
        
        # Atualiza campos simples
        if titulo:
            noticia_db.titulo = titulo
        if conteudo:
            noticia_db.conteudo = conteudo
        if subtitulo is not None:
            noticia_db.subtitulo = subtitulo
        if categoria_id is not None:
            noticia_db.categoria_id = categoria_id

        # Atualiza Tags
        if tags_str is not None:
            noticia_db.tags = self._processar_tags(tags_str)

        # Atualiza Capa (Remove antiga e salva nova)
        if imagem_capa:
            if noticia_db.imagem_capa:
                try:
                    # Remove a barra inicial para achar o arquivo no sistema
                    old_path = noticia_db.imagem_capa.lstrip("/")
                    if os.path.exists(old_path):
                        os.remove(old_path)
                except Exception:
                    pass 
            noticia_db.imagem_capa = salvar_imagem(imagem_capa)

        # Adiciona novas fotos à Galeria (Append)
        if galeria:
            for foto in galeria:
                if foto.filename:
                    caminho_foto = salvar_imagem(foto)
                    nova_imagem = NoticiaImagem(
                        caminho=caminho_foto,
                        noticia_id=noticia_db.id
                    )
                    self.session.add(nova_imagem)

        self.session.add(noticia_db)
        self.session.commit()
        self.session.refresh(noticia_db)
        return noticia_db

    # --- DELETE (SOFT DELETE) ---
    
    def deletar_noticia(self, noticia: Noticia):
        """Marca como deletado sem apagar registros do banco."""
        noticia.deleted_at = datetime.now()
        self.session.add(noticia)
        self.session.commit()
        self.session.refresh(noticia)