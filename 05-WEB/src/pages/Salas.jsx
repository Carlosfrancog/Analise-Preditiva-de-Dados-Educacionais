import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Building2, Trash2, Users, AlertCircle, Plus } from 'lucide-react'
import { api } from '../api'

export default function Salas() {
  const navigate = useNavigate()
  const [salas, setSalas]     = useState([])
  const [loading, setLoading] = useState(true)
  const [form, setForm]       = useState({ open: false, nome: '', codigo: '' })
  const [error, setError]     = useState(null)

  async function load() {
    setLoading(true)
    try { setSalas(await api.salas()) }
    catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  useEffect(() => { load() }, [])

  async function handleCreate() {
    if (!form.nome.trim() || !form.codigo.trim()) return
    try {
      await api.criarSala(form.nome.trim(), form.codigo.trim().toUpperCase())
      setForm({ open: false, nome: '', codigo: '' })
      load()
    } catch (e) { setError(e.message) }
  }

  async function handleDelete(e, id) {
    e.stopPropagation()
    if (!window.confirm('Remover esta turma? Todos os alunos serão deletados.')) return
    try { await api.deletarSala(id); load() }
    catch (e) { setError(e.message) }
  }

  return (
    <div className="p-7 max-w-5xl">
      <div className="flex items-center justify-between mb-6">
        <div>
          <p className="text-[10px] text-muted uppercase tracking-widest mb-1">Gestão Escolar</p>
          <h1 className="text-2xl font-bold text-text">Turmas</h1>
          <p className="text-sm text-muted mt-0.5">Clique em uma turma para ver seus alunos</p>
        </div>
        <button className="btn-primary flex items-center gap-2"
          onClick={() => setForm(f => ({ ...f, open: !f.open }))}>
          <Plus size={15} /> Nova Turma
        </button>
      </div>

      {form.open && (
        <div className="card p-4 mb-6 flex items-end gap-4 flex-wrap">
          <div>
            <label className="text-xs text-muted mb-1 block">Nome da turma</label>
            <input className="input w-56" placeholder="ex: 6º Fundamental"
              value={form.nome} onChange={e => setForm(f => ({ ...f, nome: e.target.value }))}
              onKeyDown={e => e.key === 'Enter' && handleCreate()} />
          </div>
          <div>
            <label className="text-xs text-muted mb-1 block">Código</label>
            <input className="input w-24" placeholder="ex: 6F"
              value={form.codigo} onChange={e => setForm(f => ({ ...f, codigo: e.target.value }))}
              onKeyDown={e => e.key === 'Enter' && handleCreate()} />
          </div>
          <button className="btn-primary" onClick={handleCreate}>Criar</button>
          <button className="btn-secondary" onClick={() => setForm({ open: false, nome: '', codigo: '' })}>
            Cancelar
          </button>
        </div>
      )}

      {error && (
        <div className="text-danger text-sm mb-4 bg-red-50 border border-red-200 rounded-lg px-4 py-2 flex items-center gap-2">
          <AlertCircle size={14} /> {error}
        </div>
      )}

      {loading ? (
        <div className="flex justify-center py-16">
          <div className="w-7 h-7 border-2 border-accent/30 border-t-accent rounded-full animate-spin" />
        </div>
      ) : salas.length === 0 ? (
        <div className="text-center py-20 text-muted">
          <Building2 size={48} className="mx-auto mb-4 opacity-30" />
          <p className="font-semibold text-text mb-1">Nenhuma turma cadastrada</p>
          <p className="text-sm">Clique em "Nova Turma" para começar</p>
        </div>
      ) : (
        <div className="grid grid-cols-2 gap-4 lg:grid-cols-3">
          {salas.map(s => (
            <div key={s.id}
              onClick={() => navigate(`/alunos?sala=${s.id}`)}
              className="card p-5 cursor-pointer hover:shadow-md hover:border-accent/30
                         transition-all group flex flex-col">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <p className="font-bold text-text text-base leading-tight">{s.nome}</p>
                  <span className="text-[10px] font-mono bg-slate-100 text-muted px-2 py-0.5 rounded mt-1 inline-block">
                    {s.codigo}
                  </span>
                </div>
                <span className="w-10 h-10 bg-accent/10 rounded-xl flex items-center justify-center text-accent">
                  <Building2 size={20} strokeWidth={1.5} />
                </span>
              </div>

              <div className="flex items-center gap-4 text-sm mb-4">
                <div className="flex items-center gap-1.5">
                  <Users size={13} className="text-blue-400" />
                  <span className="text-muted text-xs">{s.alunos} alunos</span>
                </div>
              </div>

              <div className="mt-auto flex gap-2">
                <button
                  onClick={e => { e.stopPropagation(); navigate(`/alunos?sala=${s.id}`) }}
                  className="flex-1 text-xs text-accent font-semibold py-2 rounded-lg
                             bg-indigo-50 hover:bg-indigo-100 transition-colors">
                  Ver alunos →
                </button>
                <button
                  onClick={e => handleDelete(e, s.id)}
                  className="px-3 py-2 text-danger rounded-lg hover:bg-red-50 transition-colors">
                  <Trash2 size={14} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
