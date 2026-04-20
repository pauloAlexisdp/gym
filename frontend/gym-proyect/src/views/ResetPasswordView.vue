<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center px-4">
    <div class="bg-white rounded-2xl shadow-xl p-6 w-full max-w-md">
      <h2 class="text-xl font-bold text-gray-800 mb-1">Nueva contraseña</h2>
      <p class="text-sm text-gray-500 mb-6">Ingresa tu nueva contraseña para continuar.</p>

      <div v-if="!done">
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nueva contraseña</label>
            <input
              v-model="password"
              type="password"
              required
              minlength="8"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all"
              placeholder="Mínimo 8 caracteres"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Confirmar contraseña</label>
            <input
              v-model="confirm"
              type="password"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all"
              placeholder="Repite la contraseña"
            />
          </div>

          <div v-if="error" class="p-3 bg-red-100 border border-red-400 text-red-700 text-sm rounded-lg">
            {{ error }}
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-black text-white py-3 rounded-xl font-semibold hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ loading ? 'Guardando...' : 'Guardar contraseña' }}
          </button>
        </form>
      </div>

      <div v-else class="text-center py-4 space-y-3">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="font-semibold text-gray-800">¡Contraseña actualizada!</p>
        <button @click="router.push('/')" class="text-sm text-gray-500 hover:text-black hover:underline transition-colors">
          Ir al inicio
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const password = ref('')
const confirm = ref('')
const loading = ref(false)
const done = ref(false)
const error = ref('')

async function handleSubmit() {
  if (password.value !== confirm.value) {
    error.value = 'Las contraseñas no coinciden'
    return
  }
  error.value = ''
  loading.value = true
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/reset-password/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token: route.query.token, password: password.value }),
    })
    const data = await res.json()
    if (res.ok) {
      done.value = true
    } else {
      error.value = data.message || 'Error al restablecer la contraseña'
    }
  } finally {
    loading.value = false
  }
}
</script>
