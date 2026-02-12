<template>
  <div class="min-h-screen bg-dark-bg">
    <Header />
    <section class="px-4 md:px-12 py-10">
      <!-- Title only, as Header provides main navigation -->
      <h1 class="text-4xl font-heading font-bold text-light-text mb-8">Films à l'affiche</h1>

      <!-- Loading and Error states -->
      <div v-if="loading" class="text-center text-muted-text">Chargement des films...</div>
      <div v-if="error" class="text-center text-danger">Erreur: {{ error }}</div>

      <!-- Movies Grid -->
      <div v-if="!loading && !error" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <router-link
          v-for="movie in movies"
          :key="movie.id"
          :to="`/film/${movie.id}`"
          class="group relative block h-80 bg-dark-card rounded-lg overflow-hidden
                     shadow-lg
                     transform-gpu transition-all duration-300
                     hover:scale-105 hover:shadow-xl hover:shadow-primary-accent/40 border border-dark-border"
        >
          <div 
            class="absolute inset-0 w-full h-full bg-cover bg-center transition-transform duration-500 group-hover:scale-110"
            :style="{ backgroundImage: movie.image ? `url('${movie.image}')` : '' }"
          ></div>
          <!-- Fond dégradé avec transparence -->
          <div class="absolute inset-0 bg-gradient-to-t from-dark-bg via-dark-bg/60 to-transparent group-hover:from-dark-bg/90 group-hover:via-dark-bg/70 transition-all"></div>

          <!-- Titre et Infos -->
          <div class="absolute inset-0 flex flex-col items-center justify-end text-center p-4 pb-6 text-light-text">
            <h3 class="text-2xl md:text-3xl font-heading font-extrabold drop-shadow-lg transition-transform group-hover:scale-105">
              {{ movie.title }}
            </h3>
            <p class="text-base text-muted-text mt-1">{{ movie.genre }}</p>
            <div class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 mt-2">
              <span class="text-success text-sm font-semibold">{{ movie.rating }}★</span>
              <span class="text-muted-text text-sm ml-2">{{ movie.duration }} min</span>
            </div>
          </div>
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useMoviesStore } from '@/stores/movies.store'
import { storeToRefs } from 'pinia'
import Header from '@/components/common/Header.vue'
const moviesStore = useMoviesStore()
const { movies, loading, error } = storeToRefs(moviesStore)

onMounted(() => {
  moviesStore.fetchMovies()
})
</script>

<style scoped></style>