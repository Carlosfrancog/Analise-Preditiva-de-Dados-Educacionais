import { useState, useEffect } from 'react'
import { BarChart3, TrendingUp, TrendingDown, Users, BookOpen, CheckCircle2, AlertTriangle, XCircle } from 'lucide-react'
import { api } from '../api'

const CLS_COLOR = { 'Aprovado': '#10B981', 'Recuperação': '#F59E0B', 'Reprovado': '#EF4444' }

function pct(a, b) { return b > 0 ? Math.round((a / b) * 100) : 0 }

export default function Relatorio() {
  const [salas, setSalas]       = useState([])
  const [salaId, setSalaId]     = useState('')
  const [data, setData]         = useState(null)
  const [loading, setLoading]   = useState(false)

  useEffect(() => { api.salas().then(setSalas).catch(console.error) }, [])
  useEffect(() => { load() }, [salaId])

  async function load() {
    setLoading(true)
    try {
      const d = await api.relatorio(salaId || null)
      setData(d)
    } catch (e) { console.error(e) }
    finally { setLoading(false) }
  }

  const stats = data?.stats ?? {}
  const rows  = data?.rows  ?? []

  // Group by materia — find hardest subjects
  const byMateria = {}
  rows.forEach(r => {
    if (!byMateria[r.materia_nome]) byMateria[r.materia_nome] = { total: 0, aprovado: 0, recuperacao: 0, reprovado: 0, medias: [] }
    const m = byMateria[r.materia_nome]
    m.total++
    if (r.media != null) m.medias.push(r.media)
    if (r.status === 'Aprovado')    m.aprovado++
    if (r.status === 'Recuperação') m.recuperacao++
    if (r.status === 'Reprovado')   m.reprovado++
  })
  const materias = Object.entries(byMateria)
    .map(([nome, m]) => ({
      nome,
      ...m,
      media: m.medias.length ? (m.medias.reduce((a, b) => a + b, 0) / m.medias.length) : null,
      taxaAprov: pct(m.aprovado, m.total),
    }))
    .sort((a, b) => a.taxaAprov - b.taxaAprov)

  // Group by sala (when showing all)
  const bySala = {}
  rows.forEach(r => {
    if (!bySala[r.sala_nome]) bySala[r.sala_nome] = { total: 0, aprovado: 0, recuperacao: 0, reprovado: 0 }
    const s = bySala[r.sala_nome]
    s.total++
    if (r.status === 'Aprovado')    s.aprovado++
    if (r.status === 'Recuperação') s.recuperacao++
    if (r.status === 'Reprovado')   s.reprovado++
  })
  const salaRows = Object.entries(bySala)
    .map(([nome, s]) => ({ nome, ...s, taxa: pct(s.aprovado, s.total) }))
    .sort((a, b) => a.taxa - b.taxa)

  return (
    <div className="p-7 space-y-6 max-w-5xl">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <p className="text-[10px] text-muted uppercase tracking-widest mb-1">Análise</p>
          <h1 className="text-2xl font-bold text-text">Relatório de Desempenho</h1>
          <p className="text-sm text-muted mt-0.5">Visão agregada por turma e matéria</p>
        </div>
        <div>
          <label className="text-[10px] text-muted uppercase tracking-widest block mb-1">Turma</label>
          <select className="select min-w-[180px]" value={salaId} onChange={e => setSalaId(e.target.value)}>
            <option value="">Todas as turmas</option>
            {salas.map(s => <option key={s.id} value={s.id}>{s.nome}</option>)}
          </select>
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center py-20">
          <div className="w-7 h-7 border-2 border-accent/30 border-t-accent rounded-full animate-spin" />
        </div>
      ) : !data ? null : (
        <>
          {/* KPI cards */}
          <div className="grid grid-cols-4 gap-4">
            {[
              { label: 'Total avaliações', value: stats.total,      Icon: BookOpen,      color: '#4F46E5' },
              { label: 'Aprovados',        value: stats.aprovado,   Icon: CheckCircle2,  color: '#10B981' },
              { label: 'Recuperação',      value: stats.recuperacao, Icon: AlertTriangle, color: '#F59E0B' },
              { label: 'Reprovados',       value: stats.reprovado,  Icon: XCircle,       color: '#EF4444' },
            ].map(({ label, value, Icon, color }) => (
              <div key={label} className="card p-4 relative overflow-hidden">
                <div className="absolute left-0 top-0 bottom-0 w-1 rounded-l-xl" style={{ backgroundColor: color }} />
                <div className="flex items-center justify-between mb-2">
                  <p className="text-xs text-muted">{label}</p>
                  <Icon size={15} style={{ color }} className="opacity-60" />
                </div>
                <p className="text-3xl font-bold" style={{ color }}>{value ?? '—'}</p>
                {stats.total > 0 && (
                  <p className="text-[10px] text-muted mt-1">{pct(value, stats.total)}% do total</p>
                )}
              </div>
            ))}
          </div>

          {/* Approval rate bar */}
          {stats.total > 0 && (
            <div className="card p-5">
              <div className="flex items-center justify-between mb-3">
                <p className="text-sm font-bold text-text">Taxa de aprovação geral</p>
                <span className="text-2xl font-bold text-green-600">{stats.taxa}%</span>
              </div>
              <div className="h-4 bg-slate-100 rounded-full overflow-hidden flex">
                <div className="h-full bg-green-500 transition-all"
                  style={{ width: `${pct(stats.aprovado, stats.total)}%` }} />
                <div className="h-full bg-amber-400 transition-all"
                  style={{ width: `${pct(stats.recuperacao, stats.total)}%` }} />
                <div className="h-full bg-red-400 transition-all"
                  style={{ width: `${pct(stats.reprovado, stats.total)}%` }} />
              </div>
              <div className="flex items-center gap-5 mt-2 text-xs text-muted">
                <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-green-500" /> Aprovado</span>
                <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-amber-400" /> Recuperação</span>
                <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-red-400" /> Reprovado</span>
              </div>
            </div>
          )}

          {/* Hardest subjects */}
          {materias.length > 0 && (
            <div>
              <p className="text-[10px] text-muted uppercase tracking-widest mb-3">
                Matérias — menor taxa de aprovação primeiro
              </p>
              <div className="card overflow-hidden">
                <table className="w-full text-sm">
                  <thead className="bg-hdr-bg text-[10px] text-muted uppercase tracking-wider">
                    <tr>
                      <th className="px-4 py-2.5 text-left font-semibold">Matéria</th>
                      <th className="px-4 py-2.5 text-center font-semibold">Média</th>
                      <th className="px-4 py-2.5 text-center font-semibold text-green-600">Aprovados</th>
                      <th className="px-4 py-2.5 text-center font-semibold text-amber-600">Recuperação</th>
                      <th className="px-4 py-2.5 text-center font-semibold text-red-600">Reprovados</th>
                      <th className="px-4 py-2.5 text-left font-semibold">Taxa aprovação</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border">
                    {materias.map((m, i) => {
                      const barColor = m.taxaAprov >= 70 ? '#10B981' : m.taxaAprov >= 50 ? '#F59E0B' : '#EF4444'
                      return (
                        <tr key={m.nome} className={i % 2 === 1 ? 'bg-hdr-bg/40' : ''}>
                          <td className="px-4 py-2.5 font-semibold text-text">{m.nome}</td>
                          <td className="px-4 py-2.5 text-center font-bold"
                            style={{ color: m.media >= 6 ? '#10B981' : m.media >= 5 ? '#F59E0B' : '#EF4444' }}>
                            {m.media != null ? m.media.toFixed(1) : '—'}
                          </td>
                          <td className="px-4 py-2.5 text-center text-green-700">{m.aprovado}</td>
                          <td className="px-4 py-2.5 text-center text-amber-700">{m.recuperacao}</td>
                          <td className="px-4 py-2.5 text-center text-red-700">{m.reprovado}</td>
                          <td className="px-4 py-2.5">
                            <div className="flex items-center gap-2">
                              <div className="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
                                <div className="h-full rounded-full" style={{ width: `${m.taxaAprov}%`, backgroundColor: barColor }} />
                              </div>
                              <span className="text-xs font-bold w-8 text-right" style={{ color: barColor }}>
                                {m.taxaAprov}%
                              </span>
                            </div>
                          </td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* By sala (when not filtered) */}
          {!salaId && salaRows.length > 0 && (
            <div>
              <p className="text-[10px] text-muted uppercase tracking-widest mb-3">Desempenho por Turma</p>
              <div className="card overflow-hidden">
                <table className="w-full text-sm">
                  <thead className="bg-hdr-bg text-[10px] text-muted uppercase tracking-wider">
                    <tr>
                      <th className="px-4 py-2.5 text-left font-semibold">Turma</th>
                      <th className="px-4 py-2.5 text-center font-semibold text-green-600">Aprovados</th>
                      <th className="px-4 py-2.5 text-center font-semibold text-amber-600">Recuperação</th>
                      <th className="px-4 py-2.5 text-center font-semibold text-red-600">Reprovados</th>
                      <th className="px-4 py-2.5 text-left font-semibold">Taxa</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border">
                    {salaRows.map((s, i) => {
                      const barColor = s.taxa >= 70 ? '#10B981' : s.taxa >= 50 ? '#F59E0B' : '#EF4444'
                      return (
                        <tr key={s.nome} className={i % 2 === 1 ? 'bg-hdr-bg/40' : ''}>
                          <td className="px-4 py-2.5 font-semibold text-text">{s.nome}</td>
                          <td className="px-4 py-2.5 text-center text-green-700">{s.aprovado}</td>
                          <td className="px-4 py-2.5 text-center text-amber-700">{s.recuperacao}</td>
                          <td className="px-4 py-2.5 text-center text-red-700">{s.reprovado}</td>
                          <td className="px-4 py-2.5">
                            <div className="flex items-center gap-2">
                              <div className="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
                                <div className="h-full rounded-full" style={{ width: `${s.taxa}%`, backgroundColor: barColor }} />
                              </div>
                              <span className="text-xs font-bold w-8 text-right" style={{ color: barColor }}>
                                {s.taxa}%
                              </span>
                            </div>
                          </td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}
