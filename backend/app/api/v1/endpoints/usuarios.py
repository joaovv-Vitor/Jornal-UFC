# app/api/endpoints/usuarios.py
from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from sqlmodel import select
from app.core.database import SessionDep
from app.core.security import get_password_hash
from app.core.email import enviar_email_simples
# Ajustei os imports para ficarem conforme sua estrutura de pastas (app.db...)
from app.models.usuario import Usuario, RoleEnum
from app.schemas.usuario import UsuarioCreate, UsuarioRead, SolicitacaoBolsa

router = APIRouter()

@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def create_usuario(
    usuario_in: UsuarioCreate, 
    session: SessionDep,
    background_tasks: BackgroundTasks # <--- Injeção para enviar e-mail em 2º plano
):
    """
    Cria um novo usuário no sistema.
    - **Leitor**: Criação direta (Ativo).
    - **Professor**: Requer email @ufc.br (Nasce Inativo, aguardando validação de email).
    - **Bolsista**: Requer email do orientador (Nasce Inativo, aguardando aprovação do professor).
    """

    # 1. Verificar se o email já existe
    usuario_existente = session.exec(
        select(Usuario).where(Usuario.email == usuario_in.email)
    ).first()
    
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está cadastrado."
        )

    # 2. Preparar objeto para o Banco
    novo_usuario = Usuario.model_validate(
        usuario_in, update={"senha_hash": get_password_hash(usuario_in.senha)}
    )

    # 3. Lógica específica por PERFIL (Role)
    
    # --- REGRA DO PROFESSOR ---
    if usuario_in.role == RoleEnum.PROFESSOR:
        novo_usuario.is_active = False 
        
        # Envio de Email de Confirmação
        link_ativacao = f"http://localhost:8000/api/v1/auth/verificar?email={novo_usuario.email}"
        html_content = f"""
        <h1>Bem-vindo ao Jornal UFC!</h1>
        <p>Olá professor(a) <b>{novo_usuario.nome}</b>,</p>
        <p>Para ativar sua conta e gerenciar bolsistas, clique no link abaixo:</p>
        <a href="{link_ativacao}" style="padding: 10px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">ATIVAR MINHA CONTA</a>
        """
        
        background_tasks.add_task(
            enviar_email_simples,
            "Ativação de Conta - Jornal UFC",
            [novo_usuario.email],
            html_content
        )

    # --- REGRA DO BOLSISTA ---
    elif usuario_in.role == RoleEnum.BOLSISTA:
        # Busca o ID do professor baseado no email fornecido
        orientador = session.exec(
            select(Usuario).where(Usuario.email == usuario_in.email_orientador)
        ).first()

        if not orientador or orientador.role != RoleEnum.PROFESSOR:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O e-mail do orientador informado não pertence a um Professor cadastrado."
            )
        
        novo_usuario.orientador_id = orientador.id
        novo_usuario.is_active = False 
        
        # Avisar o Professor Orientador
        html_content = f"""
        <h1>Nova Solicitação de Bolsista</h1>
        <p>O aluno <b>{novo_usuario.nome}</b> ({novo_usuario.email}) cadastrou-se indicando você como orientador.</p>
        <p>Acesse o painel do sistema para aprovar ou rejeitar esta solicitação.</p>
        """
        
        background_tasks.add_task(
            enviar_email_simples,
            "Aprovação Pendente - Jornal UFC",
            [orientador.email],
            html_content
        )

    # --- REGRA DO LEITOR ---
    else:
        novo_usuario.is_active = True

    # 4. Salvar no Banco
    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)

    return novo_usuario


@router.patch("/{user_id}/virar-bolsista", response_model=UsuarioRead)
def tornar_se_bolsista(
    user_id: int, 
    solicitacao: SolicitacaoBolsa, 
    session: SessionDep,
    background_tasks: BackgroundTasks # <--- Injeção aqui também
):
    # Busca o usuário
    usuario = session.get(Usuario, user_id)
    if not usuario:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    if usuario.role == RoleEnum.BOLSISTA:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Usuário já é bolsista")

    # Busca o Professor Orientador
    orientador = session.exec(
        select(Usuario).where(Usuario.email == solicitacao.email_orientador)
    ).first()

    if not orientador or orientador.role != RoleEnum.PROFESSOR:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, 
            detail="O e-mail informado não pertence a um Professor válido."
        )

    # APLICA A MUDANÇA
    usuario.role = RoleEnum.BOLSISTA
    usuario.orientador_id = orientador.id
    usuario.is_active = False  # Bloqueia até aprovação
    
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    
    # Envia email para o professor
    html_content = f"""
    <h1>Solicitação de Vínculo de Bolsa</h1>
    <p>O usuário leitor <b>{usuario.nome}</b> solicitou alteração para Bolsista sob sua orientação.</p>
    <p>Acesse o sistema para aprovar.</p>
    """
    
    background_tasks.add_task(
        enviar_email_simples,
        "Solicitação de Novo Bolsista",
        [orientador.email],
        html_content
    )
    
    return usuario


@router.patch("/{user_id}/virar-leitor", response_model=UsuarioRead)
def tornar_se_leitor(user_id: int, session: SessionDep):
    # Busca o usuário
    usuario = session.get(Usuario, user_id)
    if not usuario:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        
    if usuario.role != RoleEnum.BOLSISTA:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Apenas bolsistas podem reverter para leitor")

    # APLICA A MUDANÇA
    usuario.role = RoleEnum.LEITOR
    usuario.orientador_id = None
    usuario.is_active = True
    
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    
    return usuario