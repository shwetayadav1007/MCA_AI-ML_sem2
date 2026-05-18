import { motion } from 'framer-motion'
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Line,
  LineChart,
} from 'recharts'
import StatCard from '../components/StatCard'
import PredictionForm from '../components/PredictionForm'
import RiskSummary from '../components/RiskSummary'

const stats = [
  { label: 'Current Groundwater Level', value: '58%', change: '+2.1%' },
  { label: 'Rainfall This Month', value: '112 mm', change: '-8.3%' },
  { label: 'Water Usage %', value: '72%', change: '+4.3%' },
  { label: 'Drought Risk', value: 'Moderate', change: '-1' },
]

const rainfallData = [
  { name: 'Jan', Rainfall: 120, Groundwater: 45 },
  { name: 'Feb', Rainfall: 130, Groundwater: 44 },
  { name: 'Mar', Rainfall: 150, Groundwater: 40 },
  { name: 'Apr', Rainfall: 160, Groundwater: 38 },
  { name: 'May', Rainfall: 95, Groundwater: 50 },
  { name: 'Jun', Rainfall: 55, Groundwater: 58 },
  { name: 'Jul', Rainfall: 30, Groundwater: 64 },
]

const usageData = [
  { name: 'Jan', WaterUsage: 210 },
  { name: 'Feb', WaterUsage: 230 },
  { name: 'Mar', WaterUsage: 215 },
  { name: 'Apr', WaterUsage: 185 },
  { name: 'May', WaterUsage: 260 },
  { name: 'Jun', WaterUsage: 380 },
  { name: 'Jul', WaterUsage: 430 },
]

export default function DashboardPage() {
  return (
    <>
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="rounded-[2.5rem] border border-white/10 bg-slate-900/80 p-8 shadow-[0_25px_80px_rgba(14,165,233,0.12)] backdrop-blur-xl"
      >
        <div className="grid gap-6 xl:grid-cols-[1.7fr_0.9fr] xl:items-center">
          <div className="space-y-5">
            <p className="text-sm uppercase tracking-[0.35em] text-cyan-300">Smart Groundwater Prediction System</p>
            <h1 className="max-w-3xl text-4xl font-semibold leading-tight text-white sm:text-5xl">
              Future-ready groundwater forecasting for sustainable water security
            </h1>
            <p className="max-w-2xl text-lg text-slate-300">
              A next-level SIH dashboard with AI risk alerts, visual analytics, and prediction controls that help governments manage groundwater resources smarter.
            </p>
          </div>
          <div className="rounded-[2rem] bg-slate-950/80 p-6 shadow-xl border border-white/10">
            <p className="text-sm uppercase tracking-[0.3em] text-cyan-300">Live risk snapshot</p>
            <div className="mt-6 rounded-[1.75rem] bg-slate-900/95 p-6 ring-1 ring-white/10">
              <p className="text-sm text-slate-400">Current groundwater health</p>
              <p className="mt-4 text-3xl font-semibold text-white">Moderate</p>
              <p className="mt-3 text-slate-300">Critical zones detected in West region; conserve water usage and monitor rainfall closely.</p>
            </div>
          </div>
        </div>
      </motion.section>

      <section className="grid gap-6 xl:grid-cols-[1.35fr_0.85fr] mt-6">
        <div className="grid gap-6">
          <div className="grid gap-4 md:grid-cols-2">
            {stats.map((s) => (
              <StatCard key={s.label} {...s} />
            ))}
          </div>

          <div className="rounded-[2rem] bg-slate-900/90 p-6 shadow-glow border border-white/10">
            <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
              <div>
                <h2 className="text-xl font-semibold text-white">Groundwater & rain forecast</h2>
                <p className="text-sm text-slate-400">AI trend line for the next recharge cycle.</p>
              </div>
              <div className="rounded-full bg-slate-950/80 px-4 py-2 text-sm text-cyan-200 ring-1 ring-white/10">Confidence: 92%</div>
            </div>
            <div className="mt-6 h-[340px]">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={rainfallData} margin={{ top: 10, right: 20, left: -18, bottom: 0 }}>
                  <defs>
                    <linearGradient id="waterGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.6} />
                      <stop offset="95%" stopColor="#0f172a" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
                  <XAxis dataKey="name" stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" />
                  <Tooltip contentStyle={{ backgroundColor: '#020617', border: '1px solid #334155' }} />
                  <Area type="monotone" dataKey="Rainfall" stroke="#38bdf8" strokeWidth={3} fill="url(#waterGradient)" />
                  <Line type="monotone" dataKey="Groundwater" stroke="#7dd3fc" strokeWidth={3} dot={false} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        <aside className="space-y-6">
          <PredictionForm />
          <RiskSummary />
        </aside>
      </section>
    </>
  )
}
