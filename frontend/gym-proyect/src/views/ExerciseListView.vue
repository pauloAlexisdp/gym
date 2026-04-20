<template>
  <div class="min-h-screen bg-gray-100">
    <NavbarSection />

    <main class="px-4 py-8 sm:px-8 max-w-2xl mx-auto">
      <button @click="router.back()" class="flex items-center text-gray-500 hover:text-gray-800 mb-6 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        Volver
      </button>

      <h2 class="text-2xl font-bold text-gray-800 mb-4">{{ groupName }}</h2>

      <div v-if="!loading" class="relative mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11A6 6 0 115 11a6 6 0 0112 0z" />
        </svg>
        <input
          v-model="search"
          type="text"
          placeholder="Buscar ejercicio..."
          class="w-full pl-9 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl text-sm text-gray-700 focus:outline-none focus:border-black transition-colors shadow-sm"
        />
      </div>

      <div v-if="loading" class="flex justify-center py-12">
        <span class="text-gray-400">Cargando...</span>
      </div>

      <div v-else-if="filteredExercises.length === 0" class="text-center py-12 text-gray-400">
        {{ search ? 'Sin resultados para "' + search + '"' : 'No hay ejercicios en este grupo.' }}
      </div>

      <ul v-else class="space-y-3">
        <li
          v-for="exercise in filteredExercises"
          :key="exercise.id"
          class="bg-white rounded-xl px-5 py-4 shadow text-gray-800 font-medium cursor-pointer hover:shadow-md transition-shadow"
          @click="selectedExercise = exercise"
        >
          {{ exercise.name }}
        </li>
      </ul>
    </main>

    <ExerciseDetailModal
      v-if="selectedExercise"
      :exercise="selectedExercise"
      @close="selectedExercise = null"
      @updated="onExerciseUpdated"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import { useApi } from '@/composables/useApi'
import NavbarSection from '@/components/common/NavbarSection.vue'
import ExerciseDetailModal from '@/components/exercises/ExerciseDetailModal.vue'

export interface Exercise {
  id: number
  user_exercise_id: number
  name: string
  description: string
  muscle: string
  video_tutorial: string | null
  reps: number
  weight: number | null
}

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const { apiFetch } = useApi()

const muscleGroup = route.params.muscleGroup as string
const groupName = route.query.name as string

const exercises = ref<Exercise[]>([])
const loading = ref(true)
const selectedExercise = ref<Exercise | null>(null)
const search = ref('')

const filteredExercises = computed(() =>
  search.value.trim()
    ? exercises.value.filter(e => e.name.toLowerCase().includes(search.value.toLowerCase()))
    : exercises.value
)

onMounted(async () => {
  try {
    const data = await apiFetch(`${import.meta.env.VITE_API_URL}/api/exercises/by-group/${muscleGroup}/`)
    if (data) exercises.value = data
  } finally {
    loading.value = false
  }
})

function onExerciseUpdated(payload: { reps: number; weight: number }) {
  if (!selectedExercise.value) return
  selectedExercise.value.reps = payload.reps
  selectedExercise.value.weight = payload.weight
  const idx = exercises.value.findIndex(e => e.id === selectedExercise.value!.id)
  if (idx !== -1) {
    exercises.value[idx].reps = payload.reps
    exercises.value[idx].weight = payload.weight
  }
}
</script>
