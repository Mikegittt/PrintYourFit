import { useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'

export default function ReferralLanding() {
  const { referral_code } = useParams()
  const navigate = useNavigate()

  useEffect(() => {
    if (referral_code) {
      localStorage.setItem('pyf_referral_code', referral_code)
    }
    navigate('/register', { replace: true })
  }, [referral_code, navigate])

  return (
    <div className="glass-card p-10 text-center">
      <p className="text-sm uppercase tracking-[0.3em] text-indigo-200">Referral bonus activated</p>
      <h1 className="mt-4 text-4xl font-semibold text-white">Welcome to Print Your Fit</h1>
      <p className="mt-4 text-slate-300">Your referral code has been saved. You will be redirected to registration with bonus rewards ready.</p>
    </div>
  )
}
