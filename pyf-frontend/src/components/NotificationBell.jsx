import { useEffect, useState } from 'react'
import api from '../services/api'

export default function NotificationBell() {
  const [open, setOpen] = useState(false)
  const [notifications, setNotifications] = useState([])
  const [unreadCount, setUnreadCount] = useState(0)

  useEffect(() => {
    let mounted = true
    async function load() {
      try {
        const res = await api.get('/notifications/')
        if (!mounted) return
        setNotifications(res.data)
        setUnreadCount(res.data.length)
      } catch (e) {
        // ignore
      }
    }
    load()
    const iv = setInterval(load, 15000) // poll every 15s
    return () => { mounted = false; clearInterval(iv) }
  }, [])

  return (
    <div className="relative">
      <button onClick={() => setOpen(!open)} className="relative rounded-full p-2 hover:bg-white/5">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-slate-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6 6 0 10-12 0v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
        {unreadCount > 0 && (
          <span className="absolute -right-1 -top-1 inline-flex items-center justify-center rounded-full bg-rose-500 px-2 py-0.5 text-xs font-semibold text-white">{unreadCount}</span>
        )}
      </button>

      {open && (
        <div className="absolute right-0 mt-2 w-80 max-w-xs rounded-lg bg-slate-800 p-3 shadow-lg z-50">
          <div className="flex items-center justify-between">
            <p className="text-sm font-semibold text-white">Notifications</p>
            <button onClick={() => { setNotifications([]); setUnreadCount(0) }} className="text-xs text-slate-400">Clear</button>
          </div>
          <div className="mt-2 max-h-60 overflow-auto">
            {notifications.length === 0 ? (
              <p className="text-sm text-slate-400">No recent notifications</p>
            ) : (
              notifications.map((n) => (
                <div key={n.id} className="mt-2 rounded border border-white/5 p-3">
                  <p className="text-sm font-semibold text-white">{n.title}</p>
                  <p className="mt-1 text-xs text-slate-300">{n.message}</p>
                  <p className="mt-2 text-xs text-slate-500">{new Date(n.created_at).toLocaleString()}</p>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  )
}
