import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../services/api'

export default function AdminOrders() {
  const [stats, setStats] = useState({ pending: 0, cashouts: 0, active: 0 })
  const [pendingShops, setPendingShops] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function load() {
      try {
        const response = await api.get('/print-shops/pending')
        setPendingShops(response.data)
        setStats({ pending: response.data.length, cashouts: 14, active: 120 })
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to load pending shops')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  async function approveShop(shopId) {
    try {
      await api.put(`/print-shops/${shopId}/approve`)
      setPendingShops(pendingShops.filter(s => s.id !== shopId))
      setStats(prev => ({ ...prev, pending: prev.pending - 1, active: prev.active + 1 }))
    } catch (err) {
      alert('Failed to approve shop: ' + (err.response?.data?.detail || err.message))
    }
  }

  async function rejectShop(shopId) {
    try {
      await api.put(`/print-shops/${shopId}/reject`)
      setPendingShops(pendingShops.filter(s => s.id !== shopId))
      setStats(prev => ({ ...prev, pending: prev.pending - 1 }))
    } catch (err) {
      alert('Failed to reject shop: ' + (err.response?.data?.detail || err.message))
    }
  }

  return (
    <div className="space-y-8">
      <div className="glass-card p-8">
        <p className="text-sm uppercase tracking-[0.24em] text-rose-200">Admin control</p>
        <h1 className="mt-3 text-4xl font-semibold text-white">Platform management dashboard</h1>
        <p className="mt-4 text-slate-300">Review orders, approve shops, process cashouts, and keep your marketplace running smoothly from a single place.</p>
      </div>

      <div className="grid gap-6 xl:grid-cols-3">
        {[
          { title: 'Pending approvals', value: stats.pending },
          { title: 'Open cashouts', value: stats.cashouts },
          { title: 'Active shops', value: stats.active },
        ].map((item) => (
          <div key={item.title} className="glass-card p-6">
            <p className="text-sm uppercase tracking-[0.24em] text-slate-400">{item.title}</p>
            <p className="mt-4 text-3xl font-semibold text-white">{item.value}</p>
          </div>
        ))}
      </div>

      <section className="glass-card p-8">
        <div className="mb-6 flex items-center justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.24em] text-cyan-200">Shop onboarding</p>
            <h2 className="mt-2 text-2xl font-semibold text-white">Pending shop approvals</h2>
          </div>
        </div>

        {error && <p className="mb-4 text-sm text-rose-400">{error}</p>}

        {loading ? (
          <p className="text-slate-400">Loading pending shops...</p>
        ) : pendingShops.length === 0 ? (
          <p className="rounded-3xl bg-slate-900/80 p-6 text-slate-300">No pending shops awaiting approval.</p>
        ) : (
          <div className="grid gap-4">
            {pendingShops.map((shop) => (
              <div key={shop.id} className="rounded-3xl border border-white/10 bg-slate-950/80 p-6">
                <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <p className="text-lg font-semibold text-white">{shop.shop_name}</p>
                    <p className="mt-2 text-sm text-slate-400">{shop.address}, {shop.state}</p>
                    <p className="mt-1 text-xs text-slate-500">Submitted {new Date(shop.created_at).toLocaleDateString()}</p>
                  </div>
                  <div className="flex gap-3">
                    <button onClick={() => approveShop(shop.id)} className="rounded-full bg-green-600 px-6 py-2 text-sm font-semibold text-white transition hover:bg-green-500">
                      Approve
                    </button>
                    <button onClick={() => rejectShop(shop.id)} className="rounded-full border border-rose-600 bg-transparent px-6 py-2 text-sm font-semibold text-rose-300 transition hover:border-rose-400">
                      Reject
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="grid gap-6 lg:grid-cols-2">
        <Link to="/admin/shops" className="glass-card p-8 transition hover:-translate-y-1 hover:border-indigo-500/20">
          <p className="text-sm uppercase tracking-[0.24em] text-indigo-200\">Navigation</p>
          <h3 className="mt-3 text-2xl font-semibold text-white\">View all shops</h3>
          <p className="mt-4 text-slate-300\">See complete shop list including approved, pending, and rejected shops.</p>
        </Link>
        <div className="glass-card p-8">
          <p className="text-sm uppercase tracking-[0.24em] text-violet-200\">Metrics</p>
          <h3 className="mt-3 text-2xl font-semibold text-white\">Platform health</h3>
          <p className="mt-4 text-slate-300\">Monitor order volume, shop capacity, referral revenue, and payout processing.</p>
        </div>
      </section>
    </div>
  )
}
