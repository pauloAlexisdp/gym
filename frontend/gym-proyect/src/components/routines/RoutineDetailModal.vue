<template>
  <div class="fixed inset-0 bg-black/50 z-50 flex items-end sm:items-center justify-center p-0 sm:p-4">
    <div class="bg-white rounded-t-2xl sm:rounded-2xl shadow-xl w-full sm:max-w-lg max-h-[90vh] flex flex-col">

      <!-- Header -->
      <div class="flex items-center justify-between px-5 pt-5 pb-3 border-b border-gray-100 shrink-0">
        <!-- Vista detalle: botón volver -->
        <template v-if="selectedExercise">
          <button @click="selectedExercise = null" class="flex items-center gap-1 text-gray-500 hover:text-black transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            <span class="text-sm">Volver</span>
          </button>
          <h3 class="text-base font-bold text-gray-800 truncate mx-3 flex-1 text-center">{{ selectedExercise.name }}</h3>
          <div class="w-14" />
        </template>

        <!-- Vista lista -->
        <template v-else>
          <div v-if="!editingName" class="flex items-center gap-2">
            <h3 class="text-lg font-bold text-gray-800">{{ localName }}</h3>
            <button @click="editingName = true; nameInput = localName" class="text-gray-400 hover:text-black transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
            </button>
          </div>
          <div v-else class="flex items-center gap-2 flex-1 mr-3">
            <input v-model="nameInput" class="flex-1 px-2 py-1 border border-black rounded-lg text-sm font-semibold focus:outline-none" @keyup.enter="saveName" />
            <button @click="saveName" class="text-green-600 hover:text-green-800">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
            </button>
            <button @click="editingName = false" class="text-red-400 hover:text-red-600">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>
          <div class="flex items-center gap-2">
            <button @click="confirmDelete = true" class="text-red-400 hover:text-red-600 transition-colors p-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
            </button>
            <button @click="$emit('close')" class="text-gray-400 hover:text-black transition-colors p-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>
        </template>
      </div>

      <!-- VISTA: lista de ejercicios -->
      <div v-if="!selectedExercise" class="flex-1 overflow-hidden flex flex-col px-5 py-3">
        <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3 shrink-0">Ejercicios</p>

        <div v-if="exercises.length === 0" class="text-center py-6 text-gray-400 text-sm shrink-0">Sin ejercicios. Agrega uno.</div>

        <div v-else class="space-y-2 overflow-y-auto flex-1 pr-1 mb-3" @dragover.prevent @drop="onDrop">
          <div
            v-for="ex in exercises"
            :key="ex.id"
            class="flex items-center gap-3 bg-gray-50 rounded-xl px-3 py-3"
            :class="dragOverId === ex.id ? 'ring-2 ring-black' : ''"
            @dragenter.prevent="onDragEnter(ex)"
          >
            <div draggable="true" @dragstart="onDragStart(ex)" class="cursor-grab active:cursor-grabbing shrink-0 p-1 -m-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16" />
              </svg>
            </div>
            <div class="flex-1 min-w-0 cursor-pointer" @click="selectedExercise = ex">
              <p class="text-sm font-medium text-gray-800 truncate">{{ ex.name }}</p>
              <p class="text-xs text-gray-400">{{ ex.reps }} reps · {{ ex.weight ?? 0 }} kg</p>
            </div>
            <button @click="removeExercise(ex)" class="text-gray-300 hover:text-red-400 transition-colors shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>
        </div>

        <!-- Agregar ejercicio -->
        <div class="shrink-0">
          <button v-if="!showAddExercise" @click="loadUserExercises" class="w-full py-2.5 rounded-xl border-2 border-dashed border-gray-200 text-sm text-gray-400 hover:border-gray-400 hover:text-gray-600 transition-colors">
            + Agregar ejercicio
          </button>
          <div v-else class="space-y-2">
            <input v-model="exerciseSearch" type="text" placeholder="Buscar ejercicio..." class="w-full px-3 py-2 border border-gray-200 rounded-xl text-sm focus:outline-none focus:border-black transition-colors" />
            <div class="max-h-48 overflow-y-auto space-y-1">
              <button v-for="ue in filteredUserExercises" :key="ue.id" @click="addExercise(ue)" class="w-full text-left px-3 py-2 rounded-xl text-sm text-gray-700 hover:bg-gray-100 transition-colors">
                {{ ue.name }}
                <span class="text-gray-400 text-xs ml-1">{{ ue.reps }} reps · {{ ue.weight ?? 0 }} kg</span>
              </button>
              <p v-if="filteredUserExercises.length === 0" class="text-center text-gray-400 text-sm py-3">Sin resultados</p>
            </div>
            <button @click="showAddExercise = false; exerciseSearch = ''" class="text-xs text-gray-400 hover:text-gray-600">Cancelar</button>
          </div>
        </div>
      </div>

      <!-- VISTA: detalle del ejercicio -->
      <div v-else class="flex-1 overflow-y-auto px-5 py-4 space-y-4">
        <div>
          <span class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Músculo</span>
          <p class="text-gray-700 mt-1">{{ selectedExercise.muscle.charAt(0).toUpperCase() + selectedExercise.muscle.slice(1).toLowerCase() }}</p>
        </div>

        <div>
          <span class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Descripción</span>
          <p class="text-gray-600 mt-1 text-sm leading-relaxed">{{ selectedExercise.description }}</p>
        </div>

        <div class="flex items-center gap-3">
          <div class="flex-1">
            <span class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Repeticiones</span>
            <input v-model.number="editReps" type="number" min="0" :disabled="!editing"
              class="w-full mt-1 px-3 py-2 border rounded-lg text-gray-800 font-medium transition-colors"
              :class="editing ? 'border-black bg-white' : 'border-transparent bg-gray-100'" />
          </div>
          <div class="flex-1">
            <span class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Kg</span>
            <input v-model.number="editWeight" type="number" min="0" step="0.5" :disabled="!editing"
              class="w-full mt-1 px-3 py-2 border rounded-lg text-gray-800 font-medium transition-colors"
              :class="editing ? 'border-black bg-white' : 'border-transparent bg-gray-100'" />
          </div>
          <div class="flex flex-col items-center gap-2 pt-5">
            <button v-if="!editing" @click="startEdit" class="text-gray-400 hover:text-black transition-colors p-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
            </button>
            <template v-else>
              <button @click="saveExercise" :disabled="saving" class="text-green-600 hover:text-green-800 p-1">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
              </button>
              <button @click="cancelEdit" class="text-red-400 hover:text-red-600 p-1">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
              </button>
            </template>
          </div>
        </div>

        <div v-if="pr">
          <span class="text-xs font-semibold text-gray-400 uppercase tracking-wide">PR estimado (1RM)</span>
          <div class="flex items-center gap-2 mt-1">
            <p class="text-gray-600 text-sm">{{ pr }} kg</p>
            <img src="@/assets/strength-training.png" alt="PR" class="h-5 w-5 opacity-60" />
          </div>
        </div>

        <div>
          <button @click="showChart = !showChart" class="flex items-center gap-2 text-sm font-semibold text-gray-500 hover:text-black transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
            {{ showChart ? 'Ocultar progreso' : 'Ver progreso' }}
          </button>
          <div v-if="showChart" class="mt-3">
            <ExerciseHistoryChart :user-exercise-id="selectedExercise.user_exercise_id" />
          </div>
        </div>

        <div v-if="embedUrl">
          <span class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Video tutorial</span>
          <div class="mt-2 rounded-xl overflow-hidden aspect-video">
            <iframe :src="embedUrl" class="w-full h-full" allowfullscreen />
          </div>
        </div>
      </div>
    </div>

    <!-- Confirm delete -->
    <div v-if="confirmDelete" class="fixed inset-0 bg-black/60 z-60 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-xl p-6 w-full max-w-xs text-center">
        <p class="font-semibold text-gray-800 mb-2">¿Eliminar rutina?</p>
        <p class="text-sm text-gray-400 mb-5">Esta acción no se puede deshacer.</p>
        <div class="flex gap-2">
          <button @click="confirmDelete = false" class="flex-1 py-2 rounded-xl border border-gray-200 text-sm text-gray-600 hover:bg-gray-50">Cancelar</button>
          <button @click="deleteRoutine" class="flex-1 py-2 rounded-xl bg-red-500 text-white text-sm font-medium hover:bg-red-600">Eliminar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useApi } from '@/composables/useApi'
