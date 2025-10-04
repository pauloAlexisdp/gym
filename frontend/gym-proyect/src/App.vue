<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()

const isAuthPage = computed(() => route.path === '/iniciar-sesion' || route.path === '/registrarse')
</script>

<template>

  <div v-if="isAuthPage" class="min-h-screen">
    <NavbarSection />
    <RouterView />
  </div>


  <div v-else class="min-h-screen">
    <NavbarSection />
    <RouterView />
  </div>
</template>
