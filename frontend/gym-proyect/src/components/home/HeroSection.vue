<template>
  <section class="bg-black text-white py-12 md:py-20 lg:py-32 px-4 md:px-8">
    <div class="max-w-4xl mx-auto text-center">
      <h2 class="text-3xl md:text-4xl lg:text-5xl xl:text-6xl font-bold mb-4 md:mb-6">{{ heroTitle }}</h2>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{ heroTitle: string }>()
</script>
