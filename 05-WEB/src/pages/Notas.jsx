import { useState, useEffect, useCallback } from 'react'
import { PenLine, Save, AlertCircle, CheckCircle2 } from 'lucide-react'
import { api } from '../api'

const BIMESTRES = ['n1', 'n2', 'n3', 'n4']
const BIM_LABEL = { n1: 'N1 · 1º Bim', n2: 'N2 · 2º Bim', n3: 'N3 · 3º Bim', n4: 'N4 · 4º Bim' }
const PESOS     = { n1: 0.20, n2: 0.25, n3: 0.25, n4: 0.30 }

function calcMedia(row) {
  const vals = BIMESTRES.map(b => ({ v: parseFloat(row[b] ?? '') || null, w: PESOS[b] }))
    .filter(x => x.v !== null && x.v > 0)
  if (!vals.length) return null
  const tw = vals.reduce((a, x) => a + x.w, 0)
  return vals.reduce((a, x) => a + x.v * x.w, 0) / tw
}

function StatusDot({ media }) {
  if (media === null) return <span className="w-2 h-2 rounded-full bg-slate-200 inline-block" />
  if (media >= 6)  return <span className="w-2 h-2 rounded-full bg-green-400 inline-block" title="Aprovado" />
  if (media >= 5)  return <span className="w-2 h-2 rounded-full bg-amber-400 inline-block" title="Recuperação" />
  return <span className="w-2 h-2 rounded-full bg-red-400 inline-block" title="Reprovado" />
}

