<template>
  <div class="flex-1 min-h-0 flex flex-col bg-gray-900">
    <NavbarSection @open-modal="showModal = true" />
    <AuthModal v-if="showModal" @close="showModal = false" />

    <main class="flex-1 px-4 py-10 sm:px-8 max-w-5xl mx-auto w-full">
      <h2 class="text-4xl font-extrabold text-white mb-8 tracking-tight">Planes</h2>

      <div v-if="loading" class="text-center py-16 text-gray-400">Cargando...</div>

      <div v-else-if="plans.length === 0" class="text-center py-16 text-gray-400">
        No hay planes disponibles por el momento.
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="plan in plans"
          :key="plan.id"
          class="rounded-2xl overflow-hidden transition-all duration-200 hover:-translate-y-1"
          :class="plan.is_featured
            ? 'ring-2 ring-green-500 shadow-[0_0_20px_rgba(34,197,94,0.25)]'
            : 'ring-1 ring-white/10 hover:ring-white/20'"
        >
          <!-- Imagen -->
          <div class="h-56 bg-black overflow-hidden">
            <img
              v-if="plan.image"
              :src="plan.image"
              :alt="plan.title"
              class="w-full h-full object-cover"
            />
          </div>

          <!-- Info -->
          <div class="bg-white p-5 flex flex-col gap-1">
            <span
              v-if="plan.is_featured"
              class="self-start mb-1 text-xs font-bold uppercase tracking-wide bg-green-500 text-white px-3 py-1 rounded-full"
            >
              Más popular
            </span>
            <h3 class="text-sm font-bold uppercase tracking-wide text-gray-900">{{ plan.title }}</h3>
            <div class="flex items-baseline gap-1">
              <p class="text-3xl font-bold text-gray-900">${{ plan.price }}</p>
              <span v-if="plan.period" class="text-sm text-gray-400">{{ plan.period }}</span>
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
