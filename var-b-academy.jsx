// Variation B — ACADEMY (Khan-inspired, structured, professional, subtle gamification)

const B_FONT = "'Inter', system-ui, sans-serif";
const B_BG = '#F4F6FA';
const B_INK = '#0F172A';
const B_RADIUS = 10;
const B_CARD = '#FFFFFF';
const B_BORDER = '#E5E9F0';

function APP_B({ children, sidebar='dash', expanded=true, title, subtitle, kicker, headRight, breadcrumb }) {
  const navItems = [
    { id:'dash',   label:'Dashboard',    icon: I.home },
    { id:'alunos', label:'Alunos',       icon: I.users, count:202 },
    { id:'salas',  label:'Salas/Turmas', icon: I.school, count:7 },
    { id:'mat',    label:'Matérias',     icon: I.book, count:13 },
    { id:'notas',  label:'Notas',        icon: I.edit },
    { id:'pred',   label:'Predições',    icon: I.target, badge:'IA' },
    { id:'rel',    label:'Relatório',    icon: I.chart },
    { id:'ml',     label:'Machine Learning', icon: I.brain },
  ];
  const ioItems = [
    { id:'imp', label:'Importar Excel', icon: I.upload },
    { id:'exp', label:'Exportar Excel', icon: I.download },
  ];
  const sbW = expanded ? 232 : 64;
  return (
    <div style={{ width:1280, height:860, background:B_BG, fontFamily:B_FONT, color:B_INK, display:'flex', overflow:'hidden', borderRadius:14 }}>
      {/* Sidebar */}
      <aside style={{ width:sbW, background:'#0F172A', color:'#CBD5E1', padding:'14px 0', display:'flex', flexDirection:'column', transition:'width .2s' }}>
        <div style={{ display:'flex', alignItems:'center', gap:10, padding:'2px 16px 14px' }}>
          <div style={{ width:32, height:32, borderRadius:8, background:'#4F46E5', display:'grid', placeItems:'center', color:'#fff', fontWeight:900, fontSize:16, flexShrink:0 }}>E</div>
          {expanded && (
            <div>
              <div style={{ fontSize:15, fontWeight:800, color:'#fff', letterSpacing:'-0.01em' }}>EduNotas</div>
              <div style={{ fontSize:10, color:'#64748B', fontWeight:600 }}>Sistema Escolar v2.0</div>
            </div>
          )}
          <div style={{ flex:1 }}/>
          {expanded && <span style={{ color:'#64748B' }}>{I.chev({s:14})}</span>}
        </div>

        {expanded && <div style={{ padding:'0 16px 8px' }}>
          <div style={{ display:'flex', alignItems:'center', gap:6, padding:'7px 10px', background:'rgba(255,255,255,.05)', borderRadius:8, fontSize:12, color:'#94A3B8' }}>{I.search({s:14})} Buscar...</div>
        </div>}

        <div style={{ padding:'0 8px', display:'flex', flexDirection:'column', gap:1 }}>
          {expanded && <div style={{ fontSize:9.5, fontWeight:800, color:'#475569', letterSpacing:'.12em', padding:'10px 10px 4px' }}>PRINCIPAL</div>}
          {navItems.map(it=>{
            const active = it.id===sidebar;
            return (
              <div key={it.id} style={{
                display:'flex', alignItems:'center', gap:10, padding: expanded?'8px 10px':'8px', borderRadius:8,
                background: active ? '#4F46E5' : 'transparent', color: active ? '#fff' : '#94A3B8', fontWeight:600, fontSize:13, position:'relative', justifyContent: expanded?'flex-start':'center'
              }}>
                <span style={{ width:20, height:20, display:'grid', placeItems:'center', flexShrink:0 }}>{it.icon({s:17})}</span>
                {expanded && <>
                  <span style={{ flex:1 }}>{it.label}</span>
                  {it.count!=null && <span style={{ fontSize:10, fontWeight:700, padding:'2px 7px', background: active?'rgba(255,255,255,.18)':'#1E293B', color: active?'#fff':'#64748B', borderRadius:999 }}>{it.count}</span>}
                  {it.badge && <span style={{ fontSize:9, fontWeight:900, padding:'2px 6px', background:'#F59E0B', color:'#fff', borderRadius:4, letterSpacing:'.05em' }}>{it.badge}</span>}
                </>}
              </div>
            );
          })}

          {expanded && <div style={{ fontSize:9.5, fontWeight:800, color:'#475569', letterSpacing:'.12em', padding:'14px 10px 4px' }}>DADOS</div>}
          {ioItems.map(it=>(
            <div key={it.id} style={{ display:'flex', alignItems:'center', gap:10, padding: expanded?'8px 10px':'8px', borderRadius:8, color:'#94A3B8', fontWeight:600, fontSize:13, justifyContent: expanded?'flex-start':'center' }}>
              <span style={{ width:20, height:20, display:'grid', placeItems:'center', flexShrink:0 }}>{it.icon({s:17})}</span>
              {expanded && <span>{it.label}</span>}
            </div>
          ))}
        </div>

        <div style={{ flex:1 }}/>
        {expanded && (
          <div style={{ margin:'0 12px', padding:'10px 12px', background:'rgba(79,70,229,.12)', border:'1px solid rgba(79,70,229,.3)', borderRadius:8, fontSize:11 }}>
            <div style={{ display:'flex', alignItems:'center', gap:6, color:'#A5B4FC', fontWeight:800, marginBottom:3 }}>{I.sparkle({s:12})} Modelo IA Ativo</div>
            <div style={{ color:'#E2E8F0', fontWeight:700 }}>RF_M3 — 91.3%</div>
            <div style={{ color:'#64748B', fontWeight:600, marginTop:1 }}>Atualizado há 12 min</div>
          </div>
        )}
        <div style={{ height:1, background:'rgba(255,255,255,.06)', margin:'12px 12px' }}/>
        <div style={{ display:'flex', alignItems:'center', gap:10, padding: expanded?'4px 16px':'4px', justifyContent: expanded?'flex-start':'center' }}>
          <div style={{ width:30, height:30, borderRadius:'50%', background:'linear-gradient(135deg,#8B5CF6,#EC4899)', display:'grid', placeItems:'center', color:'#fff', fontWeight:800, fontSize:11, flexShrink:0 }}>MR</div>
          {expanded && <>
            <div style={{ flex:1, minWidth:0 }}>
              <div style={{ fontSize:12, fontWeight:700, color:'#fff' }}>Mariana Rocha</div>
              <div style={{ fontSize:10, color:'#64748B', fontWeight:600 }}>Coordenadora</div>
            </div>
            <span style={{ color:'#64748B' }}>{I.dots({s:14})}</span>
          </>}
        </div>
      </aside>

      {/* Main */}
      <main style={{ flex:1, display:'flex', flexDirection:'column', minWidth:0 }}>
        {/* Topbar */}
        <header style={{ display:'flex', alignItems:'center', gap:14, padding:'14px 28px 0', background:B_BG }}>
          <div style={{ flex:1 }}>
            {breadcrumb && <div style={{ fontSize:11, color:'#64748B', fontWeight:600, marginBottom:4 }}>{breadcrumb}</div>}
            <div style={{ display:'flex', alignItems:'baseline', gap:10 }}>
              <div style={{ fontSize:22, fontWeight:800, letterSpacing:'-0.02em', lineHeight:1.1 }}>{title}</div>
              {kicker && <div style={{ fontSize:11, fontWeight:700, padding:'3px 8px', borderRadius:5, background:'#EEF2FF', color:'#4F46E5', letterSpacing:'.04em' }}>{kicker}</div>}
            </div>
            {subtitle && <div style={{ fontSize:13, color:'#64748B', marginTop:3 }}>{subtitle}</div>}
          </div>
          <div style={{ display:'flex', alignItems:'center', gap:8 }}>{headRight}</div>
        </header>
        <div style={{ height:14 }}/>
        <div style={{ flex:1, overflow:'hidden', padding:'0 28px 22px' }}>{children}</div>
      </main>
    </div>
  );
}

// ============ DASHBOARD B ============
function B_Dashboard() {
  return (
    <APP_B sidebar="dash" breadcrumb="Visão geral" title="Dashboard" subtitle="Resumo do desempenho escolar — 2º trimestre, semana 14"
      headRight={<>
        <div style={{ padding:'8px 12px', background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:8, fontSize:12, fontWeight:600, color:'#475569', display:'flex', alignItems:'center', gap:6 }}>2º Trimestre {I.down({s:12})}</div>
        <div style={{ padding:'8px 12px', background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:8, fontSize:12, fontWeight:600, color:'#475569' }}>Atualizar</div>
        <div style={{ padding:'8px 14px', background:'#4F46E5', color:'#fff', borderRadius:8, fontSize:12, fontWeight:700, display:'flex', alignItems:'center', gap:6 }}>{I.download({s:14})} Relatório</div>
      </>}>
      <div style={{ display:'grid', gridTemplateColumns:'repeat(4,1fr)', gap:12, height:'100%' }}>
        {/* KPIs */}
        {[
          { lbl:'Alunos ativos', val:'202', delta:'+12', deltaC:'#10B981', sub:'em 7 turmas', icon:I.users, accent:'#4F46E5' },
          { lbl:'Notas lançadas', val:'1.846', delta:'87%', deltaC:'#0EA5E9', sub:'do trimestre', icon:I.edit, accent:'#0EA5E9' },
          { lbl:'Taxa de aprovação', val:'76,2%', delta:'+2.4', deltaC:'#10B981', sub:'vs trimestre anterior', icon:I.check, accent:'#10B981' },
          { lbl:'Em risco', val:'31', delta:'+4', deltaC:'#EF4444', sub:'previstos pela IA', icon:I.warn, accent:'#EF4444' },
        ].map((k,i)=>(
          <div key={i} style={{ gridColumn:'span 1', background:B_CARD, border:`1px solid ${B_BORDER}`, borderRadius:B_RADIUS, padding:'14px 16px' }}>
            <div style={{ display:'flex', justifyContent:'space-between', alignItems:'flex-start' }}>
              <div style={{ fontSize:12, color:'#64748B', fontWeight:600 }}>{k.lbl}</div>
              <span style={{ color:k.accent }}>{k.icon({s:16})}</span>
            </div>
            <div style={{ display:'flex', alignItems:'baseline', gap:8, marginTop:8 }}>
              <div style={{ fontSize:28, fontWeight:800, letterSpacing:'-0.02em', lineHeight:1 }}>{k.val}</div>
              <div style={{ fontSize:12, fontWeight:700, color:k.deltaC }}>{k.delta}</div>
            </div>
            <div style={{ fontSize:11, color:'#94A3B8', fontWeight:500, marginTop:4 }}>{k.sub}</div>
          </div>
        ))}

        {/* Average per turma chart */}
        <div style={{ gridColumn:'span 3', gridRow:'span 2', background:B_CARD, border:`1px solid ${B_BORDER}`, borderRadius:B_RADIUS, padding:'16px 18px', display:'flex', flexDirection:'column' }}>
          <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between', marginBottom:12 }}>
            <div>
              <div style={{ fontSize:14, fontWeight:700 }}>Média por turma × meta</div>
              <div style={{ fontSize:11, color:'#94A3B8', fontWeight:500 }}>Comparativo com a média alvo (7,0) por trimestre</div>
            </div>
            <div style={{ display:'flex', gap:12, fontSize:11 }}>
              <span style={{ display:'flex', alignItems:'center', gap:5 }}><span style={{ width:10, height:10, background:'#4F46E5', borderRadius:2 }}/>Média atual</span>
              <span style={{ display:'flex', alignItems:'center', gap:5 }}><span style={{ width:10, height:2, background:'#94A3B8' }}/>Meta (7,0)</span>
              <span style={{ display:'flex', alignItems:'center', gap:5 }}><span style={{ width:10, height:10, background:'#E2E8F0', borderRadius:2 }}/>Trim. anterior</span>
            </div>
          </div>
          <div style={{ flex:1, position:'relative', display:'flex', alignItems:'flex-end', gap:14, padding:'10px 30px 30px' }}>
            {/* Grid */}
            <div style={{ position:'absolute', inset:'10px 30px 30px', display:'flex', flexDirection:'column', justifyContent:'space-between', pointerEvents:'none' }}>
              {[10,8,6,4,2,0].map(v=>(
                <div key={v} style={{ borderTop:'1px dashed #F1F5F9', position:'relative', height:0 }}>
                  <span style={{ position:'absolute', left:-26, top:-7, fontSize:10, color:'#94A3B8', fontWeight:600 }}>{v.toFixed(1)}</span>
                </div>
              ))}
            </div>
            {/* Meta line */}
            <div style={{ position:'absolute', left:30, right:30, bottom:`calc(30px + 70%)`, borderTop:'1.5px dashed #94A3B8', zIndex:1 }}/>
            {TURMAS.map((t,i)=>{
              const cur = 6.2 + (i*0.3) + (i%2?0.4:-0.2);
              const prev = cur - 0.3 - (i*0.05);
              return (
                <div key={t.code} style={{ flex:1, display:'flex', flexDirection:'column', alignItems:'center', gap:6, height:'100%', justifyContent:'flex-end' }}>
                  <div style={{ display:'flex', alignItems:'flex-end', gap:3, width:'100%', height:'80%' }}>
                    <div style={{ flex:1, height:`${(prev/10)*100}%`, background:'#E2E8F0', borderRadius:'3px 3px 0 0' }}/>
                    <div style={{ flex:1, height:`${(cur/10)*100}%`, background: cur>=7?'#4F46E5':'#EF4444', borderRadius:'3px 3px 0 0', position:'relative' }}>
                      <div style={{ position:'absolute', top:-18, left:'50%', transform:'translateX(-50%)', fontSize:10, fontWeight:800, color: cur>=7?'#4F46E5':'#EF4444' }}>{cur.toFixed(1)}</div>
                    </div>
                  </div>
                  <div style={{ fontSize:11, fontWeight:700, color:'#475569' }}>{t.code}</div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Ranking */}
        <div style={{ gridColumn:'span 1', gridRow:'span 2', background:B_CARD, border:`1px solid ${B_BORDER}`, borderRadius:B_RADIUS, padding:'14px 16px', display:'flex', flexDirection:'column' }}>
          <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between', marginBottom:10 }}>
            <div style={{ fontSize:13, fontWeight:700 }}>Top desempenho</div>
            <span style={{ color:'#94A3B8', fontSize:11, fontWeight:600 }}>Ver todos</span>
          </div>
          <div style={{ flex:1, display:'flex', flexDirection:'column', gap:8 }}>
            {ALUNOS.filter(a=>a.status==='on').sort((a,b)=>b.media-a.media).slice(0,6).map((a,i)=>(
              <div key={a.mat} style={{ display:'flex', alignItems:'center', gap:8, padding:'6px 4px' }}>
                <div style={{ width:18, fontSize:11, fontWeight:700, color:'#94A3B8', textAlign:'center' }}>{i+1}</div>
                <Avatar a={a} size={28}/>
                <div style={{ flex:1, minWidth:0 }}>
                  <div style={{ fontSize:12, fontWeight:700, whiteSpace:'nowrap', overflow:'hidden', textOverflow:'ellipsis' }}>{a.nome}</div>
                  <div style={{ fontSize:10, color:'#94A3B8', fontWeight:600 }}>{a.turma}</div>
                </div>
                <div style={{ fontSize:12, fontWeight:800, color:'#10B981' }}>{a.media.toFixed(1)}</div>
              </div>
            ))}
          </div>
        </div>

        {/* AI predictions */}
        <div style={{ gridColumn:'span 2', background:B_CARD, border:`1px solid ${B_BORDER}`, borderRadius:B_RADIUS, padding:'14px 16px' }}>
          <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between', marginBottom:10 }}>
            <div style={{ display:'flex', alignItems:'center', gap:8 }}>
              <span style={{ width:24, height:24, borderRadius:6, background:'#EEF2FF', color:'#4F46E5', display:'grid', placeItems:'center' }}>{I.brain({s:14})}</span>
              <div style={{ fontSize:13, fontWeight:700 }}>Previsões da IA</div>
              <div style={{ fontSize:9, padding:'2px 6px', background:'#D1FAE5', color:'#047857', borderRadius:4, fontWeight:800, letterSpacing:'.04em' }}>● RF_M3 91.3%</div>
            </div>
            <span style={{ color:'#4F46E5', fontSize:11, fontWeight:700 }}>Ver todas →</span>
          </div>
          <div style={{ display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:8 }}>
            {[
              { l:'Vão melhorar', n:43, c:'#10B981', bg:'#D1FAE5', ic:I.up },
              { l:'Estáveis', n:147, c:'#0EA5E9', bg:'#E0F2FE', ic:I.target },
              { l:'Vão piorar', n:12, c:'#EF4444', bg:'#FEE2E2', ic:I.down },
            ].map(p=>(
              <div key={p.l} style={{ padding:'10px 12px', background:p.bg, borderRadius:8, display:'flex', alignItems:'center', gap:8 }}>
                <span style={{ color:p.c }}>{p.ic({s:18})}</span>
                <div>
                  <div style={{ fontSize:18, fontWeight:800, color:p.c, lineHeight:1 }}>{p.n}</div>
                  <div style={{ fontSize:10, color:p.c, fontWeight:700 }}>{p.l}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* At risk */}
        <div style={{ gridColumn:'span 2', background:B_CARD, border:`1px solid ${B_BORDER}`, borderRadius:B_RADIUS, padding:'14px 16px' }}>
          <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between', marginBottom:10 }}>
            <div style={{ display:'flex', alignItems:'center', gap:8 }}>
              <span style={{ width:24, height:24, borderRadius:6, background:'#FEE2E2', color:'#DC2626', display:'grid', placeItems:'center' }}>{I.warn({s:14})}</span>
              <div style={{ fontSize:13, fontWeight:700 }}>Alunos em risco</div>
            </div>
            <span style={{ color:'#4F46E5', fontSize:11, fontWeight:700 }}>31 total →</span>
          </div>
          <div style={{ display:'flex', flexDirection:'column', gap:6 }}>
            {ALUNOS.filter(a=>a.status==='risk').slice(0,4).map(a=>(
              <div key={a.mat} style={{ display:'flex', alignItems:'center', gap:8, padding:'6px 8px', background:'#FEF2F2', borderRadius:6, borderLeft:'3px solid #EF4444' }}>
                <Avatar a={a} size={26}/>
                <div style={{ flex:1, minWidth:0 }}>
                  <div style={{ fontSize:12, fontWeight:700 }}>{a.nome}</div>
                  <div style={{ fontSize:10, color:'#94A3B8', fontWeight:600 }}>{a.turma} • média {a.media.toFixed(1)}</div>
                </div>
                <div style={{ fontSize:10, fontWeight:800, color:'#DC2626', padding:'2px 7px', background:'#FEE2E2', borderRadius:4 }}>↓ {a.streak===0?'sem streak':`streak ${a.streak}d`}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </APP_B>
  );
}

// ============ ALUNOS B ============
function B_Alunos() {
  return (
    <APP_B sidebar="alunos" breadcrumb="Gestão / Alunos" title="Alunos" kicker="202 ATIVOS"
      headRight={<>
        <div style={{ display:'flex', alignItems:'center', gap:6, padding:'7px 10px', background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:8, fontSize:12, fontWeight:600, color:'#475569', width:220 }}>{I.search({s:14})} Buscar nome ou matrícula...</div>
        <div style={{ padding:'7px 10px', background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:8, fontSize:12, fontWeight:600, color:'#475569', display:'flex', alignItems:'center', gap:5 }}>{I.filter({s:12})} Filtros (2)</div>
        <div style={{ padding:'7px 12px', background:'#4F46E5', color:'#fff', borderRadius:8, fontSize:12, fontWeight:700, display:'flex', alignItems:'center', gap:5 }}>{I.plus({s:14})} Novo aluno</div>
      </>}>
      <div style={{ display:'flex', flexDirection:'column', gap:10, height:'100%' }}>
        {/* Tabs / filters */}
        <div style={{ display:'flex', alignItems:'center', gap:0, background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:8, padding:'3px', width:'fit-content' }}>
          {[
            { l:'Todos', n:202, active:true },
            { l:'No ritmo', n:154 },
            { l:'Atenção', n:17 },
            { l:'Risco', n:31 },
          ].map(t=>(
            <div key={t.l} style={{ padding:'6px 12px', fontSize:12, fontWeight:700, borderRadius:6, background:t.active?'#F1F5F9':'transparent', color:t.active?'#0F172A':'#64748B', display:'flex', alignItems:'center', gap:6 }}>
              {t.l} <span style={{ fontSize:10, padding:'1px 6px', borderRadius:999, background:t.active?'#0F172A':'#F1F5F9', color:t.active?'#fff':'#64748B', fontWeight:700 }}>{t.n}</span>
            </div>
          ))}
        </div>

        {/* Table */}
        <div style={{ flex:1, background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:B_RADIUS, overflow:'hidden', display:'flex', flexDirection:'column' }}>
          <div style={{ display:'grid', gridTemplateColumns:'40px 2.4fr 0.7fr 0.7fr 1.2fr 1.4fr 0.9fr 80px', gap:0, fontSize:10.5, fontWeight:800, color:'#64748B', letterSpacing:'.06em', padding:'10px 14px', background:'#F8FAFC', borderBottom:`1px solid ${B_BORDER}` }}>
            <div><input type="checkbox"/></div>
            <div>ALUNO</div><div>TURMA</div><div>MÉDIA</div><div>NÍVEL</div><div>PROGRESSO XP</div><div>STREAK</div><div style={{ textAlign:'right' }}>STATUS</div>
          </div>
          <div style={{ flex:1, overflow:'auto' }}>
            {ALUNOS.map((a,i)=>{
              const map = { on:{ bg:'#D1FAE5', fg:'#047857', lbl:'No ritmo', dot:'#10B981' }, warn:{ bg:'#FEF3C7', fg:'#92400E', lbl:'Atenção', dot:'#F59E0B' }, risk:{ bg:'#FEE2E2', fg:'#B91C1C', lbl:'Risco', dot:'#EF4444' } };
              const s = map[a.status];
              const xpPct = (a.xp%500)/500*100;
              return (
                <div key={a.mat} style={{ display:'grid', gridTemplateColumns:'40px 2.4fr 0.7fr 0.7fr 1.2fr 1.4fr 0.9fr 80px', gap:0, alignItems:'center', padding:'10px 14px', borderBottom:`1px solid ${B_BORDER}`, fontSize:13 }}>
                  <div><input type="checkbox"/></div>
                  <div style={{ display:'flex', alignItems:'center', gap:10 }}>
                    <Avatar a={a} size={32}/>
                    <div>
                      <div style={{ fontWeight:700 }}>{a.nome}</div>
                      <div style={{ fontSize:11, color:'#94A3B8', fontWeight:500 }}>#{a.mat}</div>
                    </div>
                  </div>
                  <div style={{ fontWeight:600, color:'#475569' }}>{a.turma}</div>
                  <div style={{ fontWeight:800, color: a.media<5?'#EF4444':a.media<7?'#F59E0B':'#10B981' }}>{a.media.toFixed(1)}</div>
                  <div style={{ display:'flex', alignItems:'center', gap:6 }}>
                    <div style={{ width:22, height:22, borderRadius:6, background:'#EEF2FF', color:'#4F46E5', display:'grid', placeItems:'center', fontSize:11, fontWeight:900 }}>{a.lvl}</div>
                    <span style={{ fontSize:12, color:'#475569', fontWeight:600 }}>Nv. {a.lvl}</span>
                  </div>
                  <div>
                    <div style={{ display:'flex', justifyContent:'space-between', fontSize:10, fontWeight:600, color:'#94A3B8', marginBottom:3 }}>
                      <span>{a.xp.toLocaleString()} XP</span>
                      <span>{Math.round(xpPct)}%</span>
                    </div>
                    <div style={{ height:5, background:'#F1F5F9', borderRadius:999, overflow:'hidden' }}>
                      <div style={{ width:`${xpPct}%`, height:'100%', background:'linear-gradient(90deg,#4F46E5,#8B5CF6)' }}/>
                    </div>
                  </div>
                  <div style={{ display:'flex', alignItems:'center', gap:5 }}>
                    {a.streak>0 ? <>
                      <span style={{ color:'#F97316' }}>{I.fire({s:14})}</span>
                      <span style={{ fontSize:12, fontWeight:700 }}>{a.streak}d</span>
                    </> : <span style={{ fontSize:11, color:'#94A3B8' }}>—</span>}
                  </div>
                  <div style={{ textAlign:'right' }}>
                    <span style={{ fontSize:11, padding:'3px 8px', borderRadius:6, background:s.bg, color:s.fg, fontWeight:700, display:'inline-flex', alignItems:'center', gap:4 }}><span style={{ width:6, height:6, borderRadius:'50%', background:s.dot }}/>{s.lbl}</span>
                  </div>
                </div>
              );
            })}
          </div>
          <div style={{ padding:'10px 14px', borderTop:`1px solid ${B_BORDER}`, display:'flex', alignItems:'center', justifyContent:'space-between', fontSize:12, color:'#64748B' }}>
            <div>Mostrando 1–12 de 202</div>
            <div style={{ display:'flex', gap:4 }}>
              {['‹',1,2,3,4,'…',17,'›'].map((p,i)=>(
                <div key={i} style={{ minWidth:28, height:28, padding:'0 8px', display:'grid', placeItems:'center', borderRadius:6, fontSize:12, fontWeight:600, background:p===1?'#4F46E5':'#fff', color:p===1?'#fff':'#475569', border:p===1?'none':`1px solid ${B_BORDER}` }}>{p}</div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </APP_B>
  );
}

// ============ SALAS B ============
function B_Salas() {
  return (
    <APP_B sidebar="salas" breadcrumb="Gestão / Salas e Turmas" title="Salas / Turmas" kicker="7 ATIVAS"
      headRight={<>
        <div style={{ display:'flex', alignItems:'center', gap:6, padding:'7px 10px', background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:8, fontSize:12, fontWeight:600, color:'#475569' }}>
          <span>Nome da sala:</span>
          <span style={{ color:'#94A3B8' }}>ex. 6º Fundamental</span>
        </div>
        <div style={{ display:'flex', alignItems:'center', gap:6, padding:'7px 10px', background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:8, fontSize:12, fontWeight:600, color:'#475569' }}>
          <span>Código:</span>
          <span style={{ color:'#94A3B8' }}>6F</span>
        </div>
        <div style={{ padding:'7px 12px', background:'#4F46E5', color:'#fff', borderRadius:8, fontSize:12, fontWeight:700, display:'flex', alignItems:'center', gap:5 }}>{I.plus({s:14})} Criar sala</div>
      </>}>
      <div style={{ background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:B_RADIUS, padding:0, overflow:'hidden', height:'100%', display:'flex', flexDirection:'column' }}>
        <div style={{ display:'grid', gridTemplateColumns:'2fr 0.6fr 1fr 1fr 1.4fr 1.4fr 100px', gap:0, fontSize:10.5, fontWeight:800, color:'#64748B', letterSpacing:'.06em', padding:'12px 16px', background:'#F8FAFC', borderBottom:`1px solid ${B_BORDER}` }}>
          <div>SALA</div><div>CÓDIGO</div><div>ALUNOS</div><div>EM RISCO</div><div>MÉDIA DA TURMA</div><div>PROGRESSO TRIMESTRE</div><div style={{ textAlign:'right' }}>AÇÕES</div>
        </div>
        {TURMAS.map((t,i)=>{
          const cur = 6.2 + (i*0.3) + (i%2?0.4:-0.2);
          const prog = 40 + (i*7) + (i%3)*5;
          return (
            <div key={t.code} style={{ display:'grid', gridTemplateColumns:'2fr 0.6fr 1fr 1fr 1.4fr 1.4fr 100px', gap:0, alignItems:'center', padding:'14px 16px', borderBottom:`1px solid ${B_BORDER}`, fontSize:13 }}>
              <div style={{ display:'flex', alignItems:'center', gap:10 }}>
                <div style={{ width:36, height:36, borderRadius:8, background:'#F1F5F9', color:'#0F172A', display:'grid', placeItems:'center', fontSize:13, fontWeight:900 }}>{t.code}</div>
                <div>
                  <div style={{ fontWeight:700 }}>{t.name}</div>
                  <div style={{ fontSize:11, color:'#94A3B8' }}>Sala 0{i+1} • Coordenação geral</div>
                </div>
              </div>
              <div style={{ fontWeight:700, fontSize:12, color:'#475569' }}>{t.code}</div>
              <div style={{ display:'flex', alignItems:'center', gap:6 }}>
                <span style={{ fontWeight:800, fontSize:15 }}>{t.qtd}</span>
                <div style={{ display:'flex' }}>
                  {ALUNOS.slice(i,i+3).map((a,k)=>(
                    <div key={k} style={{ marginLeft: k===0?0:-6, border:'2px solid #fff', borderRadius:'50%' }}><Avatar a={a} size={20}/></div>
                  ))}
                </div>
              </div>
              <div>
                <span style={{ fontSize:11, padding:'3px 8px', borderRadius:6, background: t.risco>5?'#FEE2E2':'#FEF3C7', color: t.risco>5?'#B91C1C':'#92400E', fontWeight:800 }}>{t.risco} alunos</span>
              </div>
              <div style={{ display:'flex', alignItems:'center', gap:8 }}>
                <div style={{ fontSize:15, fontWeight:800, color: cur>=7?'#10B981':'#EF4444', width:30 }}>{cur.toFixed(1)}</div>
                <div style={{ width:60, height:24 }}>
                  <SparkBar data={[5.4,5.8,6.0,6.2,6.5,6.7,cur]} color={cur>=7?'#10B981':'#EF4444'} h={24}/>
                </div>
              </div>
              <div>
                <div style={{ display:'flex', justifyContent:'space-between', fontSize:10, color:'#94A3B8', fontWeight:600, marginBottom:3 }}>
                  <span>{prog}% concluído</span><span>14/24 sem</span>
                </div>
                <div style={{ height:6, background:'#F1F5F9', borderRadius:999, overflow:'hidden' }}>
                  <div style={{ width:`${prog}%`, height:'100%', background:'#4F46E5', borderRadius:999 }}/>
                </div>
              </div>
              <div style={{ display:'flex', gap:4, justifyContent:'flex-end' }}>
                <div style={{ width:28, height:28, borderRadius:6, border:`1px solid ${B_BORDER}`, display:'grid', placeItems:'center', color:'#64748B' }}>{I.pencil({s:14})}</div>
                <div style={{ width:28, height:28, borderRadius:6, border:`1px solid ${B_BORDER}`, display:'grid', placeItems:'center', color:'#64748B' }}>{I.dots({s:14})}</div>
              </div>
            </div>
          );
        })}
        <div style={{ flex:1 }}/>
        <div style={{ padding:'12px 16px', borderTop:`1px solid ${B_BORDER}`, fontSize:12, color:'#64748B', display:'flex', justifyContent:'space-between' }}>
          <div>7 turmas no total — 202 alunos</div>
          <div style={{ display:'flex', gap:14 }}>
            <span>Média geral: <strong style={{ color:'#0F172A' }}>7,2</strong></span>
            <span>Em risco: <strong style={{ color:'#EF4444' }}>31</strong></span>
          </div>
        </div>
      </div>
    </APP_B>
  );
}

// ============ MATÉRIAS B ============
function B_Materias() {
  const colors = ['#4F46E5','#EF4444','#10B981','#F59E0B','#0EA5E9','#EC4899','#8B5CF6','#06B6D4','#F97316','#84CC16','#14B8A6','#A855F7','#F472B6'];
  return (
    <APP_B sidebar="mat" breadcrumb="Currículo / Matérias" title="Matérias" kicker="13 CADASTRADAS"
      headRight={<>
        <div style={{ display:'flex', alignItems:'center', gap:6, padding:'7px 10px', background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:8, fontSize:12, color:'#475569' }}>
          <span style={{ fontWeight:600 }}>Nova matéria:</span>
          <span style={{ color:'#94A3B8' }}>digite o nome...</span>
        </div>
        <div style={{ padding:'7px 12px', background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:8, fontSize:12, fontWeight:700, color:'#475569' }}>Adicionar padrão (13)</div>
        <div style={{ padding:'7px 12px', background:'#4F46E5', color:'#fff', borderRadius:8, fontSize:12, fontWeight:700, display:'flex', alignItems:'center', gap:5 }}>{I.plus({s:14})} Adicionar</div>
      </>}>
      <div style={{ display:'grid', gridTemplateColumns:'1.6fr 1fr', gap:14, height:'100%' }}>
        <div style={{ background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:B_RADIUS, overflow:'hidden', display:'flex', flexDirection:'column' }}>
          <div style={{ display:'grid', gridTemplateColumns:'40px 1.5fr 0.8fr 0.8fr 1.4fr 100px', gap:0, fontSize:10.5, fontWeight:800, color:'#64748B', letterSpacing:'.06em', padding:'10px 14px', background:'#F8FAFC', borderBottom:`1px solid ${B_BORDER}` }}>
            <div>#</div><div>MATÉRIA</div><div>TURMAS</div><div>NOTAS</div><div>APROVAÇÃO</div><div style={{ textAlign:'right' }}>AÇÕES</div>
          </div>
          <div style={{ flex:1, overflow:'auto' }}>
            {MATERIAS.map((m,i)=>{
              const aprov = 60 + (i*5)%35;
              const c = colors[i];
              return (
                <div key={m} style={{ display:'grid', gridTemplateColumns:'40px 1.5fr 0.8fr 0.8fr 1.4fr 100px', gap:0, alignItems:'center', padding:'10px 14px', borderBottom:`1px solid ${B_BORDER}`, fontSize:13 }}>
                  <div style={{ fontSize:11, fontWeight:700, color:'#94A3B8' }}>{(i+1).toString().padStart(2,'0')}</div>
                  <div style={{ display:'flex', alignItems:'center', gap:8 }}>
                    <span style={{ width:8, height:24, background:c, borderRadius:2 }}/>
                    <span style={{ fontWeight:700 }}>{m}</span>
                  </div>
                  <div style={{ color:'#475569', fontWeight:600 }}>7 turmas</div>
                  <div style={{ color:'#475569', fontWeight:600 }}>{(40+i*8)%180}</div>
                  <div style={{ display:'flex', alignItems:'center', gap:8 }}>
                    <div style={{ flex:1, height:6, background:'#F1F5F9', borderRadius:999, overflow:'hidden' }}>
                      <div style={{ width:`${aprov}%`, height:'100%', background:c, borderRadius:999 }}/>
                    </div>
                    <span style={{ fontSize:11, fontWeight:800, color:c, width:32 }}>{aprov}%</span>
                  </div>
                  <div style={{ display:'flex', gap:4, justifyContent:'flex-end' }}>
                    <div style={{ width:26, height:26, borderRadius:6, border:`1px solid ${B_BORDER}`, display:'grid', placeItems:'center', color:'#64748B' }}>{I.pencil({s:12})}</div>
                    <div style={{ width:26, height:26, borderRadius:6, border:`1px solid ${B_BORDER}`, display:'grid', placeItems:'center', color:'#EF4444' }}>{I.trash({s:12})}</div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Detail panel */}
        <div style={{ display:'flex', flexDirection:'column', gap:12 }}>
          <div style={{ background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:B_RADIUS, padding:'14px 16px' }}>
            <div style={{ display:'flex', alignItems:'center', gap:10, marginBottom:10 }}>
              <div style={{ width:40, height:40, borderRadius:8, background:'#FEE2E2', color:'#EF4444', display:'grid', placeItems:'center' }}>{I.target({s:20})}</div>
              <div>
                <div style={{ fontSize:14, fontWeight:800 }}>Matemática</div>
                <div style={{ fontSize:11, color:'#94A3B8', fontWeight:600 }}>2ª matéria com mais reprovações</div>
              </div>
            </div>
            <div style={{ display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:8 }}>
              <div style={{ padding:'8px 10px', background:'#F8FAFC', borderRadius:6 }}>
                <div style={{ fontSize:18, fontWeight:800 }}>5,4</div>
                <div style={{ fontSize:10, color:'#94A3B8', fontWeight:700 }}>MÉDIA GERAL</div>
              </div>
              <div style={{ padding:'8px 10px', background:'#FEE2E2', borderRadius:6 }}>
                <div style={{ fontSize:18, fontWeight:800, color:'#B91C1C' }}>22%</div>
                <div style={{ fontSize:10, color:'#B91C1C', fontWeight:700 }}>REPROVAÇÕES</div>
              </div>
              <div style={{ padding:'8px 10px', background:'#FEF3C7', borderRadius:6 }}>
                <div style={{ fontSize:18, fontWeight:800, color:'#92400E' }}>34%</div>
                <div style={{ fontSize:10, color:'#92400E', fontWeight:700 }}>RECUPERAÇÃO</div>
              </div>
            </div>
          </div>

          <div style={{ background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:B_RADIUS, padding:'14px 16px', flex:1 }}>
            <div style={{ fontSize:12, fontWeight:800, color:'#64748B', letterSpacing:'.06em', marginBottom:10 }}>DISTRIBUIÇÃO POR TURMA</div>
            <div style={{ display:'flex', flexDirection:'column', gap:8 }}>
              {TURMAS.map((t,i)=>{
                const v = 4.2 + (i*0.5)%4;
                return (
                  <div key={t.code} style={{ display:'flex', alignItems:'center', gap:10 }}>
                    <div style={{ width:30, fontSize:11, fontWeight:700, color:'#475569' }}>{t.code}</div>
                    <div style={{ flex:1, height:18, background:'#F8FAFC', borderRadius:4, position:'relative', overflow:'hidden' }}>
                      <div style={{ width:`${(v/10)*100}%`, height:'100%', background: v>=7?'#10B981':v>=5?'#F59E0B':'#EF4444', borderRadius:4 }}/>
                      <div style={{ position:'absolute', left:'70%', top:0, bottom:0, borderLeft:'1.5px dashed #94A3B8' }}/>
                    </div>
                    <div style={{ fontSize:12, fontWeight:800, color:v>=7?'#10B981':v>=5?'#F59E0B':'#EF4444', width:30 }}>{v.toFixed(1)}</div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </APP_B>
  );
}

// ============ NOTAS B ============
function B_Notas() {
  const aluno = ALUNOS[6];
  const notas = [
    { m:'Português',  n:[9.0,8.5,9.2,9.7], med:9.1 },
    { m:'Matemática', n:[7.8,8.2,9.0,8.5], med:8.4 },
    { m:'Ciências',   n:[8.5,9.0,8.8,9.4], med:8.9 },
    { m:'História',   n:[9.2,9.5,9.0,9.6], med:9.3 },
    { m:'Geografia',  n:[7.5,8.0,8.4,8.8], med:8.2 },
    { m:'Inglês',     n:[9.8,9.4,9.6,9.9], med:9.7 },
    { m:'Arte',       n:[8.0,8.5,9.0,8.7], med:8.6 },
    { m:'Ed. Física', n:[9.5,9.0,9.2,9.4], med:9.3 },
    { m:'Física',     n:[6.5,7.0,7.8,8.0], med:7.3 },
    { m:'Química',    n:[5.8,6.5,6.8,7.5], med:6.7 },
  ];
  return (
    <APP_B sidebar="notas" breadcrumb="Lançamento / Notas" title="Notas" kicker="2º TRIMESTRE"
      headRight={<>
        <div style={{ padding:'7px 10px', background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:8, fontSize:12, fontWeight:600, color:'#475569', display:'flex', alignItems:'center', gap:6 }}>9º Fundamental {I.down({s:12})}</div>
        <div style={{ padding:'7px 10px', background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:8, fontSize:12, fontWeight:600, color:'#475569', display:'flex', alignItems:'center', gap:6 }}>Fernanda Pinto {I.down({s:12})}</div>
        <div style={{ padding:'7px 12px', background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:8, fontSize:12, fontWeight:700, color:'#4F46E5', display:'flex', alignItems:'center', gap:5 }}>{I.sparkle({s:14})} Aleatório</div>
        <div style={{ padding:'7px 12px', background:'#10B981', color:'#fff', borderRadius:8, fontSize:12, fontWeight:700, display:'flex', alignItems:'center', gap:5 }}>{I.check({s:14})} Salvar</div>
      </>}>
      <div style={{ display:'grid', gridTemplateColumns:'1fr 280px', gap:14, height:'100%' }}>
        {/* Notas grid */}
        <div style={{ background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:B_RADIUS, overflow:'hidden', display:'flex', flexDirection:'column' }}>
          <div style={{ display:'grid', gridTemplateColumns:'1.8fr repeat(4,1fr) 0.9fr 1.3fr', gap:0, fontSize:10.5, fontWeight:800, color:'#64748B', letterSpacing:'.06em', padding:'10px 14px', background:'#F8FAFC', borderBottom:`1px solid ${B_BORDER}` }}>
            <div>MATÉRIA</div><div>N1</div><div>N2</div><div>N3</div><div>N4</div><div>MÉDIA</div><div style={{ textAlign:'right' }}>STATUS</div>
          </div>
          <div style={{ flex:1, overflow:'auto' }}>
            {notas.map((r,i)=>{
              const map = [
                { bg:'#D1FAE5', fg:'#047857', lbl:'Aprovado' },
                { bg:'#FEF3C7', fg:'#92400E', lbl:'Recuperação' },
                { bg:'#FEE2E2', fg:'#B91C1C', lbl:'Reprovado' },
              ];
              const st = r.med>=7?0: r.med>=5?1:2;
              const s = map[st];
              return (
                <div key={i} style={{ display:'grid', gridTemplateColumns:'1.8fr repeat(4,1fr) 0.9fr 1.3fr', gap:0, alignItems:'center', padding:'10px 14px', borderBottom:`1px solid ${B_BORDER}`, fontSize:13, background: i===1?'#FAFBFF':'#fff' }}>
                  <div style={{ fontWeight:700 }}>{r.m}</div>
                  {r.n.map((v,k)=>(
                    <div key={k}>
                      <div style={{ display:'inline-block', padding:'3px 8px', borderRadius:5, background: v<5?'#FEF2F2':v<7?'#FFFBEB':'#F0FDF4', color: v<5?'#DC2626':v<7?'#D97706':'#059669', fontWeight:700, fontSize:12, minWidth:40, textAlign:'center' }}>{v.toFixed(1)}</div>
                    </div>
                  ))}
                  <div style={{ fontWeight:900, fontSize:14 }}>{r.med.toFixed(1)}</div>
                  <div style={{ textAlign:'right' }}><span style={{ fontSize:11, padding:'3px 8px', borderRadius:5, background:s.bg, color:s.fg, fontWeight:700 }}>● {s.lbl}</span></div>
                </div>
              );
            })}
          </div>
          <div style={{ padding:'10px 14px', borderTop:`1px solid ${B_BORDER}`, background:'#F8FAFC', display:'flex', alignItems:'center', gap:8 }}>
            <span style={{ fontSize:11, fontWeight:700, color:'#64748B' }}>Editar:</span>
            <span style={{ fontSize:12, fontWeight:700 }}>Matemática</span>
            {['N1','N2','N3','N4'].map((n,k)=>(
              <div key={n} style={{ display:'flex', alignItems:'center', gap:5 }}>
                <span style={{ fontSize:10, fontWeight:700, color:'#94A3B8' }}>{n}</span>
                <div style={{ width:54, padding:'4px 8px', background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:5, fontSize:12, fontWeight:700 }}>{[7.8,8.2,9.0,8.5][k].toFixed(1)}</div>
              </div>
            ))}
            <div style={{ flex:1 }}/>
            <div style={{ padding:'6px 12px', background:'#4F46E5', color:'#fff', borderRadius:6, fontSize:12, fontWeight:700 }}>Aplicar</div>
          </div>
        </div>

        {/* Student card */}
        <div style={{ display:'flex', flexDirection:'column', gap:10 }}>
          <div style={{ background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:B_RADIUS, padding:'14px', display:'flex', flexDirection:'column', alignItems:'center', gap:8 }}>
            <Avatar a={aluno} size={64}/>
            <div style={{ textAlign:'center' }}>
              <div style={{ fontSize:14, fontWeight:800 }}>{aluno.nome}</div>
              <div style={{ fontSize:11, color:'#94A3B8', fontWeight:600 }}>#{aluno.mat} • 9º Fundamental</div>
            </div>
            <div style={{ width:'100%', height:1, background:B_BORDER, margin:'4px 0' }}/>
            <div style={{ width:'100%', display:'grid', gridTemplateColumns:'1fr 1fr', gap:6 }}>
              <div style={{ padding:'8px', background:'#F8FAFC', borderRadius:6, textAlign:'center' }}>
                <div style={{ fontSize:18, fontWeight:800, color:'#10B981' }}>{aluno.media.toFixed(1)}</div>
                <div style={{ fontSize:10, color:'#64748B', fontWeight:700 }}>MÉDIA GERAL</div>
              </div>
              <div style={{ padding:'8px', background:'#F8FAFC', borderRadius:6, textAlign:'center' }}>
                <div style={{ fontSize:18, fontWeight:800, color:'#4F46E5' }}>Nv. {aluno.lvl}</div>
                <div style={{ fontSize:10, color:'#64748B', fontWeight:700 }}>{aluno.xp.toLocaleString()} XP</div>
              </div>
            </div>
          </div>

          <div style={{ background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:B_RADIUS, padding:'12px 14px' }}>
            <div style={{ fontSize:11, fontWeight:800, color:'#64748B', letterSpacing:'.06em', marginBottom:8 }}>STREAK & PROGRESSO</div>
            <div style={{ display:'flex', alignItems:'center', gap:8, padding:'8px 10px', background:'#FFF7ED', borderRadius:6, marginBottom:8 }}>
              <span style={{ color:'#F97316' }}>{I.fire({s:18})}</span>
              <div>
                <div style={{ fontSize:13, fontWeight:800, color:'#9A3412' }}>{aluno.streak} dias seguidos</div>
                <div style={{ fontSize:10, color:'#9A3412', fontWeight:600 }}>Próxima medalha: 35 dias</div>
              </div>
            </div>
            <div style={{ fontSize:10, color:'#94A3B8', fontWeight:700, marginBottom:4 }}>NV. {aluno.lvl} → {aluno.lvl+1}</div>
            <div style={{ height:6, background:'#F1F5F9', borderRadius:999, overflow:'hidden' }}>
              <div style={{ width:'68%', height:'100%', background:'#4F46E5' }}/>
            </div>
            <div style={{ fontSize:10, color:'#94A3B8', fontWeight:600, marginTop:4 }}>340 / 500 XP</div>
          </div>

          <div style={{ background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:B_RADIUS, padding:'12px 14px' }}>
            <div style={{ fontSize:11, fontWeight:800, color:'#64748B', letterSpacing:'.06em', marginBottom:8 }}>CONQUISTAS (6/12)</div>
            <div style={{ display:'grid', gridTemplateColumns:'repeat(6,1fr)', gap:5 }}>
              {[I.fire,I.star,I.shield,I.trophy,I.bolt,I.target,null,null,null,null,null,null].map((Ic,i)=>(
                Ic ? <div key={i} style={{ aspectRatio:'1', borderRadius:6, background:'#EEF2FF', color:'#4F46E5', display:'grid', placeItems:'center' }}>{Ic({s:14})}</div>
                   : <div key={i} style={{ aspectRatio:'1', borderRadius:6, background:'#F1F5F9', color:'#CBD5E1', display:'grid', placeItems:'center', fontSize:10 }}>?</div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </APP_B>
  );
}

// ============ PREDIÇÕES B ============
function B_Predicoes() {
  const preds = [
    { a:ALUNOS[7], dir:'down', conf:92, motivo:'Quedas consecutivas em Matemática e Física', mat:'Matemática' },
    { a:ALUNOS[3], dir:'down', conf:88, motivo:'Streak quebrada há 3 semanas', mat:'História' },
    { a:ALUNOS[1], dir:'up',   conf:81, motivo:'Recuperação consistente últimas 4 notas', mat:'Português' },
    { a:ALUNOS[9], dir:'flat', conf:74, motivo:'Estável em zona de recuperação', mat:'Química' },
    { a:ALUNOS[5], dir:'up',   conf:79, motivo:'Tendência positiva pós-intervenção', mat:'Inglês' },
    { a:ALUNOS[11], dir:'up',  conf:95, motivo:'Performance excelente, mantém ritmo', mat:'Geral' },
    { a:ALUNOS[0], dir:'up',   conf:84, motivo:'Variação positiva em todas as áreas', mat:'Geral' },
    { a:ALUNOS[4], dir:'up',   conf:90, motivo:'Próxima de subir 2 níveis', mat:'Ciências' },
  ];
  return (
    <APP_B sidebar="pred" breadcrumb="Inteligência Artificial / Predições" title="Predições de Desempenho" kicker="RF_M3 91.3%" subtitle="Identifique déficits no início do ano — análise por aluno com modelo RF_M3"
      headRight={<>
        <div style={{ padding:'7px 10px', background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:8, fontSize:12, fontWeight:600, color:'#475569', display:'flex', alignItems:'center', gap:6 }}>9º Fundamental {I.down({s:12})}</div>
        <div style={{ padding:'7px 10px', background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:8, fontSize:12, fontWeight:600, color:'#475569', display:'flex', alignItems:'center', gap:6 }}>Todos alunos {I.down({s:12})}</div>
        <div style={{ padding:'7px 12px', background:'#4F46E5', color:'#fff', borderRadius:8, fontSize:12, fontWeight:700, display:'flex', alignItems:'center', gap:5 }}>{I.sparkle({s:14})} Analisar</div>
      </>}>
      <div style={{ display:'grid', gridTemplateColumns:'2fr 1fr', gap:14, height:'100%' }}>
        <div style={{ display:'flex', flexDirection:'column', gap:12 }}>
          {/* Summary */}
          <div style={{ display:'grid', gridTemplateColumns:'repeat(5,1fr)', gap:8 }}>
            {[
              { l:'Total', v:202, c:'#0F172A' },
              { l:'Aprovados', v:154, c:'#10B981' },
              { l:'Recuperação', v:17, c:'#F59E0B' },
              { l:'Reprovados', v:31, c:'#EF4444' },
              { l:'Confiança média', v:'87%', c:'#4F46E5' },
            ].map((s,i)=>(
              <div key={i} style={{ background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:B_RADIUS, padding:'10px 12px' }}>
                <div style={{ fontSize:11, color:'#64748B', fontWeight:600 }}>{s.l}</div>
                <div style={{ fontSize:22, fontWeight:800, color:s.c, letterSpacing:'-0.02em', marginTop:2 }}>{s.v}</div>
              </div>
            ))}
          </div>

          {/* Filter chips */}
          <div style={{ display:'flex', gap:6, alignItems:'center' }}>
            <div style={{ fontSize:11, fontWeight:800, color:'#64748B', letterSpacing:'.06em' }}>FILTRO:</div>
            {['Todas','Aprovadas','Recuperação','Reprovadas','Vai melhorar','Vai piorar'].map((t,i)=>(
              <div key={t} style={{ padding:'5px 10px', borderRadius:6, fontSize:11, fontWeight:700, background: i===0?'#4F46E5':'#fff', color:i===0?'#fff':'#475569', border:`1px solid ${i===0?'#4F46E5':B_BORDER}` }}>{t}</div>
            ))}
          </div>

          {/* List */}
          <div style={{ flex:1, background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:B_RADIUS, overflow:'hidden', display:'flex', flexDirection:'column' }}>
            <div style={{ display:'grid', gridTemplateColumns:'2fr 1.2fr 0.9fr 1.4fr 0.6fr', gap:0, fontSize:10.5, fontWeight:800, color:'#64748B', letterSpacing:'.06em', padding:'10px 14px', background:'#F8FAFC', borderBottom:`1px solid ${B_BORDER}` }}>
              <div>ALUNO</div><div>FOCO</div><div>TENDÊNCIA</div><div>CONFIANÇA</div><div></div>
            </div>
            <div style={{ flex:1, overflow:'auto' }}>
              {preds.map((p,i)=>{
                const dirMap = {
                  up:   { ic:I.up,   c:'#059669', bg:'#D1FAE5', lbl:'Vai melhorar' },
                  down: { ic:I.down, c:'#DC2626', bg:'#FEE2E2', lbl:'Vai piorar' },
                  flat: { ic:I.target, c:'#D97706', bg:'#FEF3C7', lbl:'Estável' },
                };
                const d = dirMap[p.dir];
                return (
                  <div key={i} style={{ display:'grid', gridTemplateColumns:'2fr 1.2fr 0.9fr 1.4fr 0.6fr', gap:0, alignItems:'center', padding:'10px 14px', borderBottom:`1px solid ${B_BORDER}`, fontSize:13 }}>
                    <div style={{ display:'flex', alignItems:'center', gap:8 }}>
                      <Avatar a={p.a} size={30}/>
                      <div>
                        <div style={{ fontWeight:700 }}>{p.a.nome}</div>
                        <div style={{ fontSize:11, color:'#94A3B8', fontWeight:500 }}>{p.motivo}</div>
                      </div>
                    </div>
                    <div style={{ fontWeight:700, color:'#475569' }}>{p.mat}</div>
                    <div><span style={{ fontSize:11, padding:'3px 8px', borderRadius:5, background:d.bg, color:d.c, fontWeight:700, display:'inline-flex', alignItems:'center', gap:4 }}>{d.ic({s:12})} {d.lbl}</span></div>
                    <div style={{ display:'flex', alignItems:'center', gap:8 }}>
                      <div style={{ flex:1, height:6, background:'#F1F5F9', borderRadius:999, overflow:'hidden' }}>
                        <div style={{ width:`${p.conf}%`, height:'100%', background:d.c, borderRadius:999 }}/>
                      </div>
                      <span style={{ fontSize:11, fontWeight:800, color:d.c, width:32 }}>{p.conf}%</span>
                    </div>
                    <div style={{ textAlign:'right', color:'#94A3B8' }}>{I.chev({s:14})}</div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Right panel — what-if */}
        <div style={{ display:'flex', flexDirection:'column', gap:12 }}>
          <div style={{ background:'linear-gradient(135deg,#4F46E5,#7C3AED)', color:'#fff', borderRadius:B_RADIUS, padding:'14px 16px' }}>
            <div style={{ display:'flex', alignItems:'center', gap:8, marginBottom:6 }}>
              <span>{I.sparkle({s:14})}</span>
              <div style={{ fontSize:11, fontWeight:800, letterSpacing:'.08em' }}>INSIGHT DA IA</div>
            </div>
            <div style={{ fontSize:14, fontWeight:700, lineHeight:1.4 }}>8 dos 12 alunos previstos para piorar podem ser recuperados com 2 semanas de reforço em Matemática.</div>
            <div style={{ fontSize:11, opacity:.8, marginTop:6, fontWeight:600 }}>Baseado em padrões históricos de 3 turmas anteriores</div>
          </div>

          <div style={{ background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:B_RADIUS, padding:'14px 16px', flex:1 }}>
            <div style={{ fontSize:13, fontWeight:800, marginBottom:10 }}>Distribuição de confiança</div>
            <div style={{ display:'flex', alignItems:'flex-end', gap:6, height:110, marginBottom:10 }}>
              {[5,8,12,18,24,31,42,38,25,18,12].map((v,i)=>(
                <div key={i} style={{ flex:1, height:`${(v/42)*100}%`, background: i>=8?'#10B981':i>=5?'#4F46E5':'#EF4444', borderRadius:'2px 2px 0 0' }}/>
              ))}
            </div>
            <div style={{ display:'flex', justifyContent:'space-between', fontSize:10, color:'#94A3B8', fontWeight:600 }}>
              <span>50%</span><span>70%</span><span>90%</span><span>100%</span>
            </div>
            <div style={{ height:1, background:B_BORDER, margin:'14px 0' }}/>
            <div style={{ fontSize:11, fontWeight:800, color:'#64748B', letterSpacing:'.06em', marginBottom:8 }}>FATORES DE RISCO</div>
            {[
              { l:'Streak quebrada', v:62 },
              { l:'Queda em 2+ matérias', v:48 },
              { l:'Notas < 5 em N3-N4', v:54 },
              { l:'Frequência baixa', v:31 },
            ].map(f=>(
              <div key={f.l} style={{ marginBottom:8 }}>
                <div style={{ display:'flex', justifyContent:'space-between', fontSize:11, marginBottom:3 }}>
                  <span style={{ fontWeight:600, color:'#475569' }}>{f.l}</span>
                  <span style={{ fontWeight:800 }}>{f.v}%</span>
                </div>
                <div style={{ height:5, background:'#F1F5F9', borderRadius:999, overflow:'hidden' }}>
                  <div style={{ width:`${f.v}%`, height:'100%', background:'#4F46E5' }}/>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </APP_B>
  );
}

// ============ RELATÓRIO B ============
function B_Relatorio() {
  const rows = [];
  let seed = 7;
  const rand = () => { seed = (seed*9301+49297)%233280; return seed/233280; };
  ALUNOS.slice(0,7).forEach(a=>{
    MATERIAS.slice(0,4).forEach(m=>{
      const n = [3+rand()*7, 3+rand()*7, 3+rand()*7, 3+rand()*7].map(v=>Math.round(v*10)/10);
      const med = n.reduce((s,v)=>s+v,0)/4;
      const st = med>=7?0: med>=5?1:2;
      rows.push({ a, m, n, med, st });
    });
  });
  return (
    <APP_B sidebar="rel" breadcrumb="Análise / Relatório" title="Relatório completo" kicker="1.846 NOTAS"
      headRight={<>
        <div style={{ padding:'7px 10px', background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:8, fontSize:12, fontWeight:600, color:'#475569', display:'flex', alignItems:'center', gap:6 }}>Filtrar por turma: Todas {I.down({s:12})}</div>
        <div style={{ padding:'7px 12px', background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:8, fontSize:12, fontWeight:700, color:'#475569', display:'flex', alignItems:'center', gap:5 }}>{I.download({s:14})} Excel</div>
        <div style={{ padding:'7px 12px', background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:8, fontSize:12, fontWeight:700, color:'#475569', display:'flex', alignItems:'center', gap:5 }}>{I.download({s:14})} PDF</div>
        <div style={{ padding:'7px 12px', background:'#4F46E5', color:'#fff', borderRadius:8, fontSize:12, fontWeight:700, display:'flex', alignItems:'center', gap:5 }}>Atualizar</div>
      </>}>
      <div style={{ background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:B_RADIUS, height:'100%', overflow:'hidden', display:'flex', flexDirection:'column' }}>
        <div style={{ display:'grid', gridTemplateColumns:'1.6fr 0.6fr 1.2fr repeat(4,0.6fr) 0.7fr 1.1fr', gap:0, fontSize:10.5, fontWeight:800, color:'#64748B', letterSpacing:'.06em', padding:'10px 14px', background:'#F8FAFC', borderBottom:`1px solid ${B_BORDER}` }}>
          <div>ALUNO</div><div>TURMA</div><div>MATÉRIA</div><div>N1</div><div>N2</div><div>N3</div><div>N4</div><div>MÉDIA</div><div style={{ textAlign:'right' }}>STATUS</div>
        </div>
        <div style={{ flex:1, overflow:'auto' }}>
          {rows.map((r,i)=>{
            const map = [
              { bg:'#D1FAE5', fg:'#047857', lbl:'Aprovado', accent:'#10B981' },
              { bg:'#FEF3C7', fg:'#92400E', lbl:'Recuperação', accent:'#F59E0B' },
              { bg:'#FEE2E2', fg:'#B91C1C', lbl:'Reprovado', accent:'#EF4444' },
            ];
            const s = map[r.st];
            return (
              <div key={i} style={{ display:'grid', gridTemplateColumns:'1.6fr 0.6fr 1.2fr repeat(4,0.6fr) 0.7fr 1.1fr', gap:0, alignItems:'center', padding:'8px 14px', borderBottom:`1px solid ${B_BORDER}`, fontSize:13, borderLeft:`3px solid ${s.accent}` }}>
                <div style={{ display:'flex', alignItems:'center', gap:8 }}>
                  <Avatar a={r.a} size={24}/>
                  <span style={{ fontWeight:600 }}>{r.a.nome}</span>
                </div>
                <div style={{ color:'#64748B', fontWeight:600, fontSize:12 }}>{r.a.turma}</div>
                <div style={{ fontWeight:600 }}>{r.m}</div>
                {r.n.map((v,k)=>(
                  <div key={k} style={{ fontWeight:700, color: v<5?'#EF4444':v<7?'#F59E0B':'#10B981' }}>{v.toFixed(1)}</div>
                ))}
                <div style={{ fontWeight:900 }}>{r.med.toFixed(1)}</div>
                <div style={{ textAlign:'right' }}><span style={{ fontSize:11, padding:'3px 8px', borderRadius:5, background:s.bg, color:s.fg, fontWeight:700 }}>{s.lbl}</span></div>
              </div>
            );
          })}
        </div>
        <div style={{ padding:'10px 14px', borderTop:`1px solid ${B_BORDER}`, display:'flex', alignItems:'center', justifyContent:'space-between', fontSize:12, color:'#64748B', background:'#F8FAFC' }}>
          <div>Mostrando 28 de 1.846 notas</div>
          <div style={{ display:'flex', gap:14, fontWeight:600 }}>
            <span><span style={{ display:'inline-block', width:8, height:8, background:'#10B981', borderRadius:2, marginRight:4 }}/>Aprov: 76,2%</span>
            <span><span style={{ display:'inline-block', width:8, height:8, background:'#F59E0B', borderRadius:2, marginRight:4 }}/>Rec: 17,1%</span>
            <span><span style={{ display:'inline-block', width:8, height:8, background:'#EF4444', borderRadius:2, marginRight:4 }}/>Repr: 6,7%</span>
          </div>
        </div>
      </div>
    </APP_B>
  );
}

// ============ ML B ============
function B_ML() {
  const models = [
    { name:'RF_M1', desc:'100 árvores, profundidade 5', acc:85.2, date:'20/05 19:23', active:false },
    { name:'RF_M2', desc:'150 árvores, profundidade 10', acc:90.4, date:'20/05 19:23', active:false },
    { name:'RF_M3', desc:'200 árvores, profundidade 15', acc:91.3, date:'20/05 19:24', active:true },
  ];
  return (
    <APP_B sidebar="ml" breadcrumb="IA Avançada / Machine Learning" title="Machine Learning" kicker="3 MODELOS"
      headRight={<>
        <div style={{ padding:'7px 12px', background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:8, fontSize:12, fontWeight:700, color:'#475569', display:'flex', alignItems:'center', gap:5 }}>{I.sparkle({s:14})} Gerar features</div>
        <div style={{ padding:'7px 12px', background:'#10B981', color:'#fff', borderRadius:8, fontSize:12, fontWeight:700, display:'flex', alignItems:'center', gap:5 }}>▶ Treinar todos</div>
        <div style={{ padding:'7px 12px', background:'#4F46E5', color:'#fff', borderRadius:8, fontSize:12, fontWeight:700, display:'flex', alignItems:'center', gap:5 }}>▶ Treinar RF_M3</div>
      </>}>
      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr 1fr', gridTemplateRows:'auto 1fr', gap:12, height:'100%' }}>
        {/* Models */}
        {models.map((m,i)=>(
          <div key={m.name} style={{ background:'#fff', border:`1px solid ${m.active?'#10B981':B_BORDER}`, borderRadius:B_RADIUS, padding:'12px 14px', position:'relative' }}>
            {m.active && <div style={{ position:'absolute', top:10, right:10, fontSize:9, padding:'2px 7px', borderRadius:4, background:'#D1FAE5', color:'#047857', fontWeight:800, letterSpacing:'.04em' }}>● PRODUÇÃO</div>}
            <div style={{ display:'flex', alignItems:'center', gap:8 }}>
              <div style={{ width:32, height:32, borderRadius:7, background:'#EEF2FF', color:'#4F46E5', display:'grid', placeItems:'center' }}>{I.brain({s:16})}</div>
              <div>
                <div style={{ fontSize:14, fontWeight:800 }}>{m.name}</div>
                <div style={{ fontSize:10, color:'#94A3B8', fontWeight:600 }}>{m.desc}</div>
              </div>
            </div>
            <div style={{ display:'flex', alignItems:'baseline', gap:6, marginTop:8 }}>
              <div style={{ fontSize:28, fontWeight:800, color: m.active?'#10B981':'#0F172A', letterSpacing:'-0.02em', lineHeight:1 }}>{m.acc}%</div>
              <div style={{ fontSize:10, color:'#94A3B8', fontWeight:600 }}>acurácia</div>
            </div>
            <div style={{ marginTop:8, height:5, background:'#F1F5F9', borderRadius:999, overflow:'hidden' }}>
              <div style={{ width:`${m.acc}%`, height:'100%', background:m.active?'#10B981':'#4F46E5', borderRadius:999 }}/>
            </div>
            <div style={{ fontSize:10, color:'#94A3B8', marginTop:6, fontWeight:600 }}>Última atualização: {m.date}</div>
          </div>
        ))}

        {/* Training console */}
        <div style={{ gridColumn:'span 2', background:'#0F172A', borderRadius:B_RADIUS, padding:'14px 16px', color:'#E2E8F0', display:'flex', flexDirection:'column', gap:8, overflow:'hidden', minHeight:0 }}>
          <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between' }}>
            <div style={{ display:'flex', alignItems:'center', gap:8 }}>
              <span style={{ color:'#34D399' }}>●</span>
              <div style={{ fontSize:13, fontWeight:800, color:'#fff' }}>Console de treinamento</div>
            </div>
            <div style={{ fontSize:10, color:'#64748B', fontWeight:600 }}>RF_M3 • 200 árvores • Acurácia parcial: 91.3%</div>
          </div>
          <div style={{ flex:1, fontFamily:"'JetBrains Mono', monospace", fontSize:11, lineHeight:1.7, overflow:'auto', background:'rgba(0,0,0,.3)', borderRadius:6, padding:'12px' }}>
            <div style={{ color:'#94A3B8' }}>[19:23:01] <span style={{ color:'#34D399' }}>INFO</span> Carregando 1.846 amostras de notas...</div>
            <div style={{ color:'#94A3B8' }}>[19:23:03] <span style={{ color:'#34D399' }}>INFO</span> Features geradas: 12 dimensões</div>
            <div style={{ color:'#94A3B8' }}>[19:23:05] <span style={{ color:'#34D399' }}>INFO</span> Treinando RF_M1 (100 árvores)...</div>
            <div style={{ color:'#94A3B8' }}>[19:23:18] <span style={{ color:'#FBBF24' }}>OK</span>   RF_M1 concluído — acurácia <span style={{ color:'#FBBF24' }}>85.2%</span></div>
            <div style={{ color:'#94A3B8' }}>[19:23:19] <span style={{ color:'#34D399' }}>INFO</span> Treinando RF_M2 (150 árvores)...</div>
            <div style={{ color:'#94A3B8' }}>[19:23:42] <span style={{ color:'#FBBF24' }}>OK</span>   RF_M2 concluído — acurácia <span style={{ color:'#FBBF24' }}>90.4%</span></div>
            <div style={{ color:'#94A3B8' }}>[19:23:43] <span style={{ color:'#34D399' }}>INFO</span> Treinando RF_M3 (200 árvores) — produção...</div>
            <div style={{ color:'#94A3B8' }}>[19:24:00] <span style={{ color:'#34D399' }}>DONE</span> RF_M3 — acurácia <span style={{ color:'#34D399' }}>91.3%</span> ✓ promovido para produção</div>
            <div style={{ color:'#34D399', marginTop:8 }}>━━━━━━━━━━━━━━━━━━━━━━━━━━</div>
            <div style={{ color:'#34D399' }}>✓ Treinamento concluído em 1m 59s</div>
            <div style={{ color:'#94A3B8', marginTop:4 }}>_</div>
          </div>
          <div style={{ height:6, background:'#1E293B', borderRadius:999, overflow:'hidden' }}>
            <div style={{ width:'100%', height:'100%', background:'linear-gradient(90deg,#4F46E5,#10B981)' }}/>
          </div>
        </div>

        {/* Feature importance */}
        <div style={{ background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:B_RADIUS, padding:'14px 16px', overflow:'hidden' }}>
          <div style={{ fontSize:13, fontWeight:800, marginBottom:10 }}>Importância das features</div>
          {[
            { l:'Média anterior', v:34, c:'#4F46E5' },
            { l:'Streak', v:22, c:'#F97316' },
            { l:'Variação trim.', v:18, c:'#0EA5E9' },
            { l:'Frequência', v:14, c:'#10B981' },
            { l:'Idade × série', v:8, c:'#EC4899' },
            { l:'Outros', v:4, c:'#94A3B8' },
          ].map(f=>(
            <div key={f.l} style={{ marginBottom:9 }}>
              <div style={{ display:'flex', justifyContent:'space-between', fontSize:11, marginBottom:3 }}>
                <span style={{ fontWeight:600, color:'#475569' }}>{f.l}</span>
                <span style={{ fontWeight:800, color:f.c }}>{f.v}%</span>
              </div>
              <div style={{ height:6, background:'#F1F5F9', borderRadius:999, overflow:'hidden' }}>
                <div style={{ width:`${f.v*2.8}%`, height:'100%', background:f.c, borderRadius:999 }}/>
              </div>
            </div>
          ))}
        </div>

        {/* Analyze panel */}
        <div style={{ gridColumn:'span 2', background:'#fff', border:`1px solid ${B_BORDER}`, borderRadius:B_RADIUS, padding:'14px 16px' }}>
          <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between', marginBottom:10 }}>
            <div>
              <div style={{ fontSize:13, fontWeight:800 }}>Analisar decisão do modelo</div>
              <div style={{ fontSize:11, color:'#94A3B8', fontWeight:600 }}>Entenda os fatores por trás de uma predição</div>
            </div>
            <div style={{ display:'flex', gap:6 }}>
              <div style={{ padding:'6px 10px', background:'#F1F5F9', borderRadius:6, fontSize:12, fontWeight:700, display:'flex', alignItems:'center', gap:4 }}>Gabriel Sá {I.down({s:11})}</div>
              <div style={{ padding:'6px 10px', background:'#F1F5F9', borderRadius:6, fontSize:12, fontWeight:700, display:'flex', alignItems:'center', gap:4 }}>Matemática {I.down({s:11})}</div>
              <div style={{ padding:'6px 12px', background:'#4F46E5', color:'#fff', borderRadius:6, fontSize:12, fontWeight:700 }}>{I.search({s:12})} Analisar</div>
            </div>
          </div>
          <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:10 }}>
            <div style={{ padding:'12px', background:'#FEF2F2', border:'1px solid #FECACA', borderRadius:8 }}>
              <div style={{ fontSize:10, fontWeight:800, color:'#B91C1C', letterSpacing:'.08em' }}>PREDIÇÃO</div>
              <div style={{ fontSize:18, fontWeight:800, color:'#B91C1C', marginTop:2 }}>Vai piorar</div>
              <div style={{ fontSize:11, color:'#B91C1C', fontWeight:600, marginTop:2 }}>Confiança 92% • Tendência -1.4 pontos</div>
            </div>
            <div style={{ padding:'12px', background:'#F8FAFC', borderRadius:8 }}>
              <div style={{ fontSize:10, fontWeight:800, color:'#64748B', letterSpacing:'.08em' }}>FATORES DE MAIOR PESO</div>
              <div style={{ fontSize:12, marginTop:4, color:'#0F172A', fontWeight:600 }}>↓ Média 3.9 (−2.4σ) • Streak quebrada • N4 caiu 31%</div>
              <div style={{ fontSize:11, color:'#10B981', fontWeight:700, marginTop:4 }}>↑ Português positivo (+1.1)</div>
            </div>
          </div>
        </div>
      </div>
    </APP_B>
  );
}

window.B_Dashboard = B_Dashboard;
window.B_Alunos = B_Alunos;
window.B_Salas = B_Salas;
window.B_Materias = B_Materias;
window.B_Notas = B_Notas;
window.B_Predicoes = B_Predicoes;
window.B_Relatorio = B_Relatorio;
window.B_ML = B_ML;
