<script setup lang="ts">
import { RouterView } from 'vue-router'
import FooterSection from '@/components/common/FooterSection.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <RouterView />
    <FooterSection />
  </div>
</template>
