import { useState, useEffect, useRef } from 'react'
import {
  X, Plus, Trash2, Edit2, Check, ChevronLeft, ChevronRight,
  BookOpen, Calendar, AlertCircle,
} from 'lucide-react'
import { api } from '../api'

const STATUS_META = {
  P: { label: 'Presente',    bg: '#D1FAE5', color: '#059669', ring: '#6EE7B7' },
  F: { label: 'Falta',       bg: '#FEE2E2', color: '#DC2626', ring: '#FCA5A5' },
  J: { label: 'Justificada', bg: '#FEF3C7', color: '#D97706', ring: '#FCD34D' },
}
const STATUS_CYCLE = { undefined: 'P', P: 'F', F: 'J', J: null }
const WEEKDAYS = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']

export default function MateriaBoletimModal({ alunoId, nota, onClose, onNotaChanged }) {
  const [tab, setTab]             = useState('bimestre')
  const [bimestre, setBimestre]   = useState(() => {
    // Open to the first incomplete bimestre
    for (let i = 1; i <= 4; i++) if (!nota[`n${i}`]) return i
    return 4
  })
  const [atividades, setAtividades] = useState({ 1: [], 2: [], 3: [], 4: [] })
  const [presencas, setPresencas]   = useState({})
  const [loading, setLoading]       = useState(true)
  const [calMonth, setCalMonth]     = useState(() => {
    const d = new Date(); return { year: d.getFullYear(), month: d.getMonth() }
  })
  const [newAtiv, setNewAtiv]       = useState({ nome: '', nota: '' })
  const [editingId, setEditingId]   = useState(null)
  const [editBuf, setEditBuf]       = useState({})
  const [saving, setSaving]         = useState(false)
  const [error, setError]           = useState(null)

  const materiaId = nota.materia_id
  const materiaName = nota.materia_nome

  useEffect(() => {
    setLoading(true)
    Promise.all([
      api.getAtividades(alunoId, materiaId),
      api.getPresencas(alunoId, materiaId),
    ]).then(([a, p]) => {
      setAtividades(a)
      setPresencas(p)
    }).catch(e => setError(e.message))
    .finally(() => setLoading(false))
  }, [alunoId, materiaId])

  async function handleAddAtividade() {
    if (!newAtiv.nome.trim() || newAtiv.nota === '') return
    setSaving(true); setError(null)
    try {
      await api.criarAtividade({
        aluno_id: Number(alunoId), materia_id: materiaId,
        bimestre, nome: newAtiv.nome.trim(), nota: parseFloat(newAtiv.nota),
      })
      const fresh = await api.getAtividades(alunoId, materiaId)
      setAtividades(fresh)
      setNewAtiv({ nome: '', nota: '' })
      onNotaChanged?.()
    } catch (e) { setError(e.message) }
    finally { setSaving(false) }
  }

  async function handleSaveEdit(id) {
    setSaving(true); setError(null)
    try {
      const row = atividades[bimestre].find(a => a.id === id)
      await api.editarAtividade(id, {
        aluno_id: Number(alunoId), materia_id: materiaId,
        bimestre: row.bimestre, nome: editBuf.nome, nota: parseFloat(editBuf.nota),
      })
      const fresh = await api.getAtividades(alunoId, materiaId)
      setAtividades(fresh)
      setEditingId(null)
      onNotaChanged?.()
    } catch (e) { setError(e.message) }
    finally { setSaving(false) }
  }

  async function handleDeleteAtividade(id) {
    if (!confirm('Deletar esta atividade?')) return
    setSaving(true)
    try {
      await api.deletarAtividade(id)
      const fresh = await api.getAtividades(alunoId, materiaId)
      setAtividades(fresh)
      onNotaChanged?.()
    } catch (e) { setError(e.message) }
    finally { setSaving(false) }
  }

  async function handlePresencaToggle(dateStr, currentStatus) {
    const next = STATUS_CYCLE[currentStatus ?? 'undefined']
    try {
      if (!next) {
        const entry = presencas[dateStr]
        if (entry) await api.deletarPresenca(entry.id)
        setPresencas(p => { const n = { ...p }; delete n[dateStr]; return n })
      } else {
        const res = await api.upsertPresenca({
          aluno_id: Number(alunoId), materia_id: materiaId, data: dateStr, status: next,
        })
        setPresencas(p => ({ ...p, [dateStr]: { id: res.id, status: next } }))
      }
    } catch (e) { setError(e.message) }
  }

  // Computed nota for current bimestre
  const sum = atividades[bimestre]?.reduce((a, r) => a + r.nota, 0) ?? 0
  const computedN = atividades[bimestre]?.length ? Math.min(sum, 10) : null
  const rawN = nota[`n${bimestre}`]

  // Presence stats
  const presencaList = Object.values(presencas)
  const totalAulas = presencaList.length
  const faltas     = presencaList.filter(p => p.status === 'F').length
  const justificadas = presencaList.filter(p => p.status === 'J').length
  const frequencia = totalAulas > 0 ? ((totalAulas - faltas) / totalAulas * 100) : null

  // Calendar helpers
  const firstDay = new Date(calMonth.year, calMonth.month, 1)
  const daysInMonth = new Date(calMonth.year, calMonth.month + 1, 0).getDate()
  const startDow = firstDay.getDay()
  const monthName = firstDay.toLocaleString('pt-BR', { month: 'long', year: 'numeric' })

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
      onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="modal-stickout bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[88vh] flex flex-col overflow-hidden">

        {/* Header */}
        <div className="flex items-center gap-3 px-5 py-4 border-b border-border bg-hdr-bg flex-shrink-0">
          <BookOpen size={18} className="text-accent flex-shrink-0" />
          <div className="flex-1 min-w-0">
            <p className="font-bold text-text text-base leading-tight truncate">{materiaName}</p>
            <p className="text-[10px] text-muted">
              N1 {fmt(nota.n1)} · N2 {fmt(nota.n2)} · N3 {fmt(nota.n3)} · N4 {fmt(nota.n4)}
              {frequencia !== null && (
                <span className="ml-3">
                  · Frequência{' '}
                  <span className={frequencia >= 75 ? 'text-green-600 font-bold' : 'text-red-600 font-bold'}>
                    {frequencia.toFixed(0)}%
                  </span>
                </span>
              )}
            </p>
          </div>
          <button onClick={onClose}
            className="w-8 h-8 flex items-center justify-center rounded-lg text-muted
                       hover:text-text hover:bg-slate-200 transition-colors flex-shrink-0">
            <X size={16} />
          </button>
        </div>

        {/* Tab bar */}
        <div className="flex border-b border-border flex-shrink-0 bg-white">
          <button
            onClick={() => setTab('bimestre')}
            className={`flex-1 py-2.5 text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors ${
              tab === 'bimestre'
                ? 'border-b-2 border-accent text-accent'
                : 'text-muted hover:text-text'
            }`}>
            <BookOpen size={12} /> Atividades por Bimestre
          </button>
          <button
            onClick={() => setTab('presencas')}
            className={`flex-1 py-2.5 text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors ${
              tab === 'presencas'
                ? 'border-b-2 border-accent text-accent'
                : 'text-muted hover:text-text'
            }`}>
            <Calendar size={12} /> Presenças
          </button>
        </div>

        {error && (
          <div className="flex items-center gap-2 px-4 py-2 bg-red-50 border-b border-red-200 flex-shrink-0 text-xs text-danger">
            <AlertCircle size={12} /> {error}
          </div>
        )}

        {/* Body */}
        <div className="flex-1 overflow-y-auto">
          {loading ? (
            <div className="flex justify-center py-16">
              <div className="w-7 h-7 border-2 border-accent/30 border-t-accent rounded-full animate-spin" />
            </div>
          ) : tab === 'bimestre' ? (
            <BimestreTab
              bimestre={bimestre} setBimestre={setBimestre}
              atividades={atividades}
              newAtiv={newAtiv} setNewAtiv={setNewAtiv}
              editingId={editingId} setEditingId={setEditingId}
              editBuf={editBuf} setEditBuf={setEditBuf}
              computedN={computedN} rawN={rawN}
              saving={saving}
              onAdd={handleAddAtividade}
              onSaveEdit={handleSaveEdit}
              onDelete={handleDeleteAtividade}
              nota={nota}
            />
          ) : (
            <PresencasTab
              presencas={presencas}
              calMonth={calMonth} setCalMonth={setCalMonth}
              monthName={monthName} startDow={startDow} daysInMonth={daysInMonth}
              totalAulas={totalAulas} faltas={faltas} justificadas={justificadas}
              frequencia={frequencia}
              onToggle={handlePresencaToggle}
            />
          )}
        </div>
      </div>
    </div>
  )
}

