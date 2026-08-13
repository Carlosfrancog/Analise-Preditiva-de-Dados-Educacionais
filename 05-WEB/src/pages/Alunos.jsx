import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { Trash2, User, Search, Plus, AlertCircle } from 'lucide-react'
import { api } from '../api'
import { useToast } from '../components/Toast'

function initials(nome) {
  return nome.split(' ').map(n => n[0]).filter(Boolean).slice(0, 2).join('').toUpperCase()
}

const FILTERS = [
  { key: 'todos',        label: 'Todos' },
  { key: 'risco',        label: 'Em risco' },
  { key: 'recuperacao',  label: 'Recuperação' },
  { key: 'aprovado',     label: 'Aprovado' },
]

export default function Alunos() {
  const navigate   = useNavigate()
  const toast      = useToast()
  const [params]   = useSearchParams()
  const salaId     = params.get('sala') ? parseInt(params.get('sala')) : null

  const [salas, setSalas]             = useState([])
  const [alunos, setAlunos]           = useState([])
  const [predictions, setPredictions] = useState({})
  const [salaInfo, setSalaInfo]       = useState(null)
  const [loading, setLoading]         = useState(true)
  const [predLoading, setPredLoading] = useState(false)
  const [search, setSearch]           = useState('')
  const [statusFilter, setStatusFilter] = useState('todos')
  const [form, setForm]               = useState({ open: false, nome: '', salaId: salaId || '' })
  const [error, setError]             = useState(null)

  useEffect(() => { api.salas().then(setSalas).catch(console.error) }, [])
  useEffect(() => { loadAlunos() }, [salaId])

  async function loadAlunos() {
    setLoading(true)
    setPredictions({})
    setStatusFilter('todos')
    try {
      const data = await api.alunos(salaId)
      setAlunos(data)
      if (salaId) {
        // Use already-loaded salas state instead of re-fetching
        setSalaInfo(null) // will be resolved once salas loads
        loadPredictions(salaId)
      }
    } catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  // Resolve salaInfo from salas state when both are ready
  useEffect(() => {
    if (salaId && salas.length) setSalaInfo(salas.find(s => s.id === salaId) ?? null)
  }, [salas, salaId])

  async function loadPredictions(sid) {
    if (!sid) return
    setPredLoading(true)
    try {
      const preds = await api.turmaRapida(sid)
      const map = {}
      preds.forEach(p => { map[p.id] = p })
      setPredictions(map)
    } catch (e) { console.error('preds:', e) }
    finally { setPredLoading(false) }
  }

  async function handleCreate() {
    const sid = form.salaId || salaId
    if (!form.nome.trim() || !sid) return
    try {
      await api.criarAluno(form.nome.trim(), parseInt(sid))
      await api.atribuirMaterias()
      setForm(f => ({ ...f, open: false, nome: '' }))
      loadAlunos()
      toast.success(`Aluno "${form.nome.trim()}" criado com sucesso.`)
    } catch (e) { setError(e.message); toast.error(e.message) }
  }

  async function handleDelete(e, id, nome) {
    e.stopPropagation()
    if (!window.confirm(`Remover "${nome}" e todas as suas notas?`)) return
    try {
      await api.deletarAluno(id)
      setAlunos(prev => prev.filter(a => a.id !== id))
      toast.warning(`Aluno "${nome}" removido.`)
    } catch (e) { setError(e.message); toast.error(e.message) }
  }

  const filtered = alunos.filter(a => {
    if (search && !a.nome.toLowerCase().includes(search.toLowerCase())) return false
    if (statusFilter === 'todos') return true
    const info = predictions[a.id]
    if (!info) return statusFilter === 'todos'
    if (statusFilter === 'risco')       return info.n_risco > 0
    if (statusFilter === 'recuperacao') return info.n_risco === 0 && info.n_atencao > 0
    if (statusFilter === 'aprovado')    return info.n_risco === 0 && info.n_atencao === 0 && info.n_disciplinas > 0
    return true
  })

  const hasFilter = statusFilter !== 'todos'

  return (
    <div className="p-7 max-w-5xl">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <div className="flex items-center gap-2 text-xs text-muted mb-1">
            <span className="cursor-pointer hover:text-accent" onClick={() => navigate('/salas')}>
              Turmas
            </span>
            {salaInfo && <><span>›</span><span className="text-text font-medium">{salaInfo.nome}</span></>}
          </div>
          <h1 className="text-2xl font-bold text-text">
            {salaInfo ? salaInfo.nome : 'Todos os Alunos'}
          </h1>
          <p className="text-sm text-muted mt-0.5">{alunos.length} alunos cadastrados</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="relative">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted" />
            <input className="input text-sm w-52 pl-8" placeholder="Buscar aluno..."
              value={search} onChange={e => setSearch(e.target.value)} />
          </div>
          <button className="btn-primary flex items-center gap-2"
            onClick={() => setForm(f => ({ ...f, open: !f.open }))}>
            <Plus size={15} /> Novo Aluno
          </button>
        </div>
      </div>

      {/* New student form */}
      {form.open && (
        <div className="card p-4 mb-6 flex items-end gap-4 flex-wrap">
          <div className="flex-1 min-w-48">
            <label className="text-xs text-muted mb-1 block">Nome do aluno</label>
            <input className="input" placeholder="Nome completo"
              value={form.nome} onChange={e => setForm(f => ({ ...f, nome: e.target.value }))}
              onKeyDown={e => e.key === 'Enter' && handleCreate()} />
          </div>
          {!salaId && (
            <div>
              <label className="text-xs text-muted mb-1 block">Turma</label>
              <select className="select" value={form.salaId}
                onChange={e => setForm(f => ({ ...f, salaId: e.target.value }))}>
                <option value="">Selecione...</option>
                {salas.map(s => <option key={s.id} value={s.id}>{s.nome}</option>)}
              </select>
            </div>
          )}
          <button className="btn-primary" onClick={handleCreate}>Criar</button>
          <button className="btn-secondary" onClick={() => setForm(f => ({ ...f, open: false, nome: '' }))}>
            Cancelar
          </button>
        </div>
      )}

      {error && (
        <div className="text-danger text-sm mb-4 bg-red-50 border border-red-200 rounded-lg px-4 py-2 flex items-center gap-2">
          <AlertCircle size={14} /> {error}
        </div>
      )}

      {/* Status filters (only when turmaRapida data is available) */}
      {salaId && (
        <div className="flex items-center gap-2 mb-4">
          <span className="text-[10px] text-muted uppercase tracking-widest mr-1">Filtrar:</span>
          {FILTERS.map(f => (
            <button key={f.key}
              onClick={() => setStatusFilter(f.key)}
              className={`text-xs font-semibold px-3 py-1.5 rounded-full transition-colors border ${
                statusFilter === f.key
                  ? 'bg-accent text-white border-accent'
                  : 'text-muted border-border hover:text-text hover:border-slate-300'
              }`}>
              {f.label}
              {f.key !== 'todos' && !predLoading && Object.keys(predictions).length > 0 && (
                <span className="ml-1.5 opacity-70">
                  {f.key === 'risco'
                    ? alunos.filter(a => predictions[a.id]?.n_risco > 0).length
                    : f.key === 'recuperacao'
                    ? alunos.filter(a => { const p = predictions[a.id]; return p && p.n_risco === 0 && p.n_atencao > 0 }).length
                    : alunos.filter(a => { const p = predictions[a.id]; return p && p.n_risco === 0 && p.n_atencao === 0 && p.n_disciplinas > 0 }).length
                  }
                </span>
              )}
            </button>
          ))}
          {hasFilter && (
            <button onClick={() => setStatusFilter('todos')}
              className="text-xs text-muted hover:text-accent ml-auto">
              Limpar filtro
            </button>
          )}
        </div>
      )}

      {loading ? (
        <div className="flex justify-center py-16">
          <div className="w-7 h-7 border-2 border-accent/30 border-t-accent rounded-full animate-spin" />
        </div>
      ) : (
        <div className="card overflow-hidden">
          <table className="w-full">
            <thead className="bg-hdr-bg border-b border-border">
              <tr className="text-[10px] text-muted uppercase tracking-wider">
                <th className="px-5 py-3 text-left font-semibold">Aluno</th>
                <th className="px-4 py-3 text-left font-semibold">Matrícula</th>
                <th className="px-4 py-3 text-left font-semibold">Turma</th>
                <th className="px-4 py-3 text-left font-semibold">Média</th>
                <th className="px-4 py-3 text-left font-semibold">
                  {predLoading
                    ? <span className="flex items-center gap-1.5">
                        <span className="w-3 h-3 border-2 border-accent/30 border-t-accent rounded-full animate-spin inline-block" />
                        Carregando...
                      </span>
                    : 'Situação por matéria'}
                </th>
                <th className="px-4 py-3" />
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {filtered.map((a, i) => {
                const info = predictions[a.id]
                const aprovadas = info ? Math.max(0, (info.n_disciplinas ?? 0) - (info.n_risco ?? 0) - (info.n_atencao ?? 0)) : null
                return (
                  <tr key={a.id}
                    className={`cursor-pointer hover:bg-indigo-50/50 transition-colors ${i % 2 === 1 ? 'bg-hdr-bg/40' : ''}`}
                    onClick={() => navigate(`/alunos/${a.id}`)}>
                    <td className="px-5 py-3">
                      <div className="flex items-center gap-3">
                        <div className="w-9 h-9 rounded-full bg-accent/10 flex items-center justify-center
                                        text-accent text-xs font-bold flex-shrink-0">
                          {initials(a.nome)}
                        </div>
                        <span className="font-semibold text-sm text-text">{a.nome}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-sm text-muted font-mono">{a.matricula}</td>
                    <td className="px-4 py-3 text-sm text-muted">{a.sala_nome}</td>
                    <td className="px-4 py-3 text-sm">
                      {info?.media_geral != null ? (
                        <span className={`font-bold ${
                          info.media_geral >= 6 ? 'text-green-600'
                          : info.media_geral >= 5 ? 'text-amber-600'
                          : 'text-red-600'
                        }`}>
                          {info.media_geral.toFixed(1)}
                        </span>
                      ) : '—'}
                    </td>
                    <td className="px-4 py-3">
                      {info ? (
                        <div className="flex items-center gap-1.5 flex-wrap">
                          {(info.n_risco ?? 0) > 0 && (
                            <span className="text-[10px] font-semibold text-red-700 bg-red-50 border border-red-200 px-2 py-0.5 rounded-full whitespace-nowrap">
                              {info.n_risco} reprovada{info.n_risco > 1 ? 's' : ''}
                            </span>
                          )}
                          {(info.n_atencao ?? 0) > 0 && (
                            <span className="text-[10px] font-semibold text-amber-700 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded-full whitespace-nowrap">
                              {info.n_atencao} recuperação
                            </span>
                          )}
                          {aprovadas > 0 && (
                            <span className="text-[10px] font-semibold text-green-700 bg-green-50 border border-green-200 px-2 py-0.5 rounded-full whitespace-nowrap">
                              {aprovadas} aprovada{aprovadas > 1 ? 's' : ''}
                            </span>
                          )}
                          {!info.n_disciplinas && (
                            <span className="text-[10px] text-muted italic">sem notas</span>
                          )}
                        </div>
                      ) : predLoading ? null : (
                        <span className="text-[10px] text-muted italic">—</span>
                      )}
                    </td>
                    <td className="px-4 py-3 text-right">
                      <button
                        onClick={e => handleDelete(e, a.id, a.nome)}
                        className="text-muted hover:text-danger transition-colors p-1">
                        <Trash2 size={14} />
                      </button>
                    </td>
                  </tr>
                )
              })}
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-5 py-14 text-center text-muted text-sm">
                    <User size={36} className="mx-auto mb-3 opacity-20" />
                    {search || hasFilter
                      ? 'Nenhum aluno encontrado com os filtros aplicados.'
                      : 'Nenhum aluno cadastrado nesta turma.'}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
