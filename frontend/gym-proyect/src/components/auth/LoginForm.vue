<template>
  <div class="min-h-screen bg-gray-100">
    <GymNavbar />

    <div class="flex items-center justify-center min-h-[calc(100vh-6rem)] px-4">
      <div class="bg-white rounded-lg shadow-xl p-8 w-full max-w-md">
        <h2 class="text-2xl font-bold text-gray-800 mb-6 text-center">Iniciar Sesión</h2>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Email
            </label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all"
              placeholder="tu@email.com"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              Contraseña
            </label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="w-full bg-black text-white py-3 rounded-lg font-semibold hover:bg-gray-800 transition-colors duration-200 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ isLoading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
          </button>
        </form>

        <div
          v-if="showSuccess"
          class="mt-6 p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg"
        >
          ¡Inicio de sesión exitoso! Redirigiendo...
        </div>

        <div
          v-if="showError"
          class="mt-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg"
        >
          {{ errorMessage }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService, type LoginData } from '@/services/auth.service'
import GymNavbar from '@/components/common/NavbarSection.vue'

const router = useRouter()

const formData = ref<LoginData>({
  email: '',
  password: ''
})

const showSuccess = ref(false)
const showError = ref(false)
const errorMessage = ref('')
const isLoading = ref(false)

const handleSubmit = async (): Promise<void> => {
  isLoading.value = true
  showError.value = false
  showSuccess.value = false

  try {
    const result = await authService.login(formData.value)

    if (result.success) {
      showSuccess.value = true
      // Redirigir a Home después de 2 segundos
      setTimeout(() => {
        router.push('/')
      }, 2000)
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
