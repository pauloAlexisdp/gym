const API_BASE_URL = `${import.meta.env.VITE_API_URL}/api`

export interface RegisterData {
  name: string
  lastname: string
  email: string
  password: string
}

export interface LoginData {
  email: string
  password: string
}

export interface AuthResponse {
  success: boolean
  message: string
  data?: unknown
}

export const authService = {
  async register(data: RegisterData): Promise<AuthResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/register/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })

      // Verificar si la respuesta es JSON
      const contentType = response.headers.get('content-type')
      if (!contentType || !contentType.includes('application/json')) {
        const text = await response.text()
        throw new Error(`El servidor respondió con: ${response.status} - ${text.substring(0, 100)}`)
      }

      const result = await response.json()

      if (!response.ok) {
        throw new Error(result.message || result.error?.message || 'Error en el registro')
      }

      return {
        success: true,
        message: 'Registro exitoso',
        data: result
      }
    } catch (error) {
      return {
        success: false,
        message: error instanceof Error ? error.message : 'Error desconocido'
      }
    }
  },

  async login(data: LoginData): Promise<AuthResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })

      const result = await response.json()

      if (!response.ok) {
        throw new Error(result.message || 'Error en el login')
      }

      return {
        success: true,
        message: 'Login exitoso',
        data: result
      }
    } catch (error) {
      return {
        success: false,
        message: error instanceof Error ? error.message : 'Error desconocido'
      }
    }
  }
}
