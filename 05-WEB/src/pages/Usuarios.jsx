import { useState, useEffect } from 'react'
import { Users, Plus, Edit2, Trash2, Shield, CheckCircle2, XCircle, AlertCircle } from 'lucide-react'
import { api } from '../api'
import { useAuth } from '../context/AuthContext'
import { useToast } from '../components/Toast'

const ROLE_META = {
  desenvolvedor: { label: 'Desenvolvedor', color: '#4F46E5', bg: '#EEF2FF' },
  admin:         { label: 'Admin',         color: '#7C3AED', bg: '#F5F3FF' },
  coordenador:   { label: 'Coordenador',   color: '#0EA5E9', bg: '#F0F9FF' },
  professor:     { label: 'Professor',     color: '#10B981', bg: '#ECFDF5' },
  aluno:         { label: 'Aluno',         color: '#F59E0B', bg: '#FFFBEB' },
}

const EMPTY_FORM = { nome: '', email: '', senha: '', role: 'professor', ativo: 1 }

export default function Usuarios() {
  const { user: me } = useAuth()
  const toast = useToast()
  const [usuarios, setUsuarios] = useState([])
  const [loading, setLoading]   = useState(true)
  const [modal, setModal]       = useState(null)  // null | 'criar' | { id, ...user }
  const [form, setForm]         = useState(EMPTY_FORM)
  const [saving, setSaving]     = useState(false)
  const [error, setError]       = useState(null)

  async function load() {
    setLoading(true)
    try {
      const data = await api.getUsuarios()
      setUsuarios(data)
    } catch (e) { console.error(e) }
    finally { setLoading(false) }
  }

  useEffect(() => { load() }, [])

  function openCreate() {
    setForm(EMPTY_FORM)
    setError(null)
    setModal('criar')
  }

  function openEdit(u) {
    setForm({ nome: u.nome, email: u.email, senha: '', role: u.role, ativo: u.ativo })
    setError(null)
    setModal(u)
  }

  async function handleSave() {
    setSaving(true)
    setError(null)
    try {
      if (modal === 'criar') {
        await api.criarUsuario(form)
        toast.success('Usuário criado com sucesso.')
      } else {
        const body = { ...form }
        if (!body.senha) delete body.senha
        await api.editarUsuario(modal.id, body)
        toast.success('Usuário atualizado.')
      }
      setModal(null)
      load()
    } catch (e) {
      setError(e.message)
    } finally {
      setSaving(false)
    }
  }

  async function handleDelete(u) {
    if (!confirm(`Deletar "${u.nome}"?`)) return
    try {
      await api.deletarUsuario(u.id)
      toast.warning(`Usuário "${u.nome}" removido.`)
      load()
    } catch (e) {
      toast.error(e.message)
    }
  }

  const isDev = me?.role === 'desenvolvedor'
  const availableRoles = isDev
    ? Object.keys(ROLE_META)
    : Object.keys(ROLE_META).filter(r => r !== 'desenvolvedor')

  return (
    <div className="p-7 max-w-4xl space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <p className="text-[10px] text-muted uppercase tracking-widest mb-1">Administração</p>
          <h1 className="text-2xl font-bold text-text">Usuários</h1>
          <p className="text-sm text-muted mt-0.5">Gerencie contas e permissões de acesso ao sistema.</p>
        </div>
        <button onClick={openCreate}
          className="btn-primary flex items-center gap-2 px-4 py-2.5 text-sm font-semibold">
          <Plus size={15} /> Novo Usuário
        </button>
      </div>

      {/* User table */}
      {loading ? (
        <div className="flex justify-center py-16">
          <div className="w-7 h-7 border-2 border-accent/30 border-t-accent rounded-full animate-spin" />
        </div>
      ) : (
        <div className="card overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-hdr-bg text-[10px] text-muted uppercase tracking-wider">
              <tr>
                <th className="px-4 py-3 text-left font-semibold">Nome</th>
                <th className="px-4 py-3 text-left font-semibold">E-mail</th>
                <th className="px-4 py-3 text-center font-semibold">Role</th>
                <th className="px-4 py-3 text-center font-semibold">Status</th>
                <th className="px-4 py-3 text-center font-semibold">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {usuarios.map((u, i) => {
                const rm = ROLE_META[u.role] ?? ROLE_META.professor
                const isMe = u.id === me?.id
                return (
                  <tr key={u.id} className={i % 2 === 1 ? 'bg-hdr-bg/40' : ''}>
                    <td className="px-4 py-3 font-semibold text-text">
                      {u.nome}
                      {isMe && <span className="text-[10px] text-muted ml-1.5">(você)</span>}
                    </td>
                    <td className="px-4 py-3 text-muted">{u.email}</td>
                    <td className="px-4 py-3 text-center">
                      <span className="text-[11px] font-bold px-2.5 py-1 rounded-full"
                        style={{ backgroundColor: rm.bg, color: rm.color }}>
                        <Shield size={9} className="inline mr-1" />
                        {rm.label}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-center">
                      {u.ativo
                        ? <CheckCircle2 size={15} className="inline text-green-500" />
                        : <XCircle     size={15} className="inline text-slate-400" />}
                    </td>
                    <td className="px-4 py-3 text-center">
                      <div className="flex items-center justify-center gap-2">
                        <button onClick={() => openEdit(u)}
                          className="text-muted hover:text-text transition-colors">
                          <Edit2 size={14} />
                        </button>
                        {!isMe && u.role !== 'desenvolvedor' && (
                          <button onClick={() => handleDelete(u)}
                            className="text-muted hover:text-danger transition-colors">
                            <Trash2 size={14} />
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                )
              })}
              {usuarios.length === 0 && (
                <tr><td colSpan={5} className="px-4 py-8 text-center text-muted text-sm">
                  Nenhum usuário encontrado.
                </td></tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* Modal */}
      {modal !== null && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-md p-6">
            <h2 className="font-bold text-text text-lg mb-4">
              {modal === 'criar' ? 'Novo Usuário' : `Editar — ${modal.nome}`}
            </h2>

            <div className="space-y-3">
              <div>
                <label className="text-xs text-muted font-medium block mb-1">Nome</label>
                <input className="select w-full" value={form.nome}
                  onChange={e => setForm(f => ({ ...f, nome: e.target.value }))} placeholder="Nome completo" />
              </div>
              <div>
                <label className="text-xs text-muted font-medium block mb-1">E-mail</label>
                <input className="select w-full" type="email" value={form.email}
                  onChange={e => setForm(f => ({ ...f, email: e.target.value }))} placeholder="email@escola.edu" />
              </div>
              <div>
                <label className="text-xs text-muted font-medium block mb-1">
                  {modal === 'criar' ? 'Senha' : 'Nova senha (deixe em branco para manter)'}
                </label>
                <input className="select w-full" type="password" value={form.senha}
                  onChange={e => setForm(f => ({ ...f, senha: e.target.value }))}
                  placeholder={modal === 'criar' ? 'Senha' : '••••••••'} />
              </div>
              <div className="flex gap-3">
                <div className="flex-1">
                  <label className="text-xs text-muted font-medium block mb-1">Role</label>
                  <select className="select w-full" value={form.role}
                    onChange={e => setForm(f => ({ ...f, role: e.target.value }))}>
                    {availableRoles.map(r => (
                      <option key={r} value={r}>{ROLE_META[r]?.label ?? r}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="text-xs text-muted font-medium block mb-1">Status</label>
                  <select className="select" value={form.ativo}
                    onChange={e => setForm(f => ({ ...f, ativo: Number(e.target.value) }))}>
                    <option value={1}>Ativo</option>
                    <option value={0}>Inativo</option>
                  </select>
                </div>
              </div>
            </div>

            {error && (
              <div className="mt-3 flex items-center gap-2 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
                <AlertCircle size={13} className="text-danger flex-shrink-0" />
                <p className="text-sm text-danger">{error}</p>
              </div>
            )}

            <div className="flex items-center gap-2 mt-5">
              <button onClick={() => setModal(null)}
                className="flex-1 px-4 py-2 rounded-lg border border-border text-sm text-muted hover:text-text transition-colors">
                Cancelar
              </button>
              <button onClick={handleSave} disabled={saving}
                className="flex-1 btn-primary py-2 text-sm font-semibold disabled:opacity-60">
                {saving ? 'Salvando...' : 'Salvar'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
