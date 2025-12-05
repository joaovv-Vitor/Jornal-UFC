# 📰 Jornal UFC - Lide API

API de backend para um sistema de jornal digital, desenvolvida com **FastAPI** e **PostgreSQL**. O sistema gerencia notícias, usuários, categorias, tags, comentários e uma agenda de eventos.

## 🚀 Tecnologias Utilizadas

* **Linguagem:** Python 3.12
* **Framework:** FastAPI
* **ORM:** SQLModel (SQLAlchemy + Pydantic)
* **Banco de Dados:** PostgreSQL
* **Gerenciamento de Dependências:** Docker & Docker Compose
* **Migrações/Validação:** Pydantic Settings & Email Validator

## 🗂️ Modelo de Dados (Diagrama ER)


```mermaid
erDiagram
    USUARIOS {
        int id PK
        string nome
        string email
        string senha_hash
        string role
        datetime criado_em
    }

    NOTICIAS {
        int id PK
        string titulo
        string subtitulo
        string conteudo
        string slug
        string imagem_capa
        boolean publicado
        datetime publicado_em
        datetime criado_em
        datetime atualizado_em
        int autor_id FK
        int categoria_id FK
    }

    CATEGORIAS {
        int id PK
        string nome
        string slug
    }

    TAGS {
        int id PK
        string nome
        string slug
    }

    NOTICIAS_TAGS {
        int noticia_id PK,FK
        int tag_id PK,FK
    }

    COMENTARIOS {
        int id PK
        string conteudo
        datetime criado_em
        boolean aprovado
        int usuario_id FK
        int noticia_id FK
    }

    EVENTOS {
        int id PK
        string titulo
        string descricao
        datetime data_inicio
        datetime data_fim
        string local
        string imagem_url
        boolean destaque
        datetime criado_em
        int usuario_id FK
    }

    %% Relacionamentos
    USUARIOS ||--o{ NOTICIAS : escreve
    USUARIOS ||--o{ COMENTARIOS : faz
    USUARIOS ||--o{ EVENTOS : cadastra
    
    CATEGORIAS ||--o{ NOTICIAS : classifica
    
    NOTICIAS ||--o{ COMENTARIOS : recebe
    NOTICIAS ||--o{ NOTICIAS_TAGS : possui
    TAGS ||--o{ NOTICIAS_TAGS : etiqueta