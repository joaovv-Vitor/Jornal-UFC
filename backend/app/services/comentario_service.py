from sqlmodel import Session, select
from typing import List, Optional
from app.models.comentario import Comentario
from app.models.noticia import Noticia

class ComentarioService:
    def __init__(self, session: Session):
        self.session = session

    # [US 08] - CRIAR
    def criar_comentario(self, conteudo: str, usuario_id: int, noticia_id: int) -> Comentario:
        novo_comentario = Comentario(
            conteudo=conteudo,
            usuario_id=usuario_id,
            noticia_id=noticia_id
        )
        self.session.add(novo_comentario)
        self.session.commit()
        self.session.refresh(novo_comentario)
        return novo_comentario

    # [US 08] - LISTAR (Com filtro de Ocultos)
    def listar_por_noticia(self, noticia_id: int, incluir_ocultos: bool = False) -> List[Comentario]:
        """
        Lista comentários. 
        Por padrão (visitantes), NÃO mostra ocultos.
        O autor da notícia pode querer ver os ocultos (parametro opcional).
        """
        query = select(Comentario).where(Comentario.noticia_id == noticia_id)
        
        if not incluir_ocultos:
            query = query.where(Comentario.oculto == False)
            
        # Ordenados por data (mais recentes primeiro)
        return self.session.exec(query.order_by(Comentario.criado_em.desc())).all()

    def buscar_por_id(self, id: int) -> Optional[Comentario]:
        return self.session.get(Comentario, id)

    # [US 08] - EXCLUIR (Próprio Autor)
    def deletar_comentario(self, comentario: Comentario):
        self.session.delete(comentario)
        self.session.commit()

    # [US 11] - OCULTAR (Autor da Notícia)
    def ocultar_comentario(self, comentario: Comentario):
        comentario.oculto = True
        self.session.add(comentario)
        self.session.commit()
        self.session.refresh(comentario)
        return comentario

    # [US 11] - DESOCULTAR (Publishers)
    def desocultar_comentario(self, comentario: Comentario):
        comentario.oculto = False
        self.session.add(comentario)
        self.session.commit()
        self.session.refresh(comentario)
        return comentario