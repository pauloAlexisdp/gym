<template>
  <div class="min-h-screen bg-gray-100">
    <GymNavbar @open-modal="showModal = true" />

    <main>
      <HeroSection :hero-title="config.hero_title" />
      <AboutSection :about-title="config.about_title" :about-description="config.about_description" />
      <ActivitiesSection :activities-title="config.activities_title" :activities="config.activities" />
    </main>

    <AuthModal v-if="showModal" @close="showModal = false" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import GymNavbar from '@/components/common/NavbarSection.vue'
import HeroSection from '@/components/home/HeroSection.vue'
import AboutSection from '@/components/home/AboutSection.vue'
import ActivitiesSection from '@/components/home/ActivitiesSection.vue'
import AuthModal from '@/components/auth/AuthModal.vue'

interface Activity {
  id: number
  title: string
  description: string
  image: string | null
}

interface HomeConfig {
  hero_title: string
  about_title: string
  about_description: string
  activities_title: string
  activities: Activity[]
}

const showModal = ref(false)
const config = ref<HomeConfig>({
  hero_title: 'Bienvenido a GymApp',
  about_title: 'Quiénes Somos',
  about_description: '',
  activities_title: 'Nuestras Actividades',
  activities: [],
})

onMounted(async () => {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/api/home/config/`)
    if (res.ok) config.value = await res.json()
  } catch {}
})
</script>
