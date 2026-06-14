import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import { useToast } from '../context/ToastContext'
import LoadingButton from '../components/LoadingButton'

export default function PrintShopOnboarding() {
  const [form, setForm] = useState({ shop_name: '', address: '', state: '', phone: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { showToast } = useToast()

  async function submit(event) {
    event.preventDefault()
    setError('')
    setLoading(true)
    try {
      const response = await api.post('/payments/onboard-shop', form)
      const authorizationUrl = response.data?.authorization_url
      if (!authorizationUrl) {
        throw new Error('Unable to start onboarding payment')
      }
      showToast({ message: 'Opening payment gateway…', type: 'success' })
      window.location.href = authorizationUrl
    } catch (err) {
      const message = err.response?.data?.detail || err.response?.data?.message || err.message || 'Could not initiate onboarding payment.'
      setError(message)
      showToast({ message, type: 'error' })
      setLoading(false)
    }
  }

  return (
    <div className="grid gap-10 lg:grid-cols-[0.9fr_0.75fr]">
      <div className="glass-card p-10">
        <p className="text-sm uppercase tracking-[0.3em] text-cyan-200">Print shop onboarding</p>
        <h1 className="mt-4 text-4xl font-semibold text-white">Register your print press</h1>
        <p className="mt-4 max-w-2xl text-slate-300">
          Complete the onboarding fee payment, then finish the verification step to register your shop in the Print Your Fit marketplace.
        </p>
        <div className="mt-10 space-y-4 rounded-3xl bg-slate-950/90 p-6 text-slate-300">
          <p className="text-sm uppercase tracking-[0.24em] text-slate-500">What happens next</p>
          <ul className="mt-4 space-y-3 text-sm leading-7">
            <li>1. Submit your shop details and pay the onboarding fee.</li>
            <li>2. You will be redirected to Paystack to complete payment.</li>
            <li>3. After payment, return to the verification page to finalize onboarding.</li>
          </ul>
        </div>
      </div>

      <div className="glass-card p-10">
        <form className="space-y-6" onSubmit={submit}>
          <div>
            <label className="text-sm font-medium text-slate-200">Shop or press name</label>
            <input value={form.shop_name} onChange={(e) => setForm({ ...form, shop_name: e.target.value })} className="mt-3 w-full px-4 py-3" placeholder="Print Your Press" required />
          </div>
          <div>
            <label className="text-sm font-medium text-slate-200">Business address</label>
            <input value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} className="mt-3 w-full px-4 py-3" placeholder="123 Lagos Road" required />
          </div>
          <div>
            <label className="text-sm font-medium text-slate-200">State / region</label>
            <input value={form.state} onChange={(e) => setForm({ ...form, state: e.target.value })} className="mt-3 w-full px-4 py-3" placeholder="Lagos" required />
          </div>
          <div>
            <label className="text-sm font-medium text-slate-200">Phone number</label>
            <input value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} className="mt-3 w-full px-4 py-3" placeholder="0803 000 0000" required />
          </div>
          {error && <p className="text-sm text-rose-400">{error}</p>}
          <LoadingButton
            type="submit"
            loading={loading}
            className="w-full bg-indigo-500 text-white hover:bg-indigo-400"
          >
            {loading ? 'Redirecting...' : 'Pay onboarding fee'}
          </LoadingButton>
          <button type="button" onClick={() => navigate('/shop/onboard/verify')} className="w-full rounded-full border border-slate-700 bg-transparent px-5 py-3 text-base font-semibold text-slate-200 transition hover:border-slate-500">
            Verify completed payment
          </button>
        </form>
      </div>
    </div>
  )
}