import type { Routine, RoutineExercise } from '@/views/RoutinesView.vue'
import ExerciseHistoryChart from '@/components/exercises/ExerciseHistoryChart.vue'

const props = defineProps<{ routine: Routine }>()
const emit = defineEmits<{
  close: []
  updated: [routine: Routine]
  deleted: [id: number]
}>()

const { apiFetch } = useApi()
const exercises = ref<RoutineExercise[]>([...props.routine.exercises])
const localName = ref(props.routine.name)
const editingName = ref(false)
const nameInput = ref(props.routine.name)
const confirmDelete = ref(false)
const showAddExercise = ref(false)
const exerciseSearch = ref('')
const dragItem = ref<RoutineExercise | null>(null)
const dragOverId = ref<number | null>(null)

const selectedExercise = ref<RoutineExercise | null>(null)
const editing = ref(false)
const saving = ref(false)
const showChart = ref(false)
const editReps = ref(0)
const editWeight = ref(0)

watch(selectedExercise, (ex) => {
  if (ex) {
    editReps.value = ex.reps
    editWeight.value = ex.weight ?? 0
    editing.value = false
    showChart.value = false
  }
})

const pr = computed(() => {
  const w = editWeight.value
  const r = editReps.value
  if (!w || !r || r <= 0) return null
  return (w * (1 + r / 30)).toFixed(1)
})

