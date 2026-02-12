<template>
  <app-layout>
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 class="text-2xl font-bold text-white">Gestion des Films</h2>
          <p class="text-slate-400 text-sm">Ajouter, modifier ou supprimer des films du catalogue.</p>
        </div>
        <button 
          @click="openAddMovieModal"
          class="bg-cinema-accent hover:bg-cinema-accentHover text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
        >
          <i class="fa-solid fa-plus"></i> Nouveau Film
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="moviesStore.loading && moviesStore.movies.length === 0" class="flex justify-center py-12">
        <div class="text-slate-400">
          <i class="fa-solid fa-spinner animate-spin text-2xl"></i>
          <p class="mt-2">Chargement...</p>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="moviesStore.error" class="bg-red-900/20 border border-red-500/30 rounded-lg p-4 text-center">
        <p class="text-red-400"><i class="fa-solid fa-circle-exclamation mr-2"></i>{{ moviesStore.error }}</p>
      </div>

      <!-- Movies Grid -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div 
          v-for="movie in moviesStore.movies" 
          :key="movie.id"
          class="group bg-cinema-800 rounded-xl overflow-hidden border border-cinema-700 hover:border-cinema-accent/50 transition-all hover:shadow-lg hover:shadow-cinema-accent/10"
        >
          <div class="relative aspect-[2/3] overflow-hidden">
            <img 
              :src="movie.image || 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=800&q=80'" 
              :alt="movie.title" 
              class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
            >
            <div class="absolute inset-0 bg-gradient-to-t from-cinema-900 via-transparent to-transparent opacity-80"></div>
            <div class="absolute bottom-0 left-0 right-0 p-4">
              <span class="text-xs font-bold text-cinema-accent uppercase tracking-wider mb-1 block">{{ movie.genre }}</span>
              <h3 class="text-lg font-bold text-white leading-tight">{{ movie.title }}</h3>
              <p class="text-xs text-slate-300 mt-1 flex items-center gap-2">
                <span v-if="movie.duration"><i class="fa-regular fa-clock"></i> {{ movie.duration }} min</span>
                <span v-if="movie.year">· {{ movie.year }}</span>
                <span v-if="movie.rating" class="text-yellow-400">★ {{ movie.rating }}</span>
              </p>
            </div>
            
            <!-- Actions Overlay -->
            <div class="absolute top-2 right-2 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
              <button 
                @click="editMovie(movie)"
                class="w-8 h-8 rounded-full bg-black/50 backdrop-blur text-white hover:bg-cinema-accent flex items-center justify-center transition-colors"
              >
                <i class="fa-solid fa-pen text-xs"></i>
              </button>
              <button 
                @click="deleteMovie(movie.id)"
                class="w-8 h-8 rounded-full bg-black/50 backdrop-blur text-white hover:bg-red-600 flex items-center justify-center transition-colors"
              >
                <i class="fa-solid fa-trash text-xs"></i>
              </button>
            </div>
          </div>
        </div>

        <!-- Add New Placeholder -->
        <button 
          @click="openAddMovieModal"
          class="bg-cinema-800/50 rounded-xl border-2 border-dashed border-cinema-700 hover:border-cinema-accent hover:bg-cinema-800 transition-all flex flex-col items-center justify-center gap-3 aspect-[2/3] group"
        >
          <div class="w-12 h-12 rounded-full bg-cinema-700 group-hover:bg-cinema-accent flex items-center justify-center transition-colors">
            <i class="fa-solid fa-plus text-white text-xl"></i>
          </div>
          <span class="text-sm font-medium text-slate-400 group-hover:text-white">Ajouter un film</span>
        </button>
      </div>
    </div>

    <!-- Modal Add/Edit Movie -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80" @click.self="closeModal">
      <div class="bg-cinema-800 rounded-xl border border-cinema-700 p-8 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-white">{{ editingMovie ? 'Modifier le film' : 'Ajouter un film' }}</h3>
          <button @click="closeModal" class="text-slate-400 hover:text-white"><i class="fa-solid fa-xmark text-xl"></i></button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-slate-300 mb-1">Titre *</label>
              <input v-model="form.title" type="text" required class="w-full bg-slate-900 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-cinema-accent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-300 mb-1">Genre</label>
              <input v-model="form.genre" type="text" class="w-full bg-slate-900 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-cinema-accent" placeholder="Comédie, Thriller, Drame..." />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-300 mb-1">Durée (min)</label>
              <input v-model.number="form.duration" type="number" class="w-full bg-slate-900 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-cinema-accent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-300 mb-1">Année</label>
              <input v-model.number="form.year" type="number" class="w-full bg-slate-900 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-cinema-accent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-300 mb-1">Note (0-5)</label>
              <input v-model.number="form.rating" type="number" step="0.1" min="0" max="5" class="w-full bg-slate-900 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-cinema-accent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-300 mb-1">Âge requis</label>
              <input v-model="form.ageRating" type="text" class="w-full bg-slate-900 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-cinema-accent" placeholder="TP, 12+, 16+..." />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-300 mb-1">Réalisateur</label>
              <input v-model="form.director" type="text" class="w-full bg-slate-900 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-cinema-accent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-300 mb-1">Scénariste</label>
              <input v-model="form.writer" type="text" class="w-full bg-slate-900 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-cinema-accent" />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-300 mb-1">URL Image</label>
            <input v-model="form.image" type="url" class="w-full bg-slate-900 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-cinema-accent" placeholder="https://..." />
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-300 mb-1">Description courte</label>
            <textarea v-model="form.description" rows="2" class="w-full bg-slate-900 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-cinema-accent resize-none"></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-300 mb-1">Synopsis</label>
            <textarea v-model="form.synopsis" rows="3" class="w-full bg-slate-900 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-cinema-accent resize-none"></textarea>
          </div>

          <div v-if="submitError" class="bg-red-900/20 border border-red-500/30 rounded-lg p-3 text-red-400 text-sm">
            {{ submitError }}
          </div>

          <div class="flex justify-end gap-3 pt-4 border-t border-slate-700">
            <button type="button" @click="closeModal" class="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg text-sm">
              Annuler
            </button>
            <button type="submit" :disabled="submitting" class="px-6 py-2 bg-cinema-accent hover:bg-cinema-accentHover text-white rounded-lg text-sm font-medium disabled:opacity-50 flex items-center gap-2">
              <i v-if="submitting" class="fa-solid fa-spinner animate-spin"></i>
              {{ editingMovie ? 'Modifier' : 'Créer' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </app-layout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import AppLayout from '@/components/layout/AppLayout.vue'
import { useMoviesStore } from '@/stores/movies.store'

const moviesStore = useMoviesStore()
const showModal = ref(false)
const editingMovie = ref(null)
const submitting = ref(false)
const submitError = ref(null)

const defaultForm = () => ({
  title: '',
  genre: '',
  duration: null,
  year: new Date().getFullYear(),
  rating: null,
  ageRating: '',
  image: '',
  description: '',
  synopsis: '',
  director: '',
  writer: '',
})

const form = reactive(defaultForm())

onMounted(async () => {
  await moviesStore.fetchMovies()
})

const resetForm = () => {
  Object.assign(form, defaultForm())
}

const openAddMovieModal = () => {
  editingMovie.value = null
  resetForm()
  submitError.value = null
  showModal.value = true
}

const editMovie = (movie) => {
  editingMovie.value = movie
  Object.assign(form, {
    title: movie.title || '',
    genre: movie.genre || '',
    duration: movie.duration || null,
    year: movie.year || null,
    rating: movie.rating || null,
    ageRating: movie.ageRating || '',
    image: movie.image || '',
    description: movie.description || '',
    synopsis: movie.synopsis || '',
    director: movie.director || '',
    writer: movie.writer || '',
  })
  submitError.value = null
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingMovie.value = null
  resetForm()
}

const handleSubmit = async () => {
  submitting.value = true
  submitError.value = null
  try {
    if (editingMovie.value) {
      await moviesStore.updateMovie(editingMovie.value.id, { ...form })
    } else {
      await moviesStore.createMovie({ ...form })
    }
    closeModal()
  } catch (error) {
    submitError.value = error.response?.data?.error || error.message || 'Une erreur est survenue.'
  } finally {
    submitting.value = false
  }
}

const deleteMovie = async (id) => {
  if (confirm('Êtes-vous sûr de vouloir supprimer ce film ?')) {
    await moviesStore.deleteMovie(id)
  }
}
</script>
