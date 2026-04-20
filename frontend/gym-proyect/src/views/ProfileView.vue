<template>
  <div class="min-h-screen bg-gray-100">
    <NavbarSection />

    <main class="px-4 py-8 sm:px-8 max-w-2xl mx-auto">
      <button @click="router.back()" class="flex items-center text-gray-500 hover:text-gray-800 mb-6 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        Volver
      </button>

      <h2 class="text-2xl font-bold text-gray-800 mb-6">Mi Perfil</h2>

      <!-- Foto de perfil -->
      <div class="bg-white rounded-2xl shadow p-6 mb-4 flex flex-col items-center gap-4">
        <div class="relative">
          <img
            v-if="profile.profile_picture"
            :src="profile.profile_picture"
            alt="Foto de perfil"
            class="h-24 w-24 rounded-full object-cover ring-4 ring-gray-100"
          />
          <div
            v-else
            class="h-24 w-24 rounded-full bg-gray-200 flex items-center justify-center ring-4 ring-gray-100"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>

          <label class="absolute bottom-0 right-0 bg-black text-white rounded-full p-1.5 cursor-pointer hover:bg-gray-800 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <input type="file" accept="image/*" class="hidden" @change="uploadPicture" />
          </label>
        </div>

        <div class="text-center">
          <p class="font-semibold text-gray-800 text-lg">{{ profile.name }} {{ profile.lastname }}</p>
          <p class="text-gray-400 text-sm">{{ profile.email }}</p>
        </div>
      </div>

      <!-- Estatura -->
      <div class="bg-white rounded-2xl shadow p-6 mb-4">
        <div class="flex items-center justify-between mb-1">
          <span class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Estatura</span>
          <button v-if="!editingHeight" @click="editingHeight = true" class="text-gray-400 hover:text-black transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
            </svg>
          </button>
          <div v-else class="flex gap-2">
            <button @click="saveHeight" class="text-green-600 hover:text-green-800 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </button>
            <button @click="editingHeight = false" class="text-red-400 hover:text-red-600 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        <div class="flex items-center gap-2 mt-1">
          <input
            v-model.number="heightInput"
            type="number"
            min="100"
            max="250"
            step="0.1"
            :disabled="!editingHeight"
            class="w-32 px-3 py-2 border rounded-lg text-gray-800 font-medium transition-colors"
            :class="editingHeight ? 'border-black bg-white' : 'border-transparent bg-gray-100'"
          />
          <span class="text-gray-500 text-sm">cm</span>
        </div>
      </div>

      <!-- Peso -->
      <div class="bg-white rounded-2xl shadow p-6 mb-4">
        <div class="flex items-center justify-between mb-1">
          <span class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Peso</span>
          <button v-if="!editingWeight" @click="editingWeight = true" class="text-gray-400 hover:text-black transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
            </svg>
          </button>
          <div v-else class="flex gap-2">
            <button @click="addWeight" class="text-green-600 hover:text-green-800 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </button>
            <button @click="editingWeight = false" class="text-red-400 hover:text-red-600 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        <div class="flex items-center gap-2 mt-1">
          <input
            v-model.number="newWeight"
            type="number"
            min="1"
            max="500"
            step="0.1"
            :disabled="!editingWeight"
            class="w-32 px-3 py-2 border rounded-lg text-gray-800 font-medium transition-colors"
            :class="editingWeight ? 'border-black bg-white' : 'border-transparent bg-gray-100'"
          />
          <span class="text-gray-500 text-sm">kg</span>
        </div>

        <div class="mt-4">
          <div v-if="loadingWeight" class="text-gray-400 text-sm">Cargando historial...</div>
          <div v-else-if="weightHistory.length === 0" class="text-gray-400 text-sm">Sin registros de peso aún.</div>
          <div v-else>
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Historial de peso (kg)</p>
            <Line :data="chartData" :options="chartOptions" class="max-h-52" />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, LineElement, PointElement, LinearScale, CategoryScale, Tooltip } from 'chart.js'
import { useAuthStore } from '@/stores/auth.store'
import NavbarSection from '@/components/common/NavbarSection.vue'

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Tooltip)

const router = useRouter()
const auth = useAuthStore()

interface Profile {
  name: string
  lastname: string
  email: string
  height: number | null
  profile_picture: string | null
}

interface WeightEntry {
  date: string
  weight: number
}

const profile = ref<Profile>({
  name: auth.user?.name ?? '',
  lastname: auth.user?.lastname ?? '',
  email: auth.user?.email ?? '',
  height: null,
  profile_picture: auth.user?.profile_picture ?? null,
})

const heightInput = ref<number | null>(null)
const editingHeight = ref(false)
const editingWeight = ref(false)
const newWeight = ref<number | null>(null)
const savingWeight = ref(false)
const loadingWeight = ref(true)
const weightHistory = ref<WeightEntry[]>([])

onMounted(async () => {
  const [profileRes, weightRes] = await Promise.all([
    fetch(`${import.meta.env.VITE_API_URL}/api/auth/profile/`, {
      headers: { Authorization: `Bearer ${auth.token}` },
    }),
    fetch(`${import.meta.env.VITE_API_URL}/api/auth/weight/`, {
      headers: { Authorization: `Bearer ${auth.token}` },
    }),
  ])
  if (profileRes.ok) {
    const data = await profileRes.json()
    profile.value = data
    heightInput.value = data.height
    auth.updateProfilePicture(data.profile_picture)
  }
  if (weightRes.ok) {
    weightHistory.value = await weightRes.json()
    const last = weightHistory.value[weightHistory.value.length - 1]
    if (last) newWeight.value = last.weight
  }
  loadingWeight.value = false
})

async function saveHeight() {
  const res = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/profile/`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${auth.token}` },
    body: JSON.stringify({ height: heightInput.value }),
  })
  if (res.ok) {
    profile.value.height = heightInput.value
    editingHeight.value = false
  }
}

async function uploadPicture(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  const form = new FormData()
  form.append('profile_picture', file)
  const res = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/profile/`, {
    method: 'PATCH',
    headers: { Authorization: `Bearer ${auth.token}` },
    body: form,
  })
  if (res.ok) {
    const data = await res.json()
    profile.value.profile_picture = data.profile_picture
    auth.updateProfilePicture(data.profile_picture)
  }
}

async function addWeight() {
  if (!newWeight.value) return
  savingWeight.value = true
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/weight/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${auth.token}` },
      body: JSON.stringify({ weight: newWeight.value }),
    })
    if (res.ok) {
      const entry = await res.json()
      weightHistory.value.push(entry)
      editingWeight.value = false
    }
  } finally {
    savingWeight.value = false
  }
}

const chartData = computed(() => ({
  labels: weightHistory.value.map(e => e.date),
  datasets: [{
    label: 'Kg',
    data: weightHistory.value.map(e => e.weight),
    borderColor: '#000000',
    backgroundColor: '#000000',
    pointRadius: 5,
    pointHoverRadius: 7,
    tension: 0.3,
    fill: false,
  }],
}))

const chartOptions = computed(() => ({
  responsive: true,
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (item: any) => `${item.raw} kg`,
      },
    },
  },
  scales: {
    x: { grid: { display: false } },
    y: { beginAtZero: false },
  },
}))
</script>
