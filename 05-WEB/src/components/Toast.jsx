import { createContext, useContext, useState, useCallback } from 'react'
import { CheckCircle2, XCircle, AlertCircle, Info, X } from 'lucide-react'

const Ctx = createContext(null)

const META = {
  success: { Icon: CheckCircle2, color: '#059669', bg: '#D1FAE5', border: '#6EE7B7' },
  error:   { Icon: XCircle,      color: '#DC2626', bg: '#FEE2E2', border: '#FCA5A5' },
  warning: { Icon: AlertCircle,  color: '#D97706', bg: '#FEF3C7', border: '#FCD34D' },
  info:    { Icon: Info,         color: '#4F46E5', bg: '#EEF2FF', border: '#A5B4FC' },
}

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([])

  const add = useCallback((message, type = 'info') => {
    const id = Date.now() + Math.random()
    setToasts(prev => [...prev, { id, message, type }])
    setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 4000)
  }, [])

  const remove = useCallback((id) => {
    setToasts(prev => prev.filter(t => t.id !== id))
  }, [])

  const toast = {
    success: (msg) => add(msg, 'success'),
    error:   (msg) => add(msg, 'error'),
    warning: (msg) => add(msg, 'warning'),
    info:    (msg) => add(msg, 'info'),
  }

  return (
    <Ctx.Provider value={toast}>
      {children}
      <div className="fixed bottom-5 right-5 z-[9999] flex flex-col gap-2 pointer-events-none">
        {toasts.map(t => {
          const { Icon, color, bg, border } = META[t.type] ?? META.info
          return (
            <div key={t.id}
              className="toast-enter flex items-center gap-3 px-4 py-3 rounded-xl shadow-xl border
                         pointer-events-auto min-w-[280px] max-w-sm"
              style={{ backgroundColor: bg, borderColor: border }}>
              <Icon size={16} style={{ color }} className="flex-shrink-0" />
              <span className="text-sm font-medium text-slate-800 flex-1 leading-snug">{t.message}</span>
              <button onClick={() => remove(t.id)}
                className="text-slate-400 hover:text-slate-600 flex-shrink-0 transition-colors">
                <X size={14} />
              </button>
            </div>
          )
        })}
      </div>
    </Ctx.Provider>
  )
}

export function useToast() {
  return useContext(Ctx)
}
