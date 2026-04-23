<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="h-screen flex flex-col">
    <div class="flex-1 min-h-0 overflow-y-auto flex flex-col bg-gray-100 no-scrollbar">
      <RouterView />
    </div>
  </div>
</template>

<style>
.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { scrollbar-width: none; -ms-overflow-style: none; }
</style>
