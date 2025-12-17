// Define as estruturas aninhadas para garantir a tipagem correta

interface Autor {
    id: number;
    nome: string;
    email: string; // Adicionado do AutorRead
}

interface Categoria {
    id: number;
    nome: string;
}

interface Tag {
    id: number;
    nome: string;
    slug: string;
}

interface NoticiaImagem {
    id: number;
    caminho: string;
}

// Interface principal Noticia (Espelha o NoticiaRead do Backend)
export interface Noticia {
    id: number;
    titulo: string;
    subtitulo: string | undefined;
    conteudo: string;
    slug: string;
    
    imagem_capa: string | undefined; // Caminho no servidor
    
    publicado: boolean;
    publicado_em: string | undefined; 
    criado_em: string;
    atualizado_em: string;
    
    // ID do autor (sempre presente no read)
    autor_id: number;
    
    // --- RELACIONAMENTOS (Objetos) ---
    
    // Autor (Objeto completo, pode ser undefined se for um campo opcional em outra view)
    autor: Autor | undefined;
    
    // Categoria
    categoria: Categoria | undefined;
    
    // Tags (LISTA DE OBJETOS)
    tags: Tag[]; 
    
    // Galeria (ADICIONADO)
    imagens_galeria: NoticiaImagem[];
}