import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import { useToast } from '../context/ToastContext'
import LoadingButton from '../components/LoadingButton'

export default function Register() {
  const [form, setForm] = useState({ full_name: '', email: '', password: '', role: 'CUSTOMER', target_campus: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { showToast } = useToast()

  async function submit(event) {
    event.preventDefault()
    setError('')
    setLoading(true)
    try {
      const referral_code = localStorage.getItem('pyf_referral_code')
      const body = referral_code ? { ...form, referral_code } : form
      await api.post('/auth/register', body)
      localStorage.removeItem('pyf_referral_code')
      showToast({ message: 'Account created successfully. Please log in.', type: 'success' })
      navigate('/login')
    } catch (err) {
      const message = err.response?.data?.detail || err.response?.data?.message || err.message || 'Registration failed.'
      setError(message)
      showToast({ message, type: 'error' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="grid gap-10 lg:grid-cols-[0.95fr_0.85fr]">
      <div className="glass-card p-10">
        <p className="text-sm uppercase tracking-[0.3em] text-indigo-200">Create your account</p>
        <h1 className="mt-4 text-4xl font-semibold text-white">Join Print Your Fit</h1>
        <p className="mt-4 max-w-xl text-slate-300">
          Register as a customer, ambassador, or print shop and start managing orders, tracking referrals, and growing your printing business.
        </p>
        <div className="mt-10 grid gap-4">
          <div className="rounded-3xl bg-slate-900/90 p-5 text-slate-200">
            <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Why register?</p>
            <p className="mt-3 text-sm leading-6 text-slate-300">Connect with buyers, earn referral rewards, and build print shop visibility on a modern marketplace.</p>
          </div>
          <div className="rounded-3xl bg-indigo-500/10 p-5 text-indigo-100">
            <p className="text-sm uppercase tracking-[0.24em]">Referral ready</p>
            <p className="mt-3 text-sm leading-6 text-slate-300">If you have a referral code, it will be applied automatically for ambassador rewards.</p>
          </div>
        </div>
      </div>
      <div className="glass-card p-10">
        <form className="space-y-6" onSubmit={submit}>
          <div>
            <label className="text-sm font-medium text-slate-200">Full name</label>
            <input required value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} className="mt-3 w-full px-4 py-3" placeholder="Jane Doe" />
          </div>
          <div>
            <label className="text-sm font-medium text-slate-200">Email</label>
            <input required value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} className="mt-3 w-full px-4 py-3" type="email" placeholder="jane@example.com" />
          </div>
          <div>
            <label className="text-sm font-medium text-slate-200">Password</label>
            <input required value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} className="mt-3 w-full px-4 py-3" type="password" placeholder="Create a secure password" />
          </div>
          <div>
            <label className="text-sm font-medium text-slate-200">Role</label>
            <select value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })} className="mt-3 w-full px-4 py-3 bg-slate-900/90">
              <option value="CUSTOMER">Customer</option>
              <option value="AMBASSADOR">Ambassador</option>
              <option value="PRINT_SHOP">Print Shop</option>
            </select>
          </div>
          <div>
            <label className="text-sm font-medium text-slate-200">Campus (optional)</label>
            <input value={form.target_campus} onChange={(e) => setForm({ ...form, target_campus: e.target.value })} className="mt-3 w-full px-4 py-3" placeholder="University or campus name" />
          </div>
          {error && <p className="text-sm text-rose-400">{error}</p>}
          <LoadingButton
            type="submit"
            loading={loading}
            className="w-full bg-indigo-500 text-white hover:bg-indigo-400"
          >
            {loading ? 'Creating account...' : 'Create account'}
          </LoadingButton>
        </form>
      </div>
    </div>
  )
}
