import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  XCircle, AlertTriangle, CheckCircle2,
  GitBranch, PenLine, Save, ClipboardList, Bot, AlertCircle,
  TrendingUp, TrendingDown, Minus,
} from 'lucide-react'
import { api } from '../api'
import MateriaBoletimModal from '../components/MateriaBoletimModal'

const CLS = {
  0: { name: 'Reprovado',   color: '#EF4444', bg: '#FEE2E2', Icon: XCircle,       ring: '#FECACA' },
  1: { name: 'Recuperação', color: '#F59E0B', bg: '#FEF3C7', Icon: AlertTriangle,  ring: '#FDE68A' },
  2: { name: 'Aprovado',    color: '#10B981', bg: '#D1FAE5', Icon: CheckCircle2,   ring: '#A7F3D0' },
}

const MODELS = {
  RF_M1: { label: 'M1 — Alerta',      desc: '83.8% · 100 árvores · profund. 5', color: '#10B981' },
  RF_M2: { label: 'M2 — Intermediário', desc: '90.4% · 150 árvores · profund. 10', color: '#0EA5E9' },
  RF_M3: { label: 'M3 — Produção',    desc: '91.3% · 200 árvores · livre',       color: '#4F46E5' },
}

function initials(nome) {
  return nome.split(' ').map(n => n[0]).filter(Boolean).slice(0, 2).join('').toUpperCase()
}

function calcVariancia(v1, v2, v3, v4) {
  const vals = [v1, v2, v3, v4].filter(v => v > 0)
  if (vals.length < 2) return null
  const mean = vals.reduce((a, b) => a + b, 0) / vals.length
  return vals.reduce((a, v) => a + (v - mean) ** 2, 0) / vals.length
}

function calcSlope(v1, v2, v3, v4) {
  const pts = [[0,v1],[1,v2],[2,v3],[3,v4]].filter(([,y]) => y > 0)
  if (pts.length < 2) return null
  const mx = pts.reduce((a,[x]) => a+x, 0) / pts.length
  const my = pts.reduce((a,[,y]) => a+y, 0) / pts.length
  const num = pts.reduce((a,[x,y]) => a + (x-mx)*(y-my), 0)
  const den = pts.reduce((a,[x]) => a + (x-mx)**2, 0)
  return den !== 0 ? num / den : 0
}

function trendInfo(slope) {
  if (slope === null) return { Icon: null, label: null, color: '#94A3B8' }
  if (slope >  0.5)  return { Icon: TrendingUp,   label: 'melhorando', color: '#10B981' }
  if (slope >  0.1)  return { Icon: TrendingUp,   label: 'subindo',    color: '#34D399' }
  if (slope < -0.5)  return { Icon: TrendingDown,  label: 'caindo',     color: '#EF4444' }
  if (slope < -0.1)  return { Icon: TrendingDown,  label: 'caindo leve', color: '#F59E0B' }
  return { Icon: Minus, label: 'estável', color: '#94A3B8' }
}

function calcMedia(n1, n2, n3, n4, tipoMedia = 'ponderada', set75Aprova = false) {
  let m
  if (tipoMedia === 'simples') {
    const vals = [n1, n2, n3, n4].filter(n => n > 0)
    if (!vals.length) return null
    m = vals.reduce((a, b) => a + b, 0) / vals.length
  } else {
    const vals = [[n1, 0.20], [n2, 0.25], [n3, 0.25], [n4, 0.30]].filter(([n]) => n > 0)
    if (!vals.length) return null
    const totalW = vals.reduce((a, [, w]) => a + w, 0)
    m = vals.reduce((a, [n, w]) => a + n * w, 0) / totalW
  }
  return set75Aprova && m >= 5.75 ? 6.0 : m
}

