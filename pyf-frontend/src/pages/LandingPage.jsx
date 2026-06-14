import { Link } from 'react-router-dom'

const stats = [
  { label: 'Shops onboarded', value: '120+' },
  { label: 'Referral commissions paid', value: '3.2k' },
  { label: 'Orders delivered', value: '5.6k' },
]

const roleCards = [
  {
    title: 'Customers',
    description: 'Upload your design, choose a print shop, and track every order from request to delivery.',
    accent: 'bg-indigo-500/10 text-indigo-100',
  },
  {
    title: 'Ambassadors',
    description: 'Share your referral code, earn points, and convert new customers.',
    accent: 'bg-violet-500/10 text-violet-100',
  },
  {
    title: 'Print Shops',
    description: 'Manage job queues, verify orders, and keep production flowing without delays.',
    accent: 'bg-cyan-500/10 text-cyan-100',
  },
  {
    title: 'Admins',
    description: 'Oversee shops, payouts, and platform metrics from a single command center.',
    accent: 'bg-rose-500/10 text-rose-100',
  },
]

export default function LandingPage() {
  return (
    <div className="space-y-20">
      <section className="relative overflow-hidden rounded-[40px] bg-slate-900/95 p-8 sm:p-10 lg:p-12 shadow-soft-xl">
        <div className="absolute -left-24 top-10 h-64 w-64 rounded-full bg-violet-500/20 blur-3xl" />
        <div className="absolute right-0 top-0 h-72 w-72 rounded-full bg-cyan-500/10 blur-3xl" />
        <div className="relative grid gap-10 lg:grid-cols-[1.15fr_0.85fr] items-center">
          <div className="space-y-6">
            <span className="hero-badge">One platform for print jobs, referrals, and shop fulfillment</span>
            <h1 className="text-5xl font-semibold tracking-tight text-white md:text-6xl">
              Print Your Fit makes custom prints fast, social, and profitable.
            </h1>
            <p className="max-w-2xl text-lg leading-8 text-slate-300">
              Seamlessly connect customers, ambassadors, print shops, and admins in a single modern marketplace. Submit prints, earn commissions, manage logistics, and get paid — all from one dashboard.
            </p>
            <div className="flex flex-wrap gap-4">
              <Link to="/register" className="inline-flex items-center justify-center rounded-full bg-indigo-500 px-7 py-3 text-base font-semibold text-white shadow-lg shadow-indigo-500/20 transition hover:bg-indigo-400">
                Start printing
              </Link>
              <Link to="/login" className="inline-flex items-center justify-center rounded-full border border-white/10 bg-white/5 px-7 py-3 text-base font-semibold text-slate-100 transition hover:border-white/20 hover:bg-white/10">
                Login to your account
              </Link>
            </div>
            <div className="grid gap-4 sm:grid-cols-3">
              {stats.map((item) => (
                <div key={item.label} className="glass-card p-5 text-center">
                  <p className="text-3xl font-semibold text-white">{item.value}</p>
                  <p className="mt-2 text-sm text-slate-400">{item.label}</p>
                </div>
              ))}
            </div>
          </div>
          <div className="space-y-6">
            <div className="glass-card p-6">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Fast order flow</p>
                  <h2 className="mt-3 text-2xl font-semibold text-white">Flow from request to delivery</h2>
                </div>
                <div className="rounded-3xl bg-slate-900/90 p-4 text-slate-200 shadow-soft-xl">
                  <span className="text-2xl font-semibold">4.8/5</span>
                  <p className="text-xs uppercase tracking-[0.2em] text-slate-400">Customer rating</p>
                </div>
              </div>
              <div className="mt-8 grid gap-4">
                {[
                  'Create your order with upload or prompt input',
                  'Assign it to an approved print shop and start production',
                  'Track status, confirm payment, and receive dispatch updates',
                ].map((step) => (
                  <div key={step} className="rounded-3xl border border-white/10 bg-slate-950/80 p-4 text-slate-200">
                    <p className="text-sm text-slate-400">{step}</p>
                  </div>
                ))}
              </div>
            </div>
            <div className="glass-card p-6">
              <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Ambassador spotlight</p>
              <h2 className="mt-3 text-2xl font-semibold text-white">Earn every referral</h2>
              <p className="mt-4 text-slate-300">
                Ambassadors receive points automatically as orders complete. Convert referrals into cashouts or airtime top-ups with transparent history and payout controls.
              </p>
              <div className="mt-6 grid gap-3 sm:grid-cols-2">
                <div className="rounded-3xl bg-indigo-500/10 p-5 text-indigo-100">
                  <p className="text-3xl font-semibold">5%</p>
                  <p className="mt-2 text-sm text-slate-300">Commission rate</p>
                </div>
                <div className="rounded-3xl bg-cyan-500/10 p-5 text-cyan-100">
                  <p className="text-3xl font-semibold">100</p>
                  <p className="mt-2 text-sm text-slate-300">Minimum points cashout</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-2">
        <div className="glass-card p-10">
          <p className="text-sm uppercase tracking-[0.3em] text-indigo-200">Why Print Your Fit</p>
          <h2 className="mt-4 text-4xl font-semibold text-white">A complete print marketplace designed for every role.</h2>
          <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-300">
            From customers ordering custom apparel to ambassadors growing their commission streams and print shops managing production, PYF brings everyone together with an intuitive workflow built for speed and reliability.
          </p>
          <div className="mt-10 grid gap-4 sm:grid-cols-2">
            {[
              { title: 'Instant shop matching', description: 'Route jobs to verified print shops with capacity and quality controls.' },
              { title: 'Smart referral tracking', description: 'Track every referral and pay points automatically when orders complete.' },
              { title: 'Secure payments', description: 'Pay via Paystack with verification and order status updates.' },
              { title: 'Admin oversight', description: 'Approve shops, manage requests, and monitor platform metrics in one place.' },
            ].map((item) => (
              <div key={item.title} className="rounded-3xl border border-white/10 bg-slate-950/80 p-5">
                <p className="text-lg font-semibold text-white">{item.title}</p>
                <p className="mt-2 text-sm text-slate-400">{item.description}</p>
              </div>
            ))}
          </div>
        </div>
        <div className="grid gap-6">
          {roleCards.map((role) => (
            <div key={role.title} className="glass-card p-8">
              <div className={`inline-flex rounded-full px-4 py-2 text-sm font-semibold ${role.accent}`}>{role.title}</div>
              <p className="mt-5 text-slate-300">{role.description}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="space-y-8">
        <div className="space-y-3 text-center">
          <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Ready to experience smarter printing?</p>
          <h2 className="text-4xl font-semibold text-white">Everything you need to run print jobs, referrals, and shop logistics.</h2>
        </div>
        <div className="grid gap-6 lg:grid-cols-3">
          {[
            { title: 'Custom order creation', details: 'Upload design files, add instructions, and estimate delivery with clarity.' },
            { title: 'Commission & wallet', details: 'Track ambassador earnings, points balance, and withdraw with ease.' },
            { title: 'Production tracking', details: 'Keep jobs moving through shop queues, dispatch, and delivery milestones.' },
          ].map((item) => (
            <div key={item.title} className="glass-card p-8 transition hover:-translate-y-1 hover:border-indigo-500/20">
              <h3 className="text-2xl font-semibold text-white">{item.title}</h3>
              <p className="mt-4 text-slate-400">{item.details}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="glass-card p-10">
        <div className="sm:flex sm:items-center sm:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Support your print business</p>
            <h2 className="mt-3 text-3xl font-semibold text-white">Launch your print brand with confidence.</h2>
            <p className="mt-4 max-w-2xl text-slate-300">
              Whether you're ordering a batch of tees, promoting a referral program, or managing shop capacity, Print Your Fit gives you the tools to scale without friction.
            </p>
          </div>
          <Link to="/register" className="mt-8 inline-flex rounded-full bg-indigo-500 px-7 py-3 text-base font-semibold text-white shadow-lg shadow-indigo-500/20 transition hover:bg-indigo-400 sm:mt-0">
            Get started now
          </Link>
        </div>
      </section>
    </div>
  )
}
