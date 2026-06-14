import { useEffect, useState } from 'react'
import { useLocation } from 'react-router-dom'
import api from '../services/api'

function useQuery() {
  return new URLSearchParams(useLocation().search)
}

export default function PrintShopVerify() {
  const query = useQuery()
  const [status, setStatus] = useState('pending')
  const [message, setMessage] = useState('Verifying your onboarding payment...')

  useEffect(() => {
    const reference = query.get('reference')
    if (!reference) {
      setStatus('failed')
      setMessage('Missing Paystack reference in the URL. Please return from Paystack or enter the payment reference manually.')
      return
    }

    async function verify() {
      try {
        const response = await api.post('/payments/verify-onboarding', { reference })
        if (response.data?.status === 'paid') {
          setStatus('success')
          setMessage('Onboarding payment verified. Your print shop has been registered and is pending admin approval.')
        } else {
          setStatus('failed')
          setMessage('Payment verification failed. Please try again or contact support.')
        }
      } catch (error) {
        setStatus('failed')
        setMessage(error.response?.data?.detail || 'Unable to verify onboarding payment.')
      }
    }

    verify()
  }, [query])

  return (
    <div className="glass-card p-10">
      <p className="text-sm uppercase tracking-[0.3em] text-cyan-200">Verify onboarding</p>
      <h1 className="mt-4 text-4xl font-semibold text-white">Print shop onboarding verification</h1>
      <p className="mt-4 max-w-2xl text-slate-300">{message}</p>

      {status === 'success' ? (
        <div className="mt-8 rounded-3xl bg-slate-900/90 p-6 text-slate-200">
          <p className="text-lg font-semibold text-white">Success!</p>
          <p className="mt-3 text-slate-300">Your shop is now registered. Admin approval may still be required before it begins receiving orders.</p>
        </div>
      ) : status === 'failed' ? (
        <div className="mt-8 rounded-3xl bg-rose-900/80 p-6 text-rose-100">
          <p className="text-lg font-semibold">Verification error</p>
          <p className="mt-3">{message}</p>
        </div>
      ) : null}
    </div>
  )
}
