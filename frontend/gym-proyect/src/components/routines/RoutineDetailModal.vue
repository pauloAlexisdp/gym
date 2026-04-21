<template>
  <div class="fixed inset-0 bg-black/50 z-50 flex items-end sm:items-center justify-center p-0 sm:p-4">
    <div class="bg-white rounded-t-2xl sm:rounded-2xl shadow-xl w-full sm:max-w-lg max-h-[90vh] flex flex-col">

      <!-- Header -->
      <div class="flex items-center justify-between px-5 pt-5 pb-3 border-b border-gray-100">
        <div v-if="!editingName" class="flex items-center gap-2">
          <h3 class="text-lg font-bold text-gray-800">{{ routine.name }}</h3>
          <button @click="editingName = true; nameInput = routine.name" class="text-gray-400 hover:text-black transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
            </svg>
          </button>
        </div>
        <div v-else class="flex items-center gap-2 flex-1 mr-3">
          <input
            v-model="nameInput"
            class="flex-1 px-2 py-1 border border-black rounded-lg text-sm font-semibold focus:outline-none"
            @keyup.enter="saveName"
          />
          <button @click="saveName" class="text-green-600 hover:text-green-800">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </button>
          <button @click="editingName = false" class="text-red-400 hover:text-red-600">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="flex items-center gap-2">
          <button @click="confirmDelete = true" class="text-red-400 hover:text-red-600 transition-colors p-1" title="Eliminar rutina">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
          <button @click="$emit('close')" class="text-gray-400 hover:text-black transition-colors p-1">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Ejercicios -->
      <div class="flex-1 overflow-y-auto px-5 py-3">
        <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3">Ejercicios</p>

        <div v-if="exercises.length === 0" class="text-center py-6 text-gray-400 text-sm">
          Sin ejercicios. Agrega uno.
        </div>

        <div
          v-else
          class="space-y-2"
          @dragover.prevent
          @drop="onDrop"
        >
          <div
            v-for="ex in exercises"
            :key="ex.id"
            draggable="true"
            @dragstart="onDragStart(ex)"
            @dragenter.prevent="onDragEnter(ex)"
            class="flex items-center gap-3 bg-gray-50 rounded-xl px-3 py-3 cursor-grab active:cursor-grabbing select-none"
            :class="dragOverId === ex.id ? 'ring-2 ring-black' : ''"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-300 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16" />
            </svg>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-800 truncate">{{ ex.name }}</p>
              <p class="text-xs text-gray-400">{{ ex.reps }} reps · {{ ex.weight ?? 0 }} kg</p>
            </div>
            <button @click="removeExercise(ex)" class="text-gray-300 hover:text-red-400 transition-colors shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Agregar ejercicio -->
        <div class="mt-4">
          <button
            v-if="!showAddExercise"
            @click="loadUserExercises"
            class="w-full py-2.5 rounded-xl border-2 border-dashed border-gray-200 text-sm text-gray-400 hover:border-gray-400 hover:text-gray-600 transition-colors"
          >
            + Agregar ejercicio
          </button>

          <div v-else class="space-y-2">
            <input
              v-model="exerciseSearch"
              type="text"
              placeholder="Buscar ejercicio..."
              class="w-full px-3 py-2 border border-gray-200 rounded-xl text-sm focus:outline-none focus:border-black transition-colors"
            />
            <div class="max-h-48 overflow-y-auto space-y-1">
              <button
                v-for="ue in filteredUserExercises"
                :key="ue.id"
                @click="addExercise(ue)"
                class="w-full text-left px-3 py-2 rounded-xl text-sm text-gray-700 hover:bg-gray-100 transition-colors"
              >
                {{ ue.name }}
                <span class="text-gray-400 text-xs ml-1">{{ ue.reps }} reps · {{ ue.weight ?? 0 }} kg</span>
              </button>
              <p v-if="filteredUserExercises.length === 0" class="text-center text-gray-400 text-sm py-3">Sin resultados</p>
            </div>
            <button @click="showAddExercise = false; exerciseSearch = ''" class="text-xs text-gray-400 hover:text-gray-600">Cancelar</button>
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
import { ref, computed } from 'vue'
import { useApi } from '@/composables/useApi'
import type { Routine, RoutineExercise } from '@/views/RoutinesView.vue'

