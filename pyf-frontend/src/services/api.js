import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'https://printyourfit.onrender.com/api',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
})

api.defaults.xsrfCookieName = 'csrftoken'
api.defaults.xsrfHeaderName = 'X-CSRFToken'

export default api
