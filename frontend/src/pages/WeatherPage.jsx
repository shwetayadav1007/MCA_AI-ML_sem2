import { useEffect, useState } from 'react'
import Api from '../api/Api'

export default function WeatherPage(){
  const [weather,setWeather] = useState(null)

  useEffect(()=>{
    const load = async()=>{
      try{
        const res = await Api.get('/weather-data')
        setWeather(res.data)
      }catch(e){
        setWeather({ temp: 'N/A', rain_forecast: 'N/A', humidity: 'N/A' })
      }
    }
    load()
  },[])

  return (
    <div className="space-y-6">
      <div className="rounded-3xl bg-slate-900/90 p-6 shadow-glow border border-white/10">
        <h2 className="text-xl font-semibold text-white">Weather Monitoring</h2>
        <p className="mt-2 text-sm text-slate-400">Live weather information and forecast.</p>

        <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="rounded-3xl bg-slate-950/80 p-4">
            <p className="text-sm text-slate-400">Temperature</p>
            <p className="mt-2 text-2xl font-semibold text-white">{weather?.temp ?? '--'}°C</p>
          </div>
          <div className="rounded-3xl bg-slate-950/80 p-4">
            <p className="text-sm text-slate-400">Rain Forecast</p>
            <p className="mt-2 text-2xl font-semibold text-white">{weather?.rain_forecast ?? '--'}</p>
          </div>
          <div className="rounded-3xl bg-slate-950/80 p-4">
            <p className="text-sm text-slate-400">Humidity</p>
            <p className="mt-2 text-2xl font-semibold text-white">{weather?.humidity ?? '--'}%</p>
          </div>
        </div>
      </div>
    </div>
  )
}
