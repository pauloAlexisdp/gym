<template>
  <nav class="sticky top-0 z-40 bg-black h-16 sm:h-20 lg:h-24 flex items-center justify-between px-4 sm:px-6 lg:px-8 shadow-lg">
    <div class="flex items-center">
      <img
        src="/logo_sr_powergym.png"
        alt="SR POWER GYM"
        class="h-8 w-8 sm:h-10 sm:w-10 lg:h-12 lg:w-12 mr-2 sm:mr-3 rounded-full object-cover"
      />
      <h1 class="text-white text-lg sm:text-xl lg:text-2xl xl:text-3xl font-bold">
        Sr Power Gym
      </h1>
    </div>

    <button
      v-if="!auth.isLoggedIn"
      @click="$emit('open-modal')"
      class="text-white hover:text-gray-300 transition-colors p-1 sm:p-2"
      title="Iniciar sesión"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 lg:h-7 lg:w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
      </svg>
    </button>

    <div v-else class="flex items-center gap-2 sm:gap-3">
      <button @click="router.push('/profile')" class="shrink-0" title="Mi perfil">
        <img
          v-if="auth.user?.profile_picture"
          :src="auth.user.profile_picture"
          alt="Perfil"
          class="h-8 w-8 sm:h-9 sm:w-9 rounded-full object-cover ring-2 ring-white/30 hover:ring-white transition-all"
        />
        <div
          v-else
          class="h-8 w-8 sm:h-9 sm:w-9 rounded-full bg-gray-600 hover:bg-gray-500 flex items-center justify-center ring-2 ring-white/30 hover:ring-white transition-all"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
      </button>

      <button @click="handleLogout" class="text-white hover:text-red-400 transition-colors p-1 sm:p-2" title="Cerrar sesión">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 lg:h-7 lg:w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
        </svg>
      </button>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'

defineEmits<{ 'open-modal': [] }>()

const auth = useAuthStore()
const router = useRouter()

function handleLogout() {
  auth.logout()
  router.push('/')
}
</script>
