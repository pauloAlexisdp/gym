<template>
  <div class="auth-container bg-gray-100 flex items-center justify-center px-4 sm:px-6 lg:px-8 py-8">
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
  overflow: visible;
  min-height: calc(100vh - 4rem); /* 4rem = h-16 */
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Cuando el contenido es más alto que la pantalla, cambiar a items-start */
@media (max-height: 600px) {
  .auth-container {
    align-items: flex-start;
    padding-top: 2rem;
  }
}

@media (min-width: 640px) {
  .auth-container {
    min-height: calc(100vh - 5rem); /* 5rem = h-20 */
  }

  @media (max-height: 700px) {
    .auth-container {
      align-items: flex-start;
      padding-top: 2rem;
    }
  }
}

@media (min-width: 1024px) {
  .auth-container {
    min-height: calc(100vh - 6rem); /* 6rem = h-24 */
  }

  @media (max-height: 800px) {
    .auth-container {
      align-items: flex-start;
      padding-top: 2rem;
    }
  }
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
