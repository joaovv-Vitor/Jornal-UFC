<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted } from 'vue'
import { useRoute} from 'vue-router'
import { buscarNoticia, listarNoticias } from '../../services/noticias.api'
import { useAuthStore } from '../../store/auth.store'
import { curtirNoticia, obterStatusCurtida, listarComentarios, criarComentario, ocultarComentario, desocultarComentario, type Comentario } from '../../services/interacao.api'
import BackButton from '../../components/BackButton.vue'

const route = useRoute()
const authStore = useAuthStore()

const noticia = ref<any>(null)
const loading = ref(true)

// Estados de Interação
const comentarios = ref<Comentario[]>([])
const novoComentario = ref('')
const likesCount = ref(0)
const userLiked = ref(false)
const outrasNoticias = ref<any[]>([])

const getImageUrl = (path: string | undefined | null) => {
  if (!path) return ''
  return path.startsWith('http') ? path : `http://localhost:8000${path}`
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('pt-BR', {
    day: '2-digit', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit'
  })
}

async function carregarInteracoes(id: number) {
  try {
    // 1. O Total de likes inicial vem da própria notícia, não da requisição de status
    // Garante que mostre 0 se vier nulo
likesCount.value = noticia.value?.curtidas_count ?? 0

    const comentariosPromise = listarComentarios(id)
    
    // Só busca status se estiver logado
    const likesPromise = authStore.isAuthenticated
      ? obterStatusCurtida(id)
      : null

    const results = await Promise.allSettled([
      comentariosPromise,
      likesPromise
    ])

    /* ------------------ Comentários ------------------ */
    const comentariosResult = results[0]
    if (comentariosResult.status === 'fulfilled') {
      comentarios.value = comentariosResult.value.data
    } else {
      console.error('Erro nos comentários:', comentariosResult.reason)
      comentarios.value = []
    }

    /* ------------------ Likes (Status do Usuário) ------------------ */
    const likesResult = results[1]

    // Se estiver logado E a promessa tiver dado certo
    if (authStore.isAuthenticated && likesResult && likesResult.status === 'fulfilled') {
      // CORREÇÃO AQUI: Verifique qual chave seu backend manda no GET. 
      // Se for o endpoint que criamos antes, a chave é 'curtido'.
      const dados = likesResult.value.data
      userLiked.value = dados.curtido !== undefined ? dados.curtido : dados.curtido_pelo_usuario
    } else {
      userLiked.value = false
    }

  } catch (error) {
    console.error('Erro geral:', error)
  }
}

async function carregarOutras(id: number) {
  try {
    // Busca notícias recentes (assumindo que o padrão traz as últimas)
    const response = await listarNoticias()
    outrasNoticias.value = response.data
      .filter((n: any) => n.id !== id) // Remove a notícia atual da lista
      .slice(0, 3) // Pega apenas 3 para exibir
  } catch (error) {
    console.error('Erro ao carregar outras notícias:', error)
  }
}

onMounted(async () => {
  try {
    const slug = route.params.slug as string
    const response = await buscarNoticia(slug)
    noticia.value = response.data
    
    // Define o título da página (opcional, mas bom pra UX)
    document.title = noticia.value.titulo

    if (noticia.value?.id) {
       await carregarInteracoes(noticia.value.id)
       await carregarOutras(noticia.value.id)
    }
  } catch (e) {
    console.error("Erro ao carregar notícia:", e)
    // DICA: Não dê router.push('/') aqui enquanto estiver debugando.
    // Isso esconde o erro real. Deixe o console.error mostrar o que houve.
    // router.push('/') 
    alert("Erro ao carregar notícia. Verifique o console.")
  } finally {
    loading.value = false
  }
})

onUnmounted(() => {
  // Restaura o título da página ao sair
  document.title = 'Jornal UFC'
})


async function handleCurtir() {
  if (!authStore.isAuthenticated) return alert("Faça login para curtir!")
  try {
    const res = await curtirNoticia(noticia.value.id)
    
    // O POST retorna 'total_curtidas' (diferente do GET da notícia que é 'curtidas_count')
    // Isso é normal em APIs, apenas certifique-se que o backend manda assim no POST.
    likesCount.value = res.data.total_curtidas 
    userLiked.value = res.data.curtido_pelo_usuario
  } catch (error) {
    console.error(error)
  }
}

async function handleComentar() {
  if (!novoComentario.value.trim()) return
  try {
    const res = await criarComentario(noticia.value.id, novoComentario.value)
    comentarios.value.unshift(res.data)
    novoComentario.value = ''
  } catch (error: any) {
    console.error("Erro ao comentar:", error)
    alert(error.response?.data?.detail || "Erro ao publicar comentário.")
  }
}

