function StatCard({ label, value, change }) {
  return (
    <div className="rounded-3xl border border-white/10 bg-slate-900/90 p-6 shadow-lg shadow-cyan-500/5">
      <p className="text-sm uppercase tracking-[0.25em] text-cyan-300">{label}</p>
      <p className="mt-5 text-3xl font-semibold text-white">{value}</p>
      <p className="mt-3 text-sm text-slate-400">{change} since last week</p>
    </div>
  )
}

export default StatCard
