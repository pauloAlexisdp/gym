<template>
  <div class="auth-container">
    <Transition name="form-slide" mode="out-in">
      <LoginForm v-if="route.path === '/iniciar-sesion'" key="login" @switch-to-register="switchToRegister" />
      <RegisterForm v-else key="register" @switch-to-login="switchToLogin" />
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import LoginForm from './LoginForm.vue'
import RegisterForm from './RegisterForm.vue'

const route = useRoute()
const router = useRouter()

const switchToRegister = () => {
  router.push('/registrarse')
}

const switchToLogin = () => {
  router.push('/iniciar-sesion')
}
</script>

<style scoped>
.auth-container {
  position: relative;
  overflow: hidden;
}

.form-slide-enter-active,
.form-slide-leave-active {
  transition: all 0.3s ease-in-out;
}

.form-slide-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.form-slide-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

.form-slide-enter-to,
.form-slide-leave-from {
  opacity: 1;
  transform: translateX(0);
}
</style>
