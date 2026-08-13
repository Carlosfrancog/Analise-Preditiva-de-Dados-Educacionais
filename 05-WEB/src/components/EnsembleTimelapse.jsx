import { useState, useEffect, useRef, useCallback } from 'react'
import { Play, Pause, RotateCcw, X, Zap, CheckCircle2, AlertTriangle, XCircle } from 'lucide-react'
import { api } from '../api'

const CLS = {
  0: { name: 'Reprovado',   color: '#EF4444', bg: 'rgba(239,68,68,0.15)',   border: 'rgba(239,68,68,0.4)',   Icon: XCircle       },
  1: { name: 'Recuperação', color: '#F59E0B', bg: 'rgba(245,158,11,0.15)',  border: 'rgba(245,158,11,0.4)',  Icon: AlertTriangle  },
  2: { name: 'Aprovado',    color: '#10B981', bg: 'rgba(16,185,129,0.15)',  border: 'rgba(16,185,129,0.4)',  Icon: CheckCircle2   },
}

const SPEEDS = [1, 2, 5, 10]
const MS_PER_FRAME = { 1: 60, 2: 30, 5: 12, 10: 6 }

export default function EnsembleTimelapse({ alunoId, materiaId, model, onClose }) {
  const [data, setData]         = useState(null)
  const [loading, setLoading]   = useState(true)
  const [error, setError]       = useState(null)
  const [tick, setTick]         = useState(0)
  const [playing, setPlaying]   = useState(false)
  const [speed, setSpeed]       = useState(1)
  const [done, setDone]         = useState(false)

  const intervalRef = useRef(null)
  const tickRef     = useRef(0)
  const dataRef     = useRef(null)

  useEffect(() => {
    setLoading(true)
    api.ensembleTimelapse(alunoId, materiaId, model)
      .then(d => {
        setData(d)
        dataRef.current = d
        setLoading(false)
        setPlaying(true)
      })
      .catch(e => { setError(e.message); setLoading(false) })
  }, [alunoId, materiaId, model])

  const advance = useCallback(() => {
    const d = dataRef.current
    if (!d) return
    setTick(prev => {
      const next = prev + 1
      if (next >= d.votes_sequence.length) {
        clearInterval(intervalRef.current)
        intervalRef.current = null
        setPlaying(false)
        setDone(true)
        return d.votes_sequence.length
      }
      tickRef.current = next
      return next
    })
  }, [])

  useEffect(() => {
    if (playing && data) {
      clearInterval(intervalRef.current)
      intervalRef.current = setInterval(advance, MS_PER_FRAME[speed])
    } else {
      clearInterval(intervalRef.current)
      intervalRef.current = null
    }
    return () => clearInterval(intervalRef.current)
  }, [playing, speed, data, advance])

  function handlePlayPause() {
    if (done) return
    setPlaying(p => !p)
  }

  function handleReset() {
    clearInterval(intervalRef.current)
    intervalRef.current = null
    setTick(0)
    tickRef.current = 0
    setDone(false)
    setPlaying(true)
  }

  function cycleSpeed() {
    const idx = SPEEDS.indexOf(speed)
    setSpeed(SPEEDS[(idx + 1) % SPEEDS.length])
  }

  // Compute counts from current tick
  const counts = [0, 0, 0]
  if (data) {
    for (let i = 0; i < tick; i++) {
      const v = data.votes_sequence[i]
      if (v >= 0 && v <= 2) counts[v]++
    }
  }

  const nTrees  = data?.votes_sequence?.length ?? 0
  const winner  = data ? [0, 1, 2].reduce((a, b) => counts[a] >= counts[b] ? a : b) : null
  const leading = nTrees > 0 ? counts[winner ?? 0] / nTrees : 0

  if (loading) return (
    <div className="absolute inset-0 bg-slate-950 flex items-center justify-center z-30">
      <div className="flex flex-col items-center gap-4">
        <div className="w-10 h-10 border-2 border-indigo-500/40 border-t-indigo-500 rounded-full animate-spin" />
        <p className="text-slate-400 text-sm">Carregando votos do ensemble...</p>
      </div>
    </div>
  )

  if (error) return (
    <div className="absolute inset-0 bg-slate-950 flex items-center justify-center z-30">
      <div className="text-center">
        <p className="text-red-400 text-sm mb-3">{error}</p>
        <button onClick={onClose} className="text-slate-400 hover:text-white text-sm underline">Fechar</button>
      </div>
    </div>
  )

  return (
    <div className="absolute inset-0 bg-slate-950 flex flex-col z-30 select-none">
      {/* Top bar */}
      <div className="flex-shrink-0 flex items-center gap-3 px-5 py-3 border-b border-slate-800 bg-slate-900/80">
        <Zap size={14} className="text-indigo-400" />
        <span className="text-xs text-slate-400 uppercase tracking-widest font-bold">Timelapse Ensemble</span>
        <span className="text-xs text-slate-500 ml-1">
          {data?.focus_disciplina && `— ${data.focus_disciplina}`}
        </span>
        <div className="flex-1" />
        <button
          onClick={onClose}
          className="w-7 h-7 flex items-center justify-center rounded-lg
                     bg-slate-800 border border-slate-700 text-slate-400
                     hover:text-white hover:border-slate-500 transition-colors">
          <X size={13} />
        </button>
      </div>

      {/* Main area */}
      <div className="flex-1 flex flex-col items-center justify-center px-8 gap-8">

        {/* Tree counter */}
        <div className="flex items-center gap-3">
          <span className="text-slate-500 text-sm">Estimador</span>
          <span className="text-5xl font-black tabular-nums text-white leading-none"
            style={{ fontVariantNumeric: 'tabular-nums' }}>
            {Math.min(tick, nTrees).toString().padStart(3, ' ')}
          </span>
          <span className="text-slate-600 text-2xl font-thin">/</span>
          <span className="text-slate-500 text-xl font-bold">{nTrees}</span>
        </div>

        {/* Vote bars */}
        <div className="w-full max-w-xl space-y-4">
          {[0, 1, 2].map(cls => {
            const meta     = CLS[cls]
            const count    = counts[cls]
            const pct      = nTrees > 0 ? (count / nTrees) * 100 : 0
            const isWinner = done && cls === winner
            const Icon     = meta.Icon
            return (
              <div key={cls}
                className={`rounded-xl border px-5 py-4 transition-all duration-300 ${
                  isWinner ? 'scale-[1.03] shadow-lg' : ''
                }`}
                style={{
                  backgroundColor: meta.bg,
                  borderColor: isWinner ? meta.color : meta.border,
                  boxShadow: isWinner ? `0 0 20px ${meta.color}44` : undefined,
                }}
              >
                <div className="flex items-center justify-between mb-2.5">
                  <div className="flex items-center gap-2">
                    <Icon size={15} style={{ color: meta.color }} />
                    <span className="font-bold text-sm" style={{ color: meta.color }}>
                      {meta.name}
                    </span>
                    {isWinner && (
                      <span className="text-[10px] font-black px-2 py-0.5 rounded-full ml-1"
                        style={{ backgroundColor: meta.color, color: '#fff' }}>
                        VENCEDOR
                      </span>
                    )}
                  </div>
                  <span className="text-2xl font-black tabular-nums"
                    style={{ color: meta.color }}>
                    {count}
                  </span>
                </div>
                <div className="h-3 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-75"
                    style={{ width: `${pct}%`, backgroundColor: meta.color }}
                  />
                </div>
                <div className="flex justify-end mt-1">
                  <span className="text-xs font-bold" style={{ color: meta.color }}>
                    {pct.toFixed(1)}%
                  </span>
                </div>
              </div>
            )
          })}
        </div>

        {/* Final result overlay (shown when done) */}
        {done && data?.final && (
          <div
            className="mt-2 rounded-2xl border-2 px-8 py-5 text-center animate-fade-in"
            style={{
              borderColor: CLS[data.final.class_value]?.color,
              backgroundColor: CLS[data.final.class_value]?.bg,
            }}
          >
            <p className="text-[10px] text-slate-400 uppercase tracking-widest mb-1.5">
              Predição final — {nTrees} estimadores
            </p>
            {(() => {
              const meta = CLS[data.final.class_value]
              const Icon = meta.Icon
              return (
                <>
                  <div className="flex items-center justify-center gap-2 mb-1">
                    <Icon size={22} style={{ color: meta.color }} />
                    <span className="text-3xl font-black" style={{ color: meta.color }}>
                      {meta.name}
                    </span>
                  </div>
                  <p className="text-sm font-bold" style={{ color: meta.color }}>
                    Confiança: {(data.final.confidence * 100).toFixed(1)}%
                  </p>
                </>
              )
            })()}
          </div>
        )}
      </div>

      {/* Controls */}
      <div className="flex-shrink-0 flex items-center justify-center gap-4 px-5 py-4 border-t border-slate-800 bg-slate-900/60">
        {/* Reset */}
        <button
          onClick={handleReset}
          title="Reiniciar"
          className="w-9 h-9 flex items-center justify-center rounded-lg
                     bg-slate-800 border border-slate-700 text-slate-400
                     hover:text-white hover:border-slate-500 transition-colors">
          <RotateCcw size={15} />
        </button>

        {/* Play / Pause */}
        <button
          onClick={handlePlayPause}
          disabled={done}
          title={playing ? 'Pausar' : 'Play'}
          className="w-12 h-12 flex items-center justify-center rounded-xl
                     border transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
          style={{
            backgroundColor: 'rgba(99,102,241,0.2)',
            borderColor: 'rgba(99,102,241,0.5)',
            color: '#818cf8',
          }}>
          {playing ? <Pause size={20} /> : <Play size={20} />}
        </button>

        {/* Speed */}
        <button
          onClick={cycleSpeed}
          title="Velocidade"
          className="w-16 h-9 flex items-center justify-center rounded-lg text-xs font-bold
                     bg-slate-800 border border-slate-700 text-slate-300
                     hover:text-white hover:border-slate-500 transition-colors">
          {speed}×
        </button>

        {/* Progress scrubber */}
        <input
          type="range"
          min={0}
          max={nTrees}
          value={tick}
          onChange={e => {
            const v = Number(e.target.value)
            setTick(v)
            tickRef.current = v
            if (v < nTrees) setDone(false)
            else setDone(true)
          }}
          className="w-56 accent-indigo-500"
        />

        <span className="text-xs text-slate-500 w-24 text-right">
          {nTrees > 0 ? `${((tick / nTrees) * 100).toFixed(0)}%` : ''}
        </span>
      </div>
    </div>
  )
}
