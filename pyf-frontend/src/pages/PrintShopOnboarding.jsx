import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import { useToast } from '../context/ToastContext'
import LoadingButton from '../components/LoadingButton'

export default function PrintShopOnboarding() {
  const [form, setForm] = useState({ shop_name: '', address: '', state: '', whatsapp_number: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [submitted, setSubmitted] = useState(false)
  const navigate = useNavigate()
  const { showToast } = useToast()

  async function submit(event) {
    event.preventDefault()
    setError('')
    setLoading(true)
    try {
      const response = await api.post('/print-shops/register', form)
      setSubmitted(true)
      showToast({ message: 'Registration submitted! Admin will contact you on WhatsApp within 5 minutes.', type: 'success' })
      setTimeout(() => navigate('/shop/dashboard'), 3000)
    } catch (err) {
      const message = err.response?.data?.detail || err.response?.data?.message || err.message || 'Could not submit print shop registration.'
      setError(message)
      showToast({ message, type: 'error' })
      setLoading(false)
    }
  }

  if (submitted) {
    return (
      <div className="grid gap-10 lg:grid-cols-[0.9fr_0.75fr]">
        <div className="glass-card p-10">
          <p className="text-sm uppercase tracking-[0.3em] text-cyan-200">Print shop onboarding</p>
          <h1 className="mt-4 text-4xl font-semibold text-white">Registration submitted!</h1>
          <p className="mt-4 max-w-2xl text-slate-300">
            Your print shop registration has been submitted successfully. Our admin team will contact you on WhatsApp within 5 minutes to complete the onboarding process.
          </p>
          <div className="mt-10 space-y-4 rounded-3xl bg-slate-950/90 p-6 text-slate-300">
            <p className="text-sm uppercase tracking-[0.24em] text-slate-500">What happens next</p>
            <ul className="mt-4 space-y-3 text-sm leading-7">
              <li>✓ Admin reviews your shop details</li>
              <li>✓ You receive a WhatsApp message to confirm details</li>
              <li>✓ Approval and access to PrintYourFit marketplace</li>
              <li>✓ Complete KYC verification within 2 weeks to remain active</li>
            </ul>
          </div>
        </div>

        <div className="glass-card p-10">
          <div className="space-y-6">
            <div>
              <h2 className="text-lg font-semibold text-white">Stay tuned!</h2>
              <p className="mt-2 text-slate-400">You'll receive a WhatsApp message shortly. Make sure to keep your phone handy.</p>
            </div>
            <button
              onClick={() => navigate('/shop/dashboard')}
              className="w-full rounded-full bg-indigo-500 px-5 py-3 text-base font-semibold text-white transition hover:bg-indigo-400"
            >
              Go to dashboard
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="grid gap-10 lg:grid-cols-[0.9fr_0.75fr]">
      <div className="glass-card p-10">
        <p className="text-sm uppercase tracking-[0.3em] text-cyan-200">Print shop onboarding</p>
        <h1 className="mt-4 text-4xl font-semibold text-white">Register your print press</h1>
        <p className="mt-4 max-w-2xl text-slate-300">
          Submit your shop details and provide your WhatsApp number. Our admin team will contact you within 5 minutes to verify your information and complete the onboarding process.
        </p>
        <div className="mt-10 space-y-4 rounded-3xl bg-slate-950/90 p-6 text-slate-300">
          <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Process overview</p>
          <ul className="mt-4 space-y-3 text-sm leading-7">
            <li>1. Submit your shop details and WhatsApp number below.</li>
            <li>2. Our admin will contact you on WhatsApp within 5 minutes.</li>
            <li>3. Complete verification call to finalize onboarding.</li>
            <li>4. Your shop goes live on PrintYourFit marketplace!</li>
            <li>5. Complete KYC verification within 2 weeks to maintain access.</li>
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
            <label className="text-sm font-medium text-slate-200">WhatsApp number</label>
            <input value={form.whatsapp_number} onChange={(e) => setForm({ ...form, whatsapp_number: e.target.value })} className="mt-3 w-full px-4 py-3" placeholder="+234 803 000 0000" required />
          </div>
          {error && <p className="text-sm text-rose-400">{error}</p>}
          <LoadingButton
            type="submit"
            loading={loading}
            className="w-full bg-indigo-500 text-white hover:bg-indigo-400"
          >
            {loading ? 'Submitting...' : 'Submit registration'}
          </LoadingButton>
        </form>
      </div>
    </div>
  )
}
