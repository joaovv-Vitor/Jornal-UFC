import { api } from './api'
import type { Categoria } from '../types/categoria'

/**
 * Busca todas as categorias cadastradas no sistema.
 * Útil para preencher Selects em formulários de notícias.
 */
export function listarCategorias() {
  return api.get<Categoria[]>('/categorias/')
}

/**
 * Busca uma categoria específica por ID.
 */
export function buscarCategoria(id: number) {
  return api.get<Categoria>(`/categorias/${id}`)
}