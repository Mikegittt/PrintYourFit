import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../services/api'

export default function OrderDetail() {
  const { id } = useParams()
  const [order, setOrder] = useState(null)

  useEffect(() => {
    async function load() {
      try {
        const res = await api.get(`/orders/${id}`)
        setOrder(res.data)
      } catch (e) {
        setOrder(null)
      }
    }
    load()
  }, [id])

  if (!order) return <div className="glass-card p-6">Loading…</div>

  return (
    <div className="space-y-6">
      <section className="glass-card p-6">
        <h1 className="text-2xl font-semibold text-white">Order: {order.id}</h1>
        <p className="text-sm text-slate-400">Status: {order.status}</p>
        <p className="mt-4 text-slate-300">Product: {order.product_type}</p>
        <p className="text-slate-300">Quantity: {order.quantity}</p>
        <p className="text-slate-300">Total: {order.total_price}</p>
      </section>
    </div>
  )
}
