import { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import {
  XCircle, AlertTriangle, CheckCircle2,
  Search, AlertCircle, BookOpen, GitBranch,
  ChevronLeft, ChevronRight, Minimize2, Clapperboard,
} from 'lucide-react'
import { api } from '../api'
import DecisionTreeCanvas from '../components/DecisionTreeCanvas'
import EnsembleTimelapse from '../components/EnsembleTimelapse'

const CLS = {
  0: { name: 'Reprovado',   color: '#EF4444', bg: '#FEE2E2', Icon: XCircle       },
  1: { name: 'Recuperação', color: '#F59E0B', bg: '#FEF3C7', Icon: AlertTriangle  },
  2: { name: 'Aprovado',    color: '#10B981', bg: '#D1FAE5', Icon: CheckCircle2   },
}

const FEAT_LABEL = {
  n1_norm: 'N1 (1º Bim)', n2_norm: 'N2 (2º Bim)',
  n3_norm: 'N3 (3º Bim)', n4_norm: 'N4 (4º Bim)',
  slope_notas: 'Tendência N1→N4', variancia_notas: 'Variância',
  media_geral_aluno: 'Média geral', serie_num_norm: 'Série',
  media_turma_norm: 'Média turma',
}

const MODELS = {
  RF_M1: { label: 'M1', desc: '83.8% · 100 árvores', color: '#10B981' },
  RF_M2: { label: 'M2', desc: '90.4% · 150 árvores', color: '#0EA5E9' },
  RF_M3: { label: 'M3', desc: '91.3% · 200 árvores', color: '#4F46E5' },
}

export default function Predicoes() {
  const location = useLocation()
  const navState = location.state ?? {}

  const [salas, setSalas]           = useState([])
  const [alunos, setAlunos]         = useState([])
  const [salaId, setSalaId]         = useState(navState.salaId ? String(navState.salaId) : '')
  const [alunoId, setAlunoId]       = useState(navState.alunoId ? String(navState.alunoId) : '')
  const [model, setModel]           = useState('RF_M3')
  const [loading, setLoading]       = useState(false)
  const [treeLoading, setTreeLoading] = useState(false)
  const [analyzeData, setAnalyzeData] = useState(null)
  const [treeData, setTreeData]     = useState(null)
  const [selectedDisc, setSelectedDisc] = useState(null)
  const [treeIdx, setTreeIdx]       = useState(0)
  const [error, setError]           = useState(null)
  const [expanded, setExpanded]     = useState(false)
  const [timelapse, setTimelapse]   = useState(false)

  useEffect(() => { api.predSalas().then(setSalas).catch(console.error) }, [])

  useEffect(() => {
    if (!salaId) { setAlunos([]); return }
    api.predAlunos(salaId).then(setAlunos).catch(console.error)
  }, [salaId])

  // Auto-analyze if navigated here with a student pre-selected
  useEffect(() => {
    if (navState.alunoId && navState.salaId) {
      handleAnalyze(navState.alunoId, navState.materiaId)
    }
  }, [])

  async function handleAnalyze(overrideAlunoId, overrideMateriaId) {
    const aid = overrideAlunoId || alunoId
    if (!aid) return
    setLoading(true); setError(null)
    setAnalyzeData(null); setTreeData(null); setSelectedDisc(null); setTreeIdx(0)
    try {
      const analyze = await api.analyze(aid, model)
      setAnalyzeData(analyze)
      // If a specific materia was requested (from navigation), use it
      let autoDisc
      if (overrideMateriaId) {
        autoDisc = analyze.disciplinas.find(d => d.id === overrideMateriaId)
      }
      if (!autoDisc) {
        const incomplete = analyze.disciplinas.filter(d => !d.completa)
        autoDisc = incomplete.length > 0
          ? incomplete.reduce((a, b) => a.media < b.media ? a : b)
          : analyze.disciplinas.find(d => d.id === analyze.worst_materia_id)
      }
      if (autoDisc) {
        setSelectedDisc(autoDisc)
        const tree = await api.decisionTree(aid, autoDisc.id, model, 0)
        setTreeData(tree)
      }
      setActiveTab('disciplinas')
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  async function loadTree(disc, idx = 0, m) {
    const aid = alunoId || (navState.alunoId ? String(navState.alunoId) : '')
    if (!aid || treeLoading) return
    const useModel = m || model
    setSelectedDisc(disc)
    setTreeIdx(idx)
    setTreeLoading(true)
    try {
      const tree = await api.decisionTree(aid, disc?.id ?? null, useModel, idx)
      setTreeData(tree)
    } catch (e) {
      setError(e.message)
    } finally {
      setTreeLoading(false)
    }
  }

  async function handleTreeNav(delta) {
    const nTrees = analyzeData?.ensemble?.n_trees ?? 200
    const newIdx = Math.max(0, Math.min(nTrees - 1, treeIdx + delta))
    if (newIdx === treeIdx || !selectedDisc) return
    await loadTree(selectedDisc, newIdx)
  }

  const aluno    = analyzeData?.aluno
  const ensemble = analyzeData?.ensemble
  const nTrees   = ensemble?.n_trees ?? 200

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* Header */}
      <div className="px-7 pt-5 pb-4 border-b border-border bg-app-bg flex-shrink-0">
        <p className="text-[10px] text-muted uppercase tracking-widest mb-1">IA / Predições</p>
        <h1 className="text-2xl font-bold text-text">Análise de Desempenho</h1>
        <p className="text-sm text-muted mt-0.5">
          Clique em uma disciplina para ver a decisão da IA — nó por nó.
        </p>
      </div>

      {/* Controls */}
      <div className="flex items-center gap-3 px-7 py-3 bg-hdr-bg border-b border-border flex-shrink-0">
        <label className="text-xs text-muted font-medium">Turma</label>
        <select className="select text-sm" value={salaId}
          onChange={e => { setSalaId(e.target.value); setAlunoId('') }}>
          <option value="">Selecione...</option>
          {salas.map(s => <option key={s.id} value={s.id}>{s.nome}</option>)}
        </select>

        <label className="text-xs text-muted font-medium ml-2">Aluno</label>
        <select className="select text-sm flex-1 max-w-xs" value={alunoId}
          onChange={e => setAlunoId(e.target.value)} disabled={!salaId}>
          <option value="">Selecione...</option>
          {alunos.map(a => (
            <option key={a.id} value={a.id}>{a.nome} ({a.matricula})</option>
          ))}
        </select>

        {/* Model selector */}
        <div className="flex items-center gap-1.5 ml-2">
          <span className="text-xs text-muted">Modelo:</span>
          <div className="flex bg-slate-100 rounded-lg p-0.5">
            {Object.entries(MODELS).map(([m, info]) => (
              <button key={m} onClick={() => setModel(m)}
                className={`px-2.5 py-1 rounded-md text-xs font-semibold transition-colors ${
                  model === m ? 'text-white shadow-sm' : 'text-muted hover:text-text'
                }`}
                style={model === m ? { backgroundColor: info.color } : {}}
                title={info.desc}>
                {info.label}
              </button>
            ))}
          </div>
        </div>

        <button className="btn-primary flex items-center gap-2 px-5"
          onClick={() => handleAnalyze()} disabled={!alunoId || loading}>
          {loading
            ? <span className="inline-block w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            : <Search size={14} />}
          {loading ? 'Analisando...' : 'Analisar'}
        </button>

        {error && (
          <span className="text-danger text-xs ml-2 flex items-center gap-1">
            <AlertCircle size={13} /> {error}
          </span>
        )}
      </div>

      {!analyzeData ? <EmptyState /> : (
        <div className="flex-1 overflow-y-auto p-6 space-y-5">

          {/* Student summary row */}
          {aluno && ensemble && (
            <div className="card p-4 flex items-center gap-5">
              <div className="flex-1">
                <p className="text-[10px] text-muted uppercase tracking-wider">{aluno.sala}</p>
                <p className="font-bold text-text text-lg leading-tight">{aluno.nome}</p>
                <p className="text-xs text-muted-2">Mat. {aluno.matricula}</p>
              </div>

              {/* Ensemble verdict */}
              <div className="rounded-xl px-5 py-3 text-center border"
                style={{ backgroundColor: CLS[ensemble.class_value]?.bg,
                         borderColor: `${CLS[ensemble.class_value]?.color}40` }}>
                <div className="flex items-center gap-1.5 justify-center mb-0.5"
                  style={{ color: CLS[ensemble.class_value]?.color }}>
                  {(() => { const I = CLS[ensemble.class_value]?.Icon; return I ? <I size={14} /> : null })()}
                  <span className="font-black text-base">{ensemble.class_name}</span>
                </div>
                <p className="text-[11px]" style={{ color: CLS[ensemble.class_value]?.color }}>
                  {(ensemble.confidence * 100).toFixed(0)}% confiança
                </p>
              </div>

              {/* Vote bars */}
              <div className="w-52 space-y-1.5">
                <p className="text-[10px] text-muted mb-1">{nTrees} árvores votaram:</p>
                {ensemble.votes.map((v, i) => (
                  <div key={i} className="flex items-center gap-2 text-[10px]">
                    <span className="w-20 text-muted">{CLS[i]?.name}</span>
                    <div className="flex-1 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                      <div className="h-full rounded-full" style={{
                        width: `${(v / nTrees) * 100}%`, backgroundColor: CLS[i]?.color }} />
                    </div>
                    <span className="w-6 text-right font-bold" style={{ color: CLS[i]?.color }}>{v}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Disciplinas grid */}
          <div>
            <p className="text-[10px] font-bold text-muted uppercase tracking-widest mb-3">
              Disciplinas — clique em uma para abrir a árvore de decisão
            </p>
            <div className="grid grid-cols-2 gap-3">
              {analyzeData.disciplinas.map(d => (
                <DiscCard
                  key={d.id} d={d}
                  selected={selectedDisc}
                  onSelect={disc => { loadTree(disc, 0); setExpanded(true) }}
                  disabled={treeLoading}
                />
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ── Canvas modal ── */}
      {expanded && analyzeData && (
        <div className="fixed inset-0 z-50 bg-slate-950 flex flex-col modal-stickout">
          {/* Modal header */}
          <div className="flex-shrink-0 flex items-center gap-3 px-4 py-2 bg-slate-900/95 border-b border-slate-800">
            {/* Discipline label */}
            <div className="flex items-center gap-2">
              <span className="text-[10px] text-slate-500 uppercase tracking-widest">Disciplina</span>
              <span className="text-sm font-bold text-white">{treeData?.focus_disciplina ?? '—'}</span>
              {treeData?.prediction && (() => {
                const cv = treeData.prediction.class_value
                const I = CLS[cv]?.Icon
                return (
                  <span className="text-xs font-bold px-2 py-0.5 rounded-full flex items-center gap-1"
                    style={{ backgroundColor: CLS[cv]?.bg, color: CLS[cv]?.color }}>
                    {I && <I size={11} />} {treeData.prediction.class_name}
                  </span>
                )
              })()}
              {selectedDisc && (
                <span className="text-[10px] text-slate-500">
                  {selectedDisc.completa
                    ? '(ano concluído — resultado calculado)'
                    : `(${selectedDisc.notas_count}/4 notas — predição ativa)`}
                </span>
              )}
            </div>

            <div className="flex-1" />

            {/* Discipline switcher */}
            <div className="flex items-center gap-1 bg-slate-800/70 rounded-lg p-0.5 max-w-xs overflow-x-auto">
              {analyzeData.disciplinas.map(d => (
                <button key={d.id}
                  onClick={() => loadTree(d, 0)}
                  disabled={treeLoading}
                  className={`px-2 py-1 rounded-md text-[10px] font-semibold whitespace-nowrap transition-colors ${
                    selectedDisc?.id === d.id
                      ? 'bg-indigo-600 text-white'
                      : 'text-slate-400 hover:text-white'
                  }`}>
                  {d.nome.split(' ')[0]}
                </button>
              ))}
            </div>

            {/* Tree navigator */}
            <div className="flex items-center gap-2 bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5">
              <span className="text-[10px] text-slate-400 uppercase tracking-widest">Estimador</span>
              <button onClick={() => handleTreeNav(-1)} disabled={treeIdx === 0 || treeLoading}
                className="w-5 h-5 flex items-center justify-center text-slate-300 hover:text-white
                           disabled:opacity-30 disabled:cursor-not-allowed transition-colors">
                <ChevronLeft size={14} />
              </button>
              <span className="text-sm font-bold text-white w-20 text-center">
                #{treeIdx + 1} de {nTrees}
              </span>
              <button onClick={() => handleTreeNav(1)} disabled={treeIdx >= nTrees - 1 || treeLoading}
                className="w-5 h-5 flex items-center justify-center text-slate-300 hover:text-white
                           disabled:opacity-30 disabled:cursor-not-allowed transition-colors">
                <ChevronRight size={14} />
              </button>
            </div>

            {/* Prediction badge */}
            {treeData?.prediction && (
              <div className="flex items-center gap-2 bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5">
                <span className="text-[10px] text-slate-400">Predição final:</span>
                <span className="text-sm font-bold"
                  style={{ color: CLS[treeData.prediction.class_value]?.color }}>
                  {treeData.prediction.class_name} · {(treeData.prediction.confidence * 100).toFixed(0)}%
                </span>
              </div>
            )}

            {/* Timelapse */}
            {treeData && (
              <button onClick={() => setTimelapse(true)}
                className="flex items-center gap-1.5 px-2.5 h-7 rounded-lg text-xs font-semibold
                           bg-indigo-900/60 border border-indigo-700/60 text-indigo-300
                           hover:bg-indigo-800/60 hover:text-white transition-colors">
                <Clapperboard size={12} /> Timelapse
              </button>
            )}

            {/* Close */}
            <button onClick={() => setExpanded(false)}
              className="w-7 h-7 flex items-center justify-center rounded-lg bg-slate-800
                         border border-slate-700 text-slate-400 hover:text-white
                         hover:border-slate-500 transition-colors">
              <Minimize2 size={13} />
            </button>
          </div>

          {/* Canvas body */}
          <div className="flex-1 overflow-hidden relative">
            {treeLoading && (
              <div className="absolute inset-0 flex items-center justify-center bg-slate-950/70 z-20">
                <div className="w-8 h-8 border-2 border-accent/30 border-t-accent rounded-full animate-spin" />
              </div>
            )}
            {timelapse && (
              <EnsembleTimelapse
                alunoId={alunoId || (navState.alunoId ? String(navState.alunoId) : '')}
                materiaId={selectedDisc?.id ?? null}
                model={model}
                onClose={() => setTimelapse(false)}
              />
            )}
            {treeData ? (
              <div className="h-full">
                <DecisionTreeCanvas
                  treeData={treeData.tree}
                  pathIds={treeData.path_ids ?? []}
                  prediction={treeData.prediction}
                  features={treeData.features ?? {}}
                />
              </div>
            ) : (
              <div className="flex items-center justify-center h-full text-slate-500 text-sm">
                Selecione uma disciplina acima
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

// ── Sub-components ─────────────────────────────────────────────────────────────

function EmptyState() {
  return (
    <div className="flex-1 flex flex-col items-center justify-center text-center p-8">
      <GitBranch size={60} className="mx-auto mb-4 text-muted opacity-20" />
      <h2 className="text-lg font-semibold text-text mb-2">Árvore de Decisão por Disciplina</h2>
      <p className="text-sm text-muted max-w-md">
        Selecione uma turma e um aluno, clique em <strong>Analisar</strong>.
        As disciplinas com menos de 4 notas mostrarão a <strong>predição da IA</strong> —
        as completas mostrarão o resultado já calculado.
      </p>
      <div className="mt-6 grid grid-cols-3 gap-2 text-xs text-muted max-w-xs">
        {['N1·N2·N3·N4', 'Tendência', 'Variância', 'Média Geral', 'Série', 'Média Turma'].map(f => (
          <span key={f} className="bg-hdr-bg border border-border rounded-lg px-2 py-1.5 text-center">{f}</span>
        ))}
      </div>
    </div>
  )
}

function DisciplinaList({ disciplinas, selected, onSelect, disabled }) {
  const incomplete = disciplinas.filter(d => !d.completa)
  const complete   = disciplinas.filter(d => d.completa)

  return (
    <div>
      {/* Incomplete first — these are the ones that NEED prediction */}
      {incomplete.length > 0 && (
        <>
          <div className="px-4 pt-3 pb-1">
            <p className="text-[10px] font-bold text-amber-600 uppercase tracking-widest">
              Predição ativa ({incomplete.length})
            </p>
            <p className="text-[10px] text-muted">Disciplinas com ano em aberto</p>
          </div>
          {incomplete.map(d => <DiscCard key={d.id} d={d} selected={selected} onSelect={onSelect} disabled={disabled} />)}
        </>
      )}

      {/* Complete disciplines */}
      {complete.length > 0 && (
        <>
          <div className="px-4 pt-3 pb-1">
            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
              Ano concluído ({complete.length})
            </p>
            <p className="text-[10px] text-muted">4 bimestres lançados — resultado definido</p>
          </div>
          {complete.map(d => <DiscCard key={d.id} d={d} selected={selected} onSelect={onSelect} disabled={disabled} />)}
        </>
      )}
    </div>
  )
}

function DiscCard({ d, selected, onSelect, disabled }) {
  const meta = CLS[d.status] ?? CLS[2]
  const isSelected = selected?.id === d.id
  const pred = d.predicao

  return (
    <div
      onClick={() => !disabled && onSelect(d)}
      className={`px-4 py-3 border-b border-border cursor-pointer transition-colors ${
        isSelected ? 'bg-indigo-50 border-l-4 border-l-accent' : 'hover:bg-slate-50'
      }`}
    >
      {/* Name + status badge */}
      <div className="flex items-center justify-between mb-1.5">
        <span className="text-sm font-semibold text-text truncate flex-1 mr-2">{d.nome}</span>
        <span className="text-[10px] font-bold px-2 py-0.5 rounded-full shrink-0 flex items-center gap-0.5"
          style={{ backgroundColor: meta.bg, color: meta.color }}>
          {meta.Icon && <meta.Icon size={9} />} {meta.name}
        </span>
      </div>

      {/* Grades row */}
      <div className="flex gap-2 text-[10px] mb-1.5">
        {[d.n1, d.n2, d.n3, d.n4].map((n, i) => (
          <span key={i} className={n > 0 ? 'text-text' : 'text-slate-300'}>
            N{i + 1}: <strong>{n > 0 ? n.toFixed(1) : '—'}</strong>
          </span>
        ))}
        <span className="ml-auto font-bold text-xs" style={{ color: meta.color }}>
          {d.media.toFixed(2)}
        </span>
      </div>

      {/* Grade bar */}
      <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden mb-1.5">
        <div className="h-full rounded-full" style={{
          width: `${Math.min(d.media * 10, 100)}%`, backgroundColor: meta.color,
        }} />
      </div>

      {/* IA prediction or "year complete" note */}
      {d.completa ? (
        <p className="text-[10px] text-slate-400 flex items-center gap-1">
          <CheckCircle2 size={10} className="text-green-500" /> Resultado calculado pelas 4 notas
          {pred && <span> · IA confirma: <span style={{ color: CLS[pred.class_value]?.color }}>{pred.class_name}</span></span>}
        </p>
      ) : (
        pred ? (
          <div className="flex items-center gap-1.5">
            <span className="text-[10px] font-bold px-1.5 py-0.5 rounded"
              style={{ backgroundColor: CLS[pred.class_value]?.bg, color: CLS[pred.class_value]?.color }}>
              IA: {pred.class_name}
            </span>
            <div className="flex-1 h-1 bg-slate-100 rounded-full overflow-hidden">
              <div className="h-full rounded-full"
                style={{ width: `${pred.confidence * 100}%`, backgroundColor: CLS[pred.class_value]?.color }} />
            </div>
            <span className="text-[10px] font-bold" style={{ color: CLS[pred.class_value]?.color }}>
              {(pred.confidence * 100).toFixed(0)}%
            </span>
          </div>
        ) : (
          <p className="text-[10px] text-slate-400">{d.notas_count}/4 notas lançadas</p>
        )
      )}
    </div>
  )
}

function FeatureTable({ features }) {
  return (
    <div className="px-4 py-3 space-y-2">
      <p className="text-[10px] text-muted uppercase tracking-widest mb-3">
        Vetor de entrada — disciplina selecionada
      </p>
      {Object.entries(features).map(([k, v]) => (
        <div key={k} className="flex items-center justify-between gap-3">
          <span className="text-xs text-muted w-28 shrink-0">{FEAT_LABEL[k] ?? k}</span>
          <div className="flex-1 h-1.5 bg-slate-100 rounded-full overflow-hidden">
            <div className="h-full bg-accent rounded-full"
              style={{ width: `${Math.min(Math.abs(v) * 100, 100)}%` }} />
          </div>
          <span className="text-xs font-mono font-bold text-accent w-12 text-right">
            {typeof v === 'number' ? v.toFixed(3) : v}
          </span>
        </div>
      ))}
    </div>
  )
}
