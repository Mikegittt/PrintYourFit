import { useEffect, useState } from 'react'
import api from '../services/api'

export default function AdminUsers() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function load() {
      try {
        const res = await api.get('/admin/users')
        setUsers(res.data)
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to load users')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  return (
    <div className="space-y-8">
      <div className="glass-card p-8">
        <p className="text-sm uppercase tracking-[0.24em] text-cyan-200">User management</p>
        <h1 className="mt-3 text-4xl font-semibold text-white">All registered users</h1>
        <p className="mt-4 text-slate-300">View user accounts, roles, and KYC status.</p>
      </div>

      {error && <p className="text-sm text-rose-400">{error}</p>}

      {loading ? (
        <p className="text-slate-400">Loading users...</p>
      ) : users.length === 0 ? (
        <p className="rounded-3xl bg-slate-900/80 p-6 text-slate-300">No users found.</p>
      ) : (
        <div className="grid gap-4">
          {users.map((u) => (
            <div key={u.id} className="rounded-3xl border border-white/10 bg-slate-950/80 p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-lg font-semibold text-white">{u.full_name} — <span className="text-sm text-slate-400">{u.email}</span></p>
                  <p className="mt-1 text-sm text-slate-400">Role: {u.role} • KYC: {u.kyc_completed ? '✓' : '✗'}</p>
                  <p className="mt-1 text-xs text-slate-500">Created: {new Date(u.created_at).toLocaleString()}</p>
                </div>
                <div className="flex flex-col items-end text-sm text-slate-400">
                  <p>ID: {u.id}</p>
                  <p>Active: {u.is_active ? 'Yes' : 'No'}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
