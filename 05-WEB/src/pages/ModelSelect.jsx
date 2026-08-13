import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { GraduationCap, Zap, CheckCircle2, ChevronRight } from 'lucide-react'
import { api } from '../api'

const MODEL_META = {
  RF_M1: {
    color:   '#10B981',
    border:  'border-emerald-500/40',
    glow:    'shadow-emerald-500/20',
    label:   'M1 — Alerta',
    trees:   100,
    depth:   'Profundidade máx. 5',
    desc:    'Mais conservador. Detecta alunos em risco mais cedo com alta sensibilidade. Ideal para alertas preventivos.',
    badge:   null,
  },
  RF_M2: {
    color:   '#0EA5E9',
    border:  'border-sky-500/40',
    glow:    'shadow-sky-500/20',
    label:   'M2 — Intermediário',
    trees:   150,
    depth:   'Profundidade máx. 10',
    desc:    'Equilíbrio entre precisão e sensibilidade. Boa escolha para uso geral e avaliações rotineiras.',
    badge:   null,
  },
  RF_M3: {
    color:   '#4F46E5',
    border:  'border-indigo-500/40',
    glow:    'shadow-indigo-500/20',
    label:   'M3 — Produção',
    trees:   200,
    depth:   'Profundidade ilimitada',
    desc:    'Modelo de maior acurácia. Recomendado para análises definitivas e predições de alta confiança.',
    badge:   'Recomendado',
  },
}

export default function ModelSelect() {
  const navigate  = useNavigate()
  const [models, setModels]       = useState({})
  const [selected, setSelected]   = useState(null)
  const [loading, setLoading]     = useState(true)
  const [activating, setActivating] = useState(false)

  useEffect(() => {
    api.mlModels()
      .then(list => {
        const byName = {}
        list.forEach(m => { byName[m.name] = m })
        setModels(byName)
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  async function handleConfirm() {
    if (!selected) return
    setActivating(true)
    try {
      await api.activateModel(selected)
      localStorage.setItem('activeModel', selected)
      navigate('/dashboard', { replace: true })
    } catch (e) {
      console.error(e)
      // proceed anyway — backend graceful fallback
      localStorage.setItem('activeModel', selected)
      navigate('/dashboard', { replace: true })
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-8">
      {/* Logo */}
      <div className="flex items-center gap-3 mb-2" style={{ animation: 'fadeUp 0.5s ease both' }}>
        <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center">
          <GraduationCap size={20} className="text-white" />
        </div>
        <div>
          <p className="text-white font-bold text-xl leading-tight">EduNotas</p>
          <p className="text-slate-400 text-xs">Sistema Escolar v2.0</p>
        </div>
      </div>

      {/* Title */}
      <div className="text-center mb-10 mt-4" style={{ animation: 'fadeUp 0.5s 0.1s ease both' }}>
        <h1 className="text-2xl font-bold text-white mb-1">Escolha o Modelo de IA</h1>
        <p className="text-slate-400 text-sm">
          Selecione o modelo RandomForest que será usado nas predições.
          Apenas o modelo escolhido ficará carregado na memória.
        </p>
      </div>

      {/* Model cards */}
      <div className="grid grid-cols-3 gap-5 w-full max-w-3xl mb-8">
        {Object.entries(MODEL_META).map(([name, meta], i) => {
          const m = models[name] ?? {}
          const isSelected = selected === name
          return (
            <button
              key={name}
              onClick={() => setSelected(name)}
              style={{ animation: `fadeUp 0.5s ${0.15 + i * 0.1}s ease both` }}
              className={`relative text-left rounded-2xl border-2 p-5 transition-all duration-200 outline-none
                ${isSelected
                  ? `${meta.border} shadow-lg ${meta.glow} bg-slate-900 scale-[1.02]`
                  : 'border-slate-800 bg-slate-900/50 hover:bg-slate-900 hover:border-slate-700'
                }`}
            >
              {/* Selected check */}
              {isSelected && (
                <CheckCircle2
                  size={18}
                  className="absolute top-3 right-3"
                  style={{ color: meta.color }}
                />
              )}

              {/* Recommended badge */}
              {meta.badge && (
                <span className="absolute top-3 right-3 text-[10px] font-bold px-2 py-0.5 rounded-full"
                  style={{ backgroundColor: `${meta.color}22`, color: meta.color }}>
                  {isSelected ? '' : meta.badge}
                </span>
              )}

              {/* Color dot */}
              <div className="w-3 h-3 rounded-full mb-3" style={{ backgroundColor: meta.color }} />

              <p className="text-white font-bold text-sm mb-0.5">{meta.label}</p>
              <p className="text-slate-400 text-[10px] mb-3">{name}</p>

              {/* Accuracy */}
              {!loading && (
                <p className="text-2xl font-bold mb-1" style={{ color: meta.color }}>
                  {m.accuracy > 0 ? `${(m.accuracy * 100).toFixed(1)}%` : '—'}
                </p>
              )}
              {loading && (
                <div className="w-16 h-7 bg-slate-800 rounded animate-pulse mb-1" />
              )}
              <p className="text-[10px] text-slate-500 mb-3">acurácia</p>

              <div className="space-y-1 text-[11px] text-slate-400">
                <div className="flex items-center gap-1.5">
                  <Zap size={10} style={{ color: meta.color }} />
                  <span>{meta.trees} árvores</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Zap size={10} style={{ color: meta.color }} />
                  <span>{meta.depth}</span>
                </div>
              </div>

              <p className="text-[11px] text-slate-500 mt-3 leading-relaxed">{meta.desc}</p>
            </button>
          )
        })}
      </div>

      {/* Confirm button */}
      <div style={{ animation: 'fadeUp 0.5s 0.5s ease both' }}>
        <button
          onClick={handleConfirm}
          disabled={!selected || activating}
          className="flex items-center gap-2 px-8 py-3 rounded-xl font-semibold text-sm
                     transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed"
          style={selected
            ? { backgroundColor: MODEL_META[selected]?.color, color: 'white' }
            : { backgroundColor: '#334155', color: '#94a3b8' }}>
          {activating ? (
            <><span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" /> Carregando modelo...</>
          ) : (
            <>{selected ? `Usar ${MODEL_META[selected]?.label}` : 'Selecione um modelo'} <ChevronRight size={16} /></>
          )}
        </button>
      </div>

      <style>{`
        @keyframes fadeUp {
          from { opacity: 0; transform: translateY(20px); }
          to   { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  )
}
