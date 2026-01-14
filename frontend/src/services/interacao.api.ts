import api from './api'

export interface Comentario {
    id: number
    conteudo: string
    criado_em: string
    oculto: boolean
    usuario?: {
        id: number
        nome: string
        email: string
    }
}

// Interface alinhada com o retorno do Python (noticia_service.py)
export interface CurtidaResponse {
    curtido_pelo_usuario: boolean
    total_curtidas: number
}

export const curtirNoticia = (id: number) => {
    return api.post<CurtidaResponse>(`/noticias/${id}/curtir`)
}

export const obterStatusCurtida = (id: number) => {
    return api.get<CurtidaResponse>(`/noticias/${id}/curtida`)
}

export const listarComentarios = (id: number) => {
    // ✅ CORRIGIDO: Backend usa /comentarios/noticia/{id}
    return api.get<Comentario[]>(`/comentarios/noticia/${id}`)
}

export const criarComentario = (id: number, conteudo: string) => {
    // ✅ CORRIGIDO: Backend usa /comentarios/noticia/{id}
    // Envia um objeto JSON { "conteudo": "texto" }
    return api.post<Comentario>(`/comentarios/noticia/${id}`, { conteudo })
}

export const ocultarComentario = (comentarioId: number) => {
    // Ocultar comentário (soft delete) - apenas publishers podem fazer
    return api.patch<Comentario>(`/comentarios/${comentarioId}/ocultar`)
}

export const desocultarComentario = (comentarioId: number) => {
    // Desocultar comentário - apenas publishers podem fazer
    return api.patch<Comentario>(`/comentarios/${comentarioId}/desocultar`)
}