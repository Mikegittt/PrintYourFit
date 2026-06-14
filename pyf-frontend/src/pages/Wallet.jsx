import { useEffect, useState } from 'react'
import api from '../services/api'
import LoadingButton from '../components/LoadingButton'

export default function Wallet() {
  const [balance, setBalance] = useState(null)
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    async function load() {
      try {
        const res = await api.get('/wallet/balance')
        setBalance(res.data)
        const h = await api.get('/wallet/history')
        setHistory(h.data.items || [])
      } catch (e) {
        // ignore
      }
    }
    load()
  }, [])

  async function handleFund() {
    // stub: open fund modal / integrate payment gateway
    alert('Fund wallet: implement payment integration')
  }

  async function handleWithdraw() {
    // stub: call /wallet/cashout endpoint
    const amount = prompt('Enter points to withdraw (min 100)')
    if (!amount) return
    try {
      setLoading(true)
      await api.post('/wallet/cashout', { points_amount: Number(amount), channel: 'BANK', destination: 'pending' })
      const h = await api.get('/wallet/history')
      setHistory(h.data.items || [])
      const b = await api.get('/wallet/balance')
      setBalance(b.data)
      alert('Cashout requested')
    } catch (e) {
      alert(e.response?.data?.detail || e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <section className="glass-card p-6">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Wallet</p>
        <h1 className="mt-2 text-2xl font-semibold text-white">Balance</h1>
        <p className="mt-2 text-lg text-slate-300">{balance ? `${balance.points} pts • ₦${balance.naira_value}` : 'Loading…'}</p>
        <div className="mt-4 flex gap-3">
          <LoadingButton onClick={handleFund} className="bg-indigo-500 text-white">Fund</LoadingButton>
          <LoadingButton onClick={handleWithdraw} loading={loading} className="bg-rose-500 text-white">Withdraw</LoadingButton>
        </div>
      </section>

      <section className="glass-card p-6">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">History</p>
        <div className="mt-4 space-y-3">
          {history.length === 0 && <p className="text-slate-400">No wallet activity yet.</p>}
          {history.map((it) => (
            <div key={it.id} className="rounded-md border border-slate-800/60 p-3">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-white">{it.transaction_type}</p>
                  <p className="text-sm text-slate-400">{it.created_at}</p>
                </div>
                <div className="text-right text-sm text-slate-200">{it.points_delta} pts</div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
