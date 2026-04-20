<template>
  <section id="quienes-somos" class="py-12 md:py-16 lg:py-20 px-4 md:px-8 lg:px-16">
    <div class="max-w-4xl mx-auto">
      <h2 class="text-2xl md:text-3xl lg:text-4xl font-bold text-center mb-6 md:mb-8 text-gray-800">{{ aboutTitle }}</h2>
      <div class="bg-white rounded-lg shadow-lg p-6 md:p-8 lg:p-10">
        <p class="text-sm md:text-base lg:text-lg text-gray-700 leading-relaxed whitespace-pre-line">{{ aboutDescription }}</p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{ aboutTitle: string; aboutDescription: string }>()
</script>
