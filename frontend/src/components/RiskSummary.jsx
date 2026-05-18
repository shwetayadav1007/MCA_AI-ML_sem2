function RiskSummary() {
  return (
    <div className="space-y-6 rounded-3xl bg-slate-900/90 p-6 shadow-glow border border-white/10">
      <div>
        <p className="text-sm uppercase tracking-[0.3em] text-cyan-300">Regional risk overview</p>
        <h3 className="mt-3 text-2xl font-semibold text-white">Village heatmap insights</h3>
      </div>
      <div className="grid gap-4 rounded-3xl bg-slate-950/70 p-5 text-slate-200">
        <div className="flex items-center justify-between gap-4 rounded-3xl bg-slate-800/70 p-4">
          <div>
            <p className="text-sm text-slate-400">North Zone</p>
            <p className="mt-2 text-lg font-semibold text-white">Safe</p>
          </div>
          <span className="rounded-full bg-emerald-400/15 px-3 py-2 text-sm text-emerald-300">Stable</span>
        </div>
        <div className="flex items-center justify-between gap-4 rounded-3xl bg-slate-800/70 p-4">
          <div>
            <p className="text-sm text-slate-400">South Zone</p>
            <p className="mt-2 text-lg font-semibold text-white">Moderate</p>
          </div>
          <span className="rounded-full bg-amber-400/15 px-3 py-2 text-sm text-amber-300">Watch</span>
        </div>
        <div className="flex items-center justify-between gap-4 rounded-3xl bg-slate-800/70 p-4">
          <div>
            <p className="text-sm text-slate-400">West Zone</p>
            <p className="mt-2 text-lg font-semibold text-white">Critical</p>
          </div>
          <span className="rounded-full bg-rose-400/15 px-3 py-2 text-sm text-rose-300">Action</span>
        </div>
      </div>
    </div>
  )
}

export default RiskSummary
