import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import api from '../services/api'

export default function ShopDetail() {
  const { id } = useParams()
  const [shop, setShop] = useState(null)

  useEffect(() => {
    async function load() {
      try {
        const res = await api.get(`/print-shops/${id}`)
        setShop(res.data)
      } catch (e) {
        setShop(null)
      }
    }
    load()
  }, [id])

  if (!shop) return <div className="glass-card p-6">Loading…</div>

  return (
    <div className="space-y-6">
      <section className="glass-card p-6">
        <h1 className="text-2xl font-semibold text-white">{shop.shop_name}</h1>
        <p className="text-sm text-slate-400">{shop.address} · {shop.state}</p>
        <div className="mt-4">
          <Link to="/orders" className="rounded-full bg-indigo-500 px-4 py-2 text-white">Create order</Link>
        </div>
      </section>
    </div>
  )
}
