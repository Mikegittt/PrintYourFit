import { Navigate } from 'react-router-dom'

export default function AdminGate({ children }) {
  try {
    const allowed = localStorage.getItem('pyf_admin_access') === 'granted'
    if (!allowed) {
      return <Navigate to="/admin" replace />
    }
    return children
  } catch (e) {
    return <Navigate to="/admin" replace />
  }
}
