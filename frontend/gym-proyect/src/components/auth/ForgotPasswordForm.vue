<template>
  <div>
    <div v-if="!sent">
      <p class="text-xs sm:text-sm text-gray-500 mb-4">
        Ingresa tu email y te enviaremos un enlace para restablecer tu contraseña.
      </p>
      <form @submit.prevent="handleSubmit" class="space-y-3 sm:space-y-4">
        <div>
          <label class="block text-xs sm:text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            v-model="email"
            type="email"
            required
            class="w-full px-3 py-2 sm:px-4 sm:py-3 text-sm sm:text-base border border-gray-300 rounded-xl focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all"
            placeholder="nombre@correo.com"
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-black text-white py-2 sm:py-3 text-sm sm:text-base rounded-xl font-semibold hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ loading ? 'Enviando...' : 'Enviar enlace' }}
        </button>
      </form>
    </div>

    <div v-else class="text-center py-4 space-y-2">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
      </svg>
      <p class="text-sm font-semibold text-gray-800">Revisa tu email</p>
      <p class="text-xs text-gray-500">Si el email existe, recibirás un enlace en los próximos minutos.</p>
    </div>

    <p class="mt-3 text-center">
      <button @click="$emit('back-to-login')" class="text-xs sm:text-sm text-gray-500 hover:text-black hover:underline transition-colors">
        Volver al inicio de sesión
      </button>
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineEmits<{ 'back-to-login': [] }>()

const email = ref('')
const loading = ref(false)
const sent = ref(false)

async function handleSubmit() {
  loading.value = true
  try {
    await fetch(`${import.meta.env.VITE_API_URL}/api/auth/forgot-password/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value }),
    })
    sent.value = true
  } finally {
    loading.value = false
  }
}
</script>
