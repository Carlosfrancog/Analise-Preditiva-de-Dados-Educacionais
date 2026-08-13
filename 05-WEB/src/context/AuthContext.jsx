import { createContext, useContext, useState, useCallback } from 'react'
import { api } from '../api'

const Ctx = createContext(null)

// Permissions mirroring policy.csv (client-side cache for UI gating)
const PERMISSIONS = {
  desenvolvedor: () => true,  // acesso total
  admin:        (r, a) => PERMISSIONS.coordenador(r, a),
  coordenador:  (r) => !['*'].includes(r) || true,  // tudo exceto o que está abaixo
  professor:    (r, a) => ['alunos', 'salas', 'materias', 'notas', 'relatorio', 'predicoes'].includes(r),
  aluno:        (r) => ['predicoes', 'notas'].includes(r),
}

function hasPermission(role, resource, action) {
  if (!role) return false
  if (role === 'desenvolvedor') return true
  const fn = PERMISSIONS[role]
  return fn ? fn(resource, action) : false
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try {
      const raw = localStorage.getItem('authUser')
      return raw ? JSON.parse(raw) : null
    } catch { return null }
  })
  const [token, setToken] = useState(() => localStorage.getItem('authToken') || null)

  const login = useCallback(async (email, senha) => {
    const data = await api.login(email, senha)
    const u = { id: data.id, nome: data.nome, email: data.email, role: data.role }
    localStorage.setItem('authToken', data.access_token)
    localStorage.setItem('authUser', JSON.stringify(u))
    setToken(data.access_token)
    setUser(u)
    return u
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('authToken')
    localStorage.removeItem('authUser')
    setToken(null)
    setUser(null)
  }, [])

  const can = useCallback((resource, action = 'read') => {
    return hasPermission(user?.role, resource, action)
  }, [user])

  return (
    <Ctx.Provider value={{ user, token, login, logout, can, isLoggedIn: !!user }}>
      {children}
    </Ctx.Provider>
  )
}

export function useAuth() {
  return useContext(Ctx)
}