async function handleOcultarComentario(comentarioId: number) {
  if (!confirm('Tem certeza que deseja ocultar este comentário?')) {
    return
  }
  
  try {
    const res = await ocultarComentario(comentarioId)
    // Atualiza o comentário na lista (marca como oculto, mas mantém visível para publishers)
    const index = comentarios.value.findIndex(c => c.id === comentarioId)
    if (index !== -1) {
      comentarios.value[index] = res.data
    }
    alert('Comentário ocultado com sucesso!')
  } catch (error: any) {
    console.error("Erro ao ocultar comentário:", error)
    alert(error.response?.data?.detail || "Erro ao ocultar comentário.")
  }
}

async function handleDesocultarComentario(comentarioId: number) {
  if (!confirm('Tem certeza que deseja tornar este comentário visível novamente?')) {
    return
  }
  
  try {
    const res = await desocultarComentario(comentarioId)
    // Atualiza o comentário na lista (marca como não oculto)
    const index = comentarios.value.findIndex(c => c.id === comentarioId)
    if (index !== -1) {
      comentarios.value[index] = res.data
    }
    alert('Comentário desocultado com sucesso!')
  } catch (error: any) {
    console.error("Erro ao desocultar comentário:", error)
    alert(error.response?.data?.detail || "Erro ao desocultar comentário.")
  }
}

// ✅ NOVO: Recarrega comentários quando o usuário trocar de conta
watch(
  () => [authStore.user?.id, authStore.isAuthenticated], // Observa mudanças no usuário e autenticação
  async ([newUserId, newIsAuth], [oldUserId, oldIsAuth]) => {
    // Se o usuário mudou (login/logout) e já temos a notícia carregada
    if ((newUserId !== oldUserId || newIsAuth !== oldIsAuth) && noticia.value?.id) {
      // Recarrega os comentários e likes para refletir o novo estado do usuário
      await carregarInteracoes(noticia.value.id)
    }
  }
)

// Recarrega a notícia se o slug mudar (navegação pelo "Veja Mais")
watch(
  () => route.params.slug,
  async (newSlug) => {
    if (!newSlug) return
    loading.value = true
    try {
      const response = await buscarNoticia(newSlug as string)
      noticia.value = response.data
      if (noticia.value?.id) {
        await carregarInteracoes(noticia.value.id)
        await carregarOutras(noticia.value.id)
      }
    } catch (e) { console.error(e) } finally { loading.value = false }
  }
)
</script>

<template>
  <div class="detalhe-wrapper">
    <div v-if="loading" class="msg">Carregando...</div>
    <article v-else-if="noticia" class="noticia-body">
      <BackButton/>
      
      <img v-if="noticia.imagem_capa" :src="getImageUrl(noticia.imagem_capa)" class="capa">
      
      <h1>{{ noticia.titulo }}</h1>
      <p class="sub">{{ noticia.subtitulo }}</p>
      
      <div class="content" v-html="noticia.conteudo"></div>

      <div v-if="noticia.imagens_galeria?.length" class="galeria">
        <img v-for="img in noticia.imagens_galeria" :key="img.id" :src="getImageUrl(img.caminho)">
      </div>

      <!-- Área de Interação -->
      <div class="interaction-bar">
        <button class="btn-like" :class="{ liked: userLiked }" @click="handleCurtir">
          ♥ {{ userLiked ? 'Curtiu' : 'Curtir' }} ({{ likesCount }})
        </button>
      </div>

      <!-- Comentários -->
      <section class="comments-section">
        <h3>Comentários ({{ comentarios.length }})</h3>

        <div v-if="authStore.isAuthenticated" class="comment-form">
          <textarea v-model="novoComentario" placeholder="Escreva seu comentário..." rows="3"></textarea>
          <button @click="handleComentar" :disabled="!novoComentario.trim()">Publicar</button>
        </div>
        <div v-else class="login-prompt">
          <router-link to="/login">Faça login para comentar</router-link>
        </div>

        <div class="comments-list">
          <div 
            v-for="c in comentarios" 
            :key="c.id" 
            class="comment-item"
            :class="{ 'comment-oculto': c.oculto }"
          >
            <div class="comment-header">
              <div>
                <strong>{{ c.usuario?.nome || 'Usuário' }}</strong>
                <small>{{ formatDate(c.criado_em) }}</small>
                <span v-if="c.oculto" class="badge-oculto">👁️ Oculto</span>
              </div>
              <!-- Botões de moderação - apenas para publishers -->
              <div v-if="authStore.isPublisher" class="comment-actions">
                <button 
                  v-if="!c.oculto"
                  @click="handleOcultarComentario(c.id)"
                  class="btn-ocultar"
                  title="Ocultar comentário"
                >
                  🗑️ Ocultar
                </button>
                <button 
                  v-else
                  @click="handleDesocultarComentario(c.id)"
                  class="btn-desocultar"
                  title="Tornar comentário visível"
                >
                  👁️ Desocultar
                </button>
              </div>
            </div>
            <p>{{ c.conteudo }}</p>
          </div>
          <p v-if="comentarios.length === 0" class="no-comments">Seja o primeiro a comentar!</p>
        </div>
      </section>

      <!-- Veja Mais -->
      <section v-if="outrasNoticias.length" class="veja-mais-section">
        <h3>Veja também</h3>
        <div class="veja-mais-grid">
          <router-link 
            v-for="item in outrasNoticias" 
            :key="item.id" 
            :to="`/noticias/${item.slug}`" 
            class="card-pequeno"
          >
            <div class="card-pequeno-img" v-if="item.imagem_capa">
              <img :src="getImageUrl(item.imagem_capa)" :alt="item.titulo">
            </div>
            <div class="card-pequeno-content">
              <h4>{{ item.titulo }}</h4>
              <span class="card-date">{{ formatDate(item.criado_em) }}</span>
            </div>
          </router-link>
        </div>
      </section>

    </article>
  </div>
