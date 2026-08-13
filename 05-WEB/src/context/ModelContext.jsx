import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { api } from '../api'

const Ctx = createContext(null)

export function ModelProvider({ children }) {
  const [activeModel, setActiveModel] = useState(
    () => localStorage.getItem('activeModel') || 'RF_M3'
  )
  const [models, setModels] = useState([])
  const [switching, setSwitching] = useState(false)

  const refreshModels = useCallback(() => {
    api.mlModels().then(setModels).catch(console.error)
  }, [])

  useEffect(() => { refreshModels() }, [refreshModels])

  async function activateModel(name) {
    if (name === activeModel || switching) return
    setSwitching(true)
    try {
      await api.activateModel(name)
      localStorage.setItem('activeModel', name)
      setActiveModel(name)
      await refreshModels()
    } catch (e) {
      console.error(e)
    } finally {
      setSwitching(false)
    }
  }

  return (
    <Ctx.Provider value={{ activeModel, models, switching, activateModel, refreshModels }}>
      {children}
    </Ctx.Provider>
  )
}

export function useModel() {
  return useContext(Ctx)
}