export default function AlunoDetalhe() {
  const { id } = useParams()
  const navigate = useNavigate()

  const [aluno, setAluno]           = useState(null)
  const [notas, setNotas]           = useState([])
  const [analyzeData, setAnalyzeData] = useState(null)
  const [model, setModel]           = useState('RF_M3')
  const [tipoMedia, setTipoMedia]   = useState('ponderada')
  const [set75Aprova, setSet75Aprova] = useState(false)
  const [boletimNota, setBoletimNota] = useState(null)  // nota object for modal
  const [editMode, setEditMode]     = useState(false)
  const [editBuf, setEditBuf]       = useState({})
  const [tab, setTab]               = useState('notas')
  const [loading, setLoading]       = useState(true)
  const [analyzing, setAnalyzing]   = useState(false)
  const [saving, setSaving]         = useState(false)
  const [error, setError]           = useState(null)
  const modelRef = useRef(model)
  modelRef.current = model
  const tipoMediaRef = useRef(tipoMedia)
  tipoMediaRef.current = tipoMedia
  const set75AprovaRef = useRef(set75Aprova)
  set75AprovaRef.current = set75Aprova

  useEffect(() => { loadData() }, [id])

  async function loadData() {
    setLoading(true)
    setError(null)
    try {
      const [alunoData, notasData] = await Promise.all([api.getAluno(id), api.notas(id)])
      setAluno(alunoData)
      setNotas(notasData)
      runAnalyze(modelRef.current, tipoMediaRef.current, set75AprovaRef.current)
    } catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  async function runAnalyze(m, tm, s75) {
    setAnalyzing(true)
    try {
      const data = await api.analyze(id, m, tm, s75)
      setAnalyzeData(data)
    } catch (e) { console.error('analyze:', e) }
    finally { setAnalyzing(false) }
  }

  function handleModelChange(m) {
    setModel(m)
    runAnalyze(m, tipoMediaRef.current, set75AprovaRef.current)
  }

  function handleTipoMediaChange(tm) {
    setTipoMedia(tm)
    runAnalyze(modelRef.current, tm, set75AprovaRef.current)
  }

  function handleSet75AprovaChange(v) {
    setSet75Aprova(v)
    runAnalyze(modelRef.current, tipoMediaRef.current, v)
  }

  function startEdit() {
    const buf = {}
    notas.forEach(n => {
      buf[n.materia_id] = { n1: n.n1 ?? '', n2: n.n2 ?? '', n3: n.n3 ?? '', n4: n.n4 ?? '' }
    })
    setEditBuf(buf)
    setEditMode(true)
  }

  async function saveEdit() {
    setSaving(true)
    try {
      await Promise.all(
        Object.entries(editBuf).map(([mid, v]) =>
          api.salvarNota({
            aluno_id: parseInt(id), materia_id: parseInt(mid),
            n1: v.n1 !== '' ? parseFloat(v.n1) : null,
            n2: v.n2 !== '' ? parseFloat(v.n2) : null,
            n3: v.n3 !== '' ? parseFloat(v.n3) : null,
            n4: v.n4 !== '' ? parseFloat(v.n4) : null,
          })
        )
      )
      setEditMode(false)
      loadData()
    } catch (e) { setError(e.message) }
    finally { setSaving(false) }
  }

  if (loading) return (
    <div className="flex items-center justify-center h-full">
      <div className="w-8 h-8 border-2 border-accent/30 border-t-accent rounded-full animate-spin" />
    </div>
  )
  if (!aluno) return <div className="p-7 text-muted">Aluno não encontrado.</div>

  const ensemble = analyzeData?.ensemble
  const disciplinas = analyzeData?.disciplinas ?? []

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* ── Header ────────────────────────────────────────────────────────── */}
      <div className="px-7 pt-5 pb-4 border-b border-border bg-app-bg flex-shrink-0">
        {/* Breadcrumb */}
        <div className="flex items-center gap-2 text-xs text-muted mb-2">
          <span className="cursor-pointer hover:text-accent" onClick={() => navigate('/salas')}>Turmas</span>
          <span>›</span>
          <span className="cursor-pointer hover:text-accent"
            onClick={() => navigate(`/alunos?sala=${aluno.sala_id}`)}>
            {aluno.sala_nome}
          </span>
          <span>›</span>
          <span className="text-text">{aluno.nome}</span>
        </div>

        <div className="flex items-start justify-between gap-4">
          {/* Left: student info */}
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-accent/10 flex items-center justify-center
                            text-accent text-base font-bold flex-shrink-0">
              {initials(aluno.nome)}
            </div>
            <div>
              <div className="flex items-center gap-3">
                <h1 className="text-xl font-bold text-text">{aluno.nome}</h1>
                {ensemble && (() => { const C = CLS[ensemble.class_value]; return (
                  <span className="text-sm font-bold px-3 py-1 rounded-full flex items-center gap-1.5"
                    style={{ backgroundColor: C?.bg, color: C?.color }}>
                    {C?.Icon && <C.Icon size={13} />} {ensemble.class_name}
                    <span className="font-normal opacity-75">
                      · {(ensemble.confidence * 100).toFixed(0)}%
                    </span>
                  </span>
                )})()}
                {analyzing && (
                  <span className="w-4 h-4 border-2 border-accent/30 border-t-accent rounded-full animate-spin inline-block" />
                )}
              </div>
              <p className="text-sm text-muted">Mat. {aluno.matricula} · {aluno.sala_nome}</p>
            </div>
          </div>

          {/* Right: actions */}
          <div className="flex items-center gap-2 flex-shrink-0">
            <button
              className="text-sm text-accent border border-accent/40 px-4 py-2 rounded-lg
                         hover:bg-indigo-50 transition-colors font-medium flex items-center gap-2"
              onClick={() => navigate('/predicoes', { state: { alunoId: parseInt(id), salaId: aluno.sala_id } })}>
              <GitBranch size={15} /> Árvore de Decisão
            </button>
            {!editMode ? (
              <button className="btn-primary flex items-center gap-2" onClick={startEdit}>
                <PenLine size={15} /> Editar Notas
              </button>
            ) : (
              <>
                <button className="btn-primary flex items-center gap-2" onClick={saveEdit} disabled={saving}>
                  {saving
                    ? <><span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" /> Salvando...</>
                    : <><Save size={15} /> Salvar Notas</>}
                </button>
                <button className="btn-secondary" onClick={() => setEditMode(false)}>Cancelar</button>
              </>
            )}
          </div>
        </div>
      </div>

      {/* ── Tabs ─────────────────────────────────────────────────────────── */}
      <div className="flex items-center gap-2 px-7 py-2 border-b border-border bg-hdr-bg flex-shrink-0">
        <div className="flex gap-1">
          {[['notas', 'Notas do Ano', ClipboardList], ['analise', 'Análise IA', Bot]].map(([k, l, Ic]) => (
            <button key={k} onClick={() => setTab(k)}
              className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition-colors flex items-center gap-1.5 ${
                tab === k ? 'bg-accent text-white' : 'text-muted hover:text-text'
              }`}><Ic size={13} />{l}</button>
          ))}
        </div>

        {tab === 'analise' && (
          <div className="flex items-center gap-2 ml-auto">
            <span className="text-[10px] text-muted font-medium">Modelo:</span>
            <div className="flex bg-white border border-border rounded-lg p-0.5">
              {Object.entries(MODELS).map(([m, info]) => (
                <button key={m} onClick={() => handleModelChange(m)}
                  className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-colors ${
                    model === m ? 'text-white shadow-sm' : 'text-muted hover:text-text'
                  }`}
                  style={model === m ? { backgroundColor: info.color } : {}}>
                  {m.replace('RF_', '')}
                </button>
              ))}
            </div>
            <span className="text-[10px] text-muted hidden xl:inline">{MODELS[model]?.desc}</span>
          </div>
        )}
      </div>

      {/* ── Opções de cálculo ─────────────────────────────────────────────── */}
      <div className="flex items-center gap-4 px-7 py-2 border-b border-border bg-white flex-shrink-0">
        <span className="text-[10px] font-bold text-muted uppercase tracking-widest">
          Opções de cálculo
        </span>

        {/* Média type */}
        <div className="flex items-center gap-2">
          <span className="text-xs text-muted">Média:</span>
          <div className="flex bg-hdr-bg border border-border rounded-lg p-0.5">
            {[['ponderada', 'Ponderada'], ['simples', 'Simples']].map(([v, l]) => (
              <button key={v} onClick={() => handleTipoMediaChange(v)}
                className={`px-3 py-1 rounded-md text-xs font-semibold transition-colors ${
                  tipoMedia === v
                    ? 'bg-accent text-white shadow-sm'
                    : 'text-muted hover:text-text'
                }`}>
                {l}
              </button>
            ))}
          </div>
          {tipoMedia === 'ponderada' && (
            <span className="text-[10px] text-muted hidden sm:inline">
              N1×20% · N2×25% · N3×25% · N4×30%
            </span>
          )}
          {tipoMedia === 'simples' && (
            <span className="text-[10px] text-muted hidden sm:inline">
              Média aritmética das notas lançadas
            </span>
          )}
        </div>

        {/* .75 aprova toggle */}
        <label className="flex items-center gap-2 cursor-pointer select-none ml-2">
          <div
            onClick={() => handleSet75AprovaChange(!set75Aprova)}
            className={`relative w-8 h-4 rounded-full transition-colors cursor-pointer ${
              set75Aprova ? 'bg-accent' : 'bg-slate-300'
            }`}>
            <div className={`absolute top-0.5 w-3 h-3 rounded-full bg-white shadow transition-transform ${
              set75Aprova ? 'translate-x-4' : 'translate-x-0.5'
            }`} />
          </div>
          <span className="text-xs font-semibold text-text">.75 aprova</span>
          <span className="text-xs text-muted">
            {set75Aprova
              ? <span className="text-green-600 font-semibold">Ativo — 5.75 arredonda para 6.0</span>
              : 'Inativo — 5.75 permanece Recuperação'}
          </span>
        </label>

        {analyzing && (
          <span className="ml-auto flex items-center gap-1.5 text-xs text-muted">
            <span className="w-3 h-3 border-2 border-accent/30 border-t-accent rounded-full animate-spin inline-block" />
            Recalculando...
          </span>
        )}
      </div>

      {error && (
        <div className="text-danger text-sm px-7 py-2 bg-red-50 border-b border-red-200 flex items-center gap-2">
          <AlertCircle size={14} /> {error}
        </div>
      )}

      {/* ── Content ───────────────────────────────────────────────────────── */}
      <div className="flex-1 overflow-y-auto p-7">
        {tab === 'notas' && (
          <NotasTab notas={notas} editMode={editMode} editBuf={editBuf}
            tipoMedia={tipoMedia} set75Aprova={set75Aprova}
            onUpdate={(mid, field, val) =>
              setEditBuf(prev => ({ ...prev, [mid]: { ...prev[mid], [field]: val } }))}
            onOpenBoletim={n => setBoletimNota(n)} />
        )}
        {tab === 'analise' && (
          <AnaliseTab disciplinas={disciplinas} ensemble={ensemble} model={model}
            tipoMedia={tipoMedia} set75Aprova={set75Aprova}
            onVerArvore={(d) =>
              navigate('/predicoes', { state: { alunoId: parseInt(id), salaId: aluno.sala_id, materiaId: d.id } })} />
        )}
      </div>

      {/* Boletim modal */}
      {boletimNota && (
        <MateriaBoletimModal
          alunoId={id}
          nota={boletimNota}
          onClose={() => setBoletimNota(null)}
          onNotaChanged={loadData}
        />
      )}
    </div>
  )
}

