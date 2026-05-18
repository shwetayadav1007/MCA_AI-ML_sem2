import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import DashboardPage from './pages/DashboardPage'
import UploadPage from './pages/UploadPage'
import TrainPage from './pages/TrainPage'
import PredictPage from './pages/PredictPage'
import AnalyticsPage from './pages/AnalyticsPage'
import WeatherPage from './pages/WeatherPage'
import HeatmapPage from './pages/HeatmapPage'
import AlertsPage from './pages/AlertsPage'
import ReportsPage from './pages/ReportsPage'
import SettingsPage from './pages/SettingsPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<DashboardPage />} />
        <Route path="upload" element={<UploadPage />} />
        <Route path="train" element={<TrainPage />} />
        <Route path="predict" element={<PredictPage />} />
        <Route path="analytics" element={<AnalyticsPage />} />
        <Route path="weather" element={<WeatherPage />} />
        <Route path="heatmap" element={<HeatmapPage />} />
        <Route path="alerts" element={<AlertsPage />} />
        <Route path="reports" element={<ReportsPage />} />
        <Route path="settings" element={<SettingsPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
