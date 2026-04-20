<template>
  <div class="fixed inset-0 z-30 flex justify-end">
    <div class="absolute inset-0 bg-black/50" @click="$emit('close')" />

    <div class="relative bg-white w-full sm:w-1/2 flex flex-col shadow-2xl overflow-y-auto mt-16 sm:mt-20 lg:mt-24" style="height: calc(100vh - 4rem)">
      <div class="flex items-start justify-between px-6 pt-6 pb-4 border-b border-gray-100">
        <h3 class="font-bold text-gray-800 text-xl leading-tight pr-2">{{ exercise.name }}</h3>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 transition-colors shrink-0">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="flex flex-col px-6 py-5 pb-12 space-y-5">

        <div>
          <span class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Músculo</span>
          <p class="text-gray-700 mt-1">{{ exercise.muscle.charAt(0).toUpperCase() + exercise.muscle.slice(1).toLowerCase() }}</p>
        </div>

        <div>
          <span class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Descripción</span>
          <p class="text-gray-600 mt-1 text-sm leading-relaxed">{{ exercise.description }}</p>
        </div>

        <div class="flex items-center gap-3">
          <div class="flex-1">
            <span class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Repeticiones</span>
            <input
              v-model.number="editReps"
              type="number"
              min="0"
              :disabled="!editing"
              class="w-full mt-1 px-3 py-2 border rounded-lg text-gray-800 font-medium transition-colors"
              :class="editing ? 'border-black bg-white' : 'border-transparent bg-gray-100'"
            />
          </div>

          <div class="flex-1">
            <span class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Kg</span>
            <input
              v-model.number="editWeight"
              type="number"
              min="0"
              step="0.5"
              :disabled="!editing"
              class="w-full mt-1 px-3 py-2 border rounded-lg text-gray-800 font-medium transition-colors"
              :class="editing ? 'border-black bg-white' : 'border-transparent bg-gray-100'"
            />
          </div>

          <div class="flex flex-col items-center gap-2 pt-5">
            <button
              v-if="!editing"
              @click="editing = true"
              class="text-gray-400 hover:text-black transition-colors p-1"
              title="Editar"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
            </button>
            <template v-else>
              <button @click="save" :disabled="saving" class="text-green-600 hover:text-green-800 transition-colors p-1" title="Guardar">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </button>
              <button @click="cancel" class="text-red-400 hover:text-red-600 transition-colors p-1" title="Cancelar">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </template>
          </div>
        </div>

        <div v-if="pr">
          <span class="text-xs font-semibold text-gray-400 uppercase tracking-wide">PR estimado (1RM)</span>
          <div class="flex items-center gap-2 mt-1">
            <p class="text-gray-600 text-sm leading-relaxed">{{ pr }} kg</p>
            <img src="@/assets/strength-training.png" alt="PR" class="h-6 w-6 shrink-0 opacity-60" />
          </div>
        </div>

        <div>
          <button
            @click="showChart = !showChart"
            class="flex items-center gap-2 text-sm font-semibold text-gray-500 hover:text-black transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            {{ showChart ? 'Ocultar progreso' : 'Ver progreso' }}
          </button>
          <div v-if="showChart" class="mt-3">
            <ExerciseHistoryChart ref="chartRef" :user-exercise-id="exercise.user_exercise_id" />
          </div>
        </div>

        <div v-if="embedUrl">
          <span class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Video tutorial</span>
          <div class="mt-2 rounded-xl overflow-hidden aspect-video">
            <iframe
              :src="embedUrl"
              class="w-full h-full"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, type ComponentPublicInstance } from 'vue'
import { useAuthStore } from '@/stores/auth.store'
import type { Exercise } from '@/views/ExerciseListView.vue'
import ExerciseHistoryChart from './ExerciseHistoryChart.vue'

const props = defineProps<{ exercise: Exercise }>()
const emit = defineEmits<{
  close: []
  updated: [payload: { reps: number; weight: number }]
}>()

const auth = useAuthStore()
const chartRef = ref<{ refresh: () => void } | null>(null)
const editing = ref(false)
const showChart = ref(false)
const saving = ref(false)
const editReps = ref(props.exercise.reps)
const editWeight = ref(props.exercise.weight ?? 0)

function cancel() {
  editReps.value = props.exercise.reps
  editWeight.value = props.exercise.weight ?? 0
  editing.value = false
}

async function save() {
  saving.value = true
  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/api/exercises/user-exercise/${props.exercise.user_exercise_id}/`,
      {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${auth.token}`,
        },
        body: JSON.stringify({ reps: editReps.value, weight: editWeight.value }),
      }
    )
    if (response.ok) {
      const data = await response.json()
      emit('updated', { reps: data.reps, weight: data.weight })
      editing.value = false
      chartRef.value?.refresh()
    }
  } finally {
    saving.value = false
  }
}

const pr = computed(() => {
  const w = editWeight.value
  const r = editReps.value
  if (!w || !r || r <= 0) return null
  return (w * (1 + r / 30)).toFixed(1)
})

const embedUrl = computed(() => {
  const url = props.exercise.video_tutorial
  if (!url) return null

  const ytMatch = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/shorts\/)([a-zA-Z0-9_-]+)/)
  if (ytMatch) return `https://www.youtube.com/embed/${ytMatch[1]}`

  const driveMatch = url.match(/drive\.google\.com\/file\/d\/([a-zA-Z0-9_-]+)/)
  if (driveMatch) return `https://drive.google.com/file/d/${driveMatch[1]}/preview`

  return null
})
</script>
