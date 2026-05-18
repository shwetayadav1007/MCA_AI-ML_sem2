import PredictionForm from '../components/PredictionForm'

export default function PredictPage(){
  return (
    <div className="space-y-6">
      <div className="rounded-3xl bg-slate-900/90 p-6 shadow-glow border border-white/10">
        <h2 className="text-xl font-semibold text-white">Predictions</h2>
        <p className="mt-2 text-sm text-slate-400">Single-run predictions and AI recommendations.</p>
        <div className="mt-6">
          <PredictionForm />
        </div>
      </div>
    </div>
  )
}
