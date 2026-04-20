<template>
  <div class="fixed inset-0 z-50 flex items-end sm:items-center justify-center">
    <div class="absolute inset-0 bg-black/50" @click="$emit('close')" />

    <div class="relative bg-white w-full sm:max-w-md sm:mx-4 sm:rounded-2xl rounded-t-2xl shadow-2xl p-4 pb-6 sm:p-6 max-h-[85vh] overflow-y-auto">

      <div class="flex items-center gap-2 mb-6">
        <template v-if="activeTab !== 'forgot'">
          <div class="flex flex-1 bg-gray-100 rounded-xl p-1">
            <button
              @click="activeTab = 'login'"
              :class="activeTab === 'login' ? 'bg-black text-white' : 'text-gray-500'"
              class="flex-1 py-2 rounded-lg font-semibold text-sm transition-all"
            >
              Iniciar sesión
            </button>
            <button
              @click="activeTab = 'register'"
              :class="activeTab === 'register' ? 'bg-black text-white' : 'text-gray-500'"
              class="flex-1 py-2 rounded-lg font-semibold text-sm transition-all"
            >
              Registrarme
            </button>
          </div>
        </template>
        <template v-else>
          <p class="flex-1 font-semibold text-gray-800 text-sm">Recuperar contraseña</p>
        </template>

        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600 transition-colors p-1 shrink-0"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <LoginForm v-if="activeTab === 'login'" @success="onLoginSuccess" @switch-to-register="activeTab = 'register'" @forgot-password="activeTab = 'forgot'" />
      <RegisterForm v-else-if="activeTab === 'register'" @success="activeTab = 'login'" @switch-to-login="activeTab = 'login'" />
      <ForgotPasswordForm v-else @back-to-login="activeTab = 'login'" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import LoginForm from './LoginForm.vue'
import RegisterForm from './RegisterForm.vue'
import ForgotPasswordForm from './ForgotPasswordForm.vue'

interface LoginSuccessPayload {
  token: string
  user: { id: number; name: string; lastname: string; email: string; role: string; isActive: boolean }
}

const emit = defineEmits<{ close: [] }>()
const activeTab = ref<'login' | 'register' | 'forgot'>('login')
const auth = useAuthStore()
const router = useRouter()

function onLoginSuccess(payload: LoginSuccessPayload) {
  auth.setAuth(payload.token, payload.user)
  emit('close')
  router.push('/home-user')
}
</script>
