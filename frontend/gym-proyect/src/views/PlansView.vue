<template>
  <div class="flex-1 min-h-0 flex flex-col bg-gray-100">
    <NavbarSection @open-modal="showModal = true" />
    <AuthModal v-if="showModal" @close="showModal = false" />

    <main class="flex-1 px-4 py-10 sm:px-8 max-w-5xl mx-auto w-full">
      <h2 class="text-4xl font-extrabold text-gray-900 mb-8 tracking-tight">Planes</h2>

      <div v-if="loading" class="text-center py-16 text-gray-400">Cargando...</div>

      <div v-else-if="plans.length === 0" class="text-center py-16 text-gray-400">
        No hay planes disponibles por el momento.
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="plan in plans"
          :key="plan.id"
          class="bg-white rounded-2xl shadow overflow-hidden cursor-default transition-all duration-200 hover:shadow-xl hover:-translate-y-1"
        >
          <div class="h-64 bg-gray-200 overflow-hidden">
            <img
              v-if="plan.image"
              :src="plan.image"
              :alt="plan.title"
              class="w-full h-full object-cover"
            />
            <div v-else class="w-full h-full flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
          </div>

          <div class="p-5 flex flex-col gap-2">
            <h3 class="text-lg font-bold text-gray-800 uppercase tracking-wide">{{ plan.title }}</h3>
            <p class="text-2xl font-bold text-black">{{ plan.price }}</p>
            <p v-if="plan.description" class="text-sm text-gray-500 leading-relaxed">{{ plan.description }}</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import NavbarSection from '@/components/common/NavbarSection.vue'
import AuthModal from '@/components/auth/AuthModal.vue'

const showModal = ref(false)

interface Plan {
  id: number
  title: string
  price: string
  description: string
  image: string | null
}

const plans = ref<Plan[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/api/plans/`)
    if (res.ok) plans.value = await res.json()
  } finally {
    loading.value = false
  }
})
</script>
