/**
 * DecisionTreeCanvas — D3 force-graph 2.5D com polígonos e profundidade simulada.
 * Nodes no caminho: hexágono (folha) / pentágono (split).
 * Nodes fora do caminho: losango dimmed com escala por profundidade (efeito perspectiva).
 */
import { useEffect, useRef, useState, useCallback } from 'react'
import * as d3 from 'd3'

const CLS = {
  0: { name: 'Reprovado',   bg: '#EF4444', light: '#FEE2E2', ring: '#FCA5A5' },
  1: { name: 'Recuperação', bg: '#F59E0B', light: '#FEF3C7', ring: '#FCD34D' },
  2: { name: 'Aprovado',    bg: '#10B981', light: '#D1FAE5', ring: '#6EE7B7' },
}

const FEAT_SHORT = {
  n1_norm: 'N1', n2_norm: 'N2', n3_norm: 'N3', n4_norm: 'N4',
  slope_notas: 'SL', variancia_notas: 'VAR',
  media_geral_aluno: 'MG', serie_num_norm: 'SR', media_turma_norm: 'MT',
}

const FEAT_LABEL = {
  n1_norm: '1º Bimestre (N1)', n2_norm: '2º Bimestre (N2)',
  n3_norm: '3º Bimestre (N3)', n4_norm: '4º Bimestre (N4)',
  slope_notas: 'Tendência N1→N4', variancia_notas: 'Variância das notas',
  media_geral_aluno: 'Média geral do aluno', serie_num_norm: 'Série escolar',
  media_turma_norm: 'Média da turma',
}

function polygonPoints(sides, r, rotOffset = 0) {
  const step = (2 * Math.PI) / sides
  return Array.from({ length: sides }, (_, i) => {
    const a = i * step - Math.PI / 2 + rotOffset
    return `${(r * Math.cos(a)).toFixed(2)},${(r * Math.sin(a)).toFixed(2)}`
  }).join(' ')
}

function flattenTree(node, depth = 0, parent = null, acc = { nodes: [], links: [] }) {
  acc.nodes.push({ ...node, depth, _parent: parent })
  if (parent !== null) acc.links.push({ source: parent.id, target: node.id })
  if (node.children) {
    for (const child of node.children) flattenTree(child, depth + 1, node, acc)
  }
  return acc
}

