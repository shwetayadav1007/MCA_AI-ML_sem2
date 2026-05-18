import { useEffect, useState } from 'react'
import Api from '../api/Api'

export default function AlertsPage(){
  const [alerts, setAlerts] = useState([])

  useEffect(()=>{
    const load = async()=>{
      try{
        const res = await Api.get('/alerts')
        setAlerts(res.data || [])
      }catch(e){
        setAlerts([
          { id:1, text: 'Groundwater depletion warning — West zone', level: 'high' },
          { id:2, text: 'Low rainfall expected next week', level: 'medium' },
        ])
      }
    }
    load()
  },[])

  const resolve = async (id)=>{
    try{
      await Api.post('/alerts/resolve', { id })
      setAlerts((a)=>a.filter(x=>x.id!==id))
    }catch(e){
      alert('Resolve failed')
    }
  }

  return (
    <div className="space-y-6">
      <div className="rounded-3xl bg-slate-900/90 p-6 shadow-glow border border-white/10">
        <h2 className="text-xl font-semibold text-white">AI Alerts</h2>
        <p className="mt-2 text-sm text-slate-400">Active alerts from model and sensors.</p>

        <div className="mt-6 space-y-3">
          {alerts.map(a=> (
            <div key={a.id} className="rounded-2xl bg-slate-950/80 p-4 flex items-start justify-between">
              <div>
                <p className="text-sm text-white">{a.text}</p>
                <p className="text-xs text-slate-400 mt-1">Level: {a.level}</p>
              </div>
              <div className="flex gap-2">
                <button onClick={()=>resolve(a.id)} className="rounded-2xl bg-emerald-500 px-3 py-2 text-sm">Mark Resolved</button>
                <button onClick={()=>alert('Exported')} className="rounded-2xl bg-slate-800 px-3 py-2 text-sm">Export</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