</template>

<style scoped>
/* Garante que o fundo aqui seja claro para você ler o texto */
.detalhe-wrapper { 
  background: #f4f4f4; min-height: 100vh; padding: 20px; color: #333; 
}
.noticia-body { 
  max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.capa { 
  width: 100%; border-radius: 8px; margin: 20px 0; 
}
.content { 
  line-height: 1.6; white-space: pre-wrap; overflow-wrap: break-word; word-wrap: break-word;
}
.galeria { 
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 20px; 
}
.galeria img { 
  width: 100%; height: 150px; object-fit: cover; 
  }

/* Estilos de Interação */
.interaction-bar { border-top: 1px solid #eee; border-bottom: 1px solid #eee; padding: 20px 0; margin: 30px 0; }
.btn-like { background: none; border: 2px solid #ddd; border-radius: 50px; padding: 8px 20px; cursor: pointer; font-size: 1rem; color: #555; transition: all 0.2s; }
.btn-like:hover { border-color: #d32f2f; color: #d32f2f; }
.btn-like.liked { background-color: #d32f2f; border-color: #d32f2f; color: white; }

.comments-section { margin-top: 30px; }
.comment-form textarea { width: 100%; padding: 15px; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 10px; font-family: inherit; }
.comment-form button { background-color: #333; color: white; border: none; padding: 10px 25px; border-radius: 5px; cursor: pointer; }
.comment-form button:disabled { opacity: 0.6; }

.login-prompt { background: #f9f9f9; padding: 20px; text-align: center; border-radius: 8px; margin-bottom: 20px; }
.login-prompt a { color: #d32f2f; font-weight: bold; text-decoration: none; }

.comment-item { border-bottom: 1px solid #eee; padding: 20px 0; }
.comment-item.comment-oculto {
  opacity: 0.6;
  background-color: #f9f9f9;
  border-left: 3px solid #ffc107;
  padding-left: 15px;
}
.comment-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }
.comment-header strong { color: #333; display: block; }
.comment-header small { color: #999; display: block; margin-top: 4px; }
.badge-oculto {
  display: inline-block;
  background-color: #ffc107;
  color: #856404;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: bold;
  margin-left: 8px;
}
.comment-actions {
  display: flex;
  gap: 8px;
}
.btn-ocultar {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: background-color 0.2s;
}
.btn-ocultar:hover {
  background-color: #c82333;
}
.btn-desocultar {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: background-color 0.2s;
}
.btn-desocultar:hover {
  background-color: #218838;
}
.no-comments { text-align: center; color: #999; padding: 20px; }

/* Veja Mais */
.veja-mais-section { margin-top: 40px; border-top: 1px solid #eee; padding-top: 20px; }
.veja-mais-section h3 { margin-bottom: 15px; font-size: 1.2rem; color: #333; }
.veja-mais-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; }
.card-pequeno { 
  display: flex; flex-direction: column; text-decoration: none; color: inherit; 
  background: #f9f9f9; border-radius: 8px; overflow: hidden; transition: transform 0.2s;
}
.card-pequeno:hover { transform: translateY(-3px); box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
.card-pequeno-img img { width: 100%; height: 120px; object-fit: cover; }
.card-pequeno-content { padding: 10px; }
.card-pequeno-content h4 { margin: 0 0 5px 0; font-size: 0.95rem; line-height: 1.3; }
.card-date { font-size: 0.75rem; color: #888; }

.sub {
  font-size: 1.1rem;
  color: #555;
  margin-bottom: 20px;
  font-style: italic;
}
</style>