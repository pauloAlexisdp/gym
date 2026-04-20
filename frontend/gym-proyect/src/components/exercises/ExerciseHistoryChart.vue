<template>
  <div>
    <div v-if="loading" class="flex justify-center py-6">
      <span class="text-gray-400 text-sm">Cargando historial...</span>
    </div>

    <div v-else-if="history.length === 0" class="text-center py-6 text-gray-400 text-sm">
      Sin historial todavía.
    </div>

    <div v-else>
      <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Peso (kg) en el tiempo</p>
      <Line :data="chartData" :options="chartOptions" class="max-h-52" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend,
} from 'chart.js'
import { useAuthStore } from '@/stores/auth.store'

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Legend)

const props = defineProps<{ userExerciseId: number }>()

interface HistoryEntry {
  date: string
  reps: number
  weight: number
}

const auth = useAuthStore()
const history = ref<HistoryEntry[]>([])
const loading = ref(true)

async function loadHistory() {
  loading.value = true
  try {
    const res = await fetch(
      `${import.meta.env.VITE_API_URL}/api/exercises/user-exercise/${props.userExerciseId}/history/`,
      { headers: { Authorization: `Bearer ${auth.token}` } }
    )
    if (res.ok) history.value = await res.json()
  } finally {
    loading.value = false
  }
}

onMounted(loadHistory)
defineExpose({ refresh: loadHistory })

const chartData = computed(() => ({
  labels: history.value.map(h => h.date),
  datasets: [{
    label: 'Kg',
    data: history.value.map(h => h.weight),
    borderColor: '#000000',
    backgroundColor: '#000000',
    pointRadius: 5,
    pointHoverRadius: 7,
    tension: 0.3,
    fill: false,
  }]
}))

const chartOptions = computed(() => ({
  responsive: true,
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        title: (items: any[]) => items[0].label,
        label: (item: any) => {
          const entry = history.value[item.dataIndex]
          if (!entry) return []
          return [`${entry.weight} kg`, `${entry.reps} repeticiones`]
        }
      }
    }
  },
  scales: {
    x: { grid: { display: false } },
    y: { beginAtZero: false },
  }
}))
</script>