export default function Notas() {
  const [salas, setSalas]         = useState([])
  const [materias, setMaterias]   = useState([])
  const [salaId, setSalaId]       = useState('')
  const [materiaId, setMateriaId] = useState('')
  const [alunos, setAlunos]       = useState([])
  const [buf, setBuf]             = useState({})
  const [editMode, setEditMode]   = useState(false)
  const [loading, setLoading]     = useState(false)
  const [saving, setSaving]       = useState(false)
  const [saved, setSaved]         = useState(false)
  const [error, setError]         = useState(null)

  useEffect(() => {
    Promise.all([api.salas(), api.materias()])
      .then(([s, m]) => { setSalas(s); setMaterias(m) })
      .catch(e => setError(e.message))
  }, [])

  const loadGrades = useCallback(async (sid, mid) => {
    if (!sid || !mid) return
    setLoading(true)
    setEditMode(false)
    setBuf({})
    try {
      const [alunosData, allNotas] = await Promise.all([
        api.alunos(parseInt(sid)),
        api.notasTurma(parseInt(sid)),
      ])
      setAlunos(alunosData)

      const mid_ = parseInt(mid)
      const initial = {}
      alunosData.forEach(a => {
        const nota = allNotas.find(n => n.aluno_id === a.id && n.materia_id === mid_)
        initial[a.id] = {
          n1: nota?.n1 ?? '',
          n2: nota?.n2 ?? '',
          n3: nota?.n3 ?? '',
          n4: nota?.n4 ?? '',
        }
      })
      setBuf(initial)
    } catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }, [])

  function handleSalaChange(sid) {
    setSalaId(sid)
    setMateriaId('')
    setAlunos([])
    setBuf({})
  }

  function handleMateriaChange(mid) {
    setMateriaId(mid)
    loadGrades(salaId, mid)
  }

  function updateCell(alunoId, field, val) {
    setBuf(prev => ({
      ...prev,
      [alunoId]: { ...prev[alunoId], [field]: val },
    }))
  }

  async function handleSave() {
    setSaving(true)
    setSaved(false)
    const mid_ = parseInt(materiaId)
    const notas = Object.entries(buf).map(([alunoId, v]) => ({
      aluno_id: parseInt(alunoId),
      materia_id: mid_,
      n1: v.n1 !== '' ? parseFloat(v.n1) : null,
      n2: v.n2 !== '' ? parseFloat(v.n2) : null,
      n3: v.n3 !== '' ? parseFloat(v.n3) : null,
      n4: v.n4 !== '' ? parseFloat(v.n4) : null,
    }))
    try {
      await api.salvarNotasBatch(notas)
      setEditMode(false)
      setSaved(true)
      setTimeout(() => setSaved(false), 3000)
      await loadGrades(salaId, materiaId)
    } catch (e) { setError(e.message) }
    finally { setSaving(false) }
  }

  const materia = materias.find(m => m.id === parseInt(materiaId))
  const sala    = salas.find(s => s.id === parseInt(salaId))

  const stats = alunos.length ? (() => {
    const medias = alunos.map(a => calcMedia(buf[a.id] ?? {}))
    return {
      aprovados:   medias.filter(m => m !== null && m >= 6).length,
      recuperacao: medias.filter(m => m !== null && m >= 5 && m < 6).length,
      reprovados:  medias.filter(m => m !== null && m < 5).length,
      sem_nota:    medias.filter(m => m === null).length,
    }
  })() : null

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* Header */}
      <div className="px-7 pt-5 pb-4 border-b border-border bg-app-bg flex-shrink-0">
        <p className="text-[10px] text-muted uppercase tracking-widest mb-1">Gestão</p>
        <h1 className="text-2xl font-bold text-text">Lançamento de Notas</h1>
        <p className="text-sm text-muted mt-0.5">
          Selecione uma turma e matéria para lançar ou editar as notas dos alunos.
        </p>
      </div>

      {/* Selectors */}
      <div className="px-7 py-3 border-b border-border bg-hdr-bg flex-shrink-0">
        <div className="flex items-end gap-4 flex-wrap">
          <div>
            <label className="text-[10px] text-muted uppercase tracking-widest block mb-1">Turma</label>
            <select className="select min-w-[180px]" value={salaId}
              onChange={e => handleSalaChange(e.target.value)}>
              <option value="">Selecionar turma...</option>
              {salas.map(s => <option key={s.id} value={s.id}>{s.nome}</option>)}
            </select>
          </div>

          <div>
            <label className="text-[10px] text-muted uppercase tracking-widest block mb-1">Matéria</label>
            <select className="select min-w-[180px]" value={materiaId}
              onChange={e => handleMateriaChange(e.target.value)} disabled={!salaId}>
              <option value="">Selecionar matéria...</option>
              {materias.map(m => <option key={m.id} value={m.id}>{m.nome}</option>)}
            </select>
          </div>

          {alunos.length > 0 && !editMode && (
            <button className="btn-primary flex items-center gap-2" onClick={() => setEditMode(true)}>
              <PenLine size={15} /> Editar Notas
            </button>
          )}

          {editMode && (
            <>
              <button className="btn-primary flex items-center gap-2" onClick={handleSave} disabled={saving}>
                {saving
                  ? <span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  : <Save size={15} />}
                Salvar tudo
              </button>
              <button className="btn-secondary" onClick={() => { setEditMode(false); loadGrades(salaId, materiaId) }}>
                Cancelar
              </button>
            </>
          )}

          {saved && (
            <span className="text-sm text-green-600 font-semibold flex items-center gap-1.5">
              <CheckCircle2 size={15} /> Notas salvas!
            </span>
          )}
        </div>
      </div>

      {error && (
        <div className="text-danger text-sm px-7 py-2 bg-red-50 border-b border-red-200 flex items-center gap-2">
          <AlertCircle size={14} /> {error}
        </div>
      )}

      {/* Content */}
      <div className="flex-1 overflow-y-auto">
        {!salaId || !materiaId ? (
          <div className="flex flex-col items-center justify-center h-full text-center text-muted py-20">
            <PenLine size={48} className="mx-auto mb-4 opacity-20" />
            <p className="font-semibold text-text">Selecione turma e matéria</p>
            <p className="text-sm mt-1">
              Escolha uma turma e uma disciplina para visualizar e lançar as notas.
            </p>
          </div>
        ) : loading ? (
          <div className="flex justify-center py-16">
            <div className="w-7 h-7 border-2 border-accent/30 border-t-accent rounded-full animate-spin" />
          </div>
        ) : (
          <div className="p-7">
            {/* Stats bar */}
            {stats && (
              <div className="flex items-center gap-6 mb-5">
                <div>
                  <p className="text-base font-bold text-text">{sala?.nome}</p>
                  <p className="text-sm text-muted">{materia?.nome} · {alunos.length} alunos</p>
                </div>
                <div className="flex items-center gap-4 ml-auto">
                  <StatBadge label="Aprovados"   count={stats.aprovados}   color="text-green-600 bg-green-50" />
                  <StatBadge label="Recuperação" count={stats.recuperacao} color="text-amber-600 bg-amber-50" />
                  <StatBadge label="Reprovados"  count={stats.reprovados}  color="text-red-600 bg-red-50" />
                  {stats.sem_nota > 0 && (
                    <StatBadge label="Sem nota" count={stats.sem_nota} color="text-muted bg-slate-100" />
                  )}
                </div>
              </div>
            )}

            {/* Grade table */}
            <div className="card overflow-hidden">
              <table className="w-full">
                <thead className="bg-hdr-bg border-b border-border">
                  <tr className="text-[10px] text-muted uppercase tracking-wider">
                    <th className="px-5 py-3 text-left font-semibold w-8">#</th>
                    <th className="px-4 py-3 text-left font-semibold">Aluno</th>
                    {BIMESTRES.map(b => (
                      <th key={b} className="px-3 py-3 text-center font-semibold w-24">
                        <div>{BIM_LABEL[b].split(' · ')[0]}</div>
                        <div className="text-[9px] normal-case text-muted/70 font-normal">
                          peso {(PESOS[b] * 100).toFixed(0)}%
                        </div>
                      </th>
                    ))}
                    <th className="px-4 py-3 text-center font-semibold w-20">Média</th>
                    <th className="px-3 py-3 text-center w-10" />
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {alunos.map((a, i) => {
                    const row   = buf[a.id] ?? {}
                    const media = calcMedia(row)
                    const mediaColor = media === null ? '#94A3B8'
                      : media >= 6 ? '#10B981'
                      : media >= 5 ? '#F59E0B'
                      : '#EF4444'

                    return (
                      <tr key={a.id}
                        className={`transition-colors ${i % 2 === 1 ? 'bg-hdr-bg/40' : ''} ${editMode ? 'hover:bg-indigo-50/30' : ''}`}>
                        <td className="px-5 py-2 text-[10px] text-muted font-mono">{i + 1}</td>
                        <td className="px-4 py-2 text-sm font-semibold text-text">{a.nome}</td>
                        {BIMESTRES.map(b => {
                          const val = row[b]
                          const num = parseFloat(val)
                          const numColor = !val || val === '' ? '#94A3B8'
                            : num >= 6 ? '#10B981' : num >= 5 ? '#F59E0B' : '#EF4444'
                          return (
                            <td key={b} className="px-3 py-2 text-center">
                              {editMode ? (
                                <input
                                  type="number" min="0" max="10" step="0.1"
                                  value={val ?? ''}
                                  onChange={e => updateCell(a.id, b, e.target.value)}
                                  className="w-16 text-center text-sm font-bold py-1 px-1 border border-border
                                             rounded-lg bg-white focus:outline-none focus:border-accent
                                             focus:ring-1 focus:ring-accent/30"
                                  style={{ color: numColor }}
                                  placeholder="—"
                                />
                              ) : (
                                <span className="text-sm font-bold" style={{ color: numColor }}>
                                  {val !== '' && val != null ? parseFloat(val).toFixed(1) : '—'}
                                </span>
                              )}
                            </td>
                          )
                        })}
                        <td className="px-4 py-2 text-center">
                          <span className="text-sm font-bold" style={{ color: mediaColor }}>
                            {media !== null ? media.toFixed(2) : '—'}
                          </span>
                        </td>
                        <td className="px-3 py-2 text-center">
                          <StatusDot media={media} />
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>

            {/* Legend */}
            <div className="flex items-center gap-5 text-xs text-muted mt-3">
              <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-green-400" /> Aprovado ≥ 6.0</span>
              <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-amber-400" /> Recuperação 5.0–5.9</span>
              <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-red-400" /> Reprovado &lt; 5.0</span>
              <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-slate-200" /> Sem nota</span>
              <span className="ml-auto">Média ponderada: N1×20% + N2×25% + N3×25% + N4×30%</span>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

function StatBadge({ label, count, color }) {
  return (
    <div className={`px-3 py-1.5 rounded-lg ${color}`}>
      <p className="text-lg font-bold leading-tight">{count}</p>
      <p className="text-[10px] font-medium">{label}</p>
    </div>
  )
}
