import { useEffect, useMemo, useState } from 'react'
import { AlertTriangle, Database, FlaskConical, RefreshCw } from 'lucide-react'
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
  const [catalog, setCatalog] = useState([])
  const [cutoff, setCutoff] = useState('M1')
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const selected = useMemo(
    () => catalog.find(item => item.cutoff === cutoff),
    [catalog, cutoff],
  )

  async function loadCatalog() {
    setError('')
    try {
      const data = await api.researchSnapshots()
      setCatalog(data)
      if (data.length && !data.some(item => item.cutoff === cutoff)) {
        setCutoff(data[0].cutoff)
      }
    } catch (err) {
      setError(err.message)
    }
  }

  async function loadSamples(nextCutoff = cutoff) {
    setLoading(true)
    setError('')
    try {
      const data = await api.researchSamples(nextCutoff, { limit: 30 })
      setRows(data)
    } catch (err) {
      setRows([])
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { loadCatalog() }, [])
  useEffect(() => { loadSamples(cutoff) }, [cutoff])

  return (
    <div className="p-6 max-w-[1500px] mx-auto space-y-5">
      <header className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <div className="flex items-center gap-2 text-accent mb-1">
            <FlaskConical size={18} />
            <span className="text-xs font-bold uppercase tracking-widest">Pesquisa</span>
          </div>
          <h1 className="text-2xl font-bold text-text">Dados temporais da pesquisa</h1>
          <p className="text-sm text-muted mt-1">
            Amostras e predições da pipeline experimental, separadas do modelo legado.
          </p>
        </div>
        <button className="btn-secondary flex items-center gap-2" onClick={() => loadSamples()} disabled={loading}>
          <RefreshCw size={15} className={loading ? 'animate-spin' : ''} /> Atualizar
        </button>
      </header>

      {error && (
        <div className="card border-danger/30 bg-red-50 px-4 py-3 flex items-start gap-3 text-sm text-danger">
          <AlertTriangle size={17} className="mt-0.5 flex-shrink-0" />
          <div><strong>Não foi possível carregar a pesquisa.</strong><p className="mt-1">{error}</p></div>
        </div>
      )}

      <section className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {catalog.map(item => (
          <button
            key={item.cutoff}
            onClick={() => setCutoff(item.cutoff)}
            className={`card text-left p-4 transition-all ${cutoff === item.cutoff ? 'ring-2 ring-accent' : 'hover:border-accent/40'}`}
          >
            <div className="flex items-center justify-between">
              <span className="text-lg font-bold text-text">{item.cutoff}</span>
              <span className={`text-xs font-semibold ${item.model_available ? 'text-success' : 'text-danger'}`}>
                {item.model_available ? 'modelo pronto' : 'modelo ausente'}
              </span>
            </div>
            <p className="text-xs text-muted mt-2">{item.rows.toLocaleString('pt-BR')} registros</p>
            <p className="text-xs text-muted mt-1">{item.features.join(', ')}</p>
          </button>
        ))}
      </section>

      {selected && (
        <div className="card overflow-hidden">
          <div className="px-5 py-4 border-b border-border flex flex-wrap gap-3 items-center justify-between">
            <div className="flex items-center gap-2">
              <Database size={17} className="text-accent" />
              <div>
                <h2 className="font-bold text-text">Amostras do corte {selected.cutoff}</h2>
                <p className="text-xs text-muted">Features disponíveis até o momento selecionado</p>
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
                  {selected.features.slice(0, 3).map(feature => <th key={feature} className="text-right px-3 py-3">{feature}</th>)}
                  <th className="text-left px-3 py-3">Rótulo</th>
                  <th className="text-left px-5 py-3">Predição</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {rows.map((row, index) => {
                  const prediction = row.prediction
                  const target = LABELS[row.target]
                  return (
                    <tr key={`${row.student_id}-${row.subject_id}-${index}`} className="hover:bg-hdr-bg">
                      <td className="px-5 py-3 font-medium text-text">{row.student_id}</td>
                      <td className="px-3 py-3 text-muted">{row.subject_id}</td>
                      <td className="px-3 py-3 text-muted">{row.academic_year}</td>
                      {selected.features.slice(0, 3).map(feature => <td key={feature} className="px-3 py-3 text-right font-mono text-xs text-text">{formatFeature(row[feature])}</td>)}
                      <td className={`px-3 py-3 font-medium ${target?.className ?? 'text-muted'}`}>{target?.text ?? '—'}</td>
                      <td className="px-5 py-3">
                        {prediction ? <span className="font-semibold text-text">{prediction.predicted_label} <span className="text-xs text-muted">({(prediction.confidence * 100).toFixed(1)}%)</span></span> : '—'}
                      </td>
                    </tr>
                  )
                })}
                {!loading && rows.length === 0 && <tr><td colSpan="9" className="px-5 py-8 text-center text-muted">Nenhum registro encontrado.</td></tr>}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
