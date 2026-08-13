const BASE = '/api'

async function _uploadFile(path, file) {
  const token = localStorage.getItem('authToken')
  const headers = token ? { 'Authorization': `Bearer ${token}` } : {}
  const form = new FormData()
  form.append('file', file)
  const res = await fetch(`${BASE}${path}`, { method: 'POST', headers, body: form })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || res.statusText)
  }
  return res.json()
}

async function download(path, filename) {
  const token = localStorage.getItem('authToken')
  const headers = token ? { 'Authorization': `Bearer ${token}` } : {}
  const res = await fetch(`${BASE}${path}`, { headers })
  if (!res.ok) throw new Error(res.statusText)
  const blob = await res.blob()
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url; a.download = filename; a.click()
  URL.revokeObjectURL(url)
}

function authHeaders() {
  const token = localStorage.getItem('authToken')
  return token
    ? { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
    : { 'Content-Type': 'application/json' }
}

async function get(path) {
  const res = await fetch(`${BASE}${path}`, { headers: authHeaders() })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || res.statusText)
  }
  return res.json()
}

async function post(path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method:  'POST',
    headers: authHeaders(),
    body:    JSON.stringify(body),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || res.statusText)
  }
  return res.json()
}

async function put(path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method:  'PUT',
    headers: authHeaders(),
    body:    JSON.stringify(body),
  })
  if (!res.ok) throw new Error(res.statusText)
  return res.json()
}

async function del(path) {
  const res = await fetch(`${BASE}${path}`, { method: 'DELETE', headers: authHeaders() })
  if (!res.ok) throw new Error(res.statusText)
  return res.json()
}

// POST without auth header (for login)
async function postPublic(path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify(body),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || res.statusText)
  }
  return res.json()
}

