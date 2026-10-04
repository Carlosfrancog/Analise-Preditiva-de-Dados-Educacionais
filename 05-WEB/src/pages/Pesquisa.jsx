import { useEffect, useMemo, useRef, useState } from 'react'
import {
  AlertTriangle,
  Beaker,
  Database,
  FlaskConical,
  RefreshCw,
  Search,
  ShieldCheck,
} from 'lucide-react'
import { api } from '../api'

const LABELS = {
  0: { text: 'Reprovado', className: 'text-danger' },
  1: { text: 'Recuperação', className: 'text-warn' },
  2: { text: 'Aprovado', className: 'text-success' },
}

function formatFeature(value) {
  if (value === null || value === undefined) return '—'
  return typeof value === 'number' ? value.toFixed(3) : value
}

export default function Pesquisa() {
  const requestSequence = useRef(0)
  const [pipelineStatus, setPipelineStatus] = useState(null)
  const [catalog, setCatalog] = useState([])
  const [cutoff, setCutoff] = useState('M1')
  const [rows, setRows] = useState([])
  const [filters, setFilters] = useState({ studentId: '', academicYear: '' })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const selected = useMemo(
    () => catalog.find(item => item.cutoff === cutoff),
    [catalog, cutoff],
  )

  function sampleParams(nextFilters = filters) {
    return {
      limit: 30,
      studentId: nextFilters.studentId.trim() || undefined,
      academicYear: nextFilters.academicYear
        ? Number(nextFilters.academicYear)
        : undefined,
    }
  }

  async function loadSamples(nextCutoff = cutoff, nextFilters = filters) {
    const requestId = ++requestSequence.current
    setLoading(true)
    setError('')
    try {
      const data = await api.researchSamples(nextCutoff, sampleParams(nextFilters))
      if (requestId === requestSequence.current) setRows(data)
    } catch (err) {
      if (requestId === requestSequence.current) {
        setRows([])
        setError(err.message || 'Falha ao carregar amostras.')
      }
    } finally {
      if (requestId === requestSequence.current) setLoading(false)
    }
  }

  async function loadPage() {
    const requestId = ++requestSequence.current
    setLoading(true)
    setError('')
    try {
      const data = await api.researchStatus()
      const snapshots = data.snapshots ?? []
      const nextCutoff = snapshots.some(item => item.cutoff === cutoff)
        ? cutoff
        : snapshots[0]?.cutoff

      if (requestId !== requestSequence.current) return
      setPipelineStatus(data)
      setCatalog(snapshots)
      if (nextCutoff) setCutoff(nextCutoff)

      const nextSnapshot = snapshots.find(item => item.cutoff === nextCutoff)
      if (nextSnapshot?.data_available && nextSnapshot?.model_available) {
        const samples = await api.researchSamples(nextCutoff, sampleParams(filters))
        if (requestId === requestSequence.current) setRows(samples)
      } else {
        setRows([])
      }
    } catch (err) {
      if (requestId === requestSequence.current) {
        setRows([])
        setError(err.message || 'Falha ao consultar a pipeline.')
      }
    } finally {
      if (requestId === requestSequence.current) setLoading(false)
    }
  }

  function selectCutoff(nextCutoff) {
    setCutoff(nextCutoff)
    const item = catalog.find(candidate => candidate.cutoff === nextCutoff)
    if (item?.data_available && item?.model_available) loadSamples(nextCutoff)
    else {
      requestSequence.current += 1
      setRows([])
      setLoading(false)
    }
  }

  function applyFilters(event) {
    event.preventDefault()
    if (selected?.data_available && selected?.model_available) {
      loadSamples(cutoff, filters)
    }
  }

  useEffect(() => {
    loadPage()
    // A carga inicial é intencionalmente única; as demais ações são explícitas.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const isReady = pipelineStatus?.status === 'ready'
  const columnCount = (selected?.features.length ?? 0) + 5

  return (
    <div className="p-6 max-w-[1500px] mx-auto space-y-5">
      <header className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <div className="flex items-center gap-2 text-accent mb-1">
            <FlaskConical size={18} />
            <span className="text-xs font-bold uppercase tracking-widest">Pesquisa</span>
          </div>
          <h1 className="text-2xl font-bold text-text">Pesquisa temporal</h1>
          <p className="text-sm text-muted mt-1">
            Snapshots e inferências experimentais separados do fluxo legado.
          </p>
        </div>
        <button type="button" className="btn-secondary flex items-center gap-2" onClick={loadPage} disabled={loading}>
          <RefreshCw size={15} className={loading ? 'animate-spin' : ''} />
          Atualizar
        </button>
      </header>

      <section className="card border-amber-200 bg-amber-50 px-4 py-3 flex items-start gap-3">
        <Beaker size={18} className="mt-0.5 flex-shrink-0 text-amber-700" />
        <div>
          <p className="text-sm font-semibold text-amber-900">Ambiente experimental</p>
          <p className="text-xs text-amber-800 mt-0.5">
            {pipelineStatus?.warning ?? 'Os dados desta tela são sintéticos e não representam estudantes reais.'}
          </p>
        </div>
      </section>

      {error && (
        <div className="card border-danger/30 bg-red-50 px-4 py-3 flex items-start gap-3 text-sm text-danger">
          <AlertTriangle size={17} className="mt-0.5 flex-shrink-0" />
          <div>
            <strong>Não foi possível carregar a pesquisa.</strong>
            <p className="mt-1">{error}</p>
          </div>
        </div>
      )}

      <section className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div className="card p-4">
          <p className="text-xs uppercase tracking-wide text-muted">Pipeline</p>
          <div className="flex items-center gap-2 mt-2">
            <ShieldCheck size={18} className={isReady ? 'text-success' : 'text-warn'} />
            <span className={`font-bold ${isReady ? 'text-success' : 'text-warn'}`}>
              {isReady ? 'Pronta para demonstração' : 'Preparação necessária'}
            </span>
          </div>
        </div>
        <div className="card p-4">
          <p className="text-xs uppercase tracking-wide text-muted">Fonte</p>
          <p className="font-bold text-text mt-2">
            {pipelineStatus?.source === 'synthetic' ? 'Dados sintéticos' : '—'}
          </p>
        </div>
        <div className="card p-4">
          <p className="text-xs uppercase tracking-wide text-muted">Versão</p>
          <p className="font-mono text-sm font-semibold text-text mt-2">
            {pipelineStatus?.pipeline ?? '—'}
          </p>
        </div>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {catalog.map(item => (
          <button
            type="button"
            key={item.cutoff}
            onClick={() => selectCutoff(item.cutoff)}
            className={`card text-left p-4 transition-all ${cutoff === item.cutoff ? 'ring-2 ring-accent' : 'hover:border-accent/40'}`}
          >
            <div className="flex items-center justify-between gap-3">
              <span className="text-lg font-bold text-text">{item.cutoff}</span>
              <span className={`text-xs font-semibold ${item.model_available ? 'text-success' : 'text-danger'}`}>
                {item.model_available ? 'modelo pronto' : 'modelo ausente'}
              </span>
            </div>
            <p className="text-xs text-muted mt-2">{item.rows.toLocaleString('pt-BR')} registros</p>
            <p className="text-xs text-muted mt-1 break-words">{item.features.join(', ')}</p>
          </button>
        ))}
      </section>

      {selected && (
        <form className="card p-4 grid grid-cols-1 md:grid-cols-[1fr_180px_auto] gap-3 items-end" onSubmit={applyFilters}>
          <label className="text-xs font-semibold text-muted">
            Aluno
            <input
              className="input mt-1.5"
              value={filters.studentId}
              onChange={event => setFilters(current => ({ ...current, studentId: event.target.value }))}
              placeholder="Ex.: stu_00001"
            />
          </label>
          <label className="text-xs font-semibold text-muted">
            Ano acadêmico
            <input
              className="input mt-1.5"
              type="number"
              min="2000"
              max="2100"
              value={filters.academicYear}
              onChange={event => setFilters(current => ({ ...current, academicYear: event.target.value }))}
              placeholder="Todos"
            />
          </label>
          <button type="submit" className="btn-primary flex items-center justify-center gap-2" disabled={loading || !selected.model_available}>
            <Search size={15} /> Aplicar filtros
          </button>
        </form>
      )}

      {selected && (
        <div className="card overflow-hidden">
          <div className="px-5 py-4 border-b border-border flex flex-wrap gap-3 items-center justify-between">
            <div className="flex items-center gap-2">
              <Database size={17} className="text-accent" />
              <div>
                <h2 className="font-bold text-text">Amostras do corte {selected.cutoff}</h2>
                <p className="text-xs text-muted">
                  {selected.model?.evaluation_warning ?? 'Features disponíveis até o momento selecionado.'}
                </p>
              </div>
            </div>
            <span className="text-xs text-muted">{rows.length} linhas exibidas</span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-hdr-bg text-xs text-muted uppercase">
                <tr>
                  <th className="text-left px-5 py-3">Aluno</th>
                  <th className="text-left px-3 py-3">Disciplina</th>
                  <th className="text-left px-3 py-3">Ano</th>
                  {selected.features.map(feature => (
                    <th key={feature} className="text-right px-3 py-3 whitespace-nowrap">{feature}</th>
                  ))}
                  <th className="text-left px-3 py-3">Rótulo</th>
                  <th className="text-left px-5 py-3">Predição</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {loading && (
                  <tr>
                    <td colSpan={columnCount} className="px-5 py-8 text-center text-muted">
                      Carregando amostras…
                    </td>
                  </tr>
                )}
                {!loading && rows.map((row, index) => {
                  const prediction = row.prediction
                  const target = LABELS[row.target]
                  return (
                    <tr key={`${row.student_id}-${row.subject_id}-${index}`} className="hover:bg-hdr-bg">
                      <td className="px-5 py-3 font-medium text-text whitespace-nowrap">{row.student_id}</td>
                      <td className="px-3 py-3 text-muted whitespace-nowrap">{row.subject_id}</td>
                      <td className="px-3 py-3 text-muted">{row.academic_year}</td>
                      {selected.features.map(feature => (
                        <td key={feature} className="px-3 py-3 text-right font-mono text-xs text-text">
                          {formatFeature(row[feature])}
                        </td>
                      ))}
                      <td className={`px-3 py-3 font-medium whitespace-nowrap ${target?.className ?? 'text-muted'}`}>{target?.text ?? '—'}</td>
                      <td className="px-5 py-3 whitespace-nowrap">
                        {prediction ? <span className="font-semibold text-text">{prediction.predicted_label} <span className="text-xs text-muted">({(prediction.confidence * 100).toFixed(1)}%)</span></span> : '—'}
                      </td>
                    </tr>
                  )
                })}
                {!loading && rows.length === 0 && (
                  <tr>
                    <td colSpan={columnCount} className="px-5 py-8 text-center text-muted">
                      {selected.model_available
                        ? 'Nenhum registro encontrado para os filtros informados.'
                        : 'Execute a pipeline para gerar o modelo deste corte.'}
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
