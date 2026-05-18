import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

function TopNav() {
  const [now, setNow] = useState(new Date())

  useEffect(() => {
    const t = setInterval(() => setNow(new Date()), 1000)
    return () => clearInterval(t)
  }, [])

  return (
    <div className="flex flex-col gap-4 rounded-3xl bg-slate-900/85 p-6 shadow-glow border border-white/10 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p className="text-sm uppercase tracking-[0.3em] text-cyan-300">Dashboard</p>
        <h2 className="mt-2 text-2xl font-semibold text-white">AI Water Management Control Center</h2>
      </div>
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
        <div className="relative rounded-3xl bg-slate-950/80 px-4 py-3 text-slate-300 ring-1 ring-white/10">
          <input
            type="search"
            placeholder="Search insights"
            className="w-full bg-transparent text-sm text-slate-100 placeholder:text-slate-500 focus:outline-none"
          />
        </div>
        <Link to="/alerts" className="rounded-3xl bg-cyan-500 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400">
          Alerts
        </Link>
        <div className="inline-flex items-center gap-3 rounded-3xl bg-slate-800/70 px-4 py-3">
          <span className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-cyan-500/20 text-cyan-300">AI</span>
          <div>
            <p className="text-sm text-slate-400">GWP Admin</p>
            <p className="text-sm font-semibold text-white">SmartWater</p>
          </div>
        </div>
        <div className="ml-2 rounded-3xl bg-slate-800/70 px-4 py-3 text-sm text-slate-300">{now.toLocaleString()}</div>
      </div>
    </div>
  )
}

export default TopNav
