import { useEffect, useState } from 'react'
import Api from '../api/Api'

function Spinner() {
  return (
    <div className="flex items-center justify-center">
      <div className="h-8 w-8 animate-spin rounded-full border-4 border-t-transparent border-white/30" />
    </div>
  )
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000'

export default function WeatherCard() {
  const [weather, setWeather] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchWeather = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await Api.get('/current-weather')
      setWeather(data)
    } catch (err) {
      setError(err?.error || err?.message || 'Failed to fetch weather')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchWeather()
    const id = setInterval(fetchWeather, 5 * 60 * 1000) // 5 minutes
    return () => clearInterval(id)
  }, [])

  return (
    <div className="rounded-2xl bg-gradient-to-br from-sky-500 to-cyan-600 p-5 shadow-lg text-white">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-wider opacity-90">Live Weather</p>
          <h3 className="text-2xl font-semibold mt-1">Current conditions</h3>
        </div>
        <div className="w-16">
          {/* simple animated temperature circle */}
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-white/20 animate-pulse">
            <span className="text-lg font-semibold">{weather ? `${weather.temperature}°C` : '--'}</span>
          </div>
        </div>
      </div>

      <div className="mt-4">
        {loading && <Spinner />}
        {error && <p className="text-sm text-rose-200">{error}</p>}
        {weather && !loading && (
          <div className="mt-2 grid grid-cols-2 gap-3 text-sm">
            <div className="rounded-lg bg-white/10 p-3">
              <p className="text-xs text-white/80">Humidity</p>
              <p className="mt-1 text-lg font-medium">{weather.humidity ?? '--'}%</p>
            </div>
            <div className="rounded-lg bg-white/10 p-3">
              <p className="text-xs text-white/80">Rainfall</p>
              <p className="mt-1 text-lg font-medium">{weather.rainfall ?? '--'} mm</p>
            </div>
            <div className="col-span-2 mt-1 rounded-lg bg-white/10 p-3">
              <p className="text-xs text-white/80">Condition</p>
              <p className="mt-1 text-lg font-medium">{weather.weather}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
