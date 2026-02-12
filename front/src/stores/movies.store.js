import { defineStore } from 'pinia'
import moviesService from '@/api/movies.service'

export const useMoviesStore = defineStore('movies', {
    state: () => ({
        movies: [],
        selectedMovie: null,
        loading: false,
        error: null
    }),

    getters: {
        getAllMovies: (state) => state.movies,
        getMovieById: (state) => (id) => state.movies.find(m => m.id == id)
    },

    actions: {
        async fetchMovies() {
            this.loading = true
            this.error = null
            try {
                const response = await moviesService.getMovies()
                this.movies = response.data
            } catch (error) {
                this.error = 'Erreur lors du chargement des films.'
                console.error(this.error, error)
            } finally {
                this.loading = false
            }
        },

        async fetchMovieById(id) {
            this.loading = true
            this.error = null
            try {
                const response = await moviesService.getMovieById(id)
                this.selectedMovie = response.data
                return response.data
            } catch (error) {
                this.error = error.response?.data?.error || 'Film non trouve.'
                console.error('Erreur lors du chargement du film:', error)
            } finally {
                this.loading = false
            }
        },

        async createMovie(movieData) {
            this.loading = true
            this.error = null
            try {
                const response = await moviesService.createMovie(movieData)
                await this.fetchMovies()
                return response.data
            } catch (error) {
                this.error = error.response?.data?.error || 'Erreur lors de la creation du film.'
                console.error(this.error, error)
                throw error
            } finally {
                this.loading = false
            }
        },

        async updateMovie(id, movieData) {
            this.loading = true
            this.error = null
            try {
                const response = await moviesService.updateMovie(id, movieData)
                await this.fetchMovies()
                return response.data
            } catch (error) {
                this.error = error.response?.data?.error || 'Erreur lors de la mise a jour du film.'
                console.error(this.error, error)
                throw error
            } finally {
                this.loading = false
            }
        },

        async deleteMovie(id) {
            this.loading = true
            this.error = null
            try {
                await moviesService.deleteMovie(id)
                await this.fetchMovies()
            } catch (error) {
                this.error = error.response?.data?.error || 'Erreur lors de la suppression du film.'
                console.error(this.error, error)
                throw error
            } finally {
                this.loading = false
            }
        },

        async getStats() {
            try {
                const response = await moviesService.getMovieStats()
                return response.data
            } catch (error) {
                console.error('Erreur lors de la recuperation des stats:', error)
                throw error
            }
        }
    }
})