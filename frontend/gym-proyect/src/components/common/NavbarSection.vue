<template>
  <nav class="sticky top-0 z-40 bg-black shadow-lg">
    <div class="h-16 sm:h-20 flex items-center justify-between px-4 sm:px-6 lg:px-8">

      <!-- Logo -->
      <div class="flex items-center shrink-0">
        <img
          src="/logo_sr_powergym.png"
          alt="SR POWER GYM"
          class="h-8 w-8 sm:h-10 sm:w-10 mr-2 sm:mr-3 rounded-full object-cover"
        />
        <h1 class="text-white text-lg sm:text-xl font-bold">SR Power Gym</h1>
      </div>

      <!-- Links + acciones -->
      <div class="flex items-center gap-1 sm:gap-2">
        <template v-if="auth.isLoggedIn">
          <RouterLink
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="px-3 sm:px-5 py-1 text-sm font-medium transition-colors border-b-2"
            :class="isActive(link.to) ? 'text-white border-white' : 'text-white/70 border-transparent hover:text-white'"
          >
            {{ link.label }}
          </RouterLink>

          <div class="flex items-center gap-2 ml-3 pl-3 border-l border-white/20">
            <button @click="router.push('/profile')" class="shrink-0" title="Mi perfil">
              <img
                v-if="auth.user?.profile_picture"
                :src="auth.user.profile_picture"
                alt="Perfil"
                class="h-8 w-8 rounded-full object-cover ring-2 ring-white/30 hover:ring-white transition-all"
              />
              <div
                v-else
                class="h-8 w-8 rounded-full bg-gray-600 hover:bg-gray-500 flex items-center justify-center ring-2 ring-white/30 hover:ring-white transition-all"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
            </button>
            <button @click="handleLogout" class="text-white/70 hover:text-red-400 transition-colors p-1" title="Cerrar sesión">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>
        </template>

        <template v-else>
          <RouterLink
            v-for="link in publicLinks"
            :key="link.to"
            :to="link.to"
            class="px-3 sm:px-5 py-1 text-sm font-medium transition-colors border-b-2"
            :class="isActive(link.to) ? 'text-white border-white' : 'text-white/70 border-transparent hover:text-white'"
          >
            {{ link.label }}
          </RouterLink>

          <button
            @click="$emit('open-modal')"
            class="ml-3 text-sm font-medium text-white/70 hover:text-white transition-colors"
          >
            Iniciar sesión
          </button>
        </template>
      </div>

    </div>
  </nav>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'

defineEmits<{ 'open-modal': [] }>()

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const navLinks = [
  { to: '/inicio', label: 'Inicio' },
  { to: '/ejercicios', label: 'Ejercicios' },
  { to: '/planes', label: 'Planes' },
  { to: '/contactenos', label: 'Contáctenos' },
]

const publicLinks = [
  { to: '/planes', label: 'Planes' },
  { to: '/contactenos', label: 'Contáctenos' },
]

function isActive(path: string) {
  return route.path === path || route.path.startsWith(path + '/')
}

function handleLogout() {
  auth.logout()
  router.push('/')
}
</script>
