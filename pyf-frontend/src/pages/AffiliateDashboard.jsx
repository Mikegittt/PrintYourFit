export default function AffiliateDashboard() {
  return (
    <div className="space-y-8">
      <div className="glass-card p-8">
        <p className="text-sm uppercase tracking-[0.24em] text-indigo-200">Ambassador dashboard</p>
        <h1 className="mt-3 text-4xl font-semibold text-white">Track referrals and cashout milestones</h1>
        <p className="mt-4 text-slate-300">Monitor your points, referral link performance, and payout options in one polished ambassador workspace.</p>
      </div>
      <div className="grid gap-6 xl:grid-cols-2">
        <div className="glass-card p-8">
          <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Points balance</p>
          <p className="mt-3 text-5xl font-semibold text-white">480</p>
          <p className="mt-4 text-slate-300">Points are earned from completed orders and convert to cashout value automatically.</p>
        </div>
        <div className="glass-card p-8">
          <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Referral link</p>
          <p className="mt-3 break-all text-xl font-semibold text-white">https://printyourfit.app/ref/your-code</p>
          <p className="mt-4 text-slate-300">Share this link to start earning while your network orders print jobs.</p>
        </div>
      </div>
      <div className="glass-card p-8">
        <div className="grid gap-4 sm:grid-cols-3">
          {[
            { title: 'Cashout ready', value: 'Yes' },
            { title: 'Next payout', value: '24h' },
            { title: 'Open referrals', value: '12' },
          ].map((item) => (
            <div key={item.title} className="rounded-3xl bg-slate-950/80 p-5 text-slate-200">
              <p className="text-sm uppercase tracking-[0.24em] text-slate-500">{item.title}</p>
              <p className="mt-3 text-2xl font-semibold text-white">{item.value}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
