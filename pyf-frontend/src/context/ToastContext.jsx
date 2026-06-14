import { createContext, useCallback, useContext, useMemo, useState } from 'react'

const ToastContext = createContext(null)

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([])

  const showToast = useCallback(({ message, type = 'info', duration = 4500 }) => {
    const id = typeof crypto !== 'undefined' && crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}`
    setToasts((current) => [{ id, message, type }, ...current])
    window.setTimeout(() => {
      setToasts((current) => current.filter((toast) => toast.id !== id))
    }, duration)
  }, [])

  const value = useMemo(() => ({ showToast }), [showToast])

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div className="pointer-events-none fixed bottom-4 right-4 z-50 flex w-full max-w-sm flex-col gap-3 px-4 sm:px-0">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            className={`pointer-events-auto rounded-3xl border px-5 py-4 shadow-xl shadow-black/20 transition duration-200 ${
              toast.type === 'success'
                ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-100'
                : toast.type === 'error'
                ? 'border-rose-500/30 bg-rose-500/10 text-rose-100'
                : 'border-slate-600/60 bg-slate-950/95 text-slate-100'
            }`}
          >
            <p className="text-sm font-semibold">{toast.type === 'success' ? 'Success' : toast.type === 'error' ? 'Error' : 'Notice'}</p>
            <p className="mt-1 text-sm leading-6 text-slate-300">{toast.message}</p>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  )
}

export function useToast() {
  return useContext(ToastContext)
}
