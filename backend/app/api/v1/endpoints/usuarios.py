from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from app.core.database import SessionDep
from app.core.security import get_password_hash
from app.models.usuario import Usuario, RoleEnum
from app.schemas.usuario import UsuarioCreate, UsuarioRead, SolicitacaoBolsa

router = APIRouter()

@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def create_usuario(usuario_in: UsuarioCreate, session: SessionDep):
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

    # 2. Preparar objeto para o Banco (convertendo Schema -> Model)
    # exclude={"email_orientador"} remove o campo que não existe na tabela do banco
    novo_usuario = Usuario.model_validate(
        usuario_in, update={"senha_hash": get_password_hash(usuario_in.senha)}
    )

    # 3. Lógica específica por PERFIL (Role)
    
    # --- REGRA DO PROFESSOR ---
    if usuario_in.role == RoleEnum.PROFESSOR:
        # Nasce bloqueado aguardando clicar no email
        novo_usuario.is_active = False 
        # TODO: Aqui chamaremos a função de enviar email de verificação
        print(f"DEBUG: Enviar email de verificação para {novo_usuario.email}")

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
        novo_usuario.is_active = False # Nasce bloqueado aguardando o Professor aprovar
        
        # TODO: Aqui chamaremos a função de avisar o professor
        print(f"DEBUG: Enviar email para o professor {orientador.email} aprovar o aluno")

    # --- REGRA DO LEITOR ---
    else:
        # Leitor comum nasce ativo (ou inativo se quiser confirmar email também)
        novo_usuario.is_active = True

    # 4. Salvar no Banco
    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)

    return novo_usuario


# 1. Rota: Leitor vira Bolsista (Requer aprovação do Professor)
@router.patch("/{user_id}/virar-bolsista", response_model=UsuarioRead)
def tornar_se_bolsista(
    user_id: int, 
    solicitacao: SolicitacaoBolsa, 
    session: SessionDep
):
    # Busca o usuário
    usuario = session.get(Usuario, user_id)
    if not usuario:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    # Verifica se já é bolsista
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
    usuario.is_active = False  # <--- BLOQUEIA A CONTA ATÉ O PROFESSOR APROVAR!
    
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    
    # TODO: Disparar e-mail para o professor aqui
    print(f"DEBUG: Email enviado para {orientador.email} aprovar o novo bolsista.")
    
    return usuario


# 2. Rota: Bolsista vira Leitor (Perde vínculo)
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
    usuario.orientador_id = None # Remove o vínculo
    usuario.is_active = True     # Garante que ele possa logar
    
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    
    return usuario