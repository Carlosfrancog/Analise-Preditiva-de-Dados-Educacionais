import { useState, useEffect } from 'react'
import {
  Download, Users, FileText, BarChart3,
  Brain, Building2, CheckCircle2, AlertCircle, Printer,
} from 'lucide-react'
import { api } from '../api'
import { useToast } from '../components/Toast'

const EXPORT_TYPES = [
  {
    key: 'alunos',
    label: 'Alunos',
    desc: 'Lista completa de alunos com matrícula, nome e turma.',
    Icon: Users,
    color: '#4F46E5',
    filterSala: true,
    fn: (sala_id) => api.exportarAlunos(sala_id),
  },
  {
    key: 'notas',
    label: 'Notas',
    desc: 'Todas as notas por aluno e disciplina (N1–N4).',
    Icon: FileText,
    color: '#0EA5E9',
    filterSala: true,
    fn: (sala_id) => api.exportarNotas(sala_id),
  },
  {
    key: 'relatorio',
    label: 'Relatório Completo',
    desc: 'Notas, média calculada e status de aprovação por disciplina.',
    Icon: BarChart3,
    color: '#10B981',
    filterSala: true,
    fn: (sala_id) => api.exportarRelatorio(sala_id),
  },
  {
    key: 'ia_raw',
    label: 'Dataset IA',
    desc: 'Features normalizadas e status codificado usados pelo modelo ML.',
    Icon: Brain,
    color: '#8B5CF6',
    filterSala: true,
    fn: (sala_id) => api.exportarIARaw(sala_id),
  },
  {
    key: 'salas',
    label: 'Turmas',
    desc: 'Resumo de turmas com total de alunos e disciplinas cadastradas.',
    Icon: Building2,
    color: '#F59E0B',
    filterSala: false,
    fn: () => api.exportarSalas(),
  },
]

export default function Exportar() {
  const toast = useToast()
  const [salas, setSalas]       = useState([])
  const [salaId, setSalaId]     = useState('')
  const [loading, setLoading]   = useState({})
  const [success, setSuccess]   = useState({})

  useEffect(() => {
    api.salas().then(setSalas).catch(console.error)
  }, [])

  async function handleDownload(type) {
    setLoading(prev => ({ ...prev, [type.key]: true }))
    setSuccess(prev => ({ ...prev, [type.key]: false }))
    try {
      const sid = type.filterSala && salaId ? Number(salaId) : null
      await type.fn(sid)
      setSuccess(prev => ({ ...prev, [type.key]: true }))
      toast.success(`${type.label} exportado com sucesso!`)
      setTimeout(() => setSuccess(prev => ({ ...prev, [type.key]: false })), 3000)
    } catch (e) {
      toast.error(`Erro ao exportar ${type.label}: ${e.message}`)
    } finally {
      setLoading(prev => ({ ...prev, [type.key]: false }))
    }
  }

  return (
    <div className="p-7 max-w-4xl space-y-6">
      {/* Header */}
      <div>
        <p className="text-[10px] text-muted uppercase tracking-widest mb-1">Dados</p>
        <h1 className="text-2xl font-bold text-text">Exportar</h1>
        <p className="text-sm text-muted mt-0.5">
          Baixe os dados da escola em formato CSV — compatível com Excel e Google Sheets.
        </p>
      </div>

      {/* Filtro por turma */}
      <div className="card p-4 flex items-center gap-4">
        <div className="flex items-center gap-2">
          <Building2 size={14} className="text-muted" />
          <span className="text-xs font-semibold text-text">Filtrar por turma</span>
        </div>
        <select
          className="select text-sm"
          value={salaId}
          onChange={e => setSalaId(e.target.value)}
        >
          <option value="">Todas as turmas</option>
          {salas.map(s => (
            <option key={s.id} value={s.id}>{s.nome} ({s.codigo})</option>
          ))}
        </select>
        {salaId && (
          <button
            onClick={() => setSalaId('')}
            className="text-xs text-muted hover:text-danger transition-colors"
          >
            Limpar filtro
          </button>
        )}
        <p className="text-[10px] text-muted ml-auto">
          O filtro se aplica aos tipos marcados com ícone de turma.
        </p>
      </div>

      {/* Export cards */}
      <div className="grid grid-cols-2 gap-4">
        {EXPORT_TYPES.map(type => {
          const isLoading = loading[type.key]
          const isDone    = success[type.key]
          return (
            <div key={type.key} className="card p-5 flex flex-col gap-3 relative overflow-hidden">
              <div className="absolute top-0 left-0 bottom-0 w-1 rounded-l-xl"
                style={{ backgroundColor: type.color }} />

              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-xl flex items-center justify-center"
                    style={{ backgroundColor: `${type.color}15` }}>
                    <type.Icon size={18} style={{ color: type.color }} />
                  </div>
                  <div>
                    <p className="font-bold text-text">{type.label}</p>
                    {type.filterSala && salaId && (
                      <p className="text-[10px] text-accent">
                        Turma: {salas.find(s => String(s.id) === salaId)?.nome ?? ''}
                      </p>
                    )}
                    {(!type.filterSala || !salaId) && (
                      <p className="text-[10px] text-muted">Todas as turmas</p>
                    )}
                  </div>
                </div>
                <span className="text-[10px] text-muted bg-hdr-bg border border-border
                                 px-2 py-0.5 rounded-full font-mono">CSV</span>
              </div>

              <p className="text-xs text-muted leading-relaxed">{type.desc}</p>

              <button
                onClick={() => handleDownload(type)}
                disabled={isLoading}
                className="mt-auto flex items-center justify-center gap-2 py-2 px-4 rounded-lg
                           text-xs font-semibold transition-all disabled:opacity-60"
                style={{
                  backgroundColor: isDone ? '#D1FAE5' : `${type.color}15`,
                  color: isDone ? '#059669' : type.color,
                  border: `1px solid ${isDone ? '#A7F3D0' : `${type.color}30`}`,
                }}
              >
                {isLoading
                  ? <span className="w-3.5 h-3.5 border-2 border-current/30 border-t-current rounded-full animate-spin" />
                  : isDone
                    ? <CheckCircle2 size={13} />
                    : <Download size={13} />}
                {isLoading ? 'Baixando...' : isDone ? 'Baixado!' : 'Baixar CSV'}
              </button>
            </div>
          )
        })}
      </div>

      {/* Print hint */}
      <div className="card p-4 flex items-start gap-3 bg-slate-50">
        <Printer size={16} className="text-muted mt-0.5 flex-shrink-0" />
        <div>
          <p className="text-xs font-semibold text-text mb-0.5">Exportar como PDF</p>
          <p className="text-xs text-muted">
            Abra o CSV no Excel ou Google Sheets e use <kbd className="bg-white border border-border px-1 py-0.5 rounded text-[10px] font-mono">Ctrl+P</kbd> para imprimir ou salvar como PDF
            com formatação personalizada de acordo com seu layout.
          </p>
        </div>
      </div>
    </div>
  )
}
