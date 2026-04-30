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
          class="rounded-2xl overflow-hidden transition-all duration-200 hover:-translate-y-1 flex flex-col ring-1 ring-gray-200 shadow hover:ring-2 hover:ring-[#1DB954] hover:shadow-md"
        >
          <!-- Imagen -->
          <div class="h-56 bg-gray-900 overflow-hidden">
            <img
              v-if="plan.image"
              :src="plan.image"
              :alt="plan.title"
              class="w-full h-full object-cover"
            />
          </div>

          <!-- Info -->
          <div class="bg-white p-5 flex flex-col gap-1 flex-1">
            <span
              v-if="plan.is_featured"
              class="self-start mb-2 text-[10px] font-bold uppercase tracking-wide bg-[#1DB954] text-white px-2.5 py-0.5 rounded-full"
            >
              Más popular
            </span>
            <h3 class="text-sm font-bold uppercase tracking-wide text-gray-900">{{ plan.title }}</h3>
            <div class="flex items-baseline gap-1 mt-1">
              <p class="text-3xl font-bold text-gray-900">${{ plan.price }}</p>
              <span v-if="plan.period" class="text-sm text-gray-400 ml-1">{{ plan.period }}</span>
            </div>
            <p v-if="plan.description" class="text-sm text-gray-500 mt-1">{{ plan.description }}</p>
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
  period: string
  is_featured: boolean
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
