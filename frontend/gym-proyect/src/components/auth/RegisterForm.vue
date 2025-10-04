<template>
  <div class="min-h-screen bg-gray-100">
    <div class="flex items-center justify-center min-h-screen px-4">
      <div class="bg-white rounded-lg shadow-lg p-8 w-full max-w-md">
        <h2 class="text-2xl font-bold text-gray-800 mb-6 text-center">Registrarse</h2>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700 mb-2">Nombre</label>
            <input
              id="name"
              v-model="formData.name"
              type="text"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all"
              placeholder="Tu nombre"
            />
          </div>

          <div>
            <label for="lastname" class="block text-sm font-medium text-gray-700 mb-2">Apellido</label>
            <input
              id="lastname"
              v-model="formData.lastname"
              type="text"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all"
              placeholder="Tu apellido"
            />
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">Email</label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all"
              placeholder="tu@email.com"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">Contraseña</label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="w-full bg-black text-white py-2 px-4 rounded-lg hover:bg-gray-800 transition-colors font-medium mt-6 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ isLoading ? 'Registrando...' : 'Registrarse' }}
          </button>
        </form>

        <div v-if="showSuccess" class="mt-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg">
          ¡Registro exitoso! Redirigiendo a login...
        </div>

        <div v-if="showError" class="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
          {{ errorMessage }}
        </div>

        <div class="mt-4 text-center">
          <p class="text-sm text-gray-600">
            ¿Ya tienes cuenta?
            <button
              @click="$emit('switch-to-login')"
              class="text-green-600 font-semibold hover:underline ml-1 cursor-pointer"
            >
              Inicia sesión aquí
            </button>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService, type RegisterData } from '@/services/auth.service'

const router = useRouter()

defineEmits<{
  'switch-to-login': []
}>()

const formData = ref<RegisterData>({
  name: '',
  lastname: '',
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
    const result = await authService.register(formData.value)

    if (result.success) {
      showSuccess.value = true

      setTimeout(() => {
        router.push('/iniciar-sesion')
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
