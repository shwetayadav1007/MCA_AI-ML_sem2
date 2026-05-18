import { useEffect, useState } from 'react'
import Api from '../api/Api'

export default function HeatmapPage(){
  const [points,setPoints] = useState([])

  useEffect(()=>{
    const load = async()=>{
      try{
        const res = await Api.get('/heatmap-data')
        setPoints(res.data || [])
      }catch(e){
        // sample points
        setPoints([
          { lat: 12.96, lon: 77.59, risk: 'High' },
          { lat: 13.02, lon: 77.55, risk: 'Moderate' },
        ])
      }
    }
    load()
  },[])

  return (
    <div className="space-y-6">
      <div className="rounded-3xl bg-slate-900/90 p-6 shadow-glow border border-white/10">
        <h2 className="text-xl font-semibold text-white">Groundwater Heatmap</h2>
        <p className="mt-2 text-sm text-slate-400">Interactive risk heatmap (Leaflet recommended).</p>

        <div className="mt-6 grid gap-4 sm:grid-cols-2">
          <div className="h-80 rounded-2xl bg-slate-950/80 p-4">Map container (add Leaflet to view map)</div>
          <div className="rounded-2xl bg-slate-950/80 p-4">
            <h3 className="text-sm text-slate-400">Active points</h3>
            <ul className="mt-3 space-y-2 text-slate-200 text-sm">
              {points.map((p, i) => (
                <li key={i}>{p.lat}, {p.lon} — {p.risk}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
