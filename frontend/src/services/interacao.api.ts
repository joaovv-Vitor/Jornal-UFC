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

// --- CORREÇÃO AQUI ---

// 1. Interface para a AÇÃO (POST)
// O Python retorna: { "curtido_pelo_usuario": bool, "total_curtidas": int }
export interface CurtidaActionResponse {
    curtido_pelo_usuario: boolean
    total_curtidas: number
}

// 2. Interface para a VERIFICAÇÃO (GET)
// O Python retorna: { "curtido": bool }
// Se você tentar ler "curtido_pelo_usuario" aqui, vai dar erro, pois o backend manda "curtido"
export interface CurtidaStatusResponse {
    curtido: boolean
}

// --- FIM DA CORREÇÃO ---

export const curtirNoticia = (id: number) => {
    // Retorna ActionResponse (com total atualizado)
    return api.post<CurtidaActionResponse>(`/noticias/${id}/curtir`)
}

export const obterStatusCurtida = (id: number) => {
    // Retorna StatusResponse (apenas o booleano)
    return api.get<CurtidaStatusResponse>(`/noticias/${id}/curtida`)
}

export const listarComentarios = (id: number) => {
    return api.get<Comentario[]>(`/comentarios/noticia/${id}`)
}

export const criarComentario = (id: number, conteudo: string) => {
    return api.post<Comentario>(`/comentarios/noticia/${id}`, { conteudo })
}

export const ocultarComentario = (comentarioId: number) => {
    return api.patch<Comentario>(`/comentarios/${comentarioId}/ocultar`)
}

export const desocultarComentario = (comentarioId: number) => {
    return api.patch<Comentario>(`/comentarios/${comentarioId}/desocultar`)
}