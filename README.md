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

Abaixo está a estrutura do banco de dados relacional desenhada com Mermaid.

```mermaid
erDiagram
    USUARIOS {
        int id PK
        string nome
        string email UK "Unique"
        string senha_hash
        string role "default: leitor"
        datetime criado_em
    }

    NOTICIAS {
        int id PK
        string titulo
        string subtitulo
        text conteudo
        string slug UK "Unique"
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
        string slug UK
    }

    TAGS {
        int id PK
        string nome
        string slug UK
    }

    NOTICIAS_TAGS {
        int noticia_id PK,FK
        int tag_id PK,FK
    }

    COMENTARIOS {
        int id PK
        text conteudo
        datetime criado_em
        boolean aprovado
        int usuario_id FK
        int noticia_id FK
    }

    EVENTOS {
        int id PK
        string titulo
        text
    }
