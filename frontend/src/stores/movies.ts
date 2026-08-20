import { defineStore } from 'pinia'
import apiClient from '@/api/client'
import type { MovieDetail } from '@/types/movies'

export const useMoviesStore = defineStore('movies', {
  actions: {
    async fetchMovies(page: number) {
      const response = await apiClient.get('/movies/', { params: { page } })
      return response.data // { count, next, previous, results }
    },
    async fetchMovieDetail(id: number) {
      const response = await apiClient.get<MovieDetail>(`/movies/${id}/`)
      return response.data
    },
    async addReview(movieId: number, grade: number) {
      await apiClient.post('/reviews/', { movie: movieId, grade })
    },
    async updateMovie(id: number, payload: { description?: string; actor_ids?: number[] }) {
      const response = await apiClient.patch<MovieDetail>(`/movies/${id}/`, payload)
      return response.data
    },
  },
})