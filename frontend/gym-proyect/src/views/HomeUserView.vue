<template>
  <div class="min-h-screen bg-gray-100">
    <NavbarSection />

    <main class="flex flex-col items-center px-4 py-10 sm:py-16">
      <h2 class="text-xl sm:text-2xl font-bold text-gray-800 mb-10">
        Bienvenido, {{ auth.user?.name }}
      </h2>

      <div v-if="loading" class="flex justify-center py-12">
        <span class="text-gray-400">Cargando...</span>
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-3 gap-6 w-full max-w-6xl">
        <div
          v-for="card in cards"
          :key="card.id"
          class="bg-white rounded-2xl shadow overflow-hidden cursor-pointer hover:shadow-xl transition-shadow flex flex-col"
          @click="router.push({ name: 'exercise-list', params: { muscleGroup: card.muscle_group }, query: { name: card.name } })"
        >
          <img
            v-if="card.image"
            :src="card.image"
            :alt="card.name"
            class="w-full h-52 object-cover"
          />
          <div v-else class="w-full h-52 bg-gray-200 flex items-center justify-center">
            <span class="text-gray-400 text-sm">Sin imagen</span>
          </div>

          <div class="p-5">
            <h3 class="font-bold text-gray-800 text-lg">{{ card.name }}</h3>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import { useApi } from '@/composables/useApi'
import NavbarSection from '@/components/common/NavbarSection.vue'

const router = useRouter()
const auth = useAuthStore()
const { apiFetch } = useApi()

interface MuscleGroupCard {
  id: number
  muscle_group: string
  name: string
  image: string | null
}

const cards = ref<MuscleGroupCard[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const data = await apiFetch(`${import.meta.env.VITE_API_URL}/api/exercises/muscle-group-cards/`)
    if (data) cards.value = data
  } finally {
    loading.value = false
  }
})
</script>
