import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'https://printyourfit.onrender.com/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const accessToken = localStorage.getItem('pyf_access_token')
  if (accessToken) {
    config.headers = {
      ...config.headers,
      Authorization: `Bearer ${accessToken}`,
    }
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const refreshToken = localStorage.getItem('pyf_refresh_token')
      if (refreshToken) {
        try {
          const baseUrl = import.meta.env.VITE_API_BASE_URL || 'https://printyourfit.onrender.com/api/v1'
          const refresh = await axios.post(`${baseUrl}/auth/refresh`, {
            refresh_token: refreshToken,
          })
          localStorage.setItem('pyf_access_token', refresh.data.access_token)
          error.config.headers.Authorization = `Bearer ${refresh.data.access_token}`
          return axios(error.config)
        } catch (refreshError) {
          localStorage.removeItem('pyf_access_token')
          localStorage.removeItem('pyf_refresh_token')
        }
      }
    }
    return Promise.reject(error)
  },
)

export default api
