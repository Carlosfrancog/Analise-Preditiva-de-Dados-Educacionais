import { useState, useEffect } from 'react'
import { Trash2, BookOpen, Sparkles, Plus, AlertCircle } from 'lucide-react'
import { api } from '../api'

const DEFAULT_NAMES = [
  'Português', 'Matemática', 'História', 'Geografia', 'Ciências',
  'Física', 'Química', 'Biologia', 'Inglês', 'Filosofia',
  'Sociologia', 'Educação Física', 'Arte',
]

export default function Materias() {
  const [materias, setMaterias] = useState([])
  const [loading, setLoading]   = useState(true)
  const [novo, setNovo]         = useState('')
  const [saving, setSaving]     = useState(false)
  const [error, setError]       = useState(null)
  const [confirm, setConfirm]   = useState(null)

  useEffect(() => { load() }, [])

  async function load() {
    setLoading(true)
    try { setMaterias(await api.materias()) }
    catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  async function handleCreate() {
    if (!novo.trim()) return
    setSaving(true)
    try {
      await api.criarMateria(novo.trim())
      setNovo('')
      await load()
    } catch (e) { setError(e.message) }
    finally { setSaving(false) }
  }

  async function handleDefault() {
    setSaving(true)
    try {
      await api.materiasDefault()
      await load()
    } catch (e) { setError(e.message) }
    finally { setSaving(false) }
  }

  async function handleDelete(id) {
    try {
      await api.deletarMateria(id)
      setConfirm(null)
      await load()
    } catch (e) { setError(e.message) }
  }

  const existingNames   = new Set(materias.map(m => m.nome.toLowerCase()))
  const missingDefaults = DEFAULT_NAMES.filter(n => !existingNames.has(n.toLowerCase()))

  return (
    <div className="p-7 max-w-3xl">
      {/* Header */}
      <div className="flex items-start justify-between mb-6">
        <div>
          <p className="text-[10px] text-muted uppercase tracking-widest mb-1">Configurações</p>
          <h1 className="text-2xl font-bold text-text">Matérias</h1>
          <p className="text-sm text-muted mt-0.5">
            {materias.length} matéria{materias.length !== 1 ? 's' : ''} cadastrada{materias.length !== 1 ? 's' : ''}
          </p>
        </div>

        {missingDefaults.length > 0 && (
          <button
            onClick={handleDefault}
            disabled={saving}
            className="btn-secondary text-sm flex items-center gap-2">
            <Sparkles size={14} />
            Adicionar padrão
            <span className="text-[10px] bg-slate-200 text-slate-600 px-1.5 py-0.5 rounded font-bold">
              +{missingDefaults.length}
            </span>
          </button>
        )}
      </div>

      {error && (
        <div className="text-danger text-sm mb-4 bg-red-50 border border-red-200 rounded-lg px-4 py-2 flex items-center gap-2">
          <AlertCircle size={14} /> {error}
        </div>
      )}

      {/* Add new */}
      <div className="card p-4 mb-5 flex items-end gap-3">
        <div className="flex-1">
          <label className="text-xs text-muted mb-1 block">Nova matéria</label>
          <input
            className="input"
            placeholder="Ex: Redação, Artes Visuais..."
            value={novo}
            onChange={e => setNovo(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleCreate()}
          />
        </div>
        <button
          className="btn-primary flex items-center gap-2"
          onClick={handleCreate}
          disabled={saving || !novo.trim()}>
          <Plus size={15} /> Adicionar
        </button>
      </div>

      {/* List */}
      {loading ? (
        <div className="flex justify-center py-12">
          <div className="w-7 h-7 border-2 border-accent/30 border-t-accent rounded-full animate-spin" />
        </div>
      ) : materias.length === 0 ? (
        <div className="card p-12 text-center">
          <BookOpen size={40} className="mx-auto mb-3 text-muted opacity-30" />
          <p className="font-semibold text-text">Nenhuma matéria cadastrada</p>
          <p className="text-sm text-muted mt-1">
            Clique em "Adicionar padrão" para incluir as 13 matérias comuns.
          </p>
        </div>
      ) : (
        <div className="card overflow-hidden">
          <div className="px-4 py-3 bg-hdr-bg border-b border-border">
            <p className="text-[10px] text-muted uppercase tracking-widest font-semibold">
              Lista de matérias
            </p>
          </div>
          <ul className="divide-y divide-border">
            {materias.map((m, i) => (
              <li key={m.id}
                className={`flex items-center px-5 py-3 group ${i % 2 === 1 ? 'bg-hdr-bg/40' : ''}`}>
                <span className="w-6 text-[10px] text-muted font-mono">{i + 1}</span>
                <span className="flex-1 text-sm font-semibold text-text">{m.nome}</span>

                {confirm === m.id ? (
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-muted">Confirmar exclusão?</span>
                    <button
                      onClick={() => handleDelete(m.id)}
                      className="text-xs font-semibold text-white bg-danger px-2.5 py-1 rounded-lg">
                      Excluir
                    </button>
                    <button
                      onClick={() => setConfirm(null)}
                      className="text-xs text-muted hover:text-text px-2 py-1">
                      Cancelar
                    </button>
                  </div>
                ) : (
                  <button
                    onClick={() => setConfirm(m.id)}
                    className="text-muted hover:text-danger opacity-0 group-hover:opacity-100 transition-opacity p-1">
                    <Trash2 size={14} />
                  </button>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}

      {missingDefaults.length > 0 && (
        <div className="mt-4 bg-indigo-50 border border-indigo-200 rounded-xl px-4 py-3">
          <p className="text-xs font-semibold text-accent mb-1">Matérias padrão disponíveis</p>
          <p className="text-[10px] text-muted leading-relaxed">
            {missingDefaults.join(' · ')}
          </p>
        </div>
      )}
    </div>
  )
}
