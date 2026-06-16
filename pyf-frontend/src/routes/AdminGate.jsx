import { useEffect, useState } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const ADMIN_ACCESS_TOKEN = 'PrintYourFit'
const ADMIN_STORAGE_KEY = 'pyf_admin_access'

export default function AdminGate({ children }) {
  const { user } = useAuth()
  const location = useLocation()
  const [checked, setChecked] = useState(false)
  const [allowed, setAllowed] = useState(false)

  useEffect(() => {
    if (user?.role === 'ADMIN') {
      setAllowed(true)
      setChecked(true)
      return
    }

    try {
      const stored = window.localStorage.getItem(ADMIN_STORAGE_KEY)
      if (stored === ADMIN_ACCESS_TOKEN) {
        setAllowed(true)
      } else {
        const token = window.prompt('Enter admin access token:')
        if (token === ADMIN_ACCESS_TOKEN) {
          window.localStorage.setItem(ADMIN_STORAGE_KEY, ADMIN_ACCESS_TOKEN)
          setAllowed(true)
        }
      }
    } catch (err) {
      setAllowed(false)
    } finally {
      setChecked(true)
    }
  }, [user])

  if (!checked) {
    return null
  }

  if (allowed) {
    return children
  }

  return <Navigate to="/" replace state={{ from: location }} />
}
