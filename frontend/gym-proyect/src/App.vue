<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router'
import { computed } from 'vue'
import NavbarSection from '@/components/common/NavbarSection.vue'
import AuthContainer from '@/components/auth/AuthContainer.vue'

const route = useRoute()

const isAuthPage = computed(() => route.path === '/iniciar-sesion' || route.path === '/registrarse')
</script>

<template>
  <div class="min-h-screen">
    <NavbarSection />

    <div v-if="isAuthPage">
      <AuthContainer />
    </div>


    <RouterView v-else />
  </div>
</template>
