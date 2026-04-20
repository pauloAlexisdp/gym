import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'

export function useApi() {
  const auth = useAuthStore()
  const router = useRouter()

  async function apiFetch(url: string): Promise<any> {
    const response = await fetch(url, {
      headers: { Authorization: `Bearer ${auth.token}` },
    })

    if (response.status === 401) {
      auth.logout()
      router.push('/')
      return null
    }

    return response.json()
  }

  return { apiFetch }
}
