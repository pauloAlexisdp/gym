<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()

// Determinar si estamos en páginas de autenticación (login o register)
const isAuthPage = computed(() => route.path === '/login' || route.path === '/register')
</script>

<template>
  <!-- Layout para páginas de autenticación (sin navbar ni contenedor principal) -->
  <div v-if="isAuthPage" class="min-h-screen">
    <RouterView />
  </div>

  <!-- Layout normal para otras páginas -->
  <div v-else class="min-h-screen">
    <RouterView />
  </div>
</template>

<!-- Estilos manejados por Tailwind CSS -->
