import { api } from './api'
import type { Noticia } from '../types/noticias'

export function listarNoticias() {
  return api.get<Noticia[]>('/noticias')
}

export function buscarNoticia(slug: string) {
  return api.get<Noticia>(`/noticias/${slug}`)
}


export function criarNoticia(formData: FormData) { 
  return api.post('/noticias/', formData)
}


export function atualizarNoticia(id: number, formData: FormData) { 
  return api.patch(`/noticias/${id}`, formData, { // O método é PATCH
    headers: {
      'Content-Type': 'multipart/form-data', 
    },
  })
}

export function deletarNoticia(id: number) {
  return api.delete(`/noticias/${id}`)
}