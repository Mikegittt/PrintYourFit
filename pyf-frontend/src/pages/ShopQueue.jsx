export default function ShopQueue() {
  return (
    <div className="space-y-8">
      <div className="glass-card p-8">
        <p className="text-sm uppercase tracking-[0.24em] text-cyan-200">Print shop queue</p>
        <h1 className="mt-3 text-4xl font-semibold text-white">Manage active production jobs</h1>
        <p className="mt-4 text-slate-300">Review in-progress orders, dispatch status, and estimated delivery times in your shop dashboard.</p>
      </div>
      <div className="grid gap-6 xl:grid-cols-2">
        <div className="glass-card p-8">
          <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Next shipment</p>
          <h2 className="mt-3 text-2xl font-semibold text-white">3 orders ready for print</h2>
          <p className="mt-4 text-slate-300">Keep your production pipeline moving with clear task prioritization and customer expectations.</p>
        </div>
        <div className="glass-card p-8">
          <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Verification</p>
          <h2 className="mt-3 text-2xl font-semibold text-white">Shop accreditation status</h2>
          <p className="mt-4 text-slate-300">Ensure your shop is verified to receive priority print orders from ambassadors and customers.</p>
        </div>
      </div>
    </div>
  )
}
