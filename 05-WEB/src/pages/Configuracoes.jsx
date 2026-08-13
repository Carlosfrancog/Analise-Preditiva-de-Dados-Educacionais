import { useState, useEffect } from 'react'
import { Settings2, RotateCcw, Brain, CheckCircle2, AlertCircle, RefreshCw, Repeat2, TrendingUp } from 'lucide-react'
import { api } from '../api'
import { useToast } from '../components/Toast'

const DEFAULTS = {
  RF_M1: { n_estimators: 100, max_depth: 5,  unlimited_depth: false, min_samples_split: 2, min_samples_leaf: 1 },
  RF_M2: { n_estimators: 150, max_depth: 10, unlimited_depth: false, min_samples_split: 2, min_samples_leaf: 1 },
  RF_M3: { n_estimators: 200, max_depth: 20, unlimited_depth: true,  min_samples_split: 2, min_samples_leaf: 1 },
}

const MODEL_INFO = {
  RF_M1: { label: 'M1 — Alerta',        color: '#10B981', shortDesc: '100 árvores · profundidade máx. 5',    desc: 'Modelo conservador — detecta alunos em risco mais cedo, com mais falsos positivos.' },
  RF_M2: { label: 'M2 — Intermediário', color: '#0EA5E9', shortDesc: '150 árvores · profundidade máx. 10',   desc: 'Equilíbrio entre precisão e sensibilidade. Bom para uso geral.' },
  RF_M3: { label: 'M3 — Produção',      color: '#4F46E5', shortDesc: '200 árvores · sem limite (produção)',  desc: 'Modelo principal usado nas predições. Maior acurácia, mas pode subestimar alunos limítrofes.' },
}

const PARAM_INFO = {
  n_estimators:      { label: 'Número de árvores',         desc: 'Mais árvores = mais preciso, mas mais lento. Recomendado: 100–300.' },
  max_depth:         { label: 'Profundidade máxima',       desc: 'Limita o quanto cada árvore pode crescer. Valores menores evitam overfitting.' },
  min_samples_split: { label: 'Amostras mín. para dividir', desc: 'Mínimo de amostras para criar um nó. Maior = modelo mais genérico.' },
  min_samples_leaf:  { label: 'Amostras mín. por folha',   desc: 'Mínimo de amostras em cada folha final. Evita overfitting.' },
}

function Slider({ label, value, min, max, step = 1, onChange, disabled }) {
  return (
    <div>
      <div className="flex items-center justify-between mb-1">
        <span className="text-xs font-semibold text-text">{label}</span>
        <span className="text-sm font-bold text-accent w-10 text-right">{value}</span>
      </div>
      <input
        type="range" min={min} max={max} step={step}
        value={value}
        onChange={e => onChange(Number(e.target.value))}
        disabled={disabled}
        className="w-full h-1.5 accent-indigo-600 cursor-pointer disabled:opacity-40"
      />
      <div className="flex justify-between text-[10px] text-muted mt-0.5">
        <span>{min}</span><span>{max}</span>
      </div>
    </div>
  )
}

