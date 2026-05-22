import { useEffect, useState } from 'react'
import Api from '../api/Api'

export default function WeatherPage() {
  const [currentWeather, setCurrentWeather] = useState(null)
  const [forecast, setForecast] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const loadWeather = async () => {
      setLoading(true)
      setError(null)

      try {
        const current = await Api.get('/current-weather')
        setCurrentWeather(current)

        const forecastResponse = await Api.get('/weather-data')
        const daily = forecastResponse?.weather?.daily || {}
        const dates = daily?.time || []
        const highs = daily?.temperature_2m_max || []
        const lows = daily?.temperature_2m_min || []
        const rain = daily?.rain_sum || []

        const forecastItems = dates.slice(0, 4).map((date, index) => ({
          date,
          high: highs[index],
          low: lows[index],
          rain: rain[index],
        }))
        setForecast(forecastItems)
      } catch (err) {
        setError(err?.error || err?.message || 'Unable to load weather monitoring data.')
      } finally {
        setLoading(false)
      }
    }

    loadWeather()
  }, [])

  return (
    <div className="space-y-6">
      <div className="rounded-3xl bg-slate-900/90 p-6 shadow-glow border border-white/10">
        <h2 className="text-xl font-semibold text-white">Weather Monitoring</h2>
        <p className="mt-2 text-sm text-slate-400">Live weather information and forecast.</p>

        {loading ? (
          <div className="mt-6 text-slate-300">Loading weather data…</div>
        ) : error ? (
          <div className="mt-6 rounded-3xl bg-rose-500/10 p-4 text-rose-200">{error}</div>
        ) : (
          <>
            <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="rounded-3xl bg-slate-950/80 p-4">
                <p className="text-sm text-slate-400">Temperature</p>
                <p className="mt-2 text-2xl font-semibold text-white">{currentWeather?.temperature ?? '--'}°C</p>
              </div>
              <div className="rounded-3xl bg-slate-950/80 p-4">
                <p className="text-sm text-slate-400">Rainfall</p>
                <p className="mt-2 text-2xl font-semibold text-white">{currentWeather?.rainfall ?? '--'} mm</p>
              </div>
              <div className="rounded-3xl bg-slate-950/80 p-4">
                <p className="text-sm text-slate-400">Humidity</p>
                <p className="mt-2 text-2xl font-semibold text-white">{currentWeather?.humidity ?? '--'}%</p>
              </div>
            </div>

            <div className="mt-6 rounded-3xl bg-slate-950/80 p-5">
              <p className="text-sm text-slate-400 uppercase tracking-[0.3em]">Current Conditions</p>
              <p className="mt-3 text-3xl font-semibold text-white">{currentWeather?.weather ?? 'Unknown'}</p>
            </div>

            <div className="mt-6">
              <h3 className="text-lg font-semibold text-white">Forecast</h3>
              <div className="mt-4 grid gap-4 sm:grid-cols-4">
                {forecast.map((item) => (
                  <div key={item.date} className="rounded-3xl bg-slate-950/80 p-4">
                    <p className="text-sm text-slate-400">{item.date}</p>
                    <p className="mt-2 text-xl font-semibold text-white">{item.high ?? '--'}° / {item.low ?? '--'}°</p>
                    <p className="mt-1 text-sm text-slate-400">Rain: {item.rain ?? '--'} mm</p>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
