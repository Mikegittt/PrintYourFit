import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function AdminAccess() {
  const [code, setCode] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = (e) => {
    e.preventDefault()
    if (code === 'PrintYourFit') {
      localStorage.setItem('pyf_admin_access', 'granted')
      navigate('/admin/orders')
    } else {
      setError('Invalid access code')
    }
  }

  return (
    <div className="mx-auto max-w-md rounded-lg bg-slate-800 p-6 shadow">
      <h2 className="mb-4 text-xl font-semibold">Admin Access</h2>
      <p className="mb-4 text-sm text-slate-300">Enter the admin access code to continue.</p>
      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <input
          aria-label="Admin access code"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          className="rounded border border-slate-700 bg-slate-900 px-3 py-2 text-slate-100"
          placeholder="Enter access code"
        />
        {error && <div className="text-sm text-red-400">{error}</div>}
        <div className="flex justify-end">
          <button type="submit" className="rounded bg-indigo-600 px-4 py-2 text-white">Enter</button>
        </div>
      </form>
    </div>
  )
}