export const api = {
  dashboard:   () => get('/dashboard'),
  salas:       () => get('/salas'),
  alunos:      (sala_id) => get(`/alunos${sala_id ? `?sala_id=${sala_id}` : ''}`),
  materias:    () => get('/materias'),
  notas:           (aluno_id) => get(`/notas/${aluno_id}`),
  notasTurma:      (sala_id)  => get(`/notas/turma/${sala_id}`),
  salvarNotasBatch:(notas)    => put('/notas/batch', { notas }),
  relatorio:   (sala_id) => get(`/relatorio${sala_id ? `?sala_id=${sala_id}` : ''}`),
  mlStats:     () => get('/ml/stats'),
  mlModels:    () => get('/ml/models'),
  mlFeatures:  (sala_id) => get(`/ml/features${sala_id ? `?sala_id=${sala_id}` : ''}`),
  getAluno:    (id) => get(`/alunos/${id}`),

  // Predições
  predSalas:    () => get('/predicoes/salas'),
  predAlunos:   (sala_id) => get(`/predicoes/alunos/${sala_id}`),
  turmaRapida:  (sala_id) => get(`/predicoes/turma-rapida/${sala_id}`),
  turmaAnalise: (sala_id, model = 'RF_M3') => get(`/predicoes/turma/${sala_id}?model=${model}`),
  analyze: (aluno_id, model = 'RF_M3', tipoMedia = 'ponderada', arredondamento = false) => {
    const q = new URLSearchParams({ model, tipo_media: tipoMedia })
    if (arredondamento) q.set('arredondamento', 'true')
    return get(`/predicoes/analyze/${aluno_id}?${q}`)
  },
  decisionTree: (aluno_id, materia_id = null, model = 'RF_M3', tree_idx = 0) => {
    const q = new URLSearchParams({ model, tree_idx })
    if (materia_id) q.set('materia_id', materia_id)
    return get(`/predicoes/tree/${aluno_id}?${q}`)
  },
  ensembleTimelapse: (aluno_id, materia_id, model) => {
    const q = new URLSearchParams({ model: model || 'RF_M3' })
    if (materia_id) q.set('materia_id', materia_id)
    return get(`/predicoes/timelapse/${aluno_id}?${q}`)
  },

  // ML
  retrain:           (configs) => post('/ml/retrain', configs || {}),
  retrainContinuous: (body)    => post('/ml/retrain-continuous', body || {}),
  activateModel:     (name)    => post(`/ml/activate/${name}`, {}),

  // Exportar
  exportarAlunos:   (sala_id) => download(`/exportar/alunos${sala_id ? `?sala_id=${sala_id}` : ''}`, 'alunos.csv'),
  exportarNotas:    (sala_id) => download(`/exportar/notas${sala_id ? `?sala_id=${sala_id}` : ''}`, 'notas.csv'),
  exportarRelatorio:(sala_id) => download(`/exportar/relatorio${sala_id ? `?sala_id=${sala_id}` : ''}`, 'relatorio.csv'),
  exportarIARaw:    (sala_id) => download(`/exportar/ia-raw${sala_id ? `?sala_id=${sala_id}` : ''}`, 'ia_raw.csv'),
  exportarSalas:    ()        => download('/exportar/salas', 'salas.csv'),
  exportarTemplates:()        => get('/importar/templates'),

  // Importar
  importarTemplates:    ()     => get('/importar/templates'),
  importarPreviewAlunos:(file) => _uploadFile('/importar/preview/alunos', file),
  importarExecutarAlunos:(file)=> _uploadFile('/importar/executar/alunos', file),
  importarPreviewNotas: (file) => _uploadFile('/importar/preview/notas', file),
  importarExecutarNotas:(file) => _uploadFile('/importar/executar/notas', file),

  // Auth
  login:  (email, senha) => postPublic('/auth/login', { email, senha }),
  me:     () => get('/auth/me'),
  getPolicies:    () => get('/auth/policies'),
  addPolicy:      (sub, obj, act) => post('/auth/policies', { sub, obj, act }),
  removePolicy:   (sub, obj, act) => del('/auth/policies'),  // body handled by caller

  // Usuários
  getUsuarios:    () => get('/usuarios'),
  criarUsuario:   (body) => post('/usuarios', body),
  editarUsuario:  (id, body) => put(`/usuarios/${id}`, body),
  deletarUsuario: (id) => del(`/usuarios/${id}`),

  // Atividades (sub-notas por bimestre)
  getAtividades:    (alunoId, materiaId) => get(`/atividades/${alunoId}/${materiaId}`),
  criarAtividade:   (body) => post('/atividades', body),
  editarAtividade:  (id, body) => put(`/atividades/${id}`, body),
  deletarAtividade: (id) => del(`/atividades/${id}`),

  // Presenças
  getPresencas:   (alunoId, materiaId) => get(`/presencas/${alunoId}/${materiaId}`),
  upsertPresenca: (body) => post('/presencas/upsert', body),
  deletarPresenca: (id) => del(`/presencas/${id}`),

  // Mutations
  criarAluno:       (nome, sala_id) => post('/alunos', { nome, sala_id }),
  deletarAluno:     (id) => del(`/alunos/${id}`),
  criarSala:        (nome, codigo) => post('/salas', { nome, codigo }),
  deletarSala:      (id) => del(`/salas/${id}`),
  criarMateria:     (nome) => post('/materias', { nome }),
  materiasDefault:  () => post('/materias/default'),
  deletarMateria:   (id) => del(`/materias/${id}`),
  salvarNota:       (body) => put('/notas', body),
  gerarNotasAluno:  (id) => post(`/notas/gerar/aluno/${id}`),
  gerarNotasTurma:  (id) => post(`/notas/gerar/turma/${id}`),
  gerarNotasTodos:  () => post('/notas/gerar/todos'),
  gerarFeatures:    (sala_id, pesos) => post('/ml/gerar', { sala_id, pesos }),
  gerarGenericos:   (sala_id, n) => post(`/alunos/genericos?sala_id=${sala_id}&quantidade=${n}`),
  atribuirMaterias: () => post('/alunos/atribuir-materias'),
}
