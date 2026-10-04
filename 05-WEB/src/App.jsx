import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import Sidebar from './components/Sidebar'
import ProtectedRoute from './components/ProtectedRoute'
import Dashboard from './pages/Dashboard'
import Predicoes from './pages/Predicoes'
import Salas from './pages/Salas'
import Alunos from './pages/Alunos'
import AlunoDetalhe from './pages/AlunoDetalhe'
import Materias from './pages/Materias'
import Notas from './pages/Notas'
import Relatorio from './pages/Relatorio'
import Configuracoes from './pages/Configuracoes'
import Usuarios from './pages/Usuarios'
import ModelSelect from './pages/ModelSelect'
import Login from './pages/Login'
import Exportar from './pages/Exportar'
import Importar from './pages/Importar'
import Pesquisa from './pages/Pesquisa'

function RootRedirect() {
  const { isLoggedIn } = useAuth()
  if (!isLoggedIn) return <Navigate to="/login" replace />
  const hasModel = !!localStorage.getItem('activeModel')
  return <Navigate to={hasModel ? '/dashboard' : '/model-select'} replace />
}

function AppShell() {
  return (
    <div className="flex h-screen bg-app-bg overflow-hidden">
      <Sidebar />
      <main className="flex-1 overflow-auto">
        <Routes>
          <Route path="/dashboard"  element={<Dashboard />} />
          <Route path="/predicoes"  element={<Predicoes />} />
          <Route path="/salas"      element={<Salas />} />
          <Route path="/alunos"     element={<Alunos />} />
          <Route path="/alunos/:id" element={<AlunoDetalhe />} />
          <Route path="/materias"   element={<Materias />} />
          <Route path="/notas"      element={<Notas />} />
          <Route path="/relatorio"  element={<Relatorio />} />
          <Route path="/config"     element={
            <ProtectedRoute roles={['desenvolvedor','coordenador','admin']}>
              <Configuracoes />
            </ProtectedRoute>
          } />
          <Route path="/usuarios"   element={
            <ProtectedRoute roles={['desenvolvedor','coordenador','admin']}>
              <Usuarios />
            </ProtectedRoute>
          } />
          <Route path="/importar"   element={<Importar />} />
          <Route path="/exportar"   element={<Exportar />} />
          <Route path="/pesquisa"   element={<Pesquisa />} />
          <Route path="*"           element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </main>
    </div>
  )
}

export default function App() {
  const { isLoggedIn } = useAuth()
  return (
    <Routes>
      <Route path="/"             element={<RootRedirect />} />
      <Route path="/login"        element={isLoggedIn ? <Navigate to="/" replace /> : <Login />} />
      <Route path="/model-select" element={
        <ProtectedRoute><ModelSelect /></ProtectedRoute>
      } />
      <Route path="/*"            element={
        <ProtectedRoute><AppShell /></ProtectedRoute>
      } />
    </Routes>
  )
}
