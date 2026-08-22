<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMoviesStore } from '@/stores/movies'
import type { MovieDetail, Actor } from '@/types/movie'

const route = useRoute()
const router = useRouter()
const store = useMoviesStore()

const movie = ref<MovieDetail | null>(null)
const allActors = ref<Actor[]>([])
const selectedActorIds = ref<number[]>([])
const description = ref('')

const newActorFirstName = ref('')
const newActorLastName = ref('')

const reviewGrade = ref<number>(0)
const snackbar = ref(false)
const snackbarText = ref('')

const movieId = Number(route.params.id)

const actorOptions = computed(() =>
  allActors.value.map((a) => ({
    id: a.id,
    name: `${a.first_name} ${a.last_name}`,
  }))
)

async function loadMovie() {
  const detail = await store.fetchMovieDetail(movieId)
   movie.value = detail
   description.value = detail.description
   selectedActorIds.value = detail.actors.map((a) => a.id)
}

async function loadAllActors() {
  allActors.value = await store.fetchActors()
}

onMounted(() => {
  loadMovie()
  loadAllActors()
})

function goBack() {
  router.back()
}

async function saveDescription() {
  const updated = await store.updateMovie(movieId, { description: description.value })
  movie.value = updated
  showConfirmation('Description mise à jour')
}

async function saveActors() {
  const updated = await store.updateMovie(movieId, { actor_ids: selectedActorIds.value })
  movie.value = updated
  showConfirmation('Acteurs mis à jour')
}

async function addNewActor() {
  if (!newActorFirstName.value || !newActorLastName.value) return
  const actor = await store.createActor(newActorFirstName.value, newActorLastName.value)
  allActors.value.push(actor)
  selectedActorIds.value.push(actor.id)
  newActorFirstName.value = ''
  newActorLastName.value = ''
  await saveActors()
}

async function submitReview() {
  if (reviewGrade.value < 1) return
  const updated = await store.addReview(movieId, reviewGrade.value)
  movie.value = updated
  reviewGrade.value = 0
  showConfirmation('Avis ajouté, merci !')
}

function showConfirmation(text: string) {
  snackbarText.value = text
  snackbar.value = true
}
</script>

<template>
  <v-container v-if="movie">
    <v-btn @click="goBack" prepend-icon="mdi-arrow-left" variant="text" class="mb-4">
      Retour à la liste
    </v-btn>

    <h1 class="text-h4 mb-2">{{ movie.title }}</h1>

    <div class="d-flex align-center mb-4">
      <v-icon icon="mdi-star" color="amber" class="mr-1" />
      <span v-if="movie.average_grade !== null">
        {{ movie.average_grade.toFixed(1) }} / 5
      </span>
      <span v-else class="text-grey">Pas encore noté</span>
    </div>

    <!-- Description -->
    <v-card class="mb-4" variant="outlined">
      <v-card-title>Description</v-card-title>
      <v-card-text>
        <v-textarea v-model="description" rows="3" variant="outlined" />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn color="primary" @click="saveDescription">Enregistrer</v-btn>
      </v-card-actions>
    </v-card>

    <!-- Acteurs -->
    <v-card class="mb-4" variant="outlined">
      <v-card-title>Acteurs</v-card-title>
      <v-card-text>
        <v-select
            v-model="selectedActorIds"
            :items="actorOptions"
            item-title="name"
            item-value="id"
            multiple
            chips
            label="Acteurs du film"
            variant="outlined"
        />

        <div class="d-flex ga-2 mt-2">
          <v-text-field v-model="newActorFirstName" label="Prénom" density="compact" variant="outlined" />
          <v-text-field v-model="newActorLastName" label="Nom" density="compact" variant="outlined" />
          <v-btn @click="addNewActor" icon="mdi-plus" variant="tonal" :disabled="!newActorFirstName || !newActorLastName"/>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn color="primary" @click="saveActors">Enregistrer les acteurs</v-btn>
      </v-card-actions>
    </v-card>

    <!-- Ajouter un avis -->
    <v-card variant="outlined">
      <v-card-title>Laisser un avis</v-card-title>
      <v-card-text class="d-flex align-center ga-4">
        <v-rating
          v-model="reviewGrade"
          color="amber"
          hover
          length="5"
        />
        <v-btn color="primary" :disabled="reviewGrade < 1" @click="submitReview">
          Envoyer
        </v-btn>
      </v-card-text>
    </v-card>

    <v-snackbar v-model="snackbar" timeout="2000">
      {{ snackbarText }}
    </v-snackbar>
  </v-container>
</template>