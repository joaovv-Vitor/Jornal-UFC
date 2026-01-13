import api from './api'

export interface Comentario {
    id: number
    conteudo: string
    criado_em: string
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
    return api.get<Comentario[]>(`/noticias/${id}/comentarios`)
}

export const criarComentario = (id: number, conteudo: string) => {
    // Envia um objeto JSON { "conteudo": "texto" }
    return api.post<Comentario>(`/noticias/${id}/comentarios`, { conteudo })
}