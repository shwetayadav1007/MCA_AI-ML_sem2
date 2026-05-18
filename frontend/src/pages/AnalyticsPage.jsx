import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import Api from '../api/Api'

export default function AnalyticsPage(){
  const [data,setData] = useState(null)
  const [loading,setLoading] = useState(false)

  useEffect(()=>{
    const load = async ()=>{
      setLoading(true)
      try{
        const res = await Api.get('/analytics')
        setData(res.data)
      }catch(e){
        // fallback sample
        setData([
          { name: 'Jan', actual: 45, predicted: 48 },
          { name: 'Feb', actual: 44, predicted: 46 },
          { name: 'Mar', actual: 40, predicted: 42 },
          { name: 'Apr', actual: 38, predicted: 39 },
          { name: 'May', actual: 50, predicted: 49 },
        ])
      }finally{setLoading(false)}
    }
    load()
  },[])

  return (
    <div className="space-y-6">
      <div className="rounded-3xl bg-slate-900/90 p-6 shadow-glow border border-white/10">
        <h2 className="text-xl font-semibold text-white">Analytics</h2>
        <p className="mt-2 text-sm text-slate-400">Visualize trends and model performance.</p>

        <div className="mt-6 h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data || []}>
              <CartesianGrid stroke="#334155" />
              <XAxis dataKey="name" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip />
              <Line type="monotone" dataKey="actual" stroke="#38bdf8" strokeWidth={2} />
              <Line type="monotone" dataKey="predicted" stroke="#7dd3fc" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
