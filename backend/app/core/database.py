from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings

# Ajuste necessário para o driver psycopg (versão 3)
# O SQLModel/SQLAlchemy precisa do prefixo 'postgresql+psycopg://'
database_url = settings.SQLALCHEMY_DATABASE_URI.replace(
    "postgresql://", "postgresql+psycopg://"
)

# Cria a engine com a URL corrigida
engine = create_engine(database_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)