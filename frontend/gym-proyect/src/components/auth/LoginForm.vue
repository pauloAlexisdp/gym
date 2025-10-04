<template>
  <div class="min-h-screen bg-gray-100">
    <div class="flex items-center justify-center min-h-screen px-4 sm:px-6 lg:px-8">
      <div class="bg-white rounded-lg shadow-xl w-full max-w-md sm:max-w-lg">
        <div class="px-4 py-6 sm:px-8 sm:py-8">

          <h2 class="text-xl sm:text-2xl lg:text-3xl font-bold text-gray-800 mb-4 sm:mb-6 text-center font-black tracking-tight leading-none transform scale-x-95">
            ¡Bienvenido!
          </h2>

          <form @submit.prevent="handleSubmit" class="space-y-4 sm:space-y-6">
            <div>
              <label for="email" class="block text-sm sm:text-base font-medium text-gray-700 mb-1 sm:mb-2">
                Email
              </label>
              <input
                id="email"
                v-model="formData.email"
                type="email"
                required
                class="w-full px-3 py-2 sm:px-4 sm:py-3 text-sm sm:text-base border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all"
                placeholder="tu@email.com"
              />
            </div>

            <div>
              <label for="password" class="block text-sm sm:text-base font-medium text-gray-700 mb-1 sm:mb-2">
                Contraseña
              </label>
              <input
                id="password"
                v-model="formData.password"
                type="password"
                required
                class="w-full px-3 py-2 sm:px-4 sm:py-3 text-sm sm:text-base border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all"
                placeholder="••••••••"
              />
            </div>

            <button
              type="submit"
              :disabled="isLoading"
              class="w-full bg-black text-white py-2 sm:py-3 px-4 text-sm sm:text-base rounded-lg font-semibold hover:bg-gray-800 transition-colors duration-200 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ isLoading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
            </button>
          </form>

          <div
            v-if="showSuccess"
            class="mt-4 sm:mt-6 p-3 sm:p-4 bg-green-100 border border-green-400 text-green-700 text-sm sm:text-base rounded-lg"
          >
            ¡Inicio de sesión exitoso! Redirigiendo...
          </div>

          <div
            v-if="showError"
            class="mt-4 sm:mt-6 p-3 sm:p-4 bg-red-100 border border-red-400 text-red-700 text-sm sm:text-base rounded-lg"
          >
            {{ errorMessage }}
          </div>

          <div class="mt-4 sm:mt-6 text-center">
            <p class="text-sm sm:text-base text-gray-600">
              ¿No tienes cuenta?
              <button
                @click="$emit('switch-to-register')"
                class="text-green-600 font-semibold hover:underline ml-1 cursor-pointer"
              >
                Regístrate aquí
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService, type LoginData } from '@/services/auth.service'

const router = useRouter()

// Definir los emits
defineEmits<{
  'switch-to-register': []
}>()

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
