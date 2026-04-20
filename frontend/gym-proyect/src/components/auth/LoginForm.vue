<template>
  <div>
    <form @submit.prevent="handleSubmit" class="space-y-3 sm:space-y-4">
      <div>
        <label class="block text-xs sm:text-sm font-medium text-gray-700 mb-1">Email</label>
        <input
          v-model="formData.email"
          type="email"
          required
          class="w-full px-3 py-2 sm:px-4 sm:py-3 text-sm sm:text-base border border-gray-300 rounded-xl focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all"
          placeholder="nombre@correo.com"
        />
      </div>

      <div>
        <label class="block text-xs sm:text-sm font-medium text-gray-700 mb-1">Contraseña</label>
        <input
          v-model="formData.password"
          type="password"
          required
          class="w-full px-3 py-2 sm:px-4 sm:py-3 text-sm sm:text-base border border-gray-300 rounded-xl focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all"
          placeholder="••••••••"
        />
      </div>

      <button
        type="submit"
        :disabled="isLoading"
        class="w-full bg-black text-white py-2 sm:py-3 text-sm sm:text-base rounded-xl font-semibold hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {{ isLoading ? 'Ingresando...' : 'Ingresar' }}
      </button>
    </form>

    <div v-if="showError" class="mt-3 p-2 sm:p-3 bg-red-100 border border-red-400 text-red-700 text-xs sm:text-sm rounded-lg">
      {{ errorMessage }}
    </div>

    <p class="mt-2 text-center">
      <button @click="$emit('forgot-password')" class="text-xs sm:text-sm text-gray-500 hover:text-black hover:underline transition-colors">
        ¿Olvidaste tu contraseña?
      </button>
    </p>

    <p class="mt-2 text-center text-xs sm:text-sm text-gray-600">
      ¿No tienes cuenta?
      <button @click="$emit('switch-to-register')" class="text-black font-semibold hover:underline ml-1">
        Regístrate
      </button>
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { authService, type LoginData } from '@/services/auth.service'

const emit = defineEmits<{
  success: [payload: { token: string; user: any }]
  'switch-to-register': []
  'forgot-password': []
}>()

const formData = ref<LoginData>({ email: '', password: '' })
const showError = ref(false)
const errorMessage = ref('')
const isLoading = ref(false)

const handleSubmit = async () => {
  isLoading.value = true
  showError.value = false

  try {
    const result = await authService.login(formData.value)

    if (result.success && result.data) {
      const data = result.data as { data: { token: string; user: any } }
      emit('success', { token: data.data.token, user: data.data.user })
    } else {
      errorMessage.value = result.message
      showError.value = true
    }
  } catch {
    errorMessage.value = 'Error de conexión con el servidor'
    showError.value = true
  } finally {
    isLoading.value = false
  }
}
</script>
