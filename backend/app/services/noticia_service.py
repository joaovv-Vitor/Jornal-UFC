import os
import re
import unicodedata
from datetime import datetime
from typing import List, Optional

from fastapi import UploadFile
from sqlmodel import Session, select, func, col, or_
from sqlalchemy import extract # Para extrair ano/mês


# --- IMPORTAÇÕES CORRETAS (MODELOS SEPARADOS) ---
# Importamos cada entidade do seu respectivo arquivo para evitar erros de ciclo/duplicação
from app.models.noticia import Noticia
from app.models.tag import Tag
from app.models.imagem import NoticiaImagem
from app.models.usuario import Usuario
from app.models.curtida import CurtidaNoticia
from app.models.categoria import Categoria

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

    def listar_noticias(
        self, 
        skip: int = 0, 
        limit: int = 4,
        termo_busca: Optional[str] = None,    
        categoria_slug: Optional[str] = None, 
        tag_slug: Optional[str] = None,       
        ano: Optional[int] = None,            
        mes: Optional[int] = None             
    ) -> List[Noticia]:
        """
        Busca poderosa combinando Texto, Categoria, Tag e Data.
        """
        # Começa com a query base (apenas não deletados)
        query = select(Noticia).where(Noticia.deleted_at == None)

        # [US 04] - BUSCA TEXTUAL
        # Procura no Título OU Subtítulo OU Nome do Autor
        if termo_busca:
            # Precisamos fazer Join com Usuario para buscar pelo nome dele
            query = query.join(Usuario, isouter=True)
            
            query = query.where(
                or_(
                    col(Noticia.titulo).icontains(termo_busca),
                    col(Noticia.subtitulo).icontains(termo_busca),
                    col(Usuario.nome).icontains(termo_busca)
                )
            )

        # [US 12] - FILTRO POR CATEGORIA
        if categoria_slug:
            # Join com Categoria para filtrar pelo slug (ex: 'esporte')
            query = query.join(Categoria).where(Categoria.slug == categoria_slug)

        # [US 12] - FILTRO POR TAG
        if tag_slug:
            # Join Mágico do SQLModel: Entra na lista de tags da notícia e filtra
            query = query.join(Noticia.tags).where(Tag.slug == tag_slug)

        # [US 12] - FILTRO POR DATA (ANO)
        if ano:
            query = query.where(extract('year', Noticia.criado_em) == ano)

        # [US 12] - FILTRO POR DATA (MÊS)
        if mes:
            query = query.where(extract('month', Noticia.criado_em) == mes)

        # Ordenação e Paginação
        query = query.order_by(Noticia.criado_em.desc())
        query = query.offset(skip).limit(limit)

        return self.session.exec(query).unique().all()

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

    def alternar_curtida(self, noticia_id: int, usuario_id: int) -> dict:
        try:
            # 1. Busca se já existe
            statement = select(CurtidaNoticia).where(
                CurtidaNoticia.usuario_id == usuario_id,
                CurtidaNoticia.noticia_id == noticia_id
            )
            curtida_existente = self.session.exec(statement).first()

            estado_final = False

            if curtida_existente:
                # REMOVER (Descurtir)
                self.session.delete(curtida_existente)
                self.session.commit()
                estado_final = False
            else:
                # ADICIONAR (Curtir)
                nova_curtida = CurtidaNoticia(usuario_id=usuario_id, noticia_id=noticia_id)
                self.session.add(nova_curtida)
                self.session.commit()
                estado_final = True

            # 2. Conta o total (Correção aqui para garantir que seja um int)
            # Usamos .first() em vez de .one() para evitar exceção se algo bizarro acontecer
            total_query = self.session.exec(
                select(func.count())
                .select_from(CurtidaNoticia)
                .where(CurtidaNoticia.noticia_id == noticia_id)
            ).first()

            # Garante que 'total' seja um número, mesmo que venha None ou Tupla
            if total_query is None:
                total_int = 0
            else:
                # Se vier (5,), pega o 5. Se vier 5, usa o 5.
                total_int = total_query if isinstance(total_query, int) else total_query[0]

            return {
                "curtido_pelo_usuario": estado_final,
                "total_curtidas": total_int
            }

        except Exception as e:
            # Se der erro (ex: chave estrangeira inválida), faz rollback e avisa
            self.session.rollback()
            print(f"ERRO CRÍTICO NO CURTIR: {e}")
            raise e

# ... outros métodos ...

    def verificar_status_curtida(self, noticia_id: int, usuario_id: int) -> dict:
        """
        Verifica se um usuário específico curtiu a notícia e conta o total.
        Usado para carregar o estado inicial do botão no frontend.
        """
        # 1. Verifica se o usuário logado curtiu
        # Usamos .first() pois se retornar algo, é True, se None, é False
        curtida = self.session.exec(
            select(CurtidaNoticia)
            .where(CurtidaNoticia.usuario_id == usuario_id)
            .where(CurtidaNoticia.noticia_id == noticia_id)
        ).first()

        curtido_pelo_usuario = bool(curtida)

        # 2. Conta o total atualizado
        total = self.session.exec(
            select(func.count())
            .select_from(CurtidaNoticia)
            .where(CurtidaNoticia.noticia_id == noticia_id)
        ).one()

        return {
            "curtido_pelo_usuario": curtido_pelo_usuario,
            "total_curtidas": total
        }