import Api from '../api/Api'

export default function ReportsPage(){
  const downloadCsv = async ()=>{
    try{
      const res = await Api.get('/generate-report?format=csv')
      // backend should return a downloadable URL or CSV content; this is a placeholder
      alert('Report requested; check backend response in network tab')
    }catch(e){
      alert('Failed to generate report')
    }
  }

  const downloadPdf = async ()=>{
    try{
      await Api.get('/generate-report?format=pdf')
      alert('PDF generated (backend dependent)')
    }catch(e){
      alert('Failed to generate PDF')
    }
  }

  return (
    <div className="space-y-6">
      <div className="rounded-3xl bg-slate-900/90 p-6 shadow-glow border border-white/10">
        <h2 className="text-xl font-semibold text-white">Reports</h2>
        <p className="mt-2 text-sm text-slate-400">Generate downloadable reports.</p>

        <div className="mt-6 flex gap-3">
          <button onClick={downloadPdf} className="rounded-3xl bg-cyan-500 px-4 py-3 text-sm">Download PDF</button>
          <button onClick={downloadCsv} className="rounded-3xl bg-slate-800 px-4 py-3 text-sm">Export CSV</button>
        </div>
      </div>
    </div>
  )
}
