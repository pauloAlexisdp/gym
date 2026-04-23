<template>
  <div class="flex-1 min-h-0 flex flex-col bg-gray-100">
    <NavbarSection />

    <main class="flex-1 min-h-0 flex flex-col px-4 pt-10 pb-4 sm:px-8 max-w-2xl mx-auto w-full">
      <p class="text-sm text-gray-400 mb-3 shrink-0">Bienvenido, <span class="font-semibold text-gray-600">{{ auth.user?.name }}</span></p>
      <div class="flex items-center justify-between mb-6 shrink-0">
        <h2 class="text-2xl font-bold text-gray-800">Mis Rutinas</h2>
        <button
          @click="showCreateModal = true"
          class="bg-black text-white text-sm font-medium px-4 py-2 rounded-xl hover:bg-gray-800 transition-colors"
        >
          + Nueva rutina
        </button>
      </div>

      <div v-if="loading" class="text-center py-12 text-gray-400">Cargando...</div>

      <div v-else-if="routines.length === 0" class="text-center py-12 text-gray-400">
        No tienes rutinas aún. ¡Crea una!
      </div>

      <div v-else class="flex-1 min-h-0 overflow-y-auto no-scrollbar space-y-3">
        <div
          v-for="day in daysWithRoutines"
          :key="day.value"
          class="space-y-2"
        >
          <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide px-1">{{ day.label }}</p>
          <div
            v-for="routine in routinesByDay(day.value)"
            :key="routine.id"
            class="bg-white rounded-2xl shadow p-4 cursor-pointer hover:shadow-md transition-shadow"
            @click="selectedRoutine = routine"
          >
            <div class="flex items-center justify-between">
              <div>
                <p class="font-semibold text-gray-800">{{ routine.name }}</p>
                <p class="text-sm text-gray-400 mt-0.5">{{ routine.exercises.length }} ejercicio{{ routine.exercises.length !== 1 ? 's' : '' }}</p>
              </div>
              <div class="flex items-center gap-3">
                <button
                  @click.stop="routineToDelete = routine"
                  class="text-gray-300 hover:text-red-400 transition-colors p-1"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal crear rutina -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-sm p-6">
        <h3 class="text-lg font-bold text-gray-800 mb-4">Nueva rutina</h3>
        <div class="space-y-3">
          <div>
            <label class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Nombre</label>
            <input
              v-model="newRoutine.name"
              type="text"
              placeholder="Ej: Rutina pecho"
              class="mt-1 w-full px-3 py-2 border border-gray-200 rounded-xl text-sm focus:outline-none focus:border-black transition-colors"
            />
          </div>
          <div>
            <label class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Día</label>
            <select
              v-model="newRoutine.day"
              class="mt-1 w-full px-3 py-2 border border-gray-200 rounded-xl text-sm focus:outline-none focus:border-black transition-colors bg-white"
            >
              <option value="" disabled>Selecciona un día</option>
              <option v-for="d in days" :key="d.value" :value="d.value">{{ d.label }}</option>
            </select>
          </div>
        </div>
        <div class="flex gap-2 mt-5">
          <button @click="showCreateModal = false; resetNewRoutine()" class="flex-1 py-2 rounded-xl border border-gray-200 text-sm text-gray-600 hover:bg-gray-50">Cancelar</button>
          <button @click="createRoutine" :disabled="!newRoutine.name || !newRoutine.day" class="flex-1 py-2 rounded-xl bg-black text-white text-sm font-medium hover:bg-gray-800 disabled:opacity-40 transition-colors">Crear</button>
        </div>
      </div>
    </div>

    <!-- Modal confirmación eliminar -->
    <div v-if="routineToDelete" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-sm p-6">
        <h3 class="text-lg font-bold text-gray-800 mb-2">Eliminar rutina</h3>
        <p class="text-sm text-gray-500 mb-5">¿Estás seguro que deseas eliminar <span class="font-semibold text-gray-800">{{ routineToDelete.name }}</span>? Esta acción no se puede deshacer.</p>
        <div class="flex gap-2">
          <button @click="routineToDelete = null" class="flex-1 py-2 rounded-xl border border-gray-200 text-sm text-gray-600 hover:bg-gray-50">Cancelar</button>
          <button @click="confirmDelete" class="flex-1 py-2 rounded-xl bg-red-500 text-white text-sm font-medium hover:bg-red-600 transition-colors">Eliminar</button>
        </div>
      </div>
    </div>

    <!-- Modal detalle rutina -->
    <RoutineDetailModal
      v-if="selectedRoutine"
      :routine="selectedRoutine"
      @close="selectedRoutine = null"
      @updated="onRoutineUpdated"
      @deleted="onRoutineDeleted"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'
import { useAuthStore } from '@/stores/auth.store'
import NavbarSection from '@/components/common/NavbarSection.vue'
import RoutineDetailModal from '@/components/routines/RoutineDetailModal.vue'

export interface RoutineExercise {
  id: number
  order: number
  user_exercise_id: number
  exercise_id: number
  name: string
  muscle: string
  description: string
  video_tutorial: string | null
  reps: number
  weight: number | null
}

export interface Routine {
  id: number
  name: string
  day: string
  exercises: RoutineExercise[]
}

const days = [
  { value: 'LUNES', label: 'Lunes' },
  { value: 'MARTES', label: 'Martes' },
  { value: 'MIERCOLES', label: 'Miércoles' },
  { value: 'JUEVES', label: 'Jueves' },
  { value: 'VIERNES', label: 'Viernes' },
  { value: 'SABADO', label: 'Sábado' },
]

const auth = useAuthStore()
const { apiFetch } = useApi()
const routines = ref<Routine[]>([])
const loading = ref(true)
const showCreateModal = ref(false)
const selectedRoutine = ref<Routine | null>(null)
const routineToDelete = ref<Routine | null>(null)
const newRoutine = ref({ name: '', day: '' })

const daysWithRoutines = computed(() =>
  days.filter(d => routines.value.some(r => r.day === d.value))
)

function routinesByDay(day: string) {
  return routines.value.filter(r => r.day === day)
}

function resetNewRoutine() {
  newRoutine.value = { name: '', day: '' }
}

onMounted(async () => {
  const data = await apiFetch(`${import.meta.env.VITE_API_URL}/api/exercises/routines/`)
  if (data) routines.value = data
  loading.value = false
})

async function createRoutine() {
  const data = await apiFetch(`${import.meta.env.VITE_API_URL}/api/exercises/routines/`, {
    method: 'POST',
    body: JSON.stringify({ name: newRoutine.value.name, day: newRoutine.value.day }),
  })
  if (data) {
    routines.value.push(data)
    showCreateModal.value = false
    resetNewRoutine()
  }
}

function onRoutineUpdated(updated: Routine) {
  const idx = routines.value.findIndex(r => r.id === updated.id)
  if (idx !== -1) routines.value[idx] = updated
  selectedRoutine.value = updated
}

async function confirmDelete() {
  if (!routineToDelete.value) return
  await apiFetch(`${import.meta.env.VITE_API_URL}/api/exercises/routines/${routineToDelete.value.id}/`, { method: 'DELETE' })
  routines.value = routines.value.filter(r => r.id !== routineToDelete.value!.id)
  if (selectedRoutine.value?.id === routineToDelete.value.id) selectedRoutine.value = null
  routineToDelete.value = null
}

function onRoutineDeleted(id: number) {
  routines.value = routines.value.filter(r => r.id !== id)
  selectedRoutine.value = null
}
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { scrollbar-width: none; -ms-overflow-style: none; }
</style>
