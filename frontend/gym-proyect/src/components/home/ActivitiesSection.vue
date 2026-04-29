<template>
  <section id="actividades" class="py-12 md:py-16 lg:py-20 bg-white overflow-hidden">
    <div class="max-w-6xl mx-auto px-4 md:px-8 lg:px-16">
      <h2 class="text-2xl md:text-3xl lg:text-4xl font-bold text-center mb-8 md:mb-12 text-gray-800">
        {{ activitiesTitle }}
      </h2>

      <div v-if="activities.length === 0" class="text-center text-gray-400 py-8">
        No hay actividades configuradas aún.
      </div>

      <div v-else class="relative">
        <!-- Botón izquierda -->
        <button
          v-if="activities.length > visibleCount"
          @click="prev"
          class="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-3 z-10 bg-white border border-gray-200 shadow-md rounded-full w-10 h-10 flex items-center justify-center hover:bg-gray-50 transition-colors"
          :class="{ 'opacity-30 cursor-default': currentIndex === 0 }"
        >
          <svg class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
        </button>

        <!-- Track del carrusel -->
        <div
          ref="trackRef"
          class="flex gap-6 overflow-x-auto scroll-smooth snap-x snap-mandatory pb-4 cursor-grab active:cursor-grabbing select-none"
          style="scrollbar-width: none; -ms-overflow-style: none;"
          @mousedown="onDragStart"
          @mousemove="onDragMove"
          @mouseup="onDragEnd"
          @mouseleave="onDragEnd"
          @scroll.passive="onScroll"
        >
          <div
            v-for="activity in activities"
            :key="activity.id"
            class="flex-shrink-0 snap-start bg-gray-100 rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow"
            :style="{ width: cardWidth }"
          >
            <img
              v-if="activity.image"
              :src="activity.image"
              :alt="activity.title"
              class="w-full h-56 md:h-64 object-cover object-center pointer-events-none"
            />
            <div v-else class="w-full h-56 md:h-64 bg-gray-200 flex items-center justify-center">
              <span class="text-gray-400 text-sm">Sin imagen</span>
            </div>
            <div class="p-4 md:p-6">
              <h3 class="text-lg md:text-xl font-bold mb-2 text-gray-800">{{ activity.title }}</h3>
              <p class="text-sm md:text-base text-gray-600">{{ activity.description }}</p>
            </div>
          </div>
        </div>

        <!-- Botón derecha -->
        <button
          v-if="activities.length > visibleCount"
          @click="next"
          class="absolute right-0 top-1/2 -translate-y-1/2 translate-x-3 z-10 bg-white border border-gray-200 shadow-md rounded-full w-10 h-10 flex items-center justify-center hover:bg-gray-50 transition-colors"
          :class="{ 'opacity-30 cursor-default': currentIndex >= activities.length - visibleCount }"
        >
          <svg class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
          </svg>
        </button>

        <!-- Dots -->
        <div v-if="activities.length > visibleCount" class="flex justify-center gap-2 mt-4">
          <button
            v-for="i in dotCount"
            :key="i"
            @click="goTo(i - 1)"
            class="w-2.5 h-2.5 rounded-full transition-colors"
            :class="currentIndex === i - 1 ? 'bg-gray-800' : 'bg-gray-300'"
          />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

interface Activity {
  id: number
  title: string
  description: string
  image: string | null
}

const props = defineProps<{ activitiesTitle: string; activities: Activity[] }>()

const trackRef = ref<HTMLElement | null>(null)
const currentIndex = ref(0)
const windowWidth = ref(window.innerWidth)

const visibleCount = computed(() => {
  if (windowWidth.value >= 1024) return 3
  if (windowWidth.value >= 640) return 2
  return 1
})

const cardWidth = computed(() => {
  if (windowWidth.value >= 1024) return 'calc(33.333% - 16px)'
  if (windowWidth.value >= 640) return 'calc(50% - 12px)'
  return '85%'
})

const dotCount = computed(() => Math.max(0, props.activities.length - visibleCount.value + 1))

function scrollToIndex(index: number) {
  if (!trackRef.value) return
  const card = trackRef.value.children[index] as HTMLElement
  if (card) {
    trackRef.value.scrollTo({ left: card.offsetLeft, behavior: 'smooth' })
  }
  currentIndex.value = index
}

function prev() {
  if (currentIndex.value > 0) scrollToIndex(currentIndex.value - 1)
}

function next() {
  if (currentIndex.value < props.activities.length - visibleCount.value)
    scrollToIndex(currentIndex.value + 1)
}

function goTo(i: number) {
  scrollToIndex(i)
}

// Drag (mouse)
let isDragging = false
let dragStartX = 0
let scrollStartX = 0

function onDragStart(e: MouseEvent) {
  isDragging = true
  dragStartX = e.clientX
  scrollStartX = trackRef.value?.scrollLeft ?? 0
}

function onDragMove(e: MouseEvent) {
  if (!isDragging || !trackRef.value) return
  trackRef.value.scrollLeft = scrollStartX - (e.clientX - dragStartX)
}

function onDragEnd() {
  if (!isDragging) return
  isDragging = false
  snapToNearest()
}

function onScroll() {
  if (!trackRef.value || props.activities.length === 0) return
  const card = trackRef.value.children[0] as HTMLElement | undefined
  if (!card) return
  const cardW = card.offsetWidth + 24
  const nearest = Math.round(trackRef.value.scrollLeft / cardW)
  currentIndex.value = Math.max(0, Math.min(nearest, props.activities.length - 1))
}

function snapToNearest() {
  if (!trackRef.value || props.activities.length === 0) return
  const card = trackRef.value.children[0] as HTMLElement | undefined
  if (!card) return
  const cardW = card.offsetWidth + 24 // gap-6 = 24px
  const nearest = Math.round(trackRef.value.scrollLeft / cardW)
  const clamped = Math.max(0, Math.min(nearest, props.activities.length - 1))
  currentIndex.value = clamped
  trackRef.value.scrollTo({ left: clamped * cardW, behavior: 'smooth' })
}

function onResize() {
  windowWidth.value = window.innerWidth
}

onMounted(() => window.addEventListener('resize', onResize))
onUnmounted(() => window.removeEventListener('resize', onResize))
</script>

<style scoped>
div::-webkit-scrollbar {
  display: none;
}
</style>