const embedUrl = computed(() => {
  const url = selectedExercise.value?.video_tutorial
  if (!url) return null
  const ytMatch = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/shorts\/)([a-zA-Z0-9_-]+)/)
  if (ytMatch) return `https://www.youtube.com/embed/${ytMatch[1]}`
  const driveMatch = url.match(/drive\.google\.com\/file\/d\/([a-zA-Z0-9_-]+)/)
  if (driveMatch) return `https://drive.google.com/file/d/${driveMatch[1]}/preview`
  return null
})

function startEdit() {
  editing.value = true
}

function cancelEdit() {
  if (selectedExercise.value) {
    editReps.value = selectedExercise.value.reps
    editWeight.value = selectedExercise.value.weight ?? 0
  }
  editing.value = false
}

async function saveExercise() {
  if (!selectedExercise.value) return
  saving.value = true
  try {
    const data = await apiFetch(
      `${import.meta.env.VITE_API_URL}/api/exercises/user-exercise/${selectedExercise.value.user_exercise_id}/`,
      { method: 'PATCH', body: JSON.stringify({ reps: editReps.value, weight: editWeight.value }) }
    )
    if (data) {
      const idx = exercises.value.findIndex(e => e.id === selectedExercise.value!.id)
      if (idx !== -1) {
        const ex = exercises.value[idx]
        if (ex) { ex.reps = data.reps; ex.weight = data.weight }
      }
      selectedExercise.value = { ...selectedExercise.value, reps: data.reps, weight: data.weight }
      editing.value = false
      emitUpdated()
    }
  } finally {
    saving.value = false
  }
}

interface UserExerciseOption { id: number; name: string; reps: number; weight: number | null }
const userExercises = ref<UserExerciseOption[]>([])

const filteredUserExercises = computed(() => {
  const q = exerciseSearch.value.toLowerCase()
  const existingIds = new Set(exercises.value.map(e => e.user_exercise_id))
  return userExercises.value.filter(ue => !existingIds.has(ue.id) && ue.name.toLowerCase().includes(q))
})

async function loadUserExercises() {
  showAddExercise.value = true
  if (userExercises.value.length > 0) return
  const all = await apiFetch(`${import.meta.env.VITE_API_URL}/api/exercises/user-exercises/`)
  if (all) userExercises.value = all
}

async function addExercise(ue: UserExerciseOption) {
  const data = await apiFetch(`${import.meta.env.VITE_API_URL}/api/exercises/routines/${props.routine.id}/exercises/`, {
    method: 'POST',
    body: JSON.stringify({ user_exercise_id: ue.id }),
  })
  if (data) { exercises.value.push(data); emitUpdated() }
  showAddExercise.value = false
  exerciseSearch.value = ''
}

async function removeExercise(ex: RoutineExercise) {
  await apiFetch(`${import.meta.env.VITE_API_URL}/api/exercises/routines/${props.routine.id}/exercises/${ex.id}/`, { method: 'DELETE' })
  exercises.value = exercises.value.filter(e => e.id !== ex.id)
  emitUpdated()
}

async function saveName() {
  const data = await apiFetch(`${import.meta.env.VITE_API_URL}/api/exercises/routines/${props.routine.id}/`, {
    method: 'PATCH', body: JSON.stringify({ name: nameInput.value }),
  })
  if (data) { localName.value = nameInput.value; editingName.value = false; emitUpdated() }
}

async function deleteRoutine() {
  await apiFetch(`${import.meta.env.VITE_API_URL}/api/exercises/routines/${props.routine.id}/`, { method: 'DELETE' })
  emit('deleted', props.routine.id)
}

function onDragStart(ex: RoutineExercise) { dragItem.value = ex }
function onDragEnter(ex: RoutineExercise) { dragOverId.value = ex.id }

async function onDrop() {
  if (!dragItem.value || dragOverId.value === null) return
  const from = exercises.value.findIndex(e => e.id === dragItem.value!.id)
  const to = exercises.value.findIndex(e => e.id === dragOverId.value)
  if (from === to) { dragItem.value = null; dragOverId.value = null; return }
  const reordered = [...exercises.value]
  const [item] = reordered.splice(from, 1)
  if (item) reordered.splice(to, 0, item)
  exercises.value = reordered.map((e, i) => ({ ...e, order: i }))
  await apiFetch(`${import.meta.env.VITE_API_URL}/api/exercises/routines/${props.routine.id}/reorder/`, {
    method: 'POST', body: JSON.stringify({ order: exercises.value.map(e => e.id) }),
  })
  dragItem.value = null; dragOverId.value = null
  emitUpdated()
}

function emitUpdated() {
  emit('updated', { ...props.routine, name: localName.value, exercises: [...exercises.value] })
}
</script>
