import { useEffect, useState } from 'react'
import api from '../services/api'

export default function AdminShops() {
  const [shops, setShops] = useState([])
  const [filter, setFilter] = useState('all')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function load() {
      try {
        const response = await api.get('/print-shops/')
        setShops(response.data)
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to load shops')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  async function approveShop(shopId) {
    try {
      await api.put(`/print-shops/${shopId}/approve`)
      setShops(shops.map(s => s.id === shopId ? { ...s, status: 'APPROVED' } : s))
    } catch (err) {
      alert('Failed to approve shop: ' + (err.response?.data?.detail || err.message))
    }
  }

  async function rejectShop(shopId) {
    try {
      await api.put(`/print-shops/${shopId}/reject`)
      setShops(shops.map(s => s.id === shopId ? { ...s, status: 'REJECTED' } : s))
    } catch (err) {
      alert('Failed to reject shop: ' + (err.response?.data?.detail || err.message))
    }
  }

  const filteredShops = filter === 'all' ? shops : shops.filter(s => s.status === filter)

  const statusStyles = {
    PENDING: 'bg-yellow-500/10 text-yellow-200',
    APPROVED: 'bg-green-500/10 text-green-200',
    REJECTED: 'bg-rose-500/10 text-rose-200',
  }

  return (
    <div className="space-y-8">
      <div className="glass-card p-8">
        <p className="text-sm uppercase tracking-[0.24em] text-cyan-200">Shop management</p>
        <h1 className="mt-3 text-4xl font-semibold text-white">All registered print shops</h1>
        <p className="mt-4 text-slate-300">Review shop details and their current onboarding status across the platform.</p>
      </div>

      <div className="glass-card p-6">
        <div className="flex flex-wrap gap-3">
          {['all', 'PENDING', 'APPROVED', 'REJECTED'].map((status) => (
            <button
              key={status}
              onClick={() => setFilter(status)}
              className={`rounded-full px-5 py-2 text-sm font-semibold transition ${
                filter === status
                  ? 'bg-indigo-500 text-white'
                  : 'border border-white/10 bg-transparent text-slate-300 hover:border-white/20'
              }`}
            >
              {status === 'all' ? 'All shops' : status}
            </button>
          ))}
        </div>
      </div>

      {error && <p className="text-sm text-rose-400">{error}</p>}

      {loading ? (
        <p className="text-slate-400">Loading shops...</p>
      ) : filteredShops.length === 0 ? (
        <p className="rounded-3xl bg-slate-900/80 p-6 text-slate-300">No shops found.</p>
      ) : (
        <div className="grid gap-4">
          {filteredShops.map((shop) => (
            <div key={shop.id} className="rounded-3xl border border-white/10 bg-slate-950/80 p-6">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3">
                    <p className="text-lg font-semibold text-white">{shop.shop_name}</p>
                    <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${statusStyles[shop.status]}`}>
                      {shop.status}
                    </span>
                    {shop.kyc_completed && (
                      <span className="inline-flex rounded-full bg-green-500/10 px-3 py-1 text-xs font-semibold text-green-200">
                        KYC ✓
                      </span>
                    )}
                  </div>
                  <p className="mt-2 text-sm text-slate-400">{shop.address}, {shop.state}</p>
                  <div className="mt-2 grid gap-1 text-xs text-slate-500">
                    <p>WhatsApp: {shop.whatsapp_number || 'Not provided'}</p>
                    <p>ID: {shop.id}</p>
                    <p>Created: {new Date(shop.created_at).toLocaleDateString()}</p>
                  </div>
                </div>
                {shop.status === 'PENDING' && (
                  <div className="flex flex-col gap-2 sm:flex-row">
                    <button
                      onClick={() => approveShop(shop.id)}
                      className="rounded-full bg-green-600 px-6 py-2 text-sm font-semibold text-white transition hover:bg-green-500"
                    >
                      Approve
                    </button>
                    <button
                      onClick={() => rejectShop(shop.id)}
                      className="rounded-full border border-rose-600 bg-transparent px-6 py-2 text-sm font-semibold text-rose-300 transition hover:border-rose-400"
                    >
                      Reject
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
