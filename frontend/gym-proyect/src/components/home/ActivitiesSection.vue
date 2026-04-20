<template>
  <section id="actividades" class="py-12 md:py-16 lg:py-20 px-4 md:px-8 lg:px-16 bg-white">
    <div class="max-w-6xl mx-auto">
      <h2 class="text-2xl md:text-3xl lg:text-4xl font-bold text-center mb-8 md:mb-12 text-gray-800">{{ activitiesTitle }}</h2>

      <div v-if="activities.length === 0" class="text-center text-gray-400 py-8">
        No hay actividades configuradas aún.
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 lg:gap-8">
        <div
          v-for="activity in activities"
          :key="activity.id"
          class="bg-gray-100 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-shadow"
        >
          <img
            v-if="activity.image"
            :src="activity.image"
            :alt="activity.title"
            class="w-full h-56 md:h-72 object-cover object-center"
          />
          <div v-else class="w-full h-56 md:h-72 bg-gray-200 flex items-center justify-center">
            <span class="text-gray-400 text-sm">Sin imagen</span>
          </div>

          <div class="p-4 md:p-6">
            <h3 class="text-lg md:text-xl font-bold mb-2 text-gray-800">{{ activity.title }}</h3>
            <p class="text-sm md:text-base text-gray-600">{{ activity.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
interface Activity {
  id: number
  title: string
  description: string
  image: string | null
}

defineProps<{ activitiesTitle: string; activities: Activity[] }>()
</script>
