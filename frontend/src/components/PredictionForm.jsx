import { useState, useEffect } from 'react'
import Api from '../api/Api'

const defaultState = {
  Rainfall: 100,
  Temperature: 30,
  Humidity: 60,
  Soil_Moisture: 30,
  Water_Usage: 220,
  Season: 'Summer',
}

function PredictionForm() {
  const [form, setForm] = useState(defaultState)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [liveLoading, setLiveLoading] = useState(false)
  const [liveError, setLiveError] = useState(null)

  useEffect(() => {
    // auto-fill the Temperature field from backend `/current-weather` if available
    const fetchLive = async () => {
      setLiveLoading(true)
      try {
        const json = await Api.get('/current-weather')
        if (json.temperature !== null && json.temperature !== undefined) {
          setForm((s) => ({ ...s, Temperature: json.temperature }))
        }
      } catch (err) {
        setLiveError(err?.error || err?.message || 'Live weather unavailable')
      } finally {
        setLiveLoading(false)
      }
    }
    fetchLive()
  }, [])

  const handleChange = (key) => (event) => {
    setForm({ ...form, [key]: event.target.value })
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError(null)
    setResult(null)
    setLoading(true)

    const payload = {
      Rainfall: parseFloat(form.Rainfall),
      Temperature: parseFloat(form.Temperature),
      Humidity: parseFloat(form.Humidity),
      Soil_Moisture: parseFloat(form.Soil_Moisture),
      Water_Usage: parseFloat(form.Water_Usage),
      Season: form.Season,
    }

    if (Object.values(payload).slice(0, 5).some((value) => Number.isNaN(value))) {
      setError('Please enter valid numeric values for all input fields.')
      setLoading(false)
      return
    }

    try {
      const data = await Api.post('/predict', payload)
      setResult(data)
    } catch (err) {
      console.error('Prediction error', err)
      const message = err?.error || err?.message || JSON.stringify(err)
      setError(message || 'Prediction failed — check backend')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="rounded-3xl bg-slate-900/90 p-6 shadow-glow border border-white/10">
      <h3 className="text-xl font-semibold text-white">Live Groundwater Prediction</h3>
      <p className="mt-2 text-sm text-slate-400">Enter the latest environmental inputs and receive a smart forecast.</p>

      <form onSubmit={handleSubmit} className="mt-6 grid gap-4">
        {['Rainfall', 'Temperature', 'Humidity', 'Soil_Moisture', 'Water_Usage'].map((field) => (
          <label key={field} className="grid gap-2 text-sm text-slate-200">
            {field.replace('_', ' ')}
            <input
              type="number"
              value={form[field]}
              onChange={handleChange(field)}
              className="rounded-3xl border border-white/10 bg-slate-950/80 px-4 py-3 text-slate-100 focus:border-cyan-400 focus:outline-none"
            />
          </label>
        ))}

        {liveLoading && <p className="text-sm text-slate-400">Fetching live temperature...</p>}
        {liveError && <p className="text-sm text-rose-400">{liveError}</p>}

        <label className="grid gap-2 text-sm text-slate-200">
          Season
          <select
            value={form.Season}
            onChange={handleChange('Season')}
            className="rounded-3xl border border-white/10 bg-slate-950/80 px-4 py-3 text-slate-100 focus:border-cyan-400 focus:outline-none"
          >
            <option>Winter</option>
            <option>Spring</option>
            <option>Summer</option>
            <option>Monsoon</option>
          </select>
        </label>

        <div className="flex gap-3">
          <button type="submit" disabled={loading} className="rounded-3xl bg-cyan-500 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:opacity-60">
            {loading ? 'Predicting...' : 'Predict Now'}
          </button>
          <button type="button" onClick={() => { setForm(defaultState); setResult(null); setError(null) }} className="rounded-3xl bg-slate-800 px-5 py-3 text-sm font-semibold text-slate-200">
            Reset
          </button>
        </div>
      </form>

      {error && <p className="mt-4 rounded-3xl bg-rose-500/10 p-4 text-sm text-rose-300">{error}</p>}
      {result && !error && (
        <div className="mt-5 rounded-3xl bg-slate-950/80 p-5 text-slate-200">
          <p className="text-sm text-cyan-300 uppercase tracking-[0.3em]">Prediction result</p>
          <p className="mt-3 text-3xl font-semibold text-white">{result.groundwater_level ?? JSON.stringify(result)}</p>
          {result.risk_category && <p className="mt-2 text-slate-400">Risk: {result.risk_category}</p>}
          {result.recommendation && <p className="mt-3 text-sm text-slate-400">{result.recommendation}</p>}
        </div>
      )}
    </div>
  )
}

export default PredictionForm
