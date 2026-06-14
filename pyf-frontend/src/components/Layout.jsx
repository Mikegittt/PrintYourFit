import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Layout({ children }) {
  const { user, logout } = useAuth()
  return (
    <div className="relative min-h-screen overflow-hidden bg-slate-950 text-slate-100">
      <div className="pointer-events-none absolute inset-x-0 top-0 h-80 bg-[radial-gradient(circle_at_top,_rgba(99,102,241,0.24),_transparent_45%)] blur-3xl" />
      <div className="pointer-events-none absolute right-0 top-24 h-96 w-96 rounded-full bg-purple-500/10 blur-3xl" />
      <header className="relative z-10 border-b border-white/10 bg-slate-950/75 backdrop-blur-xl shadow-soft-xl">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
          <Link to="/" className="text-xl font-semibold tracking-tight text-white">Print Your Fit</Link>
          <nav className="flex flex-wrap items-center gap-4 text-sm text-slate-300">
            <Link to="/">Home</Link>
            {user ? (
              <>
                <Link to="/dashboard">Dashboard</Link>
                <Link to="/design-studio">AI Designer</Link>
                <Link to="/wallet">Wallet</Link>
                {user.role === 'ADMIN' && <Link to="/admin/orders" className="transition hover:text-white">Admin</Link>}
              </>
            ) : (
              <>
                <Link to="/login" className="transition hover:text-white">Login</Link>
                <Link to="/register" className="rounded-full bg-indigo-500 px-4 py-2 text-sm font-semibold text-white transition hover:bg-indigo-400">Sign Up</Link>
              </>
            )}
          </nav>
        </div>
      </header>
      <main className="relative z-10 mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">{children}</main>
      <footer className="relative z-10 border-t border-white/10 bg-slate-950/75 backdrop-blur-xl py-8 text-slate-400">
        <div className="mx-auto flex max-w-6xl flex-col gap-4 text-sm sm:flex-row sm:items-center sm:justify-between px-4">
          <p>© 2026 Print Your Fit. Built for fast, modern print commerce.</p>
          <p>Designed for customers, ambassadors, print shops, and admins.</p>
        </div>
      </footer>
    </div>
  )
}
