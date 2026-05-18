import { useState, useRef } from 'react'
import Api from '../api/Api'

export default function UploadPage() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [message, setMessage] = useState(null)
  const inputRef = useRef()

  const handleFile = (f) => {
    setFile(f)
    const reader = new FileReader()
    reader.onload = (e) => setPreview(e.target.result)
    reader.readAsText(f)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const f = e.dataTransfer.files[0]
    if (f) handleFile(f)
  }

  const upload = async () => {
    if (!file) return setMessage('Select a CSV first')
    setMessage('Uploading...')
    const fd = new FormData()
    fd.append('file', file)
    try {
      const { data } = await Api.post('/upload-dataset', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
      setMessage(data.message || 'Uploaded')
    } catch (err) {
      setMessage(err.error || 'Upload failed')
    }
  }

  return (
    <div className="space-y-6">
      <div className="rounded-3xl bg-slate-900/90 p-6 shadow-glow border border-white/10">
        <h2 className="text-xl font-semibold text-white">Upload Dataset</h2>
        <p className="mt-2 text-sm text-slate-400">Upload CSV data for training and analytics.</p>

        <div onDragOver={(e)=>e.preventDefault()} onDrop={handleDrop} className="mt-6 rounded-2xl border-2 border-dashed border-white/10 p-6 text-center">
          <p className="text-sm text-slate-400">Drag & drop CSV here or</p>
          <button onClick={()=>inputRef.current.click()} className="mt-4 rounded-full bg-cyan-500 px-4 py-2 text-sm font-semibold">Select file</button>
          <input ref={inputRef} type="file" accept=".csv" className="hidden" onChange={(e)=>handleFile(e.target.files[0])} />
        </div>

        {file && (
          <div className="mt-4 rounded-2xl bg-slate-950/80 p-4 text-slate-200">
            <p className="font-semibold">{file.name}</p>
            <div className="mt-3 max-h-40 overflow-auto text-xs whitespace-pre-wrap text-slate-300">{preview?.slice(0, 2000)}</div>
            <div className="mt-4 flex gap-3">
              <button onClick={upload} className="rounded-3xl bg-cyan-500 px-4 py-2 text-sm font-semibold">Upload</button>
              <button onClick={()=>{ setFile(null); setPreview(null); setMessage(null) }} className="rounded-3xl bg-slate-800 px-4 py-2 text-sm">Remove</button>
            </div>
          </div>
        )}

        {message && <p className="mt-3 text-sm text-cyan-200">{message}</p>}
      </div>
    </div>
  )
}