function fmt(v) {
  return v && v > 0 ? v.toFixed(1) : '—'
}

// ── Bimestre Tab ──────────────────────────────────────────────────────────────

function BimestreTab({
  bimestre, setBimestre, atividades, newAtiv, setNewAtiv,
  editingId, setEditingId, editBuf, setEditBuf,
  computedN, rawN, saving, onAdd, onSaveEdit, onDelete, nota,
}) {
  const list = atividades[bimestre] ?? []
  const sum  = list.reduce((a, r) => a + r.nota, 0)

  return (
    <div className="p-5 space-y-5">
      {/* Bimestre selector + nota status */}
      <div className="flex items-center gap-3">
        <div className="flex bg-slate-100 rounded-xl p-1 gap-1">
          {[1, 2, 3, 4].map(b => {
            const n = nota[`n${b}`]
            const hasActs = atividades[b]?.length > 0
            return (
              <button key={b} onClick={() => setBimestre(b)}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-colors relative ${
                  bimestre === b ? 'bg-accent text-white shadow-sm' : 'text-muted hover:text-text'
                }`}>
                {b}º Bim
                {hasActs && bimestre !== b && (
                  <span className="absolute -top-1 -right-1 w-2 h-2 bg-indigo-400 rounded-full" />
                )}
              </button>
            )
          })}
        </div>

        {/* Nota summary for this bimestre */}
        <div className="ml-auto flex items-center gap-2 text-sm">
          {computedN !== null ? (
            <>
              <span className="text-muted text-xs">Soma das atividades →</span>
              <span className={`font-black text-lg ${
                computedN >= 6 ? 'text-green-600' : computedN >= 5 ? 'text-amber-500' : 'text-red-500'
              }`}>{computedN.toFixed(1)}</span>
              <span className="text-muted text-xs">/ 10</span>
            </>
          ) : rawN ? (
            <>
              <span className="text-muted text-xs">N{bimestre} lançada manualmente →</span>
              <span className={`font-black text-lg ${
                rawN >= 6 ? 'text-green-600' : rawN >= 5 ? 'text-amber-500' : 'text-red-500'
              }`}>{Number(rawN).toFixed(1)}</span>
            </>
          ) : (
            <span className="text-muted text-xs italic">Nenhuma atividade lançada</span>
          )}
        </div>
      </div>

      {/* Activity list */}
      {list.length > 0 ? (
        <div className="space-y-2">
          {list.map(a => (
            <div key={a.id}
              className="flex items-center gap-3 px-3 py-2.5 rounded-xl border border-border bg-hdr-bg">
              {editingId === a.id ? (
                <>
                  <input
                    className="select flex-1 text-sm py-1"
                    value={editBuf.nome}
                    onChange={e => setEditBuf(b => ({ ...b, nome: e.target.value }))}
                    placeholder="Nome da atividade"
                  />
                  <input
                    type="number" min="0" max="10" step="0.1"
                    className="select w-20 text-sm py-1 text-center"
                    value={editBuf.nota}
                    onChange={e => setEditBuf(b => ({ ...b, nota: e.target.value }))}
                  />
                  <button onClick={() => onSaveEdit(a.id)} disabled={saving}
                    className="w-7 h-7 flex items-center justify-center rounded-lg bg-green-100 text-green-700 hover:bg-green-200 transition-colors">
                    <Check size={13} />
                  </button>
                  <button onClick={() => setEditingId(null)}
                    className="w-7 h-7 flex items-center justify-center rounded-lg text-muted hover:text-text transition-colors">
                    <X size={13} />
                  </button>
                </>
              ) : (
                <>
                  <span className="flex-1 text-sm text-text font-medium truncate">{a.nome}</span>
                  <NotaBadge nota={a.nota} />
                  <button onClick={() => { setEditingId(a.id); setEditBuf({ nome: a.nome, nota: String(a.nota) }) }}
                    className="w-7 h-7 flex items-center justify-center rounded-lg text-muted hover:text-text transition-colors">
                    <Edit2 size={13} />
                  </button>
                  <button onClick={() => onDelete(a.id)} disabled={saving}
                    className="w-7 h-7 flex items-center justify-center rounded-lg text-muted hover:text-danger transition-colors">
                    <Trash2 size={13} />
                  </button>
                </>
              )}
            </div>
          ))}
          {/* Sum row */}
          <div className="flex items-center justify-end gap-2 pr-1 pt-1 border-t border-border">
            <span className="text-xs text-muted">Total:</span>
            <span className="text-sm font-bold text-text">{sum.toFixed(1)}</span>
            <span className="text-xs text-muted">→ N{bimestre}:</span>
            <span className={`text-sm font-black ${
              Math.min(sum, 10) >= 6 ? 'text-green-600' : Math.min(sum, 10) >= 5 ? 'text-amber-500' : 'text-red-500'
            }`}>{Math.min(sum, 10).toFixed(1)}</span>
          </div>
        </div>
      ) : (
        <div className="text-center py-6 text-muted text-sm border-2 border-dashed border-border rounded-xl">
          Nenhuma atividade no {bimestre}º bimestre.
        </div>
      )}

      {/* Add new activity */}
      <div className="flex items-center gap-2 pt-1">
        <input
          className="select flex-1 text-sm"
          value={newAtiv.nome}
          onChange={e => setNewAtiv(a => ({ ...a, nome: e.target.value }))}
          placeholder="Nome da atividade (ex: Prova 1)"
          onKeyDown={e => e.key === 'Enter' && onAdd()}
        />
        <input
          type="number" min="0" max="10" step="0.1"
          className="select w-20 text-sm text-center"
          value={newAtiv.nota}
          onChange={e => setNewAtiv(a => ({ ...a, nota: e.target.value }))}
          placeholder="0.0"
          onKeyDown={e => e.key === 'Enter' && onAdd()}
        />
        <button
          onClick={onAdd}
          disabled={saving || !newAtiv.nome.trim() || newAtiv.nota === ''}
          className="btn-primary flex items-center gap-1.5 px-3 py-2 text-sm disabled:opacity-50">
          <Plus size={14} /> Adicionar
        </button>
      </div>
      <p className="text-[10px] text-muted -mt-2">
        A soma das atividades (máx. 10) será lançada automaticamente como N{bimestre}.
      </p>
    </div>
  )
}

// ── Presenças Tab ─────────────────────────────────────────────────────────────

function PresencasTab({
  presencas, calMonth, setCalMonth,
  monthName, startDow, daysInMonth,
  totalAulas, faltas, justificadas, frequencia,
  onToggle,
}) {
  function dateStr(day) {
    const m = String(calMonth.month + 1).padStart(2, '0')
    const d = String(day).padStart(2, '0')
    return `${calMonth.year}-${m}-${d}`
  }

  function prevMonth() {
    setCalMonth(c => {
      if (c.month === 0) return { year: c.year - 1, month: 11 }
      return { ...c, month: c.month - 1 }
    })
  }
  function nextMonth() {
    setCalMonth(c => {
      if (c.month === 11) return { year: c.year + 1, month: 0 }
      return { ...c, month: c.month + 1 }
    })
  }

  return (
    <div className="p-5 space-y-5">
      {/* Stats bar */}
      <div className="flex gap-3">
        {[
          { label: 'Total de aulas', value: totalAulas, color: '#6366F1' },
          { label: 'Presenças', value: totalAulas - faltas - justificadas, color: '#10B981' },
          { label: 'Faltas', value: faltas, color: '#EF4444' },
          { label: 'Justificadas', value: justificadas, color: '#F59E0B' },
        ].map(s => (
          <div key={s.label} className="flex-1 rounded-xl border border-border p-3 text-center">
            <p className="text-[10px] text-muted mb-0.5">{s.label}</p>
            <p className="text-xl font-black" style={{ color: s.color }}>{s.value}</p>
          </div>
        ))}
        <div className="flex-1 rounded-xl border border-border p-3 text-center">
          <p className="text-[10px] text-muted mb-0.5">Frequência</p>
          <p className={`text-xl font-black ${
            frequencia === null ? 'text-muted' :
            frequencia >= 75 ? 'text-green-600' : 'text-red-600'
          }`}>{frequencia !== null ? `${frequencia.toFixed(0)}%` : '—'}</p>
        </div>
      </div>

      {/* Month nav */}
      <div className="flex items-center justify-between">
        <button onClick={prevMonth}
          className="w-8 h-8 flex items-center justify-center rounded-lg border border-border hover:bg-hdr-bg transition-colors">
          <ChevronLeft size={15} />
        </button>
        <span className="text-sm font-bold text-text capitalize">{monthName}</span>
        <button onClick={nextMonth}
          className="w-8 h-8 flex items-center justify-center rounded-lg border border-border hover:bg-hdr-bg transition-colors">
          <ChevronRight size={15} />
        </button>
      </div>

      {/* Calendar grid */}
      <div>
        <div className="grid grid-cols-7 mb-1">
          {WEEKDAYS.map(d => (
            <div key={d} className="text-center text-[10px] text-muted font-bold py-1">{d}</div>
          ))}
        </div>
        <div className="grid grid-cols-7 gap-1">
          {/* Empty cells before month start */}
          {Array.from({ length: startDow }).map((_, i) => (
            <div key={`e${i}`} />
          ))}
          {/* Day cells */}
          {Array.from({ length: daysInMonth }, (_, i) => i + 1).map(day => {
            const ds = dateStr(day)
            const entry = presencas[ds]
            const status = entry?.status
            const meta   = status ? STATUS_META[status] : null
            const today  = new Date()
            const isToday = today.getFullYear() === calMonth.year &&
                            today.getMonth() === calMonth.month &&
                            today.getDate() === day
            return (
              <button
                key={day}
                onClick={() => onToggle(ds, status)}
                title={meta ? meta.label : 'Clique para marcar'}
                className={`aspect-square rounded-lg text-xs font-bold transition-all hover:scale-105 ${
                  isToday ? 'ring-2 ring-accent ring-offset-1' : ''
                }`}
                style={meta ? {
                  backgroundColor: meta.bg,
                  color: meta.color,
                  border: `1px solid ${meta.ring}`,
                } : {
                  backgroundColor: '#F8FAFC',
                  color: '#94A3B8',
                  border: '1px solid #E2E8F0',
                }}
              >
                {day}
                {status && (
                  <div className="text-[7px] font-black block leading-none">{status}</div>
                )}
              </button>
            )
          })}
        </div>
      </div>

      {/* Legend */}
      <div className="flex items-center gap-4 text-[10px] text-muted">
        {Object.entries(STATUS_META).map(([s, m]) => (
          <span key={s} className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded" style={{ backgroundColor: m.bg, border: `1px solid ${m.ring}` }} />
            {s} — {m.label}
          </span>
        ))}
        <span className="ml-auto">Clique no dia para alternar P → F → J → limpar</span>
      </div>
    </div>
  )
}

function NotaBadge({ nota }) {
  const color = nota >= 6 ? '#10B981' : nota >= 5 ? '#F59E0B' : '#EF4444'
  const bg    = nota >= 6 ? '#D1FAE5' : nota >= 5 ? '#FEF3C7' : '#FEE2E2'
  return (
    <span className="text-sm font-black px-2.5 py-1 rounded-lg"
      style={{ color, backgroundColor: bg }}>
      {nota.toFixed(1)}
    </span>
  )
}
