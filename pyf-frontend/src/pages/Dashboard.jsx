import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useEffect, useState } from 'react'
import api from '../services/api'

export default function Dashboard() {
  const { user } = useAuth()
  const [shops, setShops] = useState([])
  const [query, setQuery] = useState('')
  const [balance, setBalance] = useState(null)
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      setLoading(true)
      try {
        const [shopsRes, balRes, ordersRes] = await Promise.all([
          api.get('/print-shops/discover'),
          api.get('/wallet/balance'),
          api.get('/orders/my-orders'),
        ])
          setShops(shopsRes.data || [])
          setBalance(balRes.data)
          setOrders(ordersRes.data || [])
      } catch (e) {
        // ignore; toast handled globally
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const filtered = shops.filter((s) => !query || s.shop_name.toLowerCase().includes(query.toLowerCase()) || (s.address || '').toLowerCase().includes(query.toLowerCase()))

  return (
    <div className="space-y-8">
      <section className="glass-card p-6 flex items-center justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Welcome back</p>
          <h1 className="mt-2 text-3xl font-semibold text-white">{user?.full_name ?? 'Print Your Fit user'}</h1>
          <p className="mt-2 text-sm text-slate-300">Signed in as <span className="font-semibold text-white">{user?.role ?? 'USER'}</span></p>
        </div>
        <div className="text-right">
          <p className="text-sm text-slate-400">Wallet</p>
          <p className="mt-2 text-2xl font-semibold text-white">{balance ? `${balance.points} pts • ₦${balance.naira_value}` : '—'}</p>
          <div className="mt-3 flex gap-3 justify-end">
            <Link to="/wallet" className="rounded-full bg-indigo-500 px-4 py-2 text-sm font-semibold text-white">Open Wallet</Link>
          </div>
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-3">
        <div className="glass-card p-6 lg:col-span-2">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.24em] text-indigo-200">Discover</p>
              <h2 className="mt-2 text-2xl font-semibold text-white">Printing presses near you</h2>
            </div>
            <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search shops or address" className="ml-4 w-60 rounded-md bg-slate-900/60 px-3 py-2 text-sm text-slate-200" />
          </div>

          <div className="mt-6 space-y-3">
            {loading && <p className="text-slate-400">Loading shops…</p>}
            {!loading && filtered.length === 0 && <p className="text-slate-400">No shops found.</p>}
            {filtered.map((s) => (
              <div key={s.id} className="rounded-xl border border-slate-800/60 p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-semibold text-white">{s.shop_name}</h3>
                    <p className="text-sm text-slate-400">{s.address} · {s.state}</p>
                  </div>
                  <div>
                    <Link to={`/shop/${s.id}`} className="rounded-full bg-slate-800/70 px-4 py-2 text-sm text-white">View</Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="glass-card p-6">
          <p className="text-sm uppercase tracking-[0.24em] text-cyan-200">Orders</p>
          <h3 className="mt-2 text-xl font-semibold text-white">Your recent orders</h3>
          <div className="mt-4 space-y-3">
            {orders.length === 0 && <p className="text-slate-400">No orders yet.</p>}
            {orders.slice(0,5).map((o) => (
              <div key={o.id} className="rounded-lg border border-slate-800/60 p-3">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-slate-100">{o.product_type || 'Order'}</p>
                    <p className="text-sm text-slate-400">Status: {o.status}</p>
                  </div>
                  <Link to={`/orders/${o.id}`} className="text-sm text-indigo-400">View</Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {user?.role === 'PRINT_SHOP' && (
        <section className="glass-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.24em] text-indigo-200">Print shop onboarding</p>
              <h2 className="mt-2 text-2xl font-semibold text-white">Pay onboarding fee and register your press</h2>
            </div>
            <Link to="/shop/onboard" className="rounded-full bg-indigo-500 px-5 py-3 text-sm font-semibold text-white transition hover:bg-indigo-400">Start onboarding</Link>
          </div>
        </section>
      )}
    </div>
  )
}
