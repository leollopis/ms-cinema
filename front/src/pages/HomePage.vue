<template>
  <div class="min-h-screen bg-dark-bg text-light-text flex flex-col">
    <Header />

    <main class="flex-1">

      <!-- HERO SECTION - Enhanced Cinematic Showcase -->
      <section class="relative h-[70vh] flex items-center justify-center text-light-text overflow-hidden">
        <!-- Background Image/Video Placeholder -->
        <div class="absolute inset-0 w-full h-full">
          <img src="https://picsum.photos/seed/cinemabackdrop/1920/1080" alt="Cinematic Background" class="w-full h-full object-cover brightness-75">
          <!-- Subtle Gradient Overlay -->
          <div class="absolute inset-0 bg-gradient-to-t from-dark-bg via-dark-bg/50 to-transparent"></div>
        </div>

        <!-- Content Overlay -->
        <div class="relative z-10 max-w-4xl mx-auto text-center p-6 space-y-6">
          <span class="text-xl md:text-2xl uppercase tracking-widest text-primary-accent font-semibold">
              Bienvenue sur Central Cinéma
            </span>

          <h1 class="text-6xl md:text-8xl font-heading font-extrabold leading-none text-light-text drop-shadow-lg">
            Votre portail vers le grand écran.
          </h1>

          <p class="text-xl md:text-2xl text-muted-text max-w-2xl mx-auto">
            Explorez les derniers films, découvrez les horaires des séances, et réservez vos places en quelques clics. Préparez le popcorn !
          </p>

          <div class="flex justify-center gap-6 pt-4">
            <router-link to="/films" class="px-8 py-3 bg-primary-accent hover:bg-primary-hover rounded-lg font-semibold transition-colors shadow-lg">
              Voir les films
            </router-link>
            <router-link to="/seances" class="px-8 py-3 bg-dark-card hover:bg-dark-border border border-dark-border rounded-lg font-semibold transition-colors shadow-lg">
              Toutes les séances
            </router-link>
          </div>
        </div>
      </section>

      <!-- FILMS - Enhanced Movie Listings Grid -->
      <section class="px-6 md:px-12 py-20 bg-dark-card/30 border-t border-dark-border">
        <div class="max-w-7xl mx-auto">

          <div class="flex items-center justify-between mb-12">
            <h2 class="text-4xl font-heading font-bold text-light-text">À l’affiche en ce moment</h2>
            <router-link to="/films" class="text-base text-primary-accent hover:underline">
              Voir tous les films →
            </router-link>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-6">
            <div
              v-for="movie in popularMovies"
              :key="movie.id"
              @click="goToMovie(movie.id)"
              class="group relative h-64 md:h-72 rounded-lg cursor-pointer overflow-hidden
                     bg-dark-card shadow-lg
                     transform-gpu transition-all duration-300
                     hover:scale-105 hover:shadow-xl hover:shadow-primary-accent/40 border border-dark-border"
            >
              <div
                class="absolute inset-0 w-full h-full"
                :style="{ backgroundImage: `url('${movie.image}')`, backgroundSize: 'cover', backgroundPosition: 'center' }"
              ></div>
              <!-- Overlay for details on hover -->
              <div class="absolute inset-0 bg-gradient-to-t from-dark-bg via-dark-bg/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <!-- Infos -->
                <div class="absolute bottom-0 left-0 right-0 p-4 text-light-text">
                  <h3 class="text-lg font-semibold truncate group-hover:whitespace-normal group-hover:line-clamp-2">
                    {{ movie.title }}
                  </h3>
                  <div class="mt-1">
                     <p class="text-sm text-muted-text">
                      {{ movie.duration }} min • ⭐ {{ movie.rating }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </section>
      
      <!-- HOW IT WORKS - Polished Section -->
      <section class="px-6 md:px-12 py-24 border-t border-dark-border bg-dark-bg">
        <div class="max-w-5xl mx-auto text-center">
          <h2 class="text-4xl font-heading font-bold text-light-text mb-4">Votre soirée ciné en 3 étapes</h2>
          <p class="text-xl text-muted-text mb-12">C'est simple, rapide et sécurisé.</p>

          <div class="grid md:grid-cols-3 gap-12">
            <div class="flex flex-col items-center space-y-4">
              <div class="flex items-center justify-center w-16 h-16 bg-dark-card border-2 border-primary-accent/50 rounded-full text-2xl font-bold text-primary-accent">1</div>
              <h4 class="font-semibold text-xl text-light-text">Choisissez votre film</h4>
              <p class="text-base text-muted-text">Parcourez notre catalogue et trouvez le film qui vous fait envie.</p>
            </div>
            <div class="flex flex-col items-center space-y-4">
              <div class="flex items-center justify-center w-16 h-16 bg-dark-card border-2 border-primary-accent/50 rounded-full text-2xl font-bold text-primary-accent">2</div>
              <h4 class="font-semibold text-xl text-light-text">Réservez votre séance</h4>
              <p class="text-base text-muted-text">Sélectionnez la date, l'heure et vos sièges préférés.</p>
            </div>
            <div class="flex flex-col items-center space-y-4">
              <div class="flex items-center justify-center w-16 h-16 bg-dark-card border-2 border-primary-accent/50 rounded-full text-2xl font-bold text-primary-accent">3</div>
              <h4 class="font-semibold text-xl text-light-text">Profitez du spectacle</h4>
              <p class="text-base text-muted-text">Présentez votre e-billet et savourez l'expérience Central Cinéma.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- PROMO BANNER - Polished Section -->
      <section class="px-6 md:px-12 py-16">
        <div class="max-w-6xl mx-auto bg-primary-accent/10 border border-primary-accent/30 rounded-lg p-8 md:p-12 text-center shadow-lg">
          <h2 class="text-4xl font-heading font-bold text-light-text mb-3">Offre Spéciale Étudiants</h2>
          <p class="text-xl text-primary-accent max-w-xl mx-auto">
            Bénéficiez de -25% sur toutes les séances du lundi au jeudi sur présentation de votre carte étudiante.
          </p>
        </div>
      </section>

    </main>

    <Footer />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useMoviesStore } from '@/stores/movies.store'
import Header from '@/components/common/Header.vue'
import Footer from '@/components/common/Footer.vue'

const router = useRouter()
const moviesStore = useMoviesStore()
const { movies } = storeToRefs(moviesStore)

const goToMovie = (id) => router.push(`/film/${id}`)

// Show up to 6 popular movies from the real catalog
const popularMovies = computed(() => movies.value.slice(0, 6))

onMounted(() => {
  if (movies.value.length === 0) {
    moviesStore.fetchMovies()
  }
})
</script>