# jornal UFC


classDiagram
    class USUARIOS {
        int id
        string nome
        string email
        string senha_hash
        string role
        datetime criado_em
    }

    class NOTICIAS {
        int id
        string titulo
        string subtitulo
        text conteudo
        string slug
        string imagem_capa
        boolean publicado
        datetime publicado_em
        datetime criado_em
        datetime atualizado_em
        int autor_id
        int categoria_id
    }

    class CATEGORIAS {
        int id
        string nome
        string slug
    }

    class TAGS {
        int id
        string nome
        string slug
    }

    class NOTICIAS_TAGS {
        int noticia_id
        int tag_id
    }

    class COMENTARIOS {
        int id
        text conteudo
        datetime criado_em
        boolean aprovado
        int usuario_id
        int noticia_id
    }

    class EVENTOS {
        int id
        string titulo
        text descricao
        datetime data_inicio
        datetime data_fim
        string local
        string imagem_url
        boolean destaque
        datetime criado_em
        int usuario_id
    }

    %% ------- RELACIONAMENTOS -------
    USUARIOS "1" --> "0..*" NOTICIAS : escreve
    USUARIOS "1" --> "0..*" COMENTARIOS : faz
    USUARIOS "1" --> "0..*" EVENTOS : cadastra

    CATEGORIAS "1" --> "0..*" NOTICIAS : contem

    NOTICIAS "1" --> "0..*" COMENTARIOS : recebe

    NOTICIAS "0..*" --> "0..*" TAGS : possui
    NOTICIAS -- NOTICIAS_TAGS
    TAGS -- NOTICIAS_TAGS
