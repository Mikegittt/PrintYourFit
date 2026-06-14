import { createContext, useContext, useEffect, useState } from 'react'
import api from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(() => localStorage.getItem('pyf_access_token'))

  useEffect(() => {
    if (token) {
      api.defaults.headers.common.Authorization = `Bearer ${token}`
      const storedUser = localStorage.getItem('pyf_user')
      if (storedUser) {
        setUser(JSON.parse(storedUser))
      }
    }
  }, [token])

  const login = (data) => {
    localStorage.setItem('pyf_access_token', data.access_token)
    localStorage.setItem('pyf_refresh_token', data.refresh_token)
    api.defaults.headers.common.Authorization = `Bearer ${data.access_token}`
    setToken(data.access_token)
  }

  const logout = () => {
    localStorage.removeItem('pyf_access_token')
    localStorage.removeItem('pyf_refresh_token')
    localStorage.removeItem('pyf_user')
    setToken(null)
    setUser(null)
    delete api.defaults.headers.common.Authorization
  }

  return (
    <AuthContext.Provider value={{ user, setUser, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
