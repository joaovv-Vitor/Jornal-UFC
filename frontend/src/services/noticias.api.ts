import { api } from './api'
import type { Noticia } from '../types/noticias'

export function listarNoticias() {
  return api.get<Noticia[]>('/noticias')
}

export function buscarNoticia(slug: string) {
  return api.get<Noticia>(`/noticias/${slug}`)
}

// 💡 CORRIGIDO: Esperar e enviar FormData (para upload de arquivos)
export function criarNoticia(formData: FormData) { 
  return api.post('/noticias', formData, {
    headers: {
      // OBRIGATÓRIO: Garante que o Axios envie o Content-Type correto para o FastAPI
      'Content-Type': 'multipart/form-data', 
    },
  })
}

// 💡 CORRIGIDO: O endpoint de edição também precisa aceitar FormData para uploads opcionais
export function atualizarNoticia(id: number, formData: FormData) { 
  return api.patch(`/noticias/${id}`, formData, { // O método é PATCH no seu backend
    headers: {
      'Content-Type': 'multipart/form-data', 
    },
  })
}

export function deletarNoticia(id: number) {
  return api.delete(`/noticias/${id}`)
}