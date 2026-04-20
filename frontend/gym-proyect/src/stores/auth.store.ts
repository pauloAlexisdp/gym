import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface AuthUser {
  id: number
  name: string
  lastname: string
  email: string
  role: string
  isActive: boolean
  profile_picture?: string | null
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<AuthUser | null>(JSON.parse(localStorage.getItem('user') || 'null'))

  const isLoggedIn = computed(() => !!token.value)

  function setAuth(newToken: string, newUser: AuthUser) {
    token.value = newToken
    user.value = newUser
    localStorage.setItem('token', newToken)
    localStorage.setItem('user', JSON.stringify(newUser))
  }

  function updateProfilePicture(url: string | null) {
    if (user.value) {
      user.value.profile_picture = url
      localStorage.setItem('user', JSON.stringify(user.value))
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return { token, user, isLoggedIn, setAuth, updateProfilePicture, logout }
})
