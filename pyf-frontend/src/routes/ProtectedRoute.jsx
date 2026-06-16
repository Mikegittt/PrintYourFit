import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function ProtectedRoute({ children, allowedRoles }) {
  const { user } = useAuth()
  if (!user) {
    return <Navigate to="/login" replace />
  }
  if (allowedRoles) {
    const normalizedRoles = allowedRoles.map(role => role === 'AMBASSADOR' ? 'CUSTOMER' : role)
    const userRole = user.role === 'AMBASSADOR' ? 'CUSTOMER' : user.role
    if (!normalizedRoles.includes(userRole)) {
      return <Navigate to="/" replace />
    }
  }
  return children
}
