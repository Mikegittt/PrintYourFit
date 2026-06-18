import axios from 'axios'

const rawBaseURL = import.meta.env.VITE_API_BASE_URL || 'https://printyourfit.onrender.com/api'
const baseURL = rawBaseURL.replace(/\/api\/v1(\/|$)/, '/api$1')

const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
})

api.defaults.xsrfCookieName = 'csrftoken'
api.defaults.xsrfHeaderName = 'X-CSRFToken'

api.interceptors.request.use((config) => {
  if (config.url && !config.url.startsWith('http') && !config.url.endsWith('/')) {
    config.url = `${config.url}/`
  }
  return config
})

export default api