const props = defineProps<{ routine: Routine }>()
const emit = defineEmits<{
  close: []
  updated: [routine: Routine]
  deleted: [id: number]
}>()

const { apiFetch } = useApi()
const exercises = ref<RoutineExercise[]>([...props.routine.exercises])
const editingName = ref(false)
const nameInput = ref(props.routine.name)
const confirmDelete = ref(false)
const showAddExercise = ref(false)
const exerciseSearch = ref('')
const dragItem = ref<RoutineExercise | null>(null)
const dragOverId = ref<number | null>(null)

interface UserExerciseOption {
  id: number
  name: string
  reps: number
  weight: number | null
}
const userExercises = ref<UserExerciseOption[]>([])

const filteredUserExercises = computed(() => {
  const q = exerciseSearch.value.toLowerCase()
  const existingIds = new Set(exercises.value.map(e => e.user_exercise_id))
  return userExercises.value.filter(ue =>
    !existingIds.has(ue.id) &&
    ue.name.toLowerCase().includes(q)
  )
})

async function loadUserExercises() {
  showAddExercise.value = true
  if (userExercises.value.length > 0) return
  const data = await apiFetch(`${import.meta.env.VITE_API_URL}/api/exercises/routines/${props.routine.id}/`)
  // Fetch all user exercises via a general endpoint
  const all = await apiFetch(`${import.meta.env.VITE_API_URL}/api/exercises/user-exercises/`)
  if (all) userExercises.value = all
}

async function addExercise(ue: UserExerciseOption) {
  const data = await apiFetch(`${import.meta.env.VITE_API_URL}/api/exercises/routines/${props.routine.id}/exercises/`, {
    method: 'POST',
    body: JSON.stringify({ user_exercise_id: ue.id }),
  })
  if (data) {
    exercises.value.push(data)
    emitUpdated()
  }
  showAddExercise.value = false
  exerciseSearch.value = ''
}

async function removeExercise(ex: RoutineExercise) {
  await apiFetch(`${import.meta.env.VITE_API_URL}/api/exercises/routines/${props.routine.id}/exercises/${ex.id}/`, {
    method: 'DELETE',
  })
  exercises.value = exercises.value.filter(e => e.id !== ex.id)
  emitUpdated()
}

async function saveName() {
  const data = await apiFetch(`${import.meta.env.VITE_API_URL}/api/exercises/routines/${props.routine.id}/`, {
    method: 'PATCH',
    body: JSON.stringify({ name: nameInput.value }),
  })
  if (data) {
    editingName.value = false
    emitUpdated(nameInput.value)
  }
}

async function deleteRoutine() {
  await apiFetch(`${import.meta.env.VITE_API_URL}/api/exercises/routines/${props.routine.id}/`, {
    method: 'DELETE',
  })
  emit('deleted', props.routine.id)
}

function onDragStart(ex: RoutineExercise) {
  dragItem.value = ex
}

function onDragEnter(ex: RoutineExercise) {
  dragOverId.value = ex.id
}

async function onDrop() {
  if (!dragItem.value || dragOverId.value === null) return
  const from = exercises.value.findIndex(e => e.id === dragItem.value!.id)
  const to = exercises.value.findIndex(e => e.id === dragOverId.value)
  if (from === to) return

  const reordered = [...exercises.value]
  const [item] = reordered.splice(from, 1)
  if (item) reordered.splice(to, 0, item)
  exercises.value = reordered.map((e, i) => ({ ...e, order: i }))

  await apiFetch(`${import.meta.env.VITE_API_URL}/api/exercises/routines/${props.routine.id}/reorder/`, {
    method: 'POST',
    body: JSON.stringify({ order: exercises.value.map(e => e.id) }),
  })

  dragItem.value = null
  dragOverId.value = null
  emitUpdated()
}

function emitUpdated(name?: string) {
  emit('updated', {
    ...props.routine,
    name: name ?? props.routine.name,
    exercises: [...exercises.value],
  })
}
</script>
