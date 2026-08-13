import { useState, useEffect, useRef } from 'react'
import {
  Upload, Users, FileText, CheckCircle2, AlertCircle,
  XCircle, AlertTriangle, Info, Download, Eye, Zap,
} from 'lucide-react'
import { api } from '../api'
import { useToast } from '../components/Toast'

const TABS = [
  { key: 'alunos', label: 'Alunos', Icon: Users,    color: '#4F46E5' },
  { key: 'notas',  label: 'Notas',  Icon: FileText, color: '#0EA5E9' },
]

export default function Importar() {
  const toast = useToast()
  const [tab, setTab]           = useState('alunos')
  const [templates, setTemplates] = useState(null)
  const [file, setFile]         = useState(null)
  const [dragOver, setDragOver] = useState(false)
  const [preview, setPreview]   = useState(null)
  const [previewing, setPreviewing] = useState(false)
  const [importing, setImporting]   = useState(false)
  const [result, setResult]     = useState(null)
  const fileRef = useRef()

  useEffect(() => {
    api.importarTemplates().then(setTemplates).catch(console.error)
  }, [])

  function reset() {
    setFile(null); setPreview(null); setResult(null)
  }

  function onTabChange(t) {
    setTab(t); reset()
  }

  function onDrop(e) {
    e.preventDefault(); setDragOver(false)
    const f = e.dataTransfer.files[0]
    if (f) { setFile(f); setPreview(null); setResult(null) }
  }

  function onFileChange(e) {
    const f = e.target.files[0]
    if (f) { setFile(f); setPreview(null); setResult(null) }
  }

  async function handlePreview() {
    if (!file) return
    setPreviewing(true)
    try {
      const res = tab === 'alunos'
        ? await api.importarPreviewAlunos(file)
        : await api.importarPreviewNotas(file)
      setPreview(res)
    } catch (e) {
      toast.error(`Erro na pré-leitura: ${e.message}`)
    } finally {
      setPreviewing(false)
    }
  }

  async function handleImport() {
    if (!file || !preview || preview.validos === 0) return
    setImporting(true)
    try {
      const res = tab === 'alunos'
        ? await api.importarExecutarAlunos(file)
        : await api.importarExecutarNotas(file)
      setResult(res)
      toast.success('Importação concluída!')
    } catch (e) {
      toast.error(`Erro na importação: ${e.message}`)
    } finally {
      setImporting(false)
    }
  }

  function downloadTemplate() {
    const info = templates?.[tab]
    if (!info) return
    const lines = [info.colunas.join(',')]
    for (const row of info.exemplo) {
      lines.push(info.colunas.map(c => row[c] ?? '').join(','))
    }
    const blob = new Blob([lines.join('\n')], { type: 'text/csv;charset=utf-8-sig' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url; a.download = `template_${tab}.csv`; a.click()
    URL.revokeObjectURL(url)
  }

  const tplInfo = templates?.[tab]
  const tabInfo = TABS.find(t => t.key === tab)

  return (
    <div className="p-7 max-w-4xl space-y-6">
      {/* Header */}
      <div>
        <p className="text-[10px] text-muted uppercase tracking-widest mb-1">Dados</p>
        <h1 className="text-2xl font-bold text-text">Importar</h1>
        <p className="text-sm text-muted mt-0.5">
          Importe alunos ou notas em massa via arquivo CSV.
        </p>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 bg-hdr-bg border border-border rounded-xl p-1 w-fit">
        {TABS.map(t => (
          <button key={t.key} onClick={() => onTabChange(t.key)}
            className={`flex items-center gap-2 px-5 py-2 rounded-lg text-sm font-semibold transition-colors ${
              tab === t.key ? 'text-white shadow-sm' : 'text-muted hover:text-text'
            }`}
            style={tab === t.key ? { backgroundColor: t.color } : {}}>
            <t.Icon size={14} /> {t.label}
          </button>
        ))}
      </div>

      {/* Template guide */}
      {tplInfo && (
        <div className="card p-5">
          <div className="flex items-start justify-between mb-3">
            <div className="flex items-center gap-2">
              <Info size={14} className="text-accent" />
              <p className="text-sm font-bold text-text">Formato esperado</p>
            </div>
            <button
              onClick={downloadTemplate}
              className="flex items-center gap-1.5 text-xs text-accent hover:text-indigo-700
                         border border-accent/30 hover:border-accent/60 rounded-lg px-3 py-1.5
                         transition-colors font-semibold">
              <Download size={12} /> Baixar template
            </button>
          </div>

          <p className="text-xs text-muted mb-3">{tplInfo.descricao}</p>

          {/* Column tags */}
          <div className="flex flex-wrap gap-2 mb-4">
            {tplInfo.colunas.map(col => (
              <span key={col}
                className="px-2.5 py-1 rounded-lg text-xs font-mono font-semibold
                           bg-accent/10 text-accent border border-accent/20">
                {col}
              </span>
            ))}
          </div>

          {/* Example table */}
          <div className="overflow-x-auto rounded-lg border border-border">
            <table className="text-[11px] w-full">
              <thead className="bg-hdr-bg">
                <tr>
                  {tplInfo.colunas.map(c => (
                    <th key={c} className="px-3 py-2 text-left font-semibold text-muted">{c}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {tplInfo.exemplo.map((row, i) => (
                  <tr key={i} className={i % 2 === 0 ? 'bg-white' : 'bg-slate-50'}>
                    {tplInfo.colunas.map(c => (
                      <td key={c} className="px-3 py-1.5 text-text font-mono">
                        {row[c] ?? <span className="text-muted italic">vazio</span>}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Upload area */}
      <div
        onDragOver={e => { e.preventDefault(); setDragOver(true) }}
        onDragLeave={() => setDragOver(false)}
        onDrop={onDrop}
        onClick={() => fileRef.current?.click()}
        className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all ${
          dragOver
            ? 'border-accent bg-indigo-50'
            : file
              ? 'border-green-400 bg-green-50'
              : 'border-border hover:border-accent/50 hover:bg-hdr-bg'
        }`}
      >
        <input ref={fileRef} type="file" accept=".csv" className="hidden" onChange={onFileChange} />
        {file ? (
          <div className="flex items-center justify-center gap-3">
            <CheckCircle2 size={20} className="text-green-600" />
            <div className="text-left">
              <p className="text-sm font-bold text-text">{file.name}</p>
              <p className="text-xs text-muted">{(file.size / 1024).toFixed(1)} KB</p>
            </div>
            <button
              onClick={e => { e.stopPropagation(); reset() }}
              className="ml-4 text-muted hover:text-danger transition-colors">
              <XCircle size={16} />
            </button>
          </div>
        ) : (
          <>
            <Upload size={28} className="mx-auto mb-3 text-muted opacity-50" />
            <p className="text-sm font-semibold text-text">Arraste um arquivo CSV aqui</p>
            <p className="text-xs text-muted mt-1">ou clique para selecionar</p>
          </>
        )}
      </div>

      {/* Actions */}
      {file && !result && (
        <div className="flex items-center gap-3">
          <button
            onClick={handlePreview}
            disabled={previewing}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold
                       border border-border text-text hover:bg-hdr-bg transition-colors disabled:opacity-50">
            {previewing
              ? <span className="w-4 h-4 border-2 border-current/30 border-t-current rounded-full animate-spin" />
              : <Eye size={15} />}
            {previewing ? 'Verificando...' : 'Pré-visualizar'}
          </button>

          {preview && preview.validos > 0 && (
            <button
              onClick={handleImport}
              disabled={importing}
              className="btn-primary flex items-center gap-2 px-6 py-2.5 disabled:opacity-60">
              {importing
                ? <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                : <Zap size={15} />}
              {importing ? 'Importando...' : `Importar ${preview.validos} registro${preview.validos !== 1 ? 's' : ''}`}
            </button>
          )}
        </div>
      )}

      {/* Preview results */}
      {preview && !result && (
        <div className="space-y-4">
          {/* Stats */}
          <div className="grid grid-cols-3 gap-3">
            {[
              { label: 'Total de linhas', value: preview.total,   color: '#64748B' },
              { label: 'Válidos',         value: preview.validos, color: '#10B981' },
              { label: 'Com erros',       value: preview.erros,   color: preview.erros > 0 ? '#EF4444' : '#64748B' },
            ].map(s => (
              <div key={s.label} className="card p-3 text-center">
                <p className="text-2xl font-black" style={{ color: s.color }}>{s.value}</p>
                <p className="text-[10px] text-muted mt-0.5">{s.label}</p>
              </div>
            ))}
          </div>

          {/* Preview table */}
          {preview.preview?.length > 0 && (
            <div className="card p-4">
              <p className="text-xs font-bold text-text mb-3 flex items-center gap-1.5">
                <Eye size={12} /> Pré-visualização (primeiros {preview.preview.length} registros válidos)
              </p>
              <div className="overflow-x-auto rounded-lg border border-border">
                <table className="text-[11px] w-full">
                  <thead className="bg-hdr-bg">
                    <tr>
                      {Object.keys(preview.preview[0]).filter(k => !k.endsWith('_id')).map(c => (
                        <th key={c} className="px-3 py-2 text-left font-semibold text-muted">{c}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {preview.preview.map((row, i) => (
                      <tr key={i} className={i % 2 === 0 ? 'bg-white' : 'bg-slate-50'}>
                        {Object.entries(row).filter(([k]) => !k.endsWith('_id')).map(([k, v]) => (
                          <td key={k} className="px-3 py-1.5 text-text font-mono">
                            {v ?? <span className="text-muted">—</span>}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Errors */}
          {preview.detalhes_erros?.length > 0 && (
            <div className="card p-4 border-danger/30">
              <p className="text-xs font-bold text-danger mb-3 flex items-center gap-1.5">
                <AlertCircle size={12} /> Linhas com erro ({preview.detalhes_erros.length})
              </p>
              <div className="space-y-2">
                {preview.detalhes_erros.map((e, i) => (
                  <div key={i} className="flex items-center gap-3 bg-red-50 rounded-lg px-3 py-2">
                    <AlertTriangle size={12} className="text-danger flex-shrink-0" />
                    <span className="text-[10px] text-muted w-14 shrink-0">Linha {e.linha}</span>
                    <span className="text-xs text-danger font-medium">{e.erro}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Import result */}
      {result && (
        <div className="card p-6 border-green-200 bg-green-50">
          <div className="flex items-center gap-3 mb-4">
            <CheckCircle2 size={20} className="text-green-600" />
            <h2 className="font-bold text-green-800">Importação concluída!</h2>
          </div>
          <div className="flex gap-6">
            {result.inseridos !== undefined && (
              <div>
                <p className="text-2xl font-black text-green-700">{result.inseridos}</p>
                <p className="text-xs text-green-600">inseridos</p>
              </div>
            )}
            {result.atualizados !== undefined && (
              <div>
                <p className="text-2xl font-black text-blue-700">{result.atualizados}</p>
                <p className="text-xs text-blue-600">atualizados</p>
              </div>
            )}
            {result.ignorados > 0 && (
              <div>
                <p className="text-2xl font-black text-muted">{result.ignorados}</p>
                <p className="text-xs text-muted">ignorados</p>
              </div>
            )}
          </div>
          <button
            onClick={reset}
            className="mt-4 text-xs text-green-700 hover:text-green-900 font-semibold underline">
            Importar outro arquivo
          </button>
        </div>
      )}
    </div>
  )
}
