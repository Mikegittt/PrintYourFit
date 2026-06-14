import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'
import { useToast } from '../context/ToastContext'
import LoadingButton from '../components/LoadingButton'

export default function Login() {
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { login, setUser } = useAuth()
  const { showToast } = useToast()

  async function submit(event) {
    event.preventDefault()
    setError('')
    setLoading(true)
    try {
      const response = await api.post('/auth/login', form)
      login(response.data)
      const profile = await api.get('/users/me')
      setUser(profile.data)
      localStorage.setItem('pyf_user', JSON.stringify(profile.data))
      showToast({ message: 'Welcome back! Redirecting to dashboard.', type: 'success' })
      navigate('/dashboard')
    } catch (err) {
      const message = err.response?.data?.detail || err.response?.data?.message || err.message || 'Login failed.'
      setError(message)
      showToast({ message, type: 'error' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="grid gap-10 lg:grid-cols-[0.95fr_0.85fr]">
      <div className="glass-card p-10">
        <p className="text-sm uppercase tracking-[0.3em] text-cyan-200">Secure access</p>
        <h1 className="mt-4 text-4xl font-semibold text-white">Welcome back to Print Your Fit</h1>
        <p className="mt-4 max-w-xl text-slate-300">
          Log in to manage your print orders, track referral rewards, or dispatch jobs through your shop dashboard.
        </p>
        <div className="mt-10 grid gap-4">
          <div className="rounded-3xl bg-slate-900/90 p-5 text-slate-200">
            <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Trusted workflow</p>
            <p className="mt-3 text-sm leading-6 text-slate-300">Access all your active orders, cashouts, and collaboration tools in one place.</p>
          </div>
          <div className="rounded-3xl bg-indigo-500/10 p-5 text-indigo-100">
            <p className="text-sm uppercase tracking-[0.24em]">Faster success</p>
            <p className="mt-3 text-sm leading-6 text-slate-300">Keep your campus network moving with transparent status updates and payment confirmations.</p>
          </div>
        </div>
      </div>
      <div className="glass-card p-10">
        <form className="space-y-6" onSubmit={submit}>
          <div>
            <label className="text-sm font-medium text-slate-200">Email</label>
            <input required value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} className="mt-3 w-full px-4 py-3" type="email" placeholder="you@example.com" />
          </div>
          <div>
            <label className="text-sm font-medium text-slate-200">Password</label>
            <input required value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} className="mt-3 w-full px-4 py-3" type="password" placeholder="Enter your password" />
          </div>
          {error && <p className="text-sm text-rose-400">{error}</p>}
          <LoadingButton
            type="submit"
            loading={loading}
            className="w-full bg-cyan-500 text-slate-950 hover:bg-cyan-400"
          >
            {loading ? 'Signing in...' : 'Sign in'}
          </LoadingButton>
        </form>
      </div>
    </div>
  )
}
