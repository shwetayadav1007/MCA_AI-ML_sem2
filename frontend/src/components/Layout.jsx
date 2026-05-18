import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import TopNav from './TopNav'

function Layout() {
  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(56,189,248,0.18),transparent_35%),linear-gradient(180deg,_#020617_0%,_#091d30_100%)] text-slate-100">
      <div className="grid min-h-screen grid-cols-[280px_1fr] gap-6 px-6 py-6 xl:px-10">
        <Sidebar />
        <main className="space-y-8">
          <TopNav />
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default Layout
