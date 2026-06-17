import { createContext, useContext, useEffect, useState } from 'react'
import api from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)

  useEffect(() => {
    async function loadUser() {
      try {
        await api.get('/auth/csrf')
        const response = await api.get('/users/me')
        setUser(response.data)
      } catch (err) {
        setUser(null)
      }
    }
    loadUser()
  }, [])

  const login = (data) => {
    setUser(data)
  }

  const logout = async () => {
    try {
      await api.post('/auth/logout')
    } catch (err) {
      // ignore logout errors
    }
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, setUser, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
