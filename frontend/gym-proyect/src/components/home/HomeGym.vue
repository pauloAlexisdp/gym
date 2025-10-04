<template>
  <div class="min-h-screen bg-gray-100">
    <!-- NAVBAR -->
    <GymNavbar />

    <!-- MAIN CONTENT -->
    <main>
      <HeroSection />
      <AboutSection />
      <ActivitiesSection />
    </main>

    <!-- FOOTER -->
    <FooterSection />
  </div>
</template>

<script setup lang="ts">
  import GymNavbar from '@/components/common/NavbarSection.vue';
  import HeroSection from '@/components/home/HeroSection.vue';
  import AboutSection from '@/components/home/AboutSection.vue';
  import ActivitiesSection from '@/components/home/ActivitiesSection.vue';
  import FooterSection from '@/components/common/FooterSection.vue';
</script>