export default function DecisionTreeCanvas({ treeData, pathIds = [], prediction, features = {} }) {
  const svgRef  = useRef(null)
  const wrapRef = useRef(null)
  const [tooltip, setTooltip] = useState(null)

  const draw = useCallback(() => {
    if (!treeData || !svgRef.current || !wrapRef.current) return

    const W = wrapRef.current.clientWidth  || 900
    const H = wrapRef.current.clientHeight || 600
    const pathSet = new Set(pathIds)

    // ── Flatten tree ─────────────────────────────────────────────────────────
    const { nodes: rawNodes, links: rawLinks } = flattenTree(treeData)
    const maxDepth = Math.max(...rawNodes.map(n => n.depth), 1)

    const nodeById = {}
    rawNodes.forEach(n => { nodeById[n.id] = n })

    // Give nodes initial y positions based on depth
    const yScale = d3.scaleLinear().domain([0, maxDepth]).range([80, H - 80])
    rawNodes.forEach(n => {
      n.x = W / 2 + (Math.random() - 0.5) * 200
      n.y = yScale(n.depth)
    })

    // ── Force simulation ─────────────────────────────────────────────────────
    const simLinks = rawLinks.map(l => ({ ...l }))

    const simulation = d3.forceSimulation(rawNodes)
      .force('link', d3.forceLink(simLinks)
        .id(d => d.id)
        .distance(d => {
          const src = d.source
          const tgt = d.target
          const onPath = pathSet.has(src.id) && pathSet.has(tgt.id)
          return onPath ? 90 : 60
        })
        .strength(0.6))
      .force('charge', d3.forceManyBody().strength(d => pathSet.has(d.id) ? -300 : -150))
      .force('center', d3.forceCenter(W / 2, H / 2).strength(0.05))
      .force('y', d3.forceY(d => yScale(d.depth)).strength(1.2))
      .force('x', d3.forceX(W / 2).strength(0.04))
      .stop()

    // Run synchronously to stable state
    for (let i = 0; i < 400; i++) simulation.tick()

    // ── SVG setup ────────────────────────────────────────────────────────────
    const svg = d3.select(svgRef.current)
    svg.selectAll('*').remove()
    svg.attr('width', W).attr('height', H)

    // Defs: filters
    const defs = svg.append('defs')

    const glow = defs.append('filter').attr('id', 'fc-glow')
      .attr('x', '-60%').attr('y', '-60%').attr('width', '220%').attr('height', '220%')
    glow.append('feGaussianBlur').attr('stdDeviation', 6).attr('result', 'blur')
    const mg = glow.append('feMerge')
    mg.append('feMergeNode').attr('in', 'blur')
    mg.append('feMergeNode').attr('in', 'SourceGraphic')

    const leafGlow = defs.append('filter').attr('id', 'fc-leaf-glow')
      .attr('x', '-80%').attr('y', '-80%').attr('width', '260%').attr('height', '260%')
    leafGlow.append('feGaussianBlur').attr('stdDeviation', 10).attr('result', 'blur')
    const mg2 = leafGlow.append('feMerge')
    mg2.append('feMergeNode').attr('in', 'blur')
    mg2.append('feMergeNode').attr('in', 'SourceGraphic')

    const blur = defs.append('filter').attr('id', 'fc-blur')
    blur.append('feGaussianBlur').attr('stdDeviation', 1.5)

    // Zoom + pan
    const g = svg.append('g')
    const zoom = d3.zoom().scaleExtent([0.1, 4])
      .on('zoom', ev => g.attr('transform', ev.transform))
    svg.call(zoom).on('dblclick.zoom', null)
    svg.call(zoom.transform, d3.zoomIdentity.translate(0, 0).scale(0.9))

    // ── Links ────────────────────────────────────────────────────────────────
    simLinks.forEach(link => {
      const s = link.source
      const t = link.target
      const onPath = pathSet.has(s.id) && pathSet.has(t.id)
      const cls = CLS[t.majority_class]

      // Animated path for on-path links
      const path = g.append('path')
        .attr('fill', 'none')
        .attr('d', `M${s.x},${s.y} C${s.x},${(s.y + t.y) / 2} ${t.x},${(s.y + t.y) / 2} ${t.x},${t.y}`)
        .attr('stroke', onPath ? (cls?.ring ?? '#818CF8') : '#1E293B')
        .attr('stroke-width', onPath ? 2.5 : 0.8)
        .attr('opacity', onPath ? 0 : 0.2)
        .attr('stroke-dasharray', onPath ? 'none' : '5 4')

      if (onPath) {
        const length = path.node().getTotalLength()
        path
          .attr('stroke-dasharray', `${length} ${length}`)
          .attr('stroke-dashoffset', length)
          .transition().duration(600)
          .delay(t.depth * 100)
          .attr('stroke-dashoffset', 0)
          .attr('opacity', 0.85)
      }
    })

    // ── Nodes ────────────────────────────────────────────────────────────────
    // Sort: off-path first (drawn below), on-path last (on top)
    const sortedNodes = [...rawNodes].sort((a, b) => {
      const ap = pathSet.has(a.id) ? 1 : 0
      const bp = pathSet.has(b.id) ? 1 : 0
      return ap - bp
    })

    sortedNodes.forEach((node, idx) => {
      const onPath = pathSet.has(node.id)
      const isLeaf = node.is_leaf
      const cls = CLS[node.majority_class] ?? CLS[0]

      // Depth-based scale for pseudo-perspective
      const depthRatio = node.depth / maxDepth
      const scale = onPath ? 1 : Math.max(0.45, 1 - depthRatio * 0.55)
      const opacity = onPath ? 1 : Math.max(0.2, 1 - depthRatio * 0.7)
      const useBlur = !onPath && depthRatio > 0.5

      const ng = g.append('g')
        .attr('transform', `translate(${node.x},${node.y})`)
        .attr('cursor', 'pointer')
        .style('opacity', onPath ? 0 : opacity)
        .on('mouseenter', (event) => {
          const rect = wrapRef.current.getBoundingClientRect()
          setTooltip({ x: event.clientX - rect.left + 16, y: event.clientY - rect.top - 8, node })
        })
        .on('mouseleave', () => setTooltip(null))

      if (onPath && isLeaf) {
        // Hexágono — folha no caminho
        const pts = polygonPoints(6, 24)
        ng.append('polygon').attr('points', pts)
          .attr('fill', cls.bg)
          .attr('filter', 'url(#fc-leaf-glow)')
        ng.append('text').attr('text-anchor', 'middle').attr('dy', '0.35em')
          .attr('font-size', '9').attr('font-weight', 'bold').attr('fill', 'white')
          .text({ 0: 'REP', 1: 'REC', 2: 'APR' }[node.majority_class] ?? '?')

        ng.transition().duration(400).delay(node.depth * 120).style('opacity', 1)

      } else if (onPath && !isLeaf) {
        // Pentágono — split no caminho
        const pts = polygonPoints(5, 22)
        ng.append('polygon').attr('points', pts)
          .attr('fill', cls.bg)
          .attr('stroke', cls.ring).attr('stroke-width', 2.5)
          .attr('filter', 'url(#fc-glow)')
        ng.append('text').attr('text-anchor', 'middle').attr('dy', '0.35em')
          .attr('font-size', '9').attr('font-weight', 'bold').attr('fill', 'white')
          .text(FEAT_SHORT[node.feature] ?? '?')
        ng.append('text').attr('text-anchor', 'middle').attr('y', 32)
          .attr('font-size', '7.5').attr('fill', '#94A3B8')
          .text(`${node.goes_left ? '≤' : '>'} ${node.threshold?.toFixed(2) ?? ''}`)
        ng.append('text').attr('text-anchor', 'middle').attr('y', 42)
          .attr('font-size', '7.5').attr('font-weight', 'bold').attr('fill', '#A5B4FC')
          .text(`você: ${node.student_value?.toFixed(2) ?? ''}`)

        ng.transition().duration(400).delay(node.depth * 120).style('opacity', 1)

      } else if (isLeaf) {
        // Losango — folha fora do caminho (escala por profundidade)
        const r = 9 * scale
        const pts = polygonPoints(4, r, Math.PI / 4)
        ng.append('polygon').attr('points', pts)
          .attr('fill', '#1E293B').attr('stroke', '#334155').attr('stroke-width', 0.8)
          .attr('filter', useBlur ? 'url(#fc-blur)' : null)
        ng.append('text').attr('text-anchor', 'middle').attr('dy', '0.35em')
          .attr('font-size', 6 * scale).attr('fill', '#475569')
          .text({ 0: 'R', 1: 'Rc', 2: 'A' }[node.majority_class] ?? '?')

      } else {
        // Losango — split fora do caminho
        const r = 13 * scale
        const pts = polygonPoints(4, r, Math.PI / 4)
        ng.append('polygon').attr('points', pts)
          .attr('fill', '#0F172A').attr('stroke', '#334155').attr('stroke-width', 0.7)
          .attr('filter', useBlur ? 'url(#fc-blur)' : null)
        ng.append('text').attr('text-anchor', 'middle').attr('dy', '0.35em')
          .attr('font-size', 6 * scale).attr('fill', '#475569')
          .text(FEAT_SHORT[node.feature] ?? '?')
      }
    })

  }, [treeData, pathIds])

  useEffect(() => {
    draw()
    const ro = new ResizeObserver(draw)
    if (wrapRef.current) ro.observe(wrapRef.current)
    return () => ro.disconnect()
  }, [draw])

  if (!treeData) return (
    <div className="flex items-center justify-center h-full text-slate-500 text-sm">
      Selecione um aluno e clique em Analisar para ver a árvore de decisão.
    </div>
  )

  return (
    <div ref={wrapRef} className="relative w-full h-full select-none">
      <svg ref={svgRef} className="w-full h-full" />

      {/* Legend */}
      <div className="absolute bottom-3 left-3 flex gap-4 pointer-events-none">
        {Object.entries(CLS).map(([k, v]) => (
          <div key={k} className="flex items-center gap-1.5 text-[10px] text-slate-400">
            <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: v.bg }} />
            {v.name}
          </div>
        ))}
        <div className="flex items-center gap-1.5 text-[10px] text-slate-400">
          <svg width="16" height="16" viewBox="-8 -8 16 16">
            <polygon points={polygonPoints(5, 7)} fill="#818CF8" opacity="0.8" />
          </svg>
          Caminho
        </div>
      </div>

      <p className="absolute bottom-3 right-3 text-[10px] text-slate-600 pointer-events-none">
        Scroll para zoom · Arraste para mover
      </p>

      {tooltip && <Tooltip tip={tooltip} />}
    </div>
  )
}

