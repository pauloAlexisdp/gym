<template>
  <div>
    <form @submit.prevent="handleSubmit" class="space-y-3 sm:space-y-4">
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="block text-xs sm:text-sm font-medium text-gray-700 mb-1">Nombre</label>
          <input
            v-model="formData.name"
            type="text"
            required
            class="w-full px-3 py-2 sm:px-4 sm:py-3 text-sm sm:text-base border border-gray-300 rounded-xl focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all"
            placeholder="Tu nombre"
          />
        </div>

        <div>
          <label class="block text-xs sm:text-sm font-medium text-gray-700 mb-1">Apellido</label>
          <input
            v-model="formData.lastname"
            type="text"
            required
            class="w-full px-3 py-2 sm:px-4 sm:py-3 text-sm sm:text-base border border-gray-300 rounded-xl focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all"
            placeholder="Tu apellido"
          />
        </div>
      </div>

      <div>
        <label class="block text-xs sm:text-sm font-medium text-gray-700 mb-1">Email</label>
        <input
          v-model="formData.email"
          type="email"
          required
          class="w-full px-3 py-2 sm:px-4 sm:py-3 text-sm sm:text-base border border-gray-300 rounded-xl focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all"
          placeholder="tu@email.com"
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
        {{ isLoading ? 'Registrando...' : 'Registrarme' }}
      </button>
    </form>

    <div v-if="showError" class="mt-3 p-2 sm:p-3 bg-red-100 border border-red-400 text-red-700 text-xs sm:text-sm rounded-lg">
      {{ errorMessage }}
    </div>

    <div v-if="showSuccess" class="mt-3 p-2 sm:p-3 bg-green-100 border border-green-400 text-green-700 text-xs sm:text-sm rounded-lg">
      ¡Registro exitoso! Ahora puedes iniciar sesión.
    </div>

    <p class="mt-3 text-center text-xs sm:text-sm text-gray-600">
      ¿Ya tienes cuenta?
      <button @click="$emit('switch-to-login')" class="text-black font-semibold hover:underline ml-1">
        Inicia sesión
      </button>
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { authService, type RegisterData } from '@/services/auth.service'

const emit = defineEmits<{
  success: []
  'switch-to-login': []
}>()

const formData = ref<RegisterData>({ name: '', lastname: '', email: '', password: '' })
const showSuccess = ref(false)
const showError = ref(false)
const errorMessage = ref('')
const isLoading = ref(false)

const handleSubmit = async () => {
  isLoading.value = true
  showError.value = false
  showSuccess.value = false

  try {
    const result = await authService.register(formData.value)

    if (result.success) {
      showSuccess.value = true
      setTimeout(() => emit('success'), 1500)
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
