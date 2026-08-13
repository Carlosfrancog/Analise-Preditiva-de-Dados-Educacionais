import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Users, BookOpen, PenLine, AlertTriangle, Zap,
  TrendingUp, ArrowRight, Building2, BarChart3,
  Target, CheckCircle2, XCircle, GraduationCap,
  ChevronRight,
} from 'lucide-react'
import { api } from '../api'
import { useModel } from '../context/ModelContext'

function pct(a, b) { return b > 0 ? Math.round((a / b) * 100) : 0 }

export default function Dashboard() {
  const [data, setData]       = useState(null)
  const [loading, setLoading] = useState(true)
  const navigate              = useNavigate()
  const { activeModel, models } = useModel()

  useEffect(() => {
    api.dashboard().then(setData).catch(console.error).finally(() => setLoading(false))
  }, [])

  if (loading) return (
    <div className="flex items-center justify-center h-full">
      <div className="w-7 h-7 border-2 border-accent/30 border-t-accent rounded-full animate-spin" />
    </div>
  )

  const kpis   = data?.kpis        ?? {}
  const stats  = data?.notas_stats  ?? {}
  const salas  = data?.salas        ?? []
  const recent = data?.recent_notas ?? []

  const activeModelMeta = models.find(m => m.name === activeModel)
  const topRisco = [...salas].sort((a, b) => b.risco_pct - a.risco_pct).slice(0, 3)

  return (
    <div className="p-6 space-y-6 max-w-6xl">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <p className="text-[10px] text-muted uppercase tracking-widest mb-1">Visão geral</p>
          <h1 className="text-2xl font-bold text-text">Dashboard</h1>
          <p className="text-sm text-muted mt-0.5">
            {kpis.salas} turmas · {kpis.alunos} alunos · {kpis.materias} matérias
          </p>
        </div>

        {/* Quick actions */}
        <div className="flex items-center gap-2">
          {[
            { label: 'Predições IA', Icon: Target,    to: '/predicoes', accent: true  },
            { label: 'Relatório',    Icon: BarChart3,  to: '/relatorio'                },
            { label: 'Alunos',       Icon: Users,      to: '/alunos'                   },
          ].map(({ label, Icon, to, accent }) => (
            <button key={to} onClick={() => navigate(to)}
              className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-semibold transition-colors ${
                accent
                  ? 'bg-accent text-white hover:bg-indigo-700'
                  : 'border border-border text-muted hover:text-text hover:bg-hdr-bg'
              }`}>
              <Icon size={13} /> {label}
            </button>
          ))}
        </div>
      </div>

      {/* KPI row */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: 'Alunos ativos',  value: kpis.alunos,        color: '#4F46E5', Icon: GraduationCap, to: '/alunos',    sub: `em ${kpis.salas} turmas` },
          { label: 'Notas lançadas', value: kpis.notas_lancadas, color: '#10B981', Icon: PenLine,       to: '/notas',     sub: 'registros totais' },
          { label: 'Em risco (IA)',  value: kpis.em_risco,       color: '#EF4444', Icon: AlertTriangle, to: '/predicoes', sub: 'reprovação ou recuperação' },
          { label: 'Matérias',       value: kpis.materias,       color: '#0EA5E9', Icon: BookOpen,      to: '/materias',  sub: 'disciplinas ativas' },
        ].map(({ label, value, color, Icon, to, sub }) => (
          <div key={label}
            onClick={() => navigate(to)}
            className="card p-4 relative overflow-hidden cursor-pointer hover:shadow-md hover:ring-2 hover:ring-accent/20 transition-all">
            <div className="absolute left-0 top-0 bottom-0 w-1 rounded-l-xl" style={{ backgroundColor: color }} />
            <div className="flex items-center justify-between mb-2">
              <p className="text-xs text-muted">{label}</p>
              <Icon size={15} style={{ color }} className="opacity-70" />
            </div>
            <p className="text-3xl font-black" style={{ color }}>{value ?? '—'}</p>
            <p className="text-[10px] text-muted mt-1">{sub}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-3 gap-5">

        {/* Left col: approval overview + model */}
        <div className="col-span-1 space-y-4">

          {/* Approval donut-style summary */}
          {stats.total > 0 && (
            <div className="card p-4">
              <div className="flex items-center justify-between mb-3">
                <p className="text-xs font-bold text-text">Desempenho geral</p>
                <span className="text-xs text-muted">{stats.total} avaliações</span>
              </div>

              {/* Stacked bar */}
              <div className="h-3 bg-slate-100 rounded-full overflow-hidden flex mb-3">
                <div className="h-full bg-green-500"
                  style={{ width: `${pct(stats.aprovado, stats.total)}%` }} />
                <div className="h-full bg-amber-400"
                  style={{ width: `${pct(stats.recuperacao, stats.total)}%` }} />
                <div className="h-full bg-red-400"
                  style={{ width: `${pct(stats.reprovado, stats.total)}%` }} />
              </div>

              <div className="space-y-2">
                {[
                  { label: 'Aprovados',    value: stats.aprovado,    color: '#10B981', Icon: CheckCircle2 },
                  { label: 'Recuperação',  value: stats.recuperacao, color: '#F59E0B', Icon: AlertTriangle },
                  { label: 'Reprovados',   value: stats.reprovado,   color: '#EF4444', Icon: XCircle },
                ].map(({ label, value, color, Icon }) => (
                  <div key={label} className="flex items-center justify-between">
                    <div className="flex items-center gap-1.5">
                      <Icon size={12} style={{ color }} />
                      <span className="text-xs text-muted">{label}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold" style={{ color }}>{value}</span>
                      <span className="text-[10px] text-muted w-7 text-right">
                        {pct(value, stats.total)}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-3 pt-3 border-t border-border flex items-center justify-between">
                <span className="text-xs text-muted">Taxa de aprovação</span>
                <span className="text-lg font-black text-green-600">{stats.taxa_aprov}%</span>
              </div>
            </div>
          )}

          {/* Active model card */}
          <div className="rounded-xl bg-slate-900 border border-slate-800 p-4 space-y-2">
            <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest flex items-center gap-1.5">
              <Zap size={10} className="text-indigo-400" /> Modelo IA Ativo
            </p>
            <div className="flex items-center justify-between">
              <span className="text-white font-bold text-sm">{activeModel}</span>
              {activeModelMeta?.accuracy > 0 && (
                <span className="text-green-400 font-black text-sm">
                  {(activeModelMeta.accuracy * 100).toFixed(1)}%
                </span>
              )}
            </div>
            <button onClick={() => navigate('/predicoes')}
              className="w-full flex items-center justify-center gap-1.5 text-xs font-semibold
                         py-1.5 rounded-lg bg-indigo-600/30 border border-indigo-500/40
                         text-indigo-300 hover:bg-indigo-600/50 transition-colors">
              <Target size={12} /> Fazer predições <ArrowRight size={11} />
            </button>
          </div>
        </div>

        {/* Right col: salas grid */}
        <div className="col-span-2 space-y-4">

          {/* Salas grid */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <p className="text-[10px] font-bold text-muted uppercase tracking-widest">Turmas</p>
              <button onClick={() => navigate('/salas')}
                className="text-[10px] text-accent hover:underline flex items-center gap-0.5">
                Ver todas <ChevronRight size={11} />
              </button>
            </div>
            <div className="grid grid-cols-2 gap-3">
              {salas.map(s => {
                const riscoColor = s.risco_pct >= 60 ? '#EF4444' : s.risco_pct >= 40 ? '#F59E0B' : '#10B981'
                return (
                  <div key={s.id}
                    onClick={() => navigate(`/alunos?sala=${s.id}`)}
                    className="card p-3 cursor-pointer hover:shadow-md hover:ring-2 hover:ring-accent/20 transition-all">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <div className="w-6 h-6 rounded-md bg-accent/10 flex items-center justify-center">
                          <Building2 size={12} className="text-accent" />
                        </div>
                        <span className="text-xs font-bold text-text truncate max-w-[100px]">{s.nome}</span>
                      </div>
                      <span className="text-[10px] text-muted">{s.codigo}</span>
                    </div>

                    <div className="flex items-center gap-3 text-[10px]">
                      <span className="text-muted flex items-center gap-0.5">
                        <Users size={10} /> {s.alunos}
                      </span>
                      {s.com_predicao > 0 && (
                        <>
                          <span className="text-green-600 font-bold">{s.aprovados} ✓</span>
                          <span className="text-amber-500 font-bold">{s.recuperacao} !</span>
                          <span className="text-red-500 font-bold">{s.reprovados} ✗</span>
                        </>
                      )}
                    </div>

                    {s.com_predicao > 0 && (
                      <div className="mt-2">
                        <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden flex">
                          <div className="h-full bg-green-500"
                            style={{ width: `${pct(s.aprovados, s.com_predicao)}%` }} />
                          <div className="h-full bg-amber-400"
                            style={{ width: `${pct(s.recuperacao, s.com_predicao)}%` }} />
                          <div className="h-full bg-red-400"
                            style={{ width: `${pct(s.reprovados, s.com_predicao)}%` }} />
                        </div>
                      </div>
                    )}

                    {s.risco_pct > 0 && (
                      <div className="mt-1.5 flex items-center justify-between">
                        <span className="text-[9px] text-muted">em risco</span>
                        <span className="text-[10px] font-bold" style={{ color: riscoColor }}>
                          {s.risco_pct}%
                        </span>
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </div>

          {/* Alert: top 3 turmas com maior risco */}
          {topRisco.some(s => s.risco_pct > 0) && (
            <div className="card p-4">
              <p className="text-[10px] font-bold text-muted uppercase tracking-widest mb-3 flex items-center gap-1.5">
                <AlertTriangle size={11} className="text-amber-500" /> Turmas com maior risco
              </p>
              <div className="space-y-2">
                {topRisco.filter(s => s.risco_pct > 0).map(s => (
                  <div key={s.id} className="flex items-center gap-3 cursor-pointer"
                    onClick={() => navigate('/predicoes')}>
                    <span className="text-xs font-semibold text-text w-32 truncate">{s.nome}</span>
                    <div className="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
                      <div className="h-full rounded-full bg-red-400"
                        style={{ width: `${s.risco_pct}%` }} />
                    </div>
                    <span className="text-xs font-bold text-red-500 w-8 text-right">{s.risco_pct}%</span>
                    <button className="text-[10px] text-accent hover:underline flex items-center gap-0.5 shrink-0">
                      Analisar <ArrowRight size={10} />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
