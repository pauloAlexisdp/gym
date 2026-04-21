import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'

export function useApi() {
  const auth = useAuthStore()
  const router = useRouter()

  async function apiFetch(url: string, options: RequestInit = {}): Promise<any> {
    const headers: Record<string, string> = {
      Authorization: `Bearer ${auth.token}`,
      ...(options.body && !(options.body instanceof FormData) ? { 'Content-Type': 'application/json' } : {}),
      ...(options.headers as Record<string, string> ?? {}),
    }

    const response = await fetch(url, { ...options, headers })

    if (response.status === 401) {
      auth.logout()
      router.push('/')
      return null
    }

    if (response.status === 204) return null
    return response.json()
  }

  return { apiFetch }
}
