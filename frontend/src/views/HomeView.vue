<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMoviesStore } from '@/stores/movies'
import type { MovieListItem } from '@/types/movie'

const store = useMoviesStore()
const route = useRoute()
const router = useRouter()

const movies = ref<MovieListItem[]>([])
const count = ref(0)
const pageSize = 5

const currentPage = ref(Number(route.query.page) || 1)

async function loadMovies(page: number) {
  const data = await store.fetchMovies(page)
  movies.value = data.results
  count.value = data.count
}

onMounted(() => loadMovies(currentPage.value))

// Quand la pagination Vuetify change de page, on met à jour l'URL
watch(currentPage, (newPage) => {
  router.push({ path: '/', query: { page: newPage } })
  loadMovies(newPage)
})

function goToDetail(id: number) {
  router.push(`/movies/${id}`)
}
</script>

<template>
  <v-container>
    <h1 class="text-h4 mb-4">Films</h1>

    <v-list>
      <v-list-item
        v-for="movie in movies"
        :key="movie.id"
        @click="goToDetail(movie.id)"
        class="mb-2"
        border
        rounded
      >
        <v-list-item-title>{{ movie.title }}</v-list-item-title>
        <template #append>
            <div v-if="movie.average_grade !== null" class="d-flex align-center">
                <v-icon icon="mdi-star" color="amber" size="small" class="mr-1" />
                <span>{{ movie.average_grade.toFixed(1) }}</span>
            </div>
            <span v-else class="text-grey text-caption">Pas encore noté</span>
        </template>
      </v-list-item>
    </v-list>

    <div class="d-flex justify-center mt-6">
      <v-pagination
        v-model="currentPage"
        :length="Math.ceil(count / pageSize)"
        :total-visible="7"
      />
    </div>
  </v-container>
</template>