function Tooltip({ tip }) {
  const { node, x, y } = tip
  const cls = CLS[node.majority_class] ?? CLS[0]
  const label = FEAT_LABEL[node.feature] ?? node.feature

  return (
    <div className="absolute z-50 pointer-events-none bg-slate-900 border border-slate-700
                    rounded-xl p-3 text-xs text-slate-300 shadow-2xl w-56"
      style={{ left: x, top: y }}>
      {node.is_leaf ? (
        <>
          <p className="font-bold text-white mb-2">Nó Folha — Predição</p>
          <div className="flex items-center gap-2 mb-2">
            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: cls.bg }} />
            <span className="font-semibold" style={{ color: cls.bg }}>{cls.name}</span>
          </div>
          <p className="text-slate-500 mb-1">Amostras: {node.samples}</p>
          <div className="space-y-1 mt-2">
            {(node.class_proba ?? []).map((p, i) => (
              <div key={i} className="flex items-center gap-2">
                <span className="text-slate-400 w-20 truncate">{CLS[i]?.name}</span>
                <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
                  <div className="h-full rounded-full" style={{ width: `${p * 100}%`, backgroundColor: CLS[i]?.bg }} />
                </div>
                <span className="w-7 text-right">{(p * 100).toFixed(0)}%</span>
              </div>
            ))}
          </div>
        </>
      ) : (
        <>
          <p className="font-bold text-white mb-1">{label}</p>
          <p className="text-slate-500 text-[10px] mb-2">{node.feature}</p>
          <div className="space-y-1">
            <div className="flex justify-between">
              <span className="text-slate-400">Threshold</span>
              <span className="font-mono text-white">{node.threshold?.toFixed(4)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Valor do aluno</span>
              <span className="font-mono text-indigo-300 font-bold">{node.student_value?.toFixed(4)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Decisão</span>
              <span className={node.goes_left ? 'text-green-400' : 'text-orange-400'}>
                {node.goes_left ? '← esquerda' : 'direita →'}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Amostras</span><span>{node.samples}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Impureza</span><span>{node.impurity}</span>
            </div>
          </div>
          <div className="mt-2 pt-2 border-t border-slate-700">
            <p className="text-slate-500 text-[10px] mb-1">Distribuição das amostras</p>
            <div className="flex h-2 rounded overflow-hidden gap-px">
              {(node.class_proba ?? []).map((p, i) => (
                <div key={i} style={{ width: `${p * 100}%`, backgroundColor: CLS[i]?.bg ?? '#64748B' }} />
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  )
}
