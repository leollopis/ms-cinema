<template>
  <div class="bg-slate-950 text-slate-100 min-h-screen">
    
    <Header />

    <!-- Loading and Error States -->
    <div v-if="loading" class="text-center py-24 text-slate-400">Chargement du film...</div>
    <div v-if="error" class="text-center py-24 text-red-500">
      <p>Erreur: {{ error }}</p>
      <p v-if="!movie">Ce film n'a pas pu être chargé.</p>
    </div>

    <!-- Main Content -->
    <div v-if="movie && !loading">
      <!-- Hero Section -->
      <section class="relative h-[30vh] overflow-hidden">
        <div class="absolute inset-0">
          <div class="w-full h-full bg-cover bg-center opacity-30" 
              :style="{ backgroundImage: `url('${movie.image}')` }">
          </div>
          <div class="absolute inset-0 bg-gradient-to-r from-slate-950 via-slate-950/80 to-transparent"></div>
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-transparent"></div>
        </div>

        <div class="relative z-10 h-full px-6 md:px-12 py-8 flex items-center">
          <div class="max-w-4xl space-y-4">
            <h1 class="text-3xl md:text-5xl font-bold">{{ movie.title }}</h1>
            <div class="flex flex-wrap items-center gap-2 text-sm text-slate-300">
              <span class="text-green-500 font-semibold">{{ movie.rating }}★</span>
              <span>{{ movie.year }}</span>
              <span class="px-2 py-0.5 border border-slate-500 rounded">{{ movie.ageRating }}</span>
              <span>{{ movie.duration }} min</span>
              <span class="px-2 py-0.5 bg-slate-800 rounded">{{ movie.genre }}</span>
            </div>
            <p class="text-base text-slate-300 leading-relaxed">{{ movie.description }}</p>
            <div class="flex flex-wrap gap-4">
              <button @click="goToBooking" class="px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded transition flex items-center gap-2">
                <Ticket :size="18" />
                <span>Réserver des places</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Détails du film -->
      <section class="px-6 md:px-12 py-8 md:py-12">
        <div class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8 lg:gap-12">
          <div class="lg:col-span-2 space-y-8">
            <div>
              <h2 class="text-2xl font-semibold mb-2">Synopsis</h2>
              <p class="text-slate-300 leading-relaxed">{{ movie.synopsis }}</p>
            </div>
            <div v-if="movie.cast && movie.cast.length">
              <h2 class="text-2xl font-semibold mb-2">Distribution</h2>
              <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                <div v-for="actor in movie.cast" :key="actor.name" class="text-center">
                  <div class="w-20 h-20 mx-auto rounded-full bg-slate-800 mb-1"></div>
                  <p class="text-sm font-medium">{{ actor.name }}</p>
                  <p class="text-xs text-slate-400">{{ actor.role }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="space-y-6">
            <div class="bg-slate-900 border border-slate-800 rounded-lg p-4 md:p-6">
              <h3 class="text-xl font-semibold mb-2">Informations</h3>
              <div class="space-y-2 text-sm">
                <div v-if="movie.director"><span class="text-slate-400">Réalisateur:</span> <p class="text-slate-100">{{ movie.director }}</p></div>
                <div v-if="movie.writer"><span class="text-slate-400">Scénariste:</span> <p class="text-slate-100">{{ movie.writer }}</p></div>
                <div v-if="movie.releaseDate"><span class="text-slate-400">Date de sortie:</span> <p class="text-slate-100">{{ movie.releaseDate }}</p></div>
              </div>
            </div>
            <div v-if="movie.sessions && movie.sessions.length" class="bg-slate-900 border border-slate-800 rounded-lg p-4 md:p-6">
              <h3 class="text-xl font-semibold mb-2">Séances disponibles</h3>
              <div class="space-y-2">
                <div v-for="session in movie.sessions" :key="session.time" class="p-2 bg-slate-800 rounded hover:bg-slate-700 cursor-pointer transition">
                  <p class="font-medium">{{ session.date }}</p>
                  <p class="text-sm text-slate-400">{{ session.time }} • Salle {{ session.room }}</p>
                  <p class="text-xs text-green-400 mt-1">{{ session.availableSeats }} places disponibles</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Films similaires -->
      <section v-if="similarMovies.length" class="px-6 md:px-12 py-8 md:py-12 border-t border-slate-800">
        <div class="max-w-6xl mx-auto">
          <h2 class="text-2xl font-semibold mb-4">Films similaires</h2>
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            <div v-for="similar in similarMovies" :key="similar.id" @click="goToMovie(similar.id)" class="group cursor-pointer">
              <div class="relative aspect-[2/3] rounded overflow-hidden bg-cover bg-center" :style="{ backgroundImage: `url('${similar.image}')` }">
                <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-2 md:p-3">
                  <h3 class="font-semibold text-sm mb-1">{{ similar.title }}</h3>
                  <p class="text-xs text-slate-300">{{ similar.genre }}</p>
                  <span class="text-xs text-green-400 mt-1">{{ similar.rating }}★</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMoviesStore } from '@/stores/movies.store'
import { storeToRefs } from 'pinia'
import Header from '@/components/common/Header.vue'
import { Ticket } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const moviesStore = useMoviesStore()

// Reactive references to the store state
const { selectedMovie: movie, movies, loading, error } = storeToRefs(moviesStore)

// Fetch all movies if the list is empty (for similar movies)
onMounted(() => {
  if (movies.value.length === 0) {
    moviesStore.fetchMovies()
  }
})

// Function to load movie data
const loadMovie = (id) => {
  moviesStore.fetchMovieById(id)
}

// Load movie data when component mounts
onMounted(() => {
  loadMovie(route.params.id)
})

// Watch for route changes to load new movie data
watch(() => route.params.id, (newId) => {
  if (newId) {
    loadMovie(newId)
  }
})

// Computed property for similar movies
const similarMovies = computed(() => {
  if (!movie.value || movies.value.length === 0) return []
  // Exclude current movie and filter by genre, then take top 5
  return movies.value
    .filter(m => m.id !== movie.value.id && m.genre === movie.value.genre)
    .slice(0, 5)
})

// Navigation functions
const goToBooking = () => {
  if (movie.value) {
    router.push(`/client/booking?movieId=${movie.value.id}`)
  }
}
const goToMovie = (id) => {
  router.push(`/film/${id}`)
  window.scrollTo(0, 0)
}
</script>