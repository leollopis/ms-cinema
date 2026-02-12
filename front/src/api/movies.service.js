// src/api/movies.service.js
import http from './http'

// Microservice Movies: Gestion du catalogue de films via le microservice Catalog (PHP)
// Gateway route: /movies -> catalog:4001 with pathRewrite to /catalogue/movies
export const moviesService = {
    // Recuperer tous les films
    getMovies: () => http.get('/movies'),

    // Recuperer un film specifique
    getMovieById: (id) => http.get(`/movies/${id}`),

    // Creer un nouveau film (Admin)
    createMovie: (movieData) => http.post('/movies', movieData),

    // Mettre a jour un film (Admin)
    updateMovie: (id, movieData) => http.put(`/movies/${id}`, movieData),

    // Supprimer un film (Admin)
    deleteMovie: (id) => http.delete(`/movies/${id}`),

    // Obtenir les statistiques des films
    getMovieStats: () => http.get('/movies/stats/all'),

    // Health check
    health: () => http.get('/catalogue/health'),
}

export default moviesService