export default function Configuracoes() {
  const toast = useToast()
  const [models, setModels]       = useState([])
  const [configs, setConfigs]     = useState(structuredClone(DEFAULTS))
  const [active, setActive]       = useState('RF_M3')
  const [step, setStep]           = useState(null)   // null | 'generating' | 'training' | 'done' | 'error'
  const [resultado, setResultado] = useState(null)
  const [error, setError]         = useState(null)
  const [nRuns, setNRuns]         = useState(5)
  const [contStep, setContStep]   = useState(null)  // null | 'running' | 'done' | 'error'
  const [contResult, setContResult] = useState(null)
  const [contError, setContError] = useState(null)

  useEffect(() => {
    api.mlModels().then(setModels).catch(console.error)
  }, [])

  function update(field, value) {
    setConfigs(prev => ({ ...prev, [active]: { ...prev[active], [field]: value } }))
  }

  function resetModel() {
    setConfigs(prev => ({ ...prev, [active]: structuredClone(DEFAULTS[active]) }))
    toast.info(`${active} redefinido para os padrões.`)
  }

  function resetAll() {
    setConfigs(structuredClone(DEFAULTS))
    toast.info('Todas as configurações redefinidas.')
  }

  async function handleTrain() {
    setStep('generating')
    setError(null)
    setResultado(null)
    try {
      const body = {}
      for (const [name, cfg] of Object.entries(configs)) {
        body[name] = {
          n_estimators: cfg.n_estimators,
          max_depth: cfg.unlimited_depth ? null : cfg.max_depth,
          min_samples_split: cfg.min_samples_split,
          min_samples_leaf: cfg.min_samples_leaf,
        }
      }
      setStep('training')
      const res = await api.retrain(body)
      setResultado(res)
      setStep('done')
      const updated = await api.mlModels()
      setModels(updated)
      toast.success('Treinamento concluído! Modelos recarregados.')
    } catch (e) {
      setError(e.message)
      setStep('error')
      toast.error(`Erro no treinamento: ${e.message}`)
    }
  }

  async function handleContinuous() {
    setContStep('running')
    setContError(null)
    setContResult(null)
    try {
      const body = { n_runs: nRuns }
      for (const [name, cfg] of Object.entries(configs)) {
        body[name] = {
          n_estimators: cfg.n_estimators,
          max_depth: cfg.unlimited_depth ? null : cfg.max_depth,
          min_samples_split: cfg.min_samples_split,
          min_samples_leaf: cfg.min_samples_leaf,
        }
      }
      const res = await api.retrainContinuous(body)
      setContResult(res)
      setContStep('done')
      const updated = await api.mlModels()
      setModels(updated)
      toast.success(`Treinamento contínuo concluído! ${nRuns} execuções por modelo.`)
    } catch (e) {
      setContError(e.message)
      setContStep('error')
      toast.error(`Erro: ${e.message}`)
    }
  }

  const cfg = configs[active]
  const isTraining = step === 'generating' || step === 'training'
  const modelList = models.length > 0
    ? models
    : Object.keys(MODEL_INFO).map(n => ({ name: n, accuracy: 0, available: false }))

  return (
    <div className="p-7 max-w-4xl space-y-6">
      {/* Header */}
      <div>
        <p className="text-[10px] text-muted uppercase tracking-widest mb-1">Inteligência Artificial</p>
        <h1 className="text-2xl font-bold text-text">Machine Learning</h1>
        <p className="text-sm text-muted mt-0.5">
          Gerencie os modelos RandomForest, ajuste hiperparâmetros e retreine com os dados mais recentes.
        </p>
      </div>

      {/* ── Modelos Ativos ── */}
      <div>
        <p className="text-[10px] text-muted uppercase tracking-widest mb-3">Modelos Ativos</p>
        <div className="grid grid-cols-3 gap-4">
          {modelList.map(m => (
            <div key={m.name} className="card p-4 relative overflow-hidden">
              <div className="absolute top-0 left-0 right-0 h-1 rounded-t-xl"
                style={{ backgroundColor: MODEL_INFO[m.name]?.color ?? '#4F46E5' }} />
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-text">{m.name}</span>
                {m.name === 'RF_M3' && (
                  <span className="text-[10px] bg-accent text-white px-2 py-0.5 rounded-full font-bold">produção</span>
                )}
              </div>
              <p className="text-3xl font-bold mb-1" style={{ color: MODEL_INFO[m.name]?.color ?? '#4F46E5' }}>
                {m.accuracy > 0 ? `${(m.accuracy * 100).toFixed(1)}%` : '—'}
              </p>
              <p className="text-xs text-muted">acurácia</p>
              <p className="text-[10px] text-muted mt-2">{MODEL_INFO[m.name]?.shortDesc}</p>
              <div className="mt-2 flex items-center gap-1.5">
                <span className={`w-2 h-2 rounded-full ${m.available ? 'bg-green-500' : 'bg-slate-300'}`} />
                <span className="text-[10px] text-muted">{m.available ? 'carregado' : 'não disponível'}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ── Hiperparâmetros ── */}
      <div>
        <p className="text-[10px] text-muted uppercase tracking-widest mb-3">Hiperparâmetros</p>

        {/* Model tabs */}
        <div className="flex gap-1 bg-hdr-bg border border-border rounded-xl p-1 w-fit mb-4">
          {Object.entries(MODEL_INFO).map(([name, info]) => {
            const isChanged = JSON.stringify(configs[name]) !== JSON.stringify(DEFAULTS[name])
            return (
              <button key={name} onClick={() => setActive(name)}
                className={`px-5 py-2 rounded-lg text-sm font-semibold transition-colors flex items-center gap-2 ${
                  active === name ? 'text-white shadow-sm' : 'text-muted hover:text-text'
                }`}
                style={active === name ? { backgroundColor: info.color } : {}}>
                {name.replace('RF_', 'M')}
                {isChanged && <span className="w-1.5 h-1.5 rounded-full bg-amber-400" title="Modificado" />}
              </button>
            )
          })}
        </div>

        {/* Config card */}
        <div className="card p-6">
          <div className="flex items-start justify-between mb-5">
            <div>
              <p className="font-bold text-text">{MODEL_INFO[active].label}</p>
              <p className="text-xs text-muted mt-0.5 max-w-md">{MODEL_INFO[active].desc}</p>
            </div>
            <button onClick={resetModel}
              className="flex items-center gap-1.5 text-xs text-muted hover:text-text border border-border rounded-lg px-3 py-1.5 transition-colors">
              <RotateCcw size={12} /> Padrões
            </button>
          </div>

          <div className="space-y-6">
            <div className="space-y-1.5">
              <Slider
                label={`${PARAM_INFO.n_estimators.label} (n_estimators)`}
                value={cfg.n_estimators} min={50} max={500} step={10}
                onChange={v => update('n_estimators', v)} disabled={isTraining}
              />
              <p className="text-[10px] text-muted">{PARAM_INFO.n_estimators.desc}</p>
            </div>

            <div className="space-y-1.5">
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-semibold text-text">
                  {PARAM_INFO.max_depth.label} (max_depth)
                </span>
                <label className="flex items-center gap-2 cursor-pointer select-none">
                  <span className="text-xs text-muted">Sem limite</span>
                  <div
                    onClick={() => !isTraining && update('unlimited_depth', !cfg.unlimited_depth)}
                    className={`relative w-8 h-4 rounded-full transition-colors cursor-pointer ${
                      cfg.unlimited_depth ? 'bg-accent' : 'bg-slate-300'
                    } ${isTraining ? 'opacity-40 cursor-not-allowed' : ''}`}>
                    <div className={`absolute top-0.5 w-3 h-3 rounded-full bg-white shadow transition-transform ${
                      cfg.unlimited_depth ? 'translate-x-4' : 'translate-x-0.5'
                    }`} />
                  </div>
                </label>
              </div>
              {cfg.unlimited_depth ? (
                <div className="h-6 flex items-center">
                  <span className="text-xs text-muted italic">
                    Árvores crescem sem restrição de profundidade — maior risco de overfitting.
                  </span>
                </div>
              ) : (
                <Slider label="" value={cfg.max_depth} min={3} max={30}
                  onChange={v => update('max_depth', v)} disabled={isTraining} />
              )}
              <p className="text-[10px] text-muted">{PARAM_INFO.max_depth.desc}</p>
            </div>

            <div className="space-y-1.5">
              <Slider
                label={`${PARAM_INFO.min_samples_split.label} (min_samples_split)`}
                value={cfg.min_samples_split} min={2} max={20}
                onChange={v => update('min_samples_split', v)} disabled={isTraining}
              />
              <p className="text-[10px] text-muted">{PARAM_INFO.min_samples_split.desc}</p>
            </div>

            <div className="space-y-1.5">
              <Slider
                label={`${PARAM_INFO.min_samples_leaf.label} (min_samples_leaf)`}
                value={cfg.min_samples_leaf} min={1} max={10}
                onChange={v => update('min_samples_leaf', v)} disabled={isTraining}
              />
              <p className="text-[10px] text-muted">{PARAM_INFO.min_samples_leaf.desc}</p>
            </div>
          </div>

          <div className="mt-6 bg-hdr-bg rounded-xl px-4 py-3 text-xs text-muted font-mono">
            RF({cfg.n_estimators}, max_depth={cfg.unlimited_depth ? 'None' : cfg.max_depth},
            {' '}min_split={cfg.min_samples_split}, min_leaf={cfg.min_samples_leaf})
          </div>
        </div>
      </div>

      {/* ── Treinamento Contínuo ── */}
      <div className="card p-6">
        <div className="flex items-start justify-between mb-2">
          <div>
            <h2 className="font-bold text-text flex items-center gap-2">
              <Repeat2 size={16} className="text-accent" /> Treinamento Contínuo
            </h2>
            <p className="text-sm text-muted mt-1">
              Treina cada modelo <strong>{nRuns}×</strong> com seeds diferentes e salva automaticamente
              a melhor acurácia encontrada para cada um.
              Ideal para bases pequenas onde a variância entre treinos é alta.
            </p>
          </div>
          <span className="text-[10px] bg-indigo-50 border border-accent/30 text-accent
                           px-2 py-0.5 rounded-full font-semibold whitespace-nowrap">
            {nRuns * 3} treinos total
          </span>
        </div>

        <div className="mt-4 mb-5">
          <Slider
            label={`Execuções por modelo (n_runs)`}
            value={nRuns} min={2} max={20} step={1}
            onChange={setNRuns} disabled={contStep === 'running' || isTraining}
          />
          <p className="text-[10px] text-muted mt-1">
            Mais execuções = melhor chance de encontrar o ótimo, mas leva mais tempo (~15–30s por execução).
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleContinuous}
            disabled={contStep === 'running' || isTraining}
            className="flex items-center gap-2 px-6 py-2.5 rounded-xl text-sm font-semibold
                       bg-indigo-900 text-white hover:bg-indigo-800 transition-colors
                       disabled:opacity-60 border border-indigo-700">
            {contStep === 'running'
              ? <><span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Treinando {nRuns}× cada modelo...</>
              : <><Repeat2 size={15} /> Iniciar Treinamento Contínuo</>}
          </button>
          {contStep === 'done' && (
            <span className="text-xs text-green-600 flex items-center gap-1">
              <CheckCircle2 size={13} /> Concluído!
            </span>
          )}
        </div>

        {contError && (
          <div className="mt-3 bg-red-50 border border-red-200 rounded-lg px-4 py-3 flex items-center gap-2">
            <AlertCircle size={14} className="text-danger flex-shrink-0" />
            <p className="text-sm text-danger">{contError}</p>
          </div>
        )}

        {contResult && contStep === 'done' && (
          <div className="mt-4 space-y-3">
            <p className="text-xs font-bold text-text flex items-center gap-1.5">
              <TrendingUp size={13} className="text-accent" />
              Melhor resultado por modelo ({nRuns} execuções)
            </p>
            {Object.entries(contResult.modelos).map(([nome, res]) => {
              const info = MODEL_INFO[nome]
              const best = Math.max(...res.run_accuracies)
              const worst = Math.min(...res.run_accuracies)
              return (
                <div key={nome} className="border border-border rounded-xl p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-semibold text-text text-sm">{nome}</span>
                    <span className="text-xl font-black" style={{ color: info?.color }}>
                      {(res.accuracy * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden mb-2">
                    <div className="h-full rounded-full"
                      style={{ width: `${res.accuracy * 100}%`, backgroundColor: info?.color }} />
                  </div>
                  {/* Run accuracies mini chart */}
                  <div className="flex items-end gap-0.5 h-8 mt-1">
                    {res.run_accuracies.map((acc, i) => (
                      <div key={i} title={`Run ${i + 1}: ${(acc * 100).toFixed(1)}%`}
                        className="flex-1 rounded-sm transition-all"
                        style={{
                          height: `${((acc - worst) / (best - worst + 0.01)) * 100}%`,
                          minHeight: '4px',
                          backgroundColor: acc === best ? info?.color : `${info?.color}50`,
                        }} />
                    ))}
                  </div>
                  <p className="text-[9px] text-muted mt-1">
                    {nRuns} execuções · melhor: {(best * 100).toFixed(1)}% · pior: {(worst * 100).toFixed(1)}%
                  </p>
                </div>
              )
            })}
          </div>
        )}
      </div>

      {/* ── Retreinar ── */}
      <div className="card p-6">
        <h2 className="font-bold text-text mb-1">Retreinar Modelos</h2>
        <p className="text-sm text-muted mb-4">
          Pipeline completo: gera features das notas do banco → exporta CSV → treina os 3 modelos RF → salva e recarrega. Leva ~30–60 s.
        </p>

        {/* Steps */}
        <div className="flex items-center gap-0 mb-6">
          {[
            { key: 'generating', label: '1. Gerar features', Icon: Settings2 },
            { key: 'training',   label: '2. Treinar modelos', Icon: Brain },
            { key: 'done',       label: '3. Pronto',           Icon: CheckCircle2 },
          ].map((s, i) => {
            const active_ = step === s.key && step !== 'done'
            const done_   = step === 'done' || (step === 'training' && s.key === 'generating')
            return (
              <div key={s.key} className="flex items-center flex-1">
                <div className={`flex items-center gap-2 flex-1 px-3 py-2 rounded-lg border transition-colors ${
                  active_ ? 'border-accent bg-indigo-50' :
                  done_   ? 'border-green-200 bg-green-50' :
                            'border-border bg-hdr-bg'
                }`}>
                  {active_
                    ? <span className="inline-block w-4 h-4 border-2 border-accent/30 border-t-accent rounded-full animate-spin" />
                    : <s.Icon size={14} className={done_ ? 'text-green-600' : 'text-muted'} />}
                  <span className={`text-xs font-medium ${active_ ? 'text-accent' : done_ ? 'text-green-700' : 'text-muted'}`}>
                    {s.label}
                  </span>
                </div>
                {i < 2 && <div className="w-6 h-px bg-border mx-1" />}
              </div>
            )
          })}
        </div>

        <div className="flex items-center gap-3">
          <button onClick={resetAll}
            className="text-xs text-muted hover:text-text flex items-center gap-1.5">
            <RotateCcw size={12} /> Resetar tudo
          </button>
          <button
            onClick={handleTrain}
            disabled={isTraining}
            className="btn-primary flex items-center gap-2 px-6 py-2.5 font-semibold disabled:opacity-60">
            {isTraining
              ? <><span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  {step === 'generating' ? 'Gerando features...' : 'Treinando modelos...'}</>
              : <><RefreshCw size={15} /> Retreinar Agora</>}
          </button>
        </div>

        {error && (
          <div className="mt-4 bg-red-50 border border-red-200 rounded-lg px-4 py-3 flex items-center gap-2">
            <AlertCircle size={14} className="text-danger flex-shrink-0" />
            <p className="text-sm text-danger">{error}</p>
          </div>
        )}
      </div>

      {/* ── Resultados ── */}
      {resultado && step === 'done' && (
        <div className="card p-6">
          <h2 className="font-bold text-text mb-1">Resultado do Treinamento</h2>
          <p className="text-xs text-muted mb-4">
            {resultado.n_samples} amostras · {resultado.train_size} treino / {resultado.test_size} teste
          </p>
          <div className="space-y-4">
            {Object.entries(resultado.modelos).map(([nome, res]) => {
              const info = MODEL_INFO[nome]
              const pct  = (res.accuracy * 100).toFixed(1)
              const cm   = res.confusion_matrix
              const classes = ['Reprovado', 'Recup.', 'Aprovado']
              return (
                <div key={nome} className="border border-border rounded-xl p-4">
                  <div className="flex items-center justify-between mb-3">
                    <div>
                      <span className="font-bold text-text">{nome}</span>
                      <span className="text-xs text-muted ml-2">{info?.shortDesc}</span>
                    </div>
                    <div className="text-right">
                      <span className="text-2xl font-bold" style={{ color: info?.color }}>{pct}%</span>
                      <span className="text-xs text-muted ml-1">acurácia</span>
                    </div>
                  </div>
                  <div className="h-2 bg-slate-100 rounded-full overflow-hidden mb-3">
                    <div className="h-full rounded-full"
                      style={{ width: `${res.accuracy * 100}%`, backgroundColor: info?.color }} />
                  </div>
                  {cm && (
                    <>
                      <p className="text-[10px] text-muted uppercase tracking-widest mb-2">Matriz de Confusão</p>
                      <table className="text-[10px] border-collapse">
                        <thead>
                          <tr>
                            <th className="px-2 py-1 text-left text-muted">Real \ Previsto</th>
                            {classes.map(c => <th key={c} className="px-3 py-1 text-center text-muted">{c}</th>)}
                          </tr>
                        </thead>
                        <tbody>
                          {cm.map((row, i) => {
                            const rowTotal = row.reduce((a, b) => a + b, 0)
                            return (
                              <tr key={i} className={i % 2 === 0 ? 'bg-hdr-bg' : ''}>
                                <td className="px-2 py-1 font-semibold text-text">{classes[i]}</td>
                                {row.map((v, j) => (
                                  <td key={j} className={`px-3 py-1 text-center font-mono ${
                                    i === j ? 'font-bold text-green-700 bg-green-50' : 'text-muted'
                                  }`}>
                                    {v}
                                    {rowTotal > 0 && i === j && (
                                      <span className="text-[9px] ml-1 opacity-60">
                                        ({((v / rowTotal) * 100).toFixed(0)}%)
                                      </span>
                                    )}
                                  </td>
                                ))}
                              </tr>
                            )
                          })}
                        </tbody>
                      </table>
                    </>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}
