import { NavLink, useNavigate } from 'react-router-dom'
import {
  Home, Users, Building2, BookOpen, PenLine,
  Target, BarChart3, Upload, Download,
  Zap, GraduationCap, Settings, Loader2, LogOut, ShieldCheck,
  FlaskConical,
} from 'lucide-react'
import { useModel } from '../context/ModelContext'
import { useAuth } from '../context/AuthContext'

const MODEL_COLORS = {
  RF_M1: '#10B981',
  RF_M2: '#0EA5E9',
  RF_M3: '#4F46E5',
}

const NAV = [
  { to: '/dashboard', label: 'Dashboard',      Icon: Home,      section: 'PRINCIPAL' },
  { to: '/alunos',    label: 'Alunos',         Icon: Users },
  { to: '/salas',     label: 'Salas / Turmas', Icon: Building2 },
  { to: '/materias',  label: 'Matérias',       Icon: BookOpen },
  { to: '/notas',     label: 'Notas',          Icon: PenLine },
  { to: '/predicoes', label: 'Predições',      Icon: Target,    badge: 'IA', badgeAccent: true },
  { to: '/relatorio', label: 'Relatório',      Icon: BarChart3 },
  { to: '/pesquisa',  label: 'Pesquisa temporal', Icon: FlaskConical, badge: 'NOVO', badgeAccent: false },
  { to: '/config',    label: 'Machine Learning', Icon: Settings,     section: 'AVANÇADO', adminOnly: true },
  { to: '/usuarios',  label: 'Usuários',         Icon: ShieldCheck,  adminOnly: true },
  { to: '/importar',  label: 'Importar Excel',   Icon: Upload,       section: 'DADOS' },
  { to: '/exportar',  label: 'Exportar Excel',   Icon: Download },
]

function NavItem({ to, label, Icon, badge, badgeAccent }) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        `flex items-center gap-2.5 mx-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors cursor-pointer select-none
         ${isActive
           ? 'bg-accent text-white'
           : 'text-sb-text hover:bg-sidebar-h hover:text-slate-200'
         }`
      }
    >
      <Icon size={15} strokeWidth={1.75} className="flex-shrink-0" />
      <span className="flex-1">{label}</span>
      {badge && (
        <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded
          ${badgeAccent ? 'bg-accent text-white' : 'bg-sidebar-h text-muted-2'}`}>
          {badge}
        </span>
      )}
    </NavLink>
  )
}

const ROLE_COLORS = {
  desenvolvedor: '#4F46E5', admin: '#7C3AED', coordenador: '#0EA5E9',
  professor: '#10B981', aluno: '#F59E0B',
}
const ROLE_LABELS = {
  desenvolvedor: 'Dev', admin: 'Admin', coordenador: 'Coord.',
  professor: 'Professor', aluno: 'Aluno',
}

export default function Sidebar() {
  const { activeModel, models, switching, activateModel } = useModel()
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const canAdmin = ['desenvolvedor','coordenador','admin'].includes(user?.role)

  function handleLogout() {
    logout()
    navigate('/login', { replace: true })
  }

  return (
    <aside className="w-60 flex-shrink-0 bg-sidebar flex flex-col h-screen">
      {/* Logo */}
      <div className="flex items-center gap-3 px-4 py-4 border-b border-sidebar-h">
        <div className="w-8 h-8 bg-accent rounded-md flex items-center justify-center
                        text-white font-bold text-sm flex-shrink-0">
          <GraduationCap size={16} />
        </div>
        <div>
          <p className="text-white font-bold text-sm leading-tight">EduNotas</p>
          <p className="text-sb-sec text-[10px]">Sistema Escolar v2.0</p>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 py-3 overflow-y-auto space-y-0.5">
        {NAV.map((item) => {
          if (item.adminOnly && !canAdmin) return null
          return (
            <div key={item.to}>
              {item.section && (
                <p className="text-sb-sec text-[10px] font-bold px-5 pt-4 pb-1 uppercase tracking-widest">
                  {item.section}
                </p>
              )}
              <NavItem {...item} />
            </div>
          )
        })}
      </nav>

      {/* AI model panel — click to switch */}
      <div className="mx-3 mb-2 border border-slate-700 rounded-xl bg-sidebar-h px-3 py-2.5">
        <p className="text-accent-l text-[10px] font-bold uppercase tracking-wide mb-2 flex items-center gap-1">
          <Zap size={10} className="inline" /> Modelo IA ativo
          {switching && <Loader2 size={10} className="ml-auto animate-spin text-slate-400" />}
        </p>
        {models.length > 0 ? (
          <div className="space-y-1">
            {models.map(m => {
              const isActive = m.name === activeModel
              const color = MODEL_COLORS[m.name] ?? '#4F46E5'
              return (
                <button
                  key={m.name}
                  onClick={() => activateModel(m.name)}
                  disabled={switching}
                  title={isActive ? 'Modelo ativo' : `Ativar ${m.name}`}
                  className={`w-full flex items-center justify-between rounded-lg px-2 py-1 transition-colors
                    ${isActive
                      ? 'bg-slate-700'
                      : 'hover:bg-slate-800 opacity-60 hover:opacity-100'
                    } disabled:cursor-not-allowed`}
                >
                  <div className="flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full flex-shrink-0"
                      style={{ backgroundColor: isActive ? color : '#475569' }} />
                    <span className={`text-xs font-bold ${isActive ? 'text-white' : 'text-slate-400'}`}>
                      {m.name}
                    </span>
                    {isActive && (
                      <span className="text-[9px] text-slate-400">ativo</span>
                    )}
                  </div>
                  <span className={`text-[10px] font-mono ${isActive ? 'text-green-400' : 'text-slate-500'}`}>
                    {m.accuracy > 0 ? `${(m.accuracy * 100).toFixed(1)}%` : '—'}
                  </span>
                </button>
              )
            })}
          </div>
        ) : (
          <>
            <p className="text-white text-sm font-bold">{activeModel}</p>
            <p className="text-sb-sec text-[10px] mt-0.5">Carregando...</p>
          </>
        )}
      </div>

      {/* User */}
      <div className="border-t border-sidebar-h px-3 py-3 flex items-center gap-2">
        <div className="w-8 h-8 rounded-md flex items-center justify-center
                        text-white font-bold text-xs flex-shrink-0"
          style={{ backgroundColor: ROLE_COLORS[user?.role] ?? '#475569' }}>
          {user?.nome?.slice(0, 2).toUpperCase() ?? 'U'}
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-white text-xs font-semibold truncate">{user?.nome ?? 'Usuário'}</p>
          <p className="text-sb-sec text-[10px]">{ROLE_LABELS[user?.role] ?? user?.role}</p>
        </div>
        <button onClick={handleLogout} title="Sair"
          className="text-slate-500 hover:text-slate-300 transition-colors flex-shrink-0">
          <LogOut size={13} />
        </button>
      </div>
    </aside>
  )
}
