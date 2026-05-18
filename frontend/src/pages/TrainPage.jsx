import { useState } from 'react'
import Api from '../api/Api'

export default function TrainPage() {
  const [algo, setAlgo] = useState('RandomForest')
  const [training, setTraining] = useState(false)
  const [metrics, setMetrics] = useState(null)

  const train = async () => {
    setTraining(true)
    setMetrics(null)
    try {
      const { data } = await Api.post('/train-model', { algorithm: algo })
      setMetrics(data)
    } catch (err) {
      setMetrics({ error: err.error || 'Training failed' })
    } finally {
      setTraining(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="rounded-3xl bg-slate-900/90 p-6 shadow-glow border border-white/10">
        <h2 className="text-xl font-semibold text-white">Model Training</h2>
        <p className="mt-2 text-sm text-slate-400">Train ML models with uploaded dataset.</p>

        <div className="mt-6 grid gap-4 sm:grid-cols-2">
          <label className="text-sm text-slate-200">Select algorithm
            <select value={algo} onChange={(e)=>setAlgo(e.target.value)} className="mt-2 rounded-3xl bg-slate-950/80 px-4 py-3">
              <option value="RandomForest">Random Forest</option>
              <option value="XGBoost">XGBoost</option>
              <option value="LinearRegression">Linear Regression</option>
              <option value="LSTM">LSTM</option>
            </select>
          </label>

          <div className="flex items-end gap-3">
            <button onClick={train} disabled={training} className="rounded-3xl bg-cyan-500 px-4 py-3 text-sm font-semibold disabled:opacity-60">
              {training ? 'Training...' : 'Train Model'}
            </button>
            <button onClick={()=>alert('Save model feature calls /save-model (implement backend)')} className="rounded-3xl bg-slate-800 px-4 py-3 text-sm">Save Model</button>
            <button onClick={()=>alert('Compare feature not implemented in UI yet')} className="rounded-3xl bg-slate-800 px-4 py-3 text-sm">Compare Models</button>
          </div>
        </div>

        {metrics && (
          <div className="mt-6 rounded-2xl bg-slate-950/80 p-4">
            {metrics.error ? (
              <p className="text-rose-300">{metrics.error}</p>
            ) : (
              <div>
                <p className="text-sm text-slate-400">Results</p>
                <pre className="mt-3 text-sm text-slate-200">{JSON.stringify(metrics, null, 2)}</pre>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
