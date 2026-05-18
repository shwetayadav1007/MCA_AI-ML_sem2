import { useState } from 'react'

export default function SettingsPage(){
  const [apiUrl,setApiUrl] = useState(localStorage.getItem('GWP_API') || 'http://127.0.0.1:5000')
  const save = ()=>{
    localStorage.setItem('GWP_API', apiUrl)
    alert('API URL saved; reload app to apply (or update Api client)')
  }

  return (
    <div className="space-y-6">
      <div className="rounded-3xl bg-slate-900/90 p-6 shadow-glow border border-white/10 max-w-2xl">
        <h2 className="text-xl font-semibold text-white">Settings</h2>
        <p className="mt-2 text-sm text-slate-400">Configure API endpoints and preferences.</p>

        <div className="mt-6 grid gap-4">
          <label className="text-sm text-slate-200">API Base URL
            <input value={apiUrl} onChange={(e)=>setApiUrl(e.target.value)} className="mt-2 w-full rounded-3xl bg-slate-950/80 px-4 py-3" />
          </label>

          <div className="flex gap-3">
            <button onClick={save} className="rounded-3xl bg-cyan-500 px-4 py-3 text-sm">Save</button>
            <button onClick={()=>{ setApiUrl('http://127.0.0.1:5000'); localStorage.removeItem('GWP_API') }} className="rounded-3xl bg-slate-800 px-4 py-3 text-sm">Reset</button>
          </div>
        </div>
      </div>
    </div>
  )
}