// ── NotasTab ──────────────────────────────────────────────────────────────────

function NotasTab({ notas, editMode, editBuf, onUpdate, tipoMedia = 'ponderada', set75Aprova = false, onOpenBoletim }) {
  if (!notas.length) return (
    <div className="text-center py-16 text-muted">
      <PenLine size={40} className="mx-auto mb-3 opacity-20" />
      <p className="font-semibold">Nenhuma nota cadastrada</p>
      <p className="text-sm mt-1">Clique em "Editar Notas" para lançar as notas do aluno</p>
    </div>
  )

  // Pre-compute all disciplines for the difficulty map
  const diffItems = notas
    .map(n => {
      const buf = editBuf[n.materia_id] ?? { n1: n.n1, n2: n.n2, n3: n.n3, n4: n.n4 }
      const [v1,v2,v3,v4] = editMode
        ? [buf.n1,buf.n2,buf.n3,buf.n4].map(v => v !== '' ? parseFloat(v)||0 : 0)
        : [n.n1??0, n.n2??0, n.n3??0, n.n4??0]
      const media = calcMedia(v1, v2, v3, v4, tipoMedia, set75Aprova)
      if (media === null) return null
      return { nome: n.materia_nome, media, variancia: calcVariancia(v1,v2,v3,v4), slope: calcSlope(v1,v2,v3,v4) }
    })
    .filter(Boolean)
    .sort((a, b) => a.media - b.media)

  return (
    <div className="space-y-4">
      {/* Legend */}
      <div className="flex items-center gap-6 text-xs text-muted">
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-full bg-green-400" /> Aprovado (≥ 6.0)</span>
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-full bg-amber-400" /> Recuperação (5.0–5.9)</span>
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-full bg-red-400" /> Reprovado (&lt; 5.0)</span>
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-full bg-slate-200" /> Bimestre não lançado</span>
      </div>

      {/* Difficulty map */}
      {diffItems.length >= 2 && <DifficultyMap items={diffItems} />}

      {/* Discipline cards */}
      <div className="grid grid-cols-1 gap-3 lg:grid-cols-2">
        {notas.map(n => {
          const buf = editBuf[n.materia_id] ?? { n1: n.n1, n2: n.n2, n3: n.n3, n4: n.n4 }
          const [v1, v2, v3, v4] = editMode
            ? [buf.n1, buf.n2, buf.n3, buf.n4].map(v => v !== '' ? parseFloat(v) || 0 : 0)
            : [n.n1 ?? 0, n.n2 ?? 0, n.n3 ?? 0, n.n4 ?? 0]
          const rawMedia = calcMedia(v1, v2, v3, v4, tipoMedia, false)
          const media    = rawMedia !== null && set75Aprova && rawMedia >= 5.75 ? 6.0 : rawMedia
          const wasRounded = rawMedia !== null && set75Aprova && rawMedia >= 5.75 && rawMedia < 6.0
          const status = media === null ? null : media >= 6 ? 2 : media >= 5 ? 1 : 0
          const cls = status !== null ? CLS[status] : null
          const variancia = calcVariancia(v1, v2, v3, v4)
          const slope     = calcSlope(v1, v2, v3, v4)
          const trend     = trendInfo(slope)
          const TI        = trend.Icon

          return (
            <div key={n.materia_id}
              className="card p-4 cursor-pointer hover:ring-2 hover:ring-accent/30 hover:shadow-md transition-all"
              onClick={() => !editMode && onOpenBoletim?.(n)}
              title={editMode ? '' : 'Clique para ver o boletim completo'}>
              <div className="flex items-center justify-between mb-3">
                <span className="font-semibold text-text">{n.materia_nome}</span>
                {cls && (
                  <span className="text-xs font-bold px-2.5 py-1 rounded-full flex items-center gap-1"
                    style={{ backgroundColor: cls.bg, color: cls.color }}>
                    {cls.Icon && <cls.Icon size={11} />} {cls.name}
                  </span>
                )}
              </div>

              {/* Grade cells */}
              <div className="grid grid-cols-4 gap-2 mb-3">
                {[1, 2, 3, 4].map(i => {
                  const key = `n${i}`
                  const raw = editMode ? buf[key] : n[key]
                  const val = raw !== null && raw !== '' ? parseFloat(raw) : null
                  const hasVal = val !== null && !isNaN(val) && val > 0
                  const color = !hasVal ? '#94A3B8' : val >= 6 ? '#10B981' : val >= 5 ? '#F59E0B' : '#EF4444'
                  return (
                    <div key={i} className="text-center">
                      <p className="text-[10px] text-muted mb-1">N{i}</p>
                      {editMode ? (
                        <input
                          type="number" min="0" max="10" step="0.1"
                          value={buf[key] ?? ''}
                          onChange={e => onUpdate(n.materia_id, key, e.target.value)}
                          className="input text-center text-sm font-bold py-1.5 px-1"
                          style={{ color }}
                          placeholder="—"
                        />
                      ) : (
                        <div className="border border-border rounded-lg py-1.5 px-2 text-sm font-bold"
                          style={{ color, backgroundColor: hasVal ? `${color}12` : '#F8FAFC' }}>
                          {hasVal ? val.toFixed(1) : '—'}
                        </div>
                      )}
                    </div>
                  )
                })}
              </div>

              {/* Media bar */}
              {media !== null && (
                <div>
                  <div className="flex justify-between text-[10px] text-muted mb-1">
                    <span>
                      Média {tipoMedia === 'simples' ? 'simples' : 'ponderada'}
                      {wasRounded && <span className="ml-1 text-green-600 font-semibold">(arredondada ↑)</span>}
                    </span>
                    <span className="font-bold" style={{ color: cls?.color }}>{media.toFixed(2)}</span>
                  </div>
                  <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                    <div className="h-full rounded-full transition-all"
                      style={{ width: `${Math.min(media * 10, 100)}%`, backgroundColor: cls?.color ?? '#94A3B8' }} />
                  </div>

                  {/* Variance + trend */}
                  {(variancia !== null || slope !== null) && (
                    <div className="flex items-center gap-3 mt-2 text-[10px]">
                      {variancia !== null && (
                        <span className="text-muted">
                          variância{' '}
                          <span className="font-bold text-text">{variancia.toFixed(2)}</span>
                          {variancia > 2.5 && <span className="ml-1 text-amber-500 font-semibold">· irregular</span>}
                          {variancia <= 0.5 && <span className="ml-1 text-slate-400">· consistente</span>}
                        </span>
                      )}
                      {TI && (
                        <span className="flex items-center gap-0.5 ml-auto font-semibold"
                          style={{ color: trend.color }}>
                          <TI size={11} /> {trend.label}
                        </span>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}

function DifficultyMap({ items }) {
  return (
    <div className="card p-4">
      <div className="flex items-center gap-2 mb-3">
        <p className="text-[10px] font-bold text-muted uppercase tracking-widest">
          Mapa de dificuldades
        </p>
        <span className="text-[10px] text-muted">— menor média = mais dificuldade</span>
      </div>
      <div className="space-y-2.5">
        {items.map((d, i) => {
          const color = d.media >= 6 ? '#10B981' : d.media >= 5 ? '#F59E0B' : '#EF4444'
          const trend = trendInfo(d.slope)
          const TI    = trend.Icon
          const varLabel = d.variancia === null ? null
            : d.variancia > 2.5 ? { text: 'irregular', bg: '#FEF3C7', color: '#D97706' }
            : d.variancia <= 0.5 ? { text: 'consistente', bg: '#D1FAE5', color: '#059669' }
            : null
          return (
            <div key={i} className="flex items-center gap-2">
              <span className="text-xs text-muted w-32 truncate shrink-0">{d.nome}</span>
              <div className="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
                <div className="h-full rounded-full transition-all"
                  style={{ width: `${Math.min(d.media * 10, 100)}%`, backgroundColor: color }} />
              </div>
              <span className="text-xs font-bold w-8 text-right shrink-0" style={{ color }}>
                {d.media.toFixed(1)}
              </span>
              {d.variancia !== null && (
                <span className="text-[10px] font-mono text-muted w-14 text-right shrink-0">
                  σ²{d.variancia.toFixed(2)}
                </span>
              )}
              {varLabel && (
                <span className="text-[9px] font-bold px-1.5 py-0.5 rounded shrink-0"
                  style={{ backgroundColor: varLabel.bg, color: varLabel.color }}>
                  {varLabel.text}
                </span>
              )}
              {TI
                ? <TI size={12} style={{ color: trend.color }} className="shrink-0" />
                : <span className="w-3 shrink-0" />
              }
            </div>
          )
        })}
      </div>
      <div className="flex items-center gap-4 mt-3 pt-3 border-t border-border text-[10px] text-muted">
        <span>σ² = variância (0 = consistente · alto = irregular)</span>
        <span className="flex items-center gap-1 ml-auto"><TrendingUp size={10} style={{ color: '#10B981' }} /> melhorando</span>
        <span className="flex items-center gap-1"><Minus size={10} style={{ color: '#94A3B8' }} /> estável</span>
        <span className="flex items-center gap-1"><TrendingDown size={10} style={{ color: '#EF4444' }} /> caindo</span>
      </div>
    </div>
  )
}

// ── AnaliseTab ────────────────────────────────────────────────────────────────

function AnaliseTab({ disciplinas, ensemble, model, onVerArvore }) {
  if (!disciplinas.length) return (
    <div className="text-center py-16 text-muted">
      <Bot size={40} className="mx-auto mb-3 opacity-20" />
      <p>Nenhuma análise disponível. Certifique-se de que o aluno tem notas cadastradas.</p>
    </div>
  )

  const incomplete = disciplinas.filter(d => !d.completa)
  const complete   = disciplinas.filter(d => d.completa)

  return (
    <div className="space-y-6">
      {/* Ensemble summary — redesigned to be self-explanatory */}
      {ensemble && <EnsembleCard ensemble={ensemble} />}

      {/* Incomplete: prediction needed */}
      {incomplete.length > 0 && (
        <div>
          <p className="text-[10px] font-bold text-amber-600 uppercase tracking-widest mb-3 flex items-center gap-2">
            <AlertTriangle size={12} /> Disciplinas com predição ativa ({incomplete.length})
            <span className="font-normal text-muted normal-case">— ano em aberto</span>
          </p>
          <div className="grid grid-cols-1 gap-3 lg:grid-cols-2">
            {incomplete.map(d => <DisciplinaCard key={d.id} d={d} onVerArvore={onVerArvore} />)}
          </div>
        </div>
      )}

      {/* Complete: validate IA */}
      {complete.length > 0 && (
        <div>
          <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-3 flex items-center gap-2">
            <CheckCircle2 size={12} /> Disciplinas concluídas ({complete.length})
            <span className="font-normal text-muted normal-case">— comparar IA vs resultado real</span>
          </p>
          <div className="grid grid-cols-1 gap-3 lg:grid-cols-2">
            {complete.map(d => <DisciplinaCard key={d.id} d={d} onVerArvore={onVerArvore} />)}
          </div>
        </div>
      )}
    </div>
  )
}

function EnsembleCard({ ensemble }) {
  const cls = CLS[ensemble.class_value]
  const pct = (ensemble.confidence * 100).toFixed(0)
  const winner = ensemble.votes[ensemble.class_value]
  const total  = ensemble.n_trees

  const MEANING = {
    0: 'O aluno tem alto risco de reprovação. Atenção imediata é necessária.',
    1: 'O aluno está na faixa de recuperação. Pode melhorar com acompanhamento.',
    2: 'O aluno tem bom desempenho e tende a ser aprovado.',
  }

  return (
    <div className="card overflow-hidden">
      {/* Colored top strip */}
      <div className="h-1.5" style={{ backgroundColor: cls?.color }} />

      <div className="p-5">
        {/* Main result */}
        <div className="flex items-start gap-5 mb-5">
          <div className="rounded-xl p-4 flex-shrink-0"
            style={{ backgroundColor: cls?.bg }}>
            {cls?.Icon && <cls.Icon size={28} style={{ color: cls?.color }} />}
          </div>
          <div>
            <p className="text-[10px] text-muted uppercase tracking-widest mb-1">
              Diagnóstico geral do aluno
            </p>
            <p className="text-xl font-bold" style={{ color: cls?.color }}>
              {cls?.name}
            </p>
            <p className="text-sm text-muted mt-1 max-w-md">
              {MEANING[ensemble.class_value]}
            </p>
          </div>
          <div className="ml-auto text-right flex-shrink-0">
            <p className="text-3xl font-bold" style={{ color: cls?.color }}>{pct}%</p>
            <p className="text-xs text-muted">de confiança</p>
          </div>
        </div>

        {/* How it works — brief explanation */}
        <div className="bg-slate-50 border border-border rounded-xl p-4 mb-4">
          <p className="text-xs font-semibold text-text mb-1">Como essa predição funciona</p>
          <p className="text-xs text-muted leading-relaxed">
            O modelo RandomForest usa <strong className="text-text">{total} árvores de decisão independentes</strong>.
            Cada árvore analisa as notas do aluno e dá um "voto". A predição final é a opção
            que recebeu mais votos — neste caso, <strong style={{ color: cls?.color }}>{cls?.name}</strong>{' '}
            recebeu <strong style={{ color: cls?.color }}>{winner} de {total} votos ({pct}%)</strong>.
          </p>
        </div>

        {/* Vote breakdown */}
        <p className="text-[10px] text-muted uppercase tracking-widest mb-3">
          Resultado da votação — {total} árvores
        </p>
        <div className="space-y-2.5">
          {ensemble.votes.map((v, i) => {
            const pctVote = ((v / total) * 100).toFixed(0)
            const isWinner = i === ensemble.class_value
            const VoteIcon = CLS[i]?.Icon
            return (
              <div key={i} className={`rounded-lg p-2.5 ${isWinner ? 'ring-1' : ''}`}
                style={isWinner ? { backgroundColor: CLS[i]?.bg, ringColor: CLS[i]?.color } : {}}>
                <div className="flex items-center gap-3 mb-1.5">
                  {VoteIcon && <VoteIcon size={14} style={{ color: CLS[i]?.color }} />}
                  <span className="text-xs font-semibold text-text flex-1">{CLS[i]?.name}</span>
                  <span className="text-xs font-bold" style={{ color: CLS[i]?.color }}>
                    {v} votos · {pctVote}%
                  </span>
                  {isWinner && (
                    <span className="text-[10px] font-bold px-1.5 py-0.5 rounded"
                      style={{ backgroundColor: CLS[i]?.color, color: '#fff' }}>
                      vencedor
                    </span>
                  )}
                </div>
                <div className="h-2 bg-white/60 rounded-full overflow-hidden">
                  <div className="h-full rounded-full transition-all"
                    style={{ width: `${pctVote}%`, backgroundColor: CLS[i]?.color }} />
                </div>
              </div>
            )
          })}
        </div>

        <p className="text-[10px] text-muted mt-3">
          * Predição baseada na média agregada de todas as disciplinas do aluno. Use a aba de disciplinas para ver a análise individual de cada matéria.
        </p>
      </div>
    </div>
  )
}

function DisciplinaCard({ d, onVerArvore }) {
  const realMeta = CLS[d.status]
  const pred     = d.predicao
  const predMeta = pred ? CLS[pred.class_value] : null
  const iaAcertou = d.completa && pred ? pred.class_value === d.status : null

  return (
    <div className="card p-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <span className="font-semibold text-text">{d.nome}</span>
        <div className="flex items-center gap-2">
          {d.completa ? (
            <span className="text-[10px] text-slate-400">{d.notas_count}/4 notas</span>
          ) : (
            <span className="text-[10px] font-semibold text-amber-600 bg-amber-50 px-2 py-0.5 rounded">
              {d.notas_count}/4 · predição ativa
            </span>
          )}
        </div>
      </div>

      {/* Grades row */}
      <div className="flex gap-3 text-xs mb-3">
        {[d.n1, d.n2, d.n3, d.n4].map((n, i) => (
          <div key={i} className="text-center">
            <p className="text-[9px] text-muted mb-0.5">N{i + 1}</p>
            <span className={`font-bold ${n > 0 ? '' : 'text-slate-300'}`}
              style={n > 0 ? { color: n >= 6 ? '#10B981' : n >= 5 ? '#F59E0B' : '#EF4444' } : {}}>
              {n > 0 ? n.toFixed(1) : '—'}
            </span>
          </div>
        ))}
        <div className="text-center ml-auto">
          <p className="text-[9px] text-muted mb-0.5">Média</p>
          <span className="font-bold text-sm" style={{ color: realMeta?.color }}>
            {d.media.toFixed(2)}
          </span>
        </div>
      </div>

      {/* IA prediction vs real result */}
      <div className="rounded-lg p-2.5 mb-2"
        style={{ backgroundColor: d.completa ? '#F8FAFC' : predMeta?.bg ?? '#F8FAFC' }}>
        {d.completa ? (
          <div className="flex items-center justify-between">
            <div>
              <p className="text-[10px] text-muted mb-0.5">Resultado real</p>
              <span className="font-bold text-sm flex items-center gap-1" style={{ color: realMeta?.color }}>
                {realMeta?.Icon && <realMeta.Icon size={12} />} {realMeta?.name}
              </span>
            </div>
            {pred && (
              <div className="text-right">
                <p className="text-[10px] text-muted mb-0.5">IA previu</p>
                <div className="flex items-center gap-1.5">
                  <span className="font-bold text-sm" style={{ color: predMeta?.color }}>
                    {predMeta?.name}
                  </span>
                  {iaAcertou !== null && (
                    <span className={`text-xs font-bold px-1.5 py-0.5 rounded flex items-center gap-0.5 ${
                      iaAcertou ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                    }`}>
                      {iaAcertou
                        ? <><CheckCircle2 size={10} /> acertou</>
                        : <><XCircle size={10} /> errou</>}
                    </span>
                  )}
                </div>
              </div>
            )}
          </div>
        ) : pred ? (
          <div className="flex items-center justify-between">
            <div>
              <p className="text-[10px] text-muted mb-0.5">Predição da IA</p>
              <span className="font-bold text-sm flex items-center gap-1" style={{ color: predMeta?.color }}>
                {predMeta?.Icon && <predMeta.Icon size={12} />} {predMeta?.name}
              </span>
            </div>
            <div className="text-right">
              <p className="text-[10px] text-muted mb-0.5">Confiança</p>
              <div className="flex items-center gap-1.5">
                <div className="w-16 h-1.5 bg-slate-200 rounded-full overflow-hidden">
                  <div className="h-full rounded-full"
                    style={{ width: `${pred.confidence * 100}%`, backgroundColor: predMeta?.color }} />
                </div>
                <span className="text-xs font-bold" style={{ color: predMeta?.color }}>
                  {(pred.confidence * 100).toFixed(0)}%
                </span>
              </div>
            </div>
          </div>
        ) : (
          <p className="text-xs text-muted text-center">IA sem dados suficientes</p>
        )}
      </div>

      <button
        onClick={() => onVerArvore(d)}
        className="w-full text-xs text-accent font-semibold py-1.5 rounded-lg
                   bg-indigo-50 hover:bg-indigo-100 transition-colors">
        <GitBranch size={13} /> Ver caminho na árvore de decisão
      </button>
    </div>
  )
}
