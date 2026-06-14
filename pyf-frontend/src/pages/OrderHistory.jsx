export default function OrderHistory() {
  return (
    <div className="space-y-8">
      <div className="glass-card p-8">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Order history</p>
            <h1 className="mt-3 text-3xl font-semibold text-white">Track every print request</h1>
          </div>
          <button className="rounded-full bg-indigo-500 px-5 py-3 text-sm font-semibold text-white transition hover:bg-indigo-400">Create new order</button>
        </div>
      </div>
      <div className="glass-card p-8">
        <p className="text-slate-300">Your detailed order history will be displayed here as soon as you place your first print job. Each entry will include job status, payment reference, assigned print shop, and delivery tracking.</p>
      </div>
    </div>
  )
}
