import { useState, useEffect } from 'react'
import api from '../services/api'
import { useToast } from '../context/ToastContext'
import LoadingButton from '../components/LoadingButton'

export default function KYC() {
  const [form, setForm] = useState({
    full_name: '',
    phone_number: '',
    identification_type: 'NATIONAL_ID',
    identification_number: '',
    address: '',
    date_of_birth: '',
    document_url: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [status, setStatus] = useState(null)
  const { showToast } = useToast()

  useEffect(() => {
    async function checkStatus() {
      try {
        const response = await api.get('/kyc/status')
        setStatus(response.data)
      } catch (err) {
        console.error('Failed to fetch KYC status:', err)
      }
    }
    checkStatus()
  }, [])

  async function submit(event) {
    event.preventDefault()
    setError('')
    setLoading(true)
    try {
      const response = await api.post('/kyc/submit', form)
      showToast({ message: 'KYC submitted successfully. Admin will review within 2-3 business days.', type: 'success' })
      setStatus(response.data)
      setForm({
        full_name: '',
        phone_number: '',
        identification_type: 'NATIONAL_ID',
        identification_number: '',
        address: '',
        date_of_birth: '',
        document_url: ''
      })
    } catch (err) {
      const message = err.response?.data?.detail || err.response?.data?.message || err.message || 'KYC submission failed.'
      setError(message)
      showToast({ message, type: 'error' })
    } finally {
      setLoading(false)
    }
  }

  const statusColors = {
    NOT_SUBMITTED: 'bg-yellow-500/10 text-yellow-200',
    PENDING: 'bg-blue-500/10 text-blue-200',
    APPROVED: 'bg-green-500/10 text-green-200',
    REJECTED: 'bg-rose-500/10 text-rose-200',
  }

  return (
    <div className="space-y-8">
      <div className="glass-card p-8">
        <p className="text-sm uppercase tracking-[0.24em] text-cyan-200">Know Your Customer (KYC)</p>
        <h1 className="mt-3 text-4xl font-semibold text-white">Verify your identity</h1>
        <p className="mt-4 text-slate-300">Complete your KYC verification to maintain your account access. Print shops must complete KYC within 2 weeks of approval.</p>
      </div>

      {status && (
        <div className={`rounded-3xl p-6 ${statusColors[status.status]}`}>
          <p className="text-sm font-semibold">KYC Status: {status.status}</p>
          <p className="mt-2 text-sm">{status.message}</p>
          {status.submitted_at && <p className="mt-1 text-xs opacity-75">Submitted: {new Date(status.submitted_at).toLocaleDateString()}</p>}
        </div>
      )}

      {status?.status !== 'APPROVED' && (
        <div className="glass-card p-8">
          <form className="space-y-6" onSubmit={submit}>
            <div>
              <label className="text-sm font-medium text-slate-200">Full name</label>
              <input
                required
                value={form.full_name}
                onChange={(e) => setForm({ ...form, full_name: e.target.value })}
                className="mt-3 w-full px-4 py-3"
                placeholder="Your full name"
              />
            </div>

            <div>
              <label className="text-sm font-medium text-slate-200">Phone number</label>
              <input
                required
                value={form.phone_number}
                onChange={(e) => setForm({ ...form, phone_number: e.target.value })}
                className="mt-3 w-full px-4 py-3"
                placeholder="+234 803 000 0000"
              />
            </div>

            <div>
              <label className="text-sm font-medium text-slate-200">Date of birth</label>
              <input
                required
                value={form.date_of_birth}
                onChange={(e) => setForm({ ...form, date_of_birth: e.target.value })}
                type="date"
                className="mt-3 w-full px-4 py-3"
              />
            </div>

            <div>
              <label className="text-sm font-medium text-slate-200">Identification type</label>
              <select
                value={form.identification_type}
                onChange={(e) => setForm({ ...form, identification_type: e.target.value })}
                className="mt-3 w-full px-4 py-3 bg-slate-900/90"
              >
                <option value="NATIONAL_ID">National ID</option>
                <option value="PASSPORT">Passport</option>
                <option value="DRIVER_LICENSE">Driver License</option>
              </select>
            </div>

            <div>
              <label className="text-sm font-medium text-slate-200">Identification number</label>
              <input
                required
                value={form.identification_number}
                onChange={(e) => setForm({ ...form, identification_number: e.target.value })}
                className="mt-3 w-full px-4 py-3"
                placeholder="Your ID number"
              />
            </div>

            <div>
              <label className="text-sm font-medium text-slate-200">Residential address</label>
              <textarea
                required
                value={form.address}
                onChange={(e) => setForm({ ...form, address: e.target.value })}
                className="mt-3 w-full px-4 py-3 min-h-24"
                placeholder="Your full residential address"
              />
            </div>

            <div>
              <label className="text-sm font-medium text-slate-200">Document URL</label>
              <input
                value={form.document_url}
                onChange={(e) => setForm({ ...form, document_url: e.target.value })}
                className="mt-3 w-full px-4 py-3"
                placeholder="URL to uploaded ID document (optional for now)"
              />
              <p className="mt-2 text-xs text-slate-400">Upload your ID document to a cloud storage and provide the link</p>
            </div>

            {error && <p className="text-sm text-rose-400">{error}</p>}

            <LoadingButton
              type="submit"
              loading={loading}
              className="w-full bg-indigo-500 text-white hover:bg-indigo-400"
            >
              {loading ? 'Submitting...' : 'Submit KYC'}
            </LoadingButton>
          </form>
        </div>
      )}

      {status?.status === 'APPROVED' && (
        <div className="rounded-3xl border-2 border-green-500/50 bg-green-500/5 p-8 text-center">
          <p className="text-xl font-semibold text-green-300">✓ KYC Verified</p>
          <p className="mt-2 text-slate-300">Your account is fully verified. Thank you for completing the verification process.</p>
        </div>
      )}
    </div>
  )
}
