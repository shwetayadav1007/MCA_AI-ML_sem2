import { NavLink } from 'react-router-dom'

const navigation = [
  { label: 'Dashboard', to: '/', icon: '📊' },
  { label: 'Upload Dataset', to: '/upload', icon: '📥' },
  { label: 'Train Model', to: '/train', icon: '🧠' },
  { label: 'Predictions', to: '/predict', icon: '🔮' },
  { label: 'Analytics', to: '/analytics', icon: '📈' },
  { label: 'Weather Monitoring', to: '/weather', icon: '☁️' },
  { label: 'Heatmap', to: '/heatmap', icon: '🌡️' },
  { label: 'Alerts', to: '/alerts', icon: '🚨' },
  { label: 'Reports', to: '/reports', icon: '📄' },
  { label: 'Settings', to: '/settings', icon: '⚙️' },
]

function Sidebar() {
  return (
    <aside className="flex min-h-screen flex-col bg-slate-950/95 border-r border-white/10 p-6 text-slate-100 shadow-glow">
      <div className="mb-8">
        <div className="inline-flex h-16 w-16 items-center justify-center rounded-3xl bg-gradient-to-br from-cyan-400/20 to-sky-500/10 text-cyan-200 ring-1 ring-cyan-300/20">
          SI
        </div>
        <div className="mt-4">
          <p className="text-sm uppercase tracking-[0.3em] text-cyan-300">Groundwater of India</p>
          <h2 className="mt-2 text-2xl font-semibold">Groundwater AI</h2>
        </div>
      </div>
      <nav className="flex flex-col gap-3">
        {navigation.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-3xl border px-4 py-4 text-sm transition ${
                isActive ? 'bg-cyan-500/12 ring-1 ring-cyan-400/30 text-cyan-100 border-cyan-400/30' : 'bg-slate-900/60 text-slate-200 border-white/10 hover:border-cyan-400/30 hover:bg-cyan-500/8'
              }`
            }
          >
            <span className="inline-flex h-10 w-10 items-center justify-center rounded-2xl bg-slate-900/80 text-lg">
              {item.icon}
            </span>
            <span className="grow text-left">{item.label}</span>
          </NavLink>
        ))}
      </nav>
      <div className="mt-auto rounded-3xl bg-slate-900/80 p-5 text-slate-300 ring-1 ring-white/10">
        <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Live Status</p>
        <p className="mt-3 text-lg font-semibold text-emerald-300">Connected</p>
        <p className="text-sm text-slate-400">Weather API and prediction engine ready.</p>
      </div>
    </aside>
  )
}

export default Sidebar
