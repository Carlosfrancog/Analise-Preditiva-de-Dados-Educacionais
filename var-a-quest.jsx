// Variation A — QUEST (Duolingo-inspired, vibrant, playful gamification)

const A_FONT = "'Nunito', 'Plus Jakarta Sans', system-ui, sans-serif";
const A_BG = '#FAF7F2';
const A_INK = '#1B1D2A';
const A_RADIUS = 18;
const A_SHADOW = '0 1px 0 rgba(15,23,42,.04), 0 8px 24px -12px rgba(15,23,42,.12)';
const A_CARD = '#FFFFFF';
const A_BORDER = '#E8E4DA';

function APP_A({ children, sidebar='dash', expanded=true, title, subtitle, kicker, headRight }) {
  const navItems = [
    { id:'dash',   label:'Dashboard',    icon: I.home, color:'#4F46E5' },
    { id:'alunos', label:'Alunos',       icon: I.users, color:'#EC4899' },
    { id:'salas',  label:'Salas/Turmas', icon: I.school, color:'#F97316' },
    { id:'mat',    label:'Matérias',     icon: I.book, color:'#0EA5E9' },
    { id:'notas',  label:'Notas',        icon: I.edit, color:'#8B5CF6' },
    { id:'pred',   label:'Predições',    icon: I.target, color:'#10B981' },
    { id:'rel',    label:'Relatório',    icon: I.chart, color:'#FBBF24' },
    { id:'ml',     label:'Machine Learning', icon: I.brain, color:'#06B6D4' },
  ];
  const ioItems = [
    { id:'imp', label:'Importar Excel', icon: I.upload },
    { id:'exp', label:'Exportar Excel', icon: I.download },
  ];
  const sbW = expanded ? 248 : 84;
  return (
    <div style={{ width:1280, height:860, background:A_BG, fontFamily:A_FONT, color:A_INK, display:'flex', overflow:'hidden', borderRadius:14 }}>
      {/* Sidebar */}
      <aside style={{ width:sbW, background:'#fff', borderRight:`1px solid ${A_BORDER}`, padding:'18px 14px', display:'flex', flexDirection:'column', gap:6, transition:'width .2s' }}>
        <div style={{ display:'flex', alignItems:'center', gap:10, padding:'4px 6px 14px' }}>
          <div style={{ width:40, height:40, borderRadius:12, background:'linear-gradient(135deg,#4F46E5,#8B5CF6)', display:'grid', placeItems:'center', color:'#fff', boxShadow:'0 4px 12px -2px rgba(79,70,229,.4)' }}>
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M4 6h11a3 3 0 0 1 3 3v11H7a3 3 0 0 1-3-3z"/><path d="M14 2v6h6"/></svg>
          </div>
          {expanded && (
            <div>
              <div style={{ fontSize:18, fontWeight:900, letterSpacing:'-0.02em' }}>EduNotas</div>
              <div style={{ fontSize:11, color:'#94A3B8', fontWeight:600, marginTop:-2 }}>Sistema Escolar</div>
            </div>
          )}
        </div>

        <div style={{ display:'flex', flexDirection:'column', gap:2, marginTop:4 }}>
          {navItems.map(it=>{
            const active = it.id===sidebar;
            return (
              <div key={it.id} style={{
                display:'flex', alignItems:'center', gap:12, padding: expanded?'10px 12px':'10px', borderRadius:12,
                background: active ? '#F1F0FF' : 'transparent', color: active ? it.color : '#475569', fontWeight:700, fontSize:14, position:'relative', justifyContent: expanded?'flex-start':'center'
              }}>
                {active && <span style={{ position:'absolute', left:-14, top:8, bottom:8, width:4, background:it.color, borderRadius:'0 4px 4px 0' }}/>}
                <span style={{ width:32, height:32, borderRadius:10, background: active ? it.color : '#F1F5F9', color: active ? '#fff' : '#64748B', display:'grid', placeItems:'center', flexShrink:0 }}>{it.icon({s:18})}</span>
                {expanded && <span>{it.label}</span>}
              </div>
            );
          })}
        </div>

        <div style={{ height:1, background:A_BORDER, margin:'14px 4px' }}/>
        {expanded && <div style={{ fontSize:10, color:'#94A3B8', fontWeight:800, letterSpacing:'.1em', padding:'2px 12px' }}>DADOS</div>}
        {ioItems.map(it=>(
          <div key={it.id} style={{ display:'flex', alignItems:'center', gap:12, padding: expanded?'8px 12px':'8px', borderRadius:10, color:'#64748B', fontWeight:600, fontSize:13, justifyContent: expanded?'flex-start':'center' }}>
            <span style={{ width:28, height:28, display:'grid', placeItems:'center' }}>{it.icon({s:16})}</span>
            {expanded && <span>{it.label}</span>}
          </div>
        ))}

        <div style={{ flex:1 }}/>
        {expanded && (
          <div style={{ background:'linear-gradient(135deg,#FEF3C7,#FED7AA)', padding:'12px 14px', borderRadius:14, position:'relative', overflow:'hidden' }}>
            <div style={{ position:'absolute', right:-10, top:-10, opacity:.3 }}>{I.sparkle({s:54})}</div>
            <div style={{ fontSize:11, fontWeight:800, color:'#9A3412', letterSpacing:'.08em' }}>SEMANA 14</div>
            <div style={{ fontSize:15, fontWeight:900, color:'#7C2D12', marginTop:2 }}>2º Trimestre</div>
            <div style={{ fontSize:11, color:'#9A3412', marginTop:2, fontWeight:600 }}>42 dias restantes</div>
          </div>
        )}
      </aside>

      {/* Main */}
      <main style={{ flex:1, display:'flex', flexDirection:'column', minWidth:0 }}>
        {/* Topbar */}
        <header style={{ display:'flex', alignItems:'center', gap:14, padding:'18px 28px', borderBottom:`1px solid ${A_BORDER}`, background:'#fff' }}>
          <div style={{ width:36, height:36, borderRadius:10, background:'#F1F5F9', display:'grid', placeItems:'center', color:'#475569' }}>{I.menu({s:18})}</div>
          <div style={{ flex:1 }}>
            {kicker && <div style={{ fontSize:11, fontWeight:800, color:'#94A3B8', letterSpacing:'.12em' }}>{kicker}</div>}
            <div style={{ fontSize:22, fontWeight:900, letterSpacing:'-0.02em', lineHeight:1.1 }}>{title}</div>
            {subtitle && <div style={{ fontSize:13, color:'#64748B', marginTop:2, fontWeight:500 }}>{subtitle}</div>}
          </div>
          <div style={{ display:'flex', alignItems:'center', gap:10 }}>
            {headRight}
            <div style={{ width:38, height:38, borderRadius:10, background:'#F1F5F9', display:'grid', placeItems:'center', color:'#475569', position:'relative' }}>
              {I.bell({s:18})}
              <span style={{ position:'absolute', top:6, right:6, width:9, height:9, borderRadius:'50%', background:'#EF4444', border:'2px solid #fff' }}/>
            </div>
            <div style={{ display:'flex', alignItems:'center', gap:10, padding:'6px 12px 6px 6px', background:'#F1F5F9', borderRadius:999 }}>
              <div style={{ width:30, height:30, borderRadius:'50%', background:'linear-gradient(135deg,#8B5CF6,#EC4899)', display:'grid', placeItems:'center', color:'#fff', fontWeight:800, fontSize:12 }}>MR</div>
              <div style={{ fontSize:13, fontWeight:700 }}>Profa. Mariana</div>
            </div>
          </div>
        </header>
        <div style={{ flex:1, overflow:'hidden' }}>{children}</div>
      </main>
    </div>
  );
}

// ============ DASHBOARD A ============
function A_Dashboard() {
  return (
    <APP_A sidebar="dash" kicker="VISÃO GERAL" title="Olá, Mariana 👋" subtitle="Sua escola tem 31 alunos em risco esta semana — vamos ajudá-los a subir.">
      <div style={{ padding:'22px 28px', display:'flex', flexDirection:'column', gap:18, height:'100%', overflow:'hidden' }}>
        {/* KPI row */}
        <div style={{ display:'grid', gridTemplateColumns:'1.4fr 1fr 1fr 1fr', gap:14 }}>
          {/* Hero KPI: Em risco */}
          <div style={{ background:'linear-gradient(135deg,#EF4444 0%,#F97316 100%)', borderRadius:A_RADIUS, padding:'18px 20px', color:'#fff', position:'relative', overflow:'hidden' }}>
            <div style={{ position:'absolute', right:-30, bottom:-30, opacity:.12 }}>{I.warn({s:140})}</div>
            <div style={{ display:'flex', alignItems:'center', gap:8, fontSize:12, fontWeight:800, letterSpacing:'.08em', opacity:.95 }}>{I.warn({s:14})}ALUNOS EM RISCO</div>
            <div style={{ display:'flex', alignItems:'baseline', gap:10, marginTop:6 }}>
              <div style={{ fontSize:46, fontWeight:900, letterSpacing:'-0.04em', lineHeight:1 }}>31</div>
              <div style={{ display:'flex', alignItems:'center', gap:3, background:'rgba(255,255,255,.18)', padding:'4px 8px', borderRadius:999, fontSize:11, fontWeight:800 }}>{I.up({s:12})} +4 vs semana 13</div>
            </div>
            <div style={{ marginTop:10, fontSize:12, opacity:.95, fontWeight:600 }}>Modelo RF_M3 — 91.3% acurácia</div>
          </div>
          {[
            { lbl:'Alunos',  val:202, sub:'7 turmas',    icon:I.users, color:'#4F46E5', bg:'#EEF2FF', spark:[18,21,19,24,28,26,31] },
            { lbl:'Matérias',val:13,  sub:'+1 este mês', icon:I.book,  color:'#0EA5E9', bg:'#E0F2FE', spark:[10,10,11,12,12,13,13] },
            { lbl:'Notas',   val:1846,sub:'87% lançadas',icon:I.edit,  color:'#10B981', bg:'#D1FAE5', spark:[120,180,210,260,300,340,420] },
          ].map((k,i)=>(
            <div key={i} style={{ background:A_CARD, border:`1px solid ${A_BORDER}`, borderRadius:A_RADIUS, padding:'14px 16px' }}>
              <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between' }}>
                <span style={{ width:34, height:34, borderRadius:10, background:k.bg, color:k.color, display:'grid', placeItems:'center' }}>{k.icon({s:18})}</span>
                <div style={{ width:60 }}><SparkBar data={k.spark} color={k.color} h={26}/></div>
              </div>
              <div style={{ fontSize:28, fontWeight:900, letterSpacing:'-0.03em', marginTop:8, lineHeight:1 }}>{k.val.toLocaleString('pt-BR')}</div>
              <div style={{ display:'flex', justifyContent:'space-between', marginTop:4 }}>
                <span style={{ fontSize:12, color:'#475569', fontWeight:700 }}>{k.lbl}</span>
                <span style={{ fontSize:11, color:'#94A3B8', fontWeight:600 }}>{k.sub}</span>
              </div>
            </div>
          ))}
        </div>

        {/* Two columns */}
        <div style={{ display:'grid', gridTemplateColumns:'1.6fr 1fr', gap:16, flex:1, minHeight:0 }}>
          {/* Turmas chart */}
          <div style={{ background:A_CARD, border:`1px solid ${A_BORDER}`, borderRadius:A_RADIUS, padding:'18px 20px', display:'flex', flexDirection:'column' }}>
            <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between', marginBottom:12 }}>
              <div>
                <div style={{ fontSize:15, fontWeight:900 }}>Alunos por Turma</div>
                <div style={{ fontSize:12, color:'#94A3B8', fontWeight:600 }}>Verde: aprovados • Vermelho: em risco</div>
              </div>
              <div style={{ display:'flex', gap:6 }}>
                {['7 dias','30 dias','Trimestre'].map((t,i)=>(
                  <div key={t} style={{ fontSize:11, fontWeight:700, padding:'5px 10px', borderRadius:8, background: i===2?'#1B1D2A':'#F1F5F9', color: i===2?'#fff':'#64748B' }}>{t}</div>
                ))}
              </div>
            </div>
            <div style={{ flex:1, display:'flex', alignItems:'flex-end', gap:18, padding:'10px 0 4px' }}>
              {TURMAS.map((t,i)=>{
                const total = t.qtd;
                const ok = total - t.risco;
                const h = 200;
                return (
                  <div key={t.code} style={{ flex:1, display:'flex', flexDirection:'column', alignItems:'center', gap:6 }}>
                    <div style={{ fontSize:11, color:'#475569', fontWeight:700 }}>{total}</div>
                    <div style={{ width:'100%', height:h, display:'flex', flexDirection:'column', justifyContent:'flex-end', borderRadius:10, overflow:'hidden', background:'#F8FAFC' }}>
                      <div style={{ height:`${(t.risco/35)*h}px`, background:'linear-gradient(180deg,#FB7185,#EF4444)' }}/>
                      <div style={{ height:`${(ok/35)*h}px`, background:'linear-gradient(180deg,#34D399,#10B981)' }}/>
                    </div>
                    <div style={{ fontSize:11, color:'#1B1D2A', fontWeight:800 }}>{t.code}</div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Ranking */}
          <div style={{ background:A_CARD, border:`1px solid ${A_BORDER}`, borderRadius:A_RADIUS, padding:'18px 20px', display:'flex', flexDirection:'column' }}>
            <div style={{ display:'flex', alignItems:'center', gap:8, marginBottom:12 }}>
              <span style={{ width:30, height:30, borderRadius:8, background:'#FEF3C7', color:'#D97706', display:'grid', placeItems:'center' }}>{I.trophy({s:18})}</span>
              <div>
                <div style={{ fontSize:15, fontWeight:900 }}>Top Alunos</div>
                <div style={{ fontSize:11, color:'#94A3B8', fontWeight:600 }}>Ranking semanal por XP</div>
              </div>
            </div>
            <div style={{ flex:1, display:'flex', flexDirection:'column', gap:8 }}>
              {ALUNOS.filter(a=>a.status==='on').sort((a,b)=>b.xp-a.xp).slice(0,5).map((a,i)=>{
                const medal = ['#FBBF24','#94A3B8','#D97706'][i];
                return (
                  <div key={a.mat} style={{ display:'flex', alignItems:'center', gap:10, padding:'8px 10px', borderRadius:12, background: i<3?'#FFFBEB':'#F8FAFC' }}>
                    <div style={{ width:24, height:24, borderRadius:'50%', background: medal || '#E2E8F0', color:'#fff', display:'grid', placeItems:'center', fontWeight:900, fontSize:12 }}>{i+1}</div>
                    <Avatar a={a} size={32} ring ringColor="#FBBF24"/>
                    <div style={{ flex:1, minWidth:0 }}>
                      <div style={{ fontSize:13, fontWeight:800, whiteSpace:'nowrap', overflow:'hidden', textOverflow:'ellipsis' }}>{a.nome}</div>
                      <div style={{ fontSize:11, color:'#94A3B8', fontWeight:600 }}>Nv. {a.lvl} • {a.turma}</div>
                    </div>
                    <div style={{ textAlign:'right' }}>
                      <div style={{ fontSize:13, fontWeight:900, color:'#D97706' }}>{a.xp.toLocaleString()}</div>
                      <div style={{ fontSize:10, color:'#94A3B8', fontWeight:700 }}>XP</div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* AI predictions strip */}
        <div style={{ background:'linear-gradient(135deg,#1B1D2A 0%,#312E81 100%)', borderRadius:A_RADIUS, padding:'16px 20px', color:'#fff', display:'flex', alignItems:'center', gap:18 }}>
          <div style={{ width:46, height:46, borderRadius:12, background:'rgba(255,255,255,.12)', display:'grid', placeItems:'center', color:'#A5B4FC' }}>{I.brain({s:24})}</div>
          <div style={{ flex:1 }}>
            <div style={{ display:'flex', alignItems:'center', gap:8 }}>
              <div style={{ fontSize:11, fontWeight:800, letterSpacing:'.1em', color:'#A5B4FC' }}>PREVISÃO IA</div>
              <div style={{ fontSize:10, padding:'2px 8px', background:'rgba(16,185,129,.2)', color:'#34D399', borderRadius:999, fontWeight:800 }}>● ATIVO</div>
            </div>
            <div style={{ fontSize:15, fontWeight:700, marginTop:2 }}>12 alunos vão piorar nas próximas 2 semanas — 8 podem se recuperar com intervenção em Matemática.</div>
          </div>
          <div style={{ background:'#fff', color:'#1B1D2A', padding:'10px 16px', borderRadius:12, fontWeight:800, fontSize:13, display:'flex', alignItems:'center', gap:6 }}>Ver predições {I.chev({s:14})}</div>
        </div>
      </div>
    </APP_A>
  );
}

// ============ ALUNOS A ============
function A_Alunos() {
  const list = [...ALUNOS];
  return (
    <APP_A sidebar="alunos" kicker="GESTÃO" title="Alunos" subtitle="202 alunos cadastrados • 12 visíveis"
      headRight={<>
        <div style={{ display:'flex', alignItems:'center', gap:8, padding:'8px 12px', background:'#F1F5F9', borderRadius:10, fontSize:13, fontWeight:600, color:'#475569', width:220 }}>{I.search({s:16})} Buscar aluno...</div>
        <div style={{ background:'#1B1D2A', color:'#fff', padding:'9px 14px', borderRadius:10, fontWeight:800, fontSize:13, display:'flex', alignItems:'center', gap:6 }}>{I.plus({s:16})} Novo aluno</div>
      </>}>
      <div style={{ padding:'18px 28px', height:'100%', display:'flex', flexDirection:'column', gap:14 }}>
        {/* Filters */}
        <div style={{ display:'flex', alignItems:'center', gap:8, flexWrap:'wrap' }}>
          {['Todas','6F','7F','8F','9F','1M','2M','3M'].map((t,i)=>(
            <div key={t} style={{ padding:'7px 14px', borderRadius:999, fontSize:13, fontWeight:700, background: i===0?'#1B1D2A':'#fff', color:i===0?'#fff':'#475569', border:`1px solid ${i===0?'#1B1D2A':A_BORDER}` }}>{t}</div>
          ))}
          <div style={{ flex:1 }}/>
          <div style={{ display:'flex', alignItems:'center', gap:6, padding:'7px 12px', borderRadius:10, background:'#fff', border:`1px solid ${A_BORDER}`, fontSize:13, fontWeight:600, color:'#475569' }}>{I.filter({s:14})} Status: Todos</div>
          <div style={{ display:'flex', alignItems:'center', gap:6, padding:'7px 12px', borderRadius:10, background:'#fff', border:`1px solid ${A_BORDER}`, fontSize:13, fontWeight:600, color:'#475569' }}>Ordenar: XP ↓</div>
        </div>
        {/* Grid of cards */}
        <div style={{ flex:1, overflow:'auto', display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:12, alignContent:'start' }}>
          {list.map(a=>{
            const statusMap = { on:{ bg:'#D1FAE5', fg:'#047857', lbl:'No ritmo' }, warn:{ bg:'#FEF3C7', fg:'#92400E', lbl:'Atenção' }, risk:{ bg:'#FEE2E2', fg:'#B91C1C', lbl:'Risco' } };
            const s = statusMap[a.status];
            const xpPct = (a.xp%500)/500;
            return (
              <div key={a.mat} style={{ background:A_CARD, border:`1px solid ${A_BORDER}`, borderRadius:A_RADIUS, padding:14, display:'flex', flexDirection:'column', gap:10, position:'relative' }}>
                <div style={{ position:'absolute', top:12, right:12, fontSize:10, padding:'3px 8px', borderRadius:999, background:s.bg, color:s.fg, fontWeight:800 }}>● {s.lbl}</div>
                <div style={{ display:'flex', alignItems:'center', gap:10 }}>
                  <Avatar a={a} size={48} ring ringColor={a.status==='risk'?'#EF4444':a.status==='warn'?'#F59E0B':'#10B981'}/>
                  <div style={{ minWidth:0 }}>
                    <div style={{ fontSize:14, fontWeight:900, whiteSpace:'nowrap', overflow:'hidden', textOverflow:'ellipsis', maxWidth:160 }}>{a.nome}</div>
                    <div style={{ fontSize:11, color:'#94A3B8', fontWeight:700 }}>#{a.mat} • {a.turma}</div>
                  </div>
                </div>
                <div>
                  <div style={{ display:'flex', alignItems:'baseline', justifyContent:'space-between', marginBottom:4 }}>
                    <span style={{ fontSize:11, fontWeight:800, color:'#475569' }}>NÍVEL {a.lvl}</span>
                    <span style={{ fontSize:11, fontWeight:700, color:'#94A3B8' }}>{a.xp.toLocaleString()} XP</span>
                  </div>
                  <div style={{ height:8, background:'#F1F5F9', borderRadius:999, overflow:'hidden' }}>
                    <div style={{ width:`${xpPct*100}%`, height:'100%', background:'linear-gradient(90deg,#FBBF24,#F97316)', borderRadius:999 }}/>
                  </div>
                </div>
                <div style={{ display:'flex', gap:6 }}>
                  <div style={{ flex:1, background:'#FFF7ED', borderRadius:10, padding:'6px 8px', display:'flex', alignItems:'center', gap:5 }}>
                    <span style={{ color:'#EA580C' }}>{I.fire({s:14})}</span>
                    <div>
                      <div style={{ fontSize:12, fontWeight:900, color:'#9A3412', lineHeight:1 }}>{a.streak}d</div>
                      <div style={{ fontSize:9, color:'#9A3412', fontWeight:700 }}>STREAK</div>
                    </div>
                  </div>
                  <div style={{ flex:1, background:'#EEF2FF', borderRadius:10, padding:'6px 8px', display:'flex', alignItems:'center', gap:5 }}>
                    <span style={{ color:'#4F46E5' }}>{I.star({s:14})}</span>
                    <div>
                      <div style={{ fontSize:12, fontWeight:900, color:'#3730A3', lineHeight:1 }}>{a.media.toFixed(1)}</div>
                      <div style={{ fontSize:9, color:'#3730A3', fontWeight:700 }}>MÉDIA</div>
                    </div>
                  </div>
                  <div style={{ flex:1, background:'#F0FDF4', borderRadius:10, padding:'6px 8px', display:'flex', alignItems:'center', gap:5 }}>
                    <span style={{ color:'#059669' }}>{I.shield({s:14})}</span>
                    <div>
                      <div style={{ fontSize:12, fontWeight:900, color:'#064E3B', lineHeight:1 }}>{Math.floor(a.lvl/3)}</div>
                      <div style={{ fontSize:9, color:'#064E3B', fontWeight:700 }}>MEDALHAS</div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </APP_A>
  );
}

// ============ SALAS A ============
function A_Salas() {
  return (
    <APP_A sidebar="salas" kicker="GESTÃO" title="Salas / Turmas" subtitle="7 turmas ativas no 2º trimestre"
      headRight={<div style={{ background:'#1B1D2A', color:'#fff', padding:'9px 14px', borderRadius:10, fontWeight:800, fontSize:13, display:'flex', alignItems:'center', gap:6 }}>{I.plus({s:16})} Nova turma</div>}>
      <div style={{ padding:'22px 28px', display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:14, gridAutoRows:'min-content' }}>
        {TURMAS.map((t,i)=>{
          const colors = [
            ['#EEF2FF','#4F46E5'], ['#FDF2F8','#EC4899'], ['#FFF7ED','#F97316'],
            ['#F0FDF4','#10B981'], ['#E0F2FE','#0EA5E9'], ['#FAF5FF','#8B5CF6'], ['#FFFBEB','#F59E0B']
          ];
          const [bg, col] = colors[i % colors.length];
          const pct = Math.round(((t.qtd-t.risco)/t.qtd)*100);
          return (
            <div key={t.code} style={{ background:A_CARD, border:`1px solid ${A_BORDER}`, borderRadius:A_RADIUS, padding:'16px 18px', display:'flex', flexDirection:'column', gap:12 }}>
              <div style={{ display:'flex', alignItems:'center', gap:12 }}>
                <div style={{ width:56, height:56, borderRadius:14, background:bg, color:col, display:'grid', placeItems:'center', fontSize:22, fontWeight:900 }}>{t.code}</div>
                <div style={{ flex:1 }}>
                  <div style={{ fontSize:15, fontWeight:900 }}>{t.name}</div>
                  <div style={{ fontSize:12, color:'#94A3B8', fontWeight:700 }}>Sala 0{i+1} • Prof. Coordenador</div>
                </div>
                <span style={{ color:'#94A3B8' }}>{I.dots({s:18})}</span>
              </div>
              <div style={{ display:'flex', gap:8 }}>
                <div style={{ flex:1, padding:'8px 10px', background:'#F8FAFC', borderRadius:10 }}>
                  <div style={{ fontSize:18, fontWeight:900 }}>{t.qtd}</div>
                  <div style={{ fontSize:10, color:'#64748B', fontWeight:700, letterSpacing:'.05em' }}>ALUNOS</div>
                </div>
                <div style={{ flex:1, padding:'8px 10px', background: t.risco>5?'#FEE2E2':'#FEF3C7', borderRadius:10 }}>
                  <div style={{ fontSize:18, fontWeight:900, color: t.risco>5?'#B91C1C':'#92400E' }}>{t.risco}</div>
                  <div style={{ fontSize:10, color: t.risco>5?'#B91C1C':'#92400E', fontWeight:700, letterSpacing:'.05em' }}>EM RISCO</div>
                </div>
                <div style={{ flex:1, padding:'8px 10px', background:'#D1FAE5', borderRadius:10 }}>
                  <div style={{ fontSize:18, fontWeight:900, color:'#047857' }}>{pct}%</div>
                  <div style={{ fontSize:10, color:'#047857', fontWeight:700, letterSpacing:'.05em' }}>APROV.</div>
                </div>
              </div>
              <div>
                <div style={{ display:'flex', justifyContent:'space-between', fontSize:11, fontWeight:700, color:'#475569', marginBottom:5 }}>
                  <span>Progresso da turma</span><span>{pct}%</span>
                </div>
                <div style={{ height:8, background:'#F1F5F9', borderRadius:999, overflow:'hidden' }}>
                  <div style={{ width:`${pct}%`, height:'100%', background:`linear-gradient(90deg,${col},${col}cc)`, borderRadius:999 }}/>
                </div>
              </div>
              <div style={{ display:'flex', alignItems:'center', gap:-8 }}>
                {ALUNOS.slice(i,i+4).map((a,idx)=>(
                  <div key={a.mat} style={{ marginLeft: idx===0?0:-8, border:'2px solid #fff', borderRadius:'50%' }}><Avatar a={a} size={26}/></div>
                ))}
                <div style={{ marginLeft:-8, width:26, height:26, borderRadius:'50%', background:'#F1F5F9', border:'2px solid #fff', display:'grid', placeItems:'center', fontSize:10, fontWeight:800, color:'#475569' }}>+{t.qtd-4}</div>
                <div style={{ flex:1 }}/>
                <div style={{ fontSize:12, fontWeight:800, color:col }}>Abrir →</div>
              </div>
            </div>
          );
        })}
      </div>
    </APP_A>
  );
}

// ============ MATERIAS A ============
function A_Materias() {
  const dataIcons = [I.book, I.target, I.brain, I.globe, I.globe, I.globe, I.pencil, I.shield, I.bolt, I.sparkle, I.book, I.brain, I.users];
  const colors = ['#4F46E5','#EF4444','#10B981','#F59E0B','#0EA5E9','#EC4899','#8B5CF6','#06B6D4','#F97316','#84CC16','#14B8A6','#A855F7','#F472B6'];
  return (
    <APP_A sidebar="mat" kicker="CURRÍCULO" title="Matérias" subtitle="13 disciplinas no plano pedagógico"
      headRight={<>
        <div style={{ background:'#fff', border:`1px solid ${A_BORDER}`, color:'#475569', padding:'9px 14px', borderRadius:10, fontWeight:700, fontSize:13 }}>Adicionar padrão</div>
        <div style={{ background:'#1B1D2A', color:'#fff', padding:'9px 14px', borderRadius:10, fontWeight:800, fontSize:13, display:'flex', alignItems:'center', gap:6 }}>{I.plus({s:16})} Nova matéria</div>
      </>}>
      <div style={{ padding:'22px 28px', display:'grid', gridTemplateColumns:'repeat(4,1fr)', gap:12, alignContent:'start' }}>
        {MATERIAS.map((m,i)=>{
          const col = colors[i];
          const Icon = dataIcons[i];
          const turmas = 7;
          const aprov = 60 + (i*5)%35;
          return (
            <div key={m} style={{ background:A_CARD, border:`1px solid ${A_BORDER}`, borderRadius:A_RADIUS, padding:'14px 16px', position:'relative', overflow:'hidden' }}>
              <div style={{ position:'absolute', right:-12, top:-12, width:70, height:70, borderRadius:'50%', background:col, opacity:.08 }}/>
              <div style={{ width:40, height:40, borderRadius:12, background:`${col}1A`, color:col, display:'grid', placeItems:'center', marginBottom:10 }}>{Icon({s:22})}</div>
              <div style={{ fontSize:14, fontWeight:900 }}>{m}</div>
              <div style={{ fontSize:11, color:'#94A3B8', fontWeight:700, marginTop:1 }}>{turmas} turmas • {(40+i*8)%180} notas</div>
              <div style={{ marginTop:10, display:'flex', alignItems:'center', gap:6 }}>
                <div style={{ flex:1, height:6, background:'#F1F5F9', borderRadius:999, overflow:'hidden' }}>
                  <div style={{ width:`${aprov}%`, height:'100%', background:col, borderRadius:999 }}/>
                </div>
                <div style={{ fontSize:11, fontWeight:800, color:col }}>{aprov}%</div>
              </div>
            </div>
          );
        })}
        {/* Add card */}
        <div style={{ border:`2px dashed ${A_BORDER}`, borderRadius:A_RADIUS, padding:'14px 16px', display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center', gap:6, color:'#94A3B8', minHeight:138 }}>
          <div style={{ width:40, height:40, borderRadius:12, background:'#F8FAFC', display:'grid', placeItems:'center' }}>{I.plus({s:22})}</div>
          <div style={{ fontSize:13, fontWeight:800 }}>Adicionar matéria</div>
        </div>
      </div>
    </APP_A>
  );
}

// ============ NOTAS A ============
function A_Notas() {
  const aluno = ALUNOS[6]; // Fernanda
  const notasData = MATERIAS.slice(0,10).map((m,i)=>{
    const ns = [Math.round((6+Math.random()*4)*10)/10, Math.round((6+Math.random()*4)*10)/10, Math.round((5+Math.random()*5)*10)/10, Math.round((5+Math.random()*5)*10)/10];
    const med = ns.reduce((a,b)=>a+b,0)/4;
    return { m, ns, med };
  });
  // deterministic
  const fixedNotas = [
    { m:'Português',  ns:[9.0,8.5,9.2,9.7], med:9.1 },
    { m:'Matemática', ns:[7.8,8.2,9.0,8.5], med:8.4 },
    { m:'Ciências',   ns:[8.5,9.0,8.8,9.4], med:8.9 },
    { m:'História',   ns:[9.2,9.5,9.0,9.6], med:9.3 },
    { m:'Geografia',  ns:[7.5,8.0,8.4,8.8], med:8.2 },
    { m:'Inglês',     ns:[9.8,9.4,9.6,9.9], med:9.7 },
    { m:'Arte',       ns:[8.0,8.5,9.0,8.7], med:8.6 },
    { m:'Ed. Física', ns:[9.5,9.0,9.2,9.4], med:9.3 },
    { m:'Física',     ns:[6.5,7.0,7.8,8.0], med:7.3 },
    { m:'Química',    ns:[5.8,6.5,6.8,7.5], med:6.7 },
  ];
  return (
    <APP_A sidebar="notas" kicker="LANÇAMENTO" title="Notas" subtitle="Fernanda Pinto • 9º Fundamental • 2º trimestre"
      headRight={<>
        <div style={{ background:'#fff', border:`1px solid ${A_BORDER}`, color:'#475569', padding:'9px 14px', borderRadius:10, fontWeight:700, fontSize:13, display:'flex', alignItems:'center', gap:6 }}>{I.sparkle({s:14})} Gerar notas aleatórias</div>
        <div style={{ background:'#10B981', color:'#fff', padding:'9px 14px', borderRadius:10, fontWeight:800, fontSize:13, display:'flex', alignItems:'center', gap:6 }}>{I.check({s:16})} Salvar tudo</div>
      </>}>
      <div style={{ padding:'18px 28px', display:'grid', gridTemplateColumns:'320px 1fr', gap:16, height:'100%' }}>
        {/* Student panel */}
        <div style={{ background:A_CARD, border:`1px solid ${A_BORDER}`, borderRadius:A_RADIUS, padding:'20px', display:'flex', flexDirection:'column', gap:14, overflow:'auto' }}>
          <div style={{ display:'flex', flexDirection:'column', alignItems:'center', gap:8 }}>
            <Avatar a={aluno} size={84} ring ringColor="#10B981"/>
            <div style={{ fontSize:17, fontWeight:900, textAlign:'center' }}>{aluno.nome}</div>
            <div style={{ display:'flex', gap:6 }}>
              <div style={{ fontSize:11, fontWeight:800, padding:'3px 10px', borderRadius:999, background:'#EEF2FF', color:'#4F46E5' }}>NV. {aluno.lvl}</div>
              <div style={{ fontSize:11, fontWeight:800, padding:'3px 10px', borderRadius:999, background:'#D1FAE5', color:'#047857' }}>● APROVADA</div>
            </div>
          </div>
          <div style={{ display:'flex', gap:8 }}>
            <div style={{ flex:1, background:'#FFF7ED', padding:'10px 12px', borderRadius:12, textAlign:'center' }}>
              <div style={{ color:'#EA580C', display:'inline-flex' }}>{I.fire({s:18})}</div>
              <div style={{ fontSize:18, fontWeight:900, color:'#9A3412' }}>{aluno.streak}</div>
              <div style={{ fontSize:10, fontWeight:700, color:'#9A3412' }}>STREAK</div>
            </div>
            <div style={{ flex:1, background:'#EEF2FF', padding:'10px 12px', borderRadius:12, textAlign:'center' }}>
              <div style={{ color:'#4F46E5', display:'inline-flex' }}>{I.bolt({s:18})}</div>
              <div style={{ fontSize:18, fontWeight:900, color:'#3730A3' }}>{aluno.xp}</div>
              <div style={{ fontSize:10, fontWeight:700, color:'#3730A3' }}>XP TOTAL</div>
            </div>
          </div>
          <div>
            <div style={{ fontSize:11, fontWeight:800, color:'#94A3B8', letterSpacing:'.08em', marginBottom:6 }}>CONQUISTAS</div>
            <div style={{ display:'grid', gridTemplateColumns:'repeat(4,1fr)', gap:6 }}>
              {[
                { ic:I.fire, c:'#F97316', bg:'#FFF7ED', lbl:'30 dias' },
                { ic:I.star, c:'#FBBF24', bg:'#FFFBEB', lbl:'Top 5' },
                { ic:I.shield, c:'#10B981', bg:'#D1FAE5', lbl:'Defesa' },
                { ic:I.trophy, c:'#8B5CF6', bg:'#EDE9FE', lbl:'Ouro' },
                { ic:I.bolt, c:'#EF4444', bg:'#FEE2E2', lbl:'Combo' },
                { ic:I.target, c:'#0EA5E9', bg:'#E0F2FE', lbl:'Foco' },
                null, null,
              ].map((b,i)=> b ? (
                <div key={i} style={{ aspectRatio:'1', borderRadius:10, background:b.bg, color:b.c, display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center', gap:2 }}>
                  {b.ic({s:18})}
                  <div style={{ fontSize:8, fontWeight:800 }}>{b.lbl}</div>
                </div>
              ) : (
                <div key={i} style={{ aspectRatio:'1', borderRadius:10, background:'#F8FAFC', border:`1.5px dashed ${A_BORDER}`, display:'grid', placeItems:'center', color:'#CBD5E1' }}>?</div>
              ))}
            </div>
          </div>
          <div style={{ marginTop:'auto', padding:'12px', background:'#F8FAFC', borderRadius:12 }}>
            <div style={{ display:'flex', alignItems:'baseline', justifyContent:'space-between', marginBottom:6 }}>
              <span style={{ fontSize:11, fontWeight:800, color:'#475569' }}>NV. {aluno.lvl} → {aluno.lvl+1}</span>
              <span style={{ fontSize:11, fontWeight:700, color:'#94A3B8' }}>340 / 500 XP</span>
            </div>
            <div style={{ height:8, background:'#E2E8F0', borderRadius:999, overflow:'hidden' }}>
              <div style={{ width:'68%', height:'100%', background:'linear-gradient(90deg,#FBBF24,#F97316)', borderRadius:999 }}/>
            </div>
          </div>
        </div>

        {/* Notas table */}
        <div style={{ background:A_CARD, border:`1px solid ${A_BORDER}`, borderRadius:A_RADIUS, padding:'16px 20px', display:'flex', flexDirection:'column', gap:10, overflow:'hidden' }}>
          <div style={{ display:'flex', alignItems:'center', gap:10 }}>
            <div style={{ display:'flex', alignItems:'center', gap:6, padding:'7px 12px', background:'#F1F5F9', borderRadius:10, fontSize:13, fontWeight:700 }}>Turma: 9º Fundamental {I.down({s:12})}</div>
            <div style={{ display:'flex', alignItems:'center', gap:6, padding:'7px 12px', background:'#F1F5F9', borderRadius:10, fontSize:13, fontWeight:700 }}>Aluno: Fernanda Pinto {I.down({s:12})}</div>
            <div style={{ flex:1 }}/>
            <div style={{ fontSize:12, fontWeight:700, color:'#94A3B8' }}>Média geral: <span style={{ color:'#10B981', fontWeight:900, fontSize:14 }}>8.7</span></div>
          </div>
          <div style={{ flex:1, overflow:'auto' }}>
            <div style={{ display:'grid', gridTemplateColumns:'2fr repeat(4,1fr) 1fr 1.2fr', gap:0, fontSize:11, fontWeight:800, color:'#94A3B8', letterSpacing:'.06em', padding:'8px 12px', borderBottom:`1px solid ${A_BORDER}` }}>
              <div>MATÉRIA</div><div>N1</div><div>N2</div><div>N3</div><div>N4</div><div>MÉDIA</div><div style={{ textAlign:'right' }}>STATUS</div>
            </div>
            {fixedNotas.map((n,i)=>{
              const med = n.med;
              const status = med>=7?'aprov': med>=5?'rec':'rep';
              const map = { aprov:{ bg:'#D1FAE5', fg:'#047857', lbl:'Aprovado' }, rec:{ bg:'#FEF3C7', fg:'#92400E', lbl:'Recuperação' }, rep:{ bg:'#FEE2E2', fg:'#B91C1C', lbl:'Reprovado' } };
              const s = map[status];
              return (
                <div key={n.m} style={{ display:'grid', gridTemplateColumns:'2fr repeat(4,1fr) 1fr 1.2fr', gap:0, fontSize:13, alignItems:'center', padding:'10px 12px', borderBottom:`1px solid ${A_BORDER}`, background: i%2?'#FCFCFA':'#fff' }}>
                  <div style={{ fontWeight:800 }}>{n.m}</div>
                  {n.ns.map((v,k)=>(
                    <div key={k} style={{ fontWeight:700, color: v<5?'#EF4444':v<7?'#F59E0B':'#10B981' }}>{v.toFixed(1)}</div>
                  ))}
                  <div style={{ fontWeight:900, fontSize:14 }}>{med.toFixed(1)}</div>
                  <div style={{ textAlign:'right' }}><span style={{ fontSize:11, padding:'3px 10px', borderRadius:999, background:s.bg, color:s.fg, fontWeight:800 }}>● {s.lbl}</span></div>
                </div>
              );
            })}
          </div>
          <div style={{ padding:'12px 14px', background:'#F8FAFC', borderRadius:12, display:'flex', alignItems:'center', gap:10 }}>
            <span style={{ fontSize:12, fontWeight:800, color:'#475569' }}>Editar nota selecionada →</span>
            {['N1','N2','N3','N4'].map(n=>(
              <div key={n} style={{ display:'flex', alignItems:'center', gap:6 }}>
                <span style={{ fontSize:11, fontWeight:700, color:'#94A3B8' }}>{n}</span>
                <div style={{ width:50, padding:'4px 8px', background:'#fff', border:`1px solid ${A_BORDER}`, borderRadius:8, fontSize:13, fontWeight:700 }}>—</div>
              </div>
            ))}
            <div style={{ flex:1 }}/>
            <div style={{ padding:'7px 12px', background:'#10B981', color:'#fff', borderRadius:8, fontSize:12, fontWeight:800 }}>Salvar</div>
          </div>
        </div>
      </div>
    </APP_A>
  );
}

// ============ PREDIÇÕES A ============
function A_Predicoes() {
  const preds = [
    { a:ALUNOS[7], dir:'down', conf:92, motivo:'Quedas consecutivas em Matemática e Física', mat:'Matemática' },
    { a:ALUNOS[3], dir:'down', conf:88, motivo:'Streak quebrada há 3 semanas, média caindo', mat:'História' },
    { a:ALUNOS[1], dir:'up',   conf:81, motivo:'Recuperação consistente nas últimas 4 notas', mat:'Português' },
    { a:ALUNOS[9], dir:'flat', conf:74, motivo:'Estável em zona de recuperação', mat:'Química' },
    { a:ALUNOS[5], dir:'up',   conf:79, motivo:'Tendência positiva após intervenção', mat:'Inglês' },
    { a:ALUNOS[11], dir:'up',  conf:95, motivo:'Performance excelente, mantém ritmo', mat:'Geral' },
  ];
  return (
    <APP_A sidebar="pred" kicker="INTELIGÊNCIA ARTIFICIAL" title="Predições de Desempenho" subtitle="Identifique déficits logo no início do ano — análise por aluno com modelo RF_M3"
      headRight={<>
        <div style={{ display:'flex', alignItems:'center', gap:6, padding:'8px 12px', background:'#D1FAE5', color:'#047857', borderRadius:10, fontSize:12, fontWeight:800 }}>● 91.3% acurácia</div>
        <div style={{ background:'#4F46E5', color:'#fff', padding:'9px 14px', borderRadius:10, fontWeight:800, fontSize:13, display:'flex', alignItems:'center', gap:6 }}>{I.sparkle({s:14})} Re-analisar</div>
      </>}>
      <div style={{ padding:'20px 28px', display:'flex', flexDirection:'column', gap:16, height:'100%', overflow:'hidden' }}>
        {/* Filter pills */}
        <div style={{ display:'flex', gap:8, alignItems:'center' }}>
          <div style={{ fontSize:12, fontWeight:800, color:'#94A3B8' }}>FILTRO</div>
          {[
            { l:'Todas', c:'#1B1D2A', n:202 },
            { l:'Aprovadas', c:'#10B981', n:154 },
            { l:'Recuperação', c:'#F59E0B', n:17 },
            { l:'Reprovadas', c:'#EF4444', n:31 },
            { l:'Vai melhorar', c:'#0EA5E9', n:43 },
            { l:'Vai piorar', c:'#EC4899', n:12 },
          ].map((p,i)=>(
            <div key={p.l} style={{ padding:'7px 12px', borderRadius:999, fontSize:12, fontWeight:800, background: i===0?p.c:'#fff', color: i===0?'#fff':p.c, border:`1.5px solid ${i===0?p.c:`${p.c}33`}`, display:'flex', alignItems:'center', gap:6 }}>{p.l} <span style={{ fontSize:10, padding:'1px 6px', borderRadius:999, background: i===0?'rgba(255,255,255,.2)':`${p.c}1A` }}>{p.n}</span></div>
          ))}
        </div>

        {/* Summary cards */}
        <div style={{ display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:14 }}>
          <div style={{ background:'linear-gradient(135deg,#FECDD3,#FB7185)', borderRadius:A_RADIUS, padding:'14px 18px', color:'#7F1D1D', position:'relative', overflow:'hidden' }}>
            <div style={{ position:'absolute', right:-20, bottom:-20, opacity:.2 }}>{I.down({s:100})}</div>
            <div style={{ fontSize:11, fontWeight:800, letterSpacing:'.08em', opacity:.9 }}>VÃO PIORAR</div>
            <div style={{ fontSize:42, fontWeight:900, letterSpacing:'-0.04em', lineHeight:1, marginTop:4 }}>12</div>
            <div style={{ fontSize:12, fontWeight:700, marginTop:4 }}>alunos nas próximas 2 semanas</div>
          </div>
          <div style={{ background:'linear-gradient(135deg,#BAE6FD,#0EA5E9)', borderRadius:A_RADIUS, padding:'14px 18px', color:'#0C4A6E', position:'relative', overflow:'hidden' }}>
            <div style={{ position:'absolute', right:-20, bottom:-20, opacity:.2 }}>{I.up({s:100})}</div>
            <div style={{ fontSize:11, fontWeight:800, letterSpacing:'.08em', opacity:.9 }}>VÃO MELHORAR</div>
            <div style={{ fontSize:42, fontWeight:900, letterSpacing:'-0.04em', lineHeight:1, marginTop:4 }}>43</div>
            <div style={{ fontSize:12, fontWeight:700, marginTop:4 }}>com a tendência atual</div>
          </div>
          <div style={{ background:'linear-gradient(135deg,#FDE68A,#F59E0B)', borderRadius:A_RADIUS, padding:'14px 18px', color:'#78350F', position:'relative', overflow:'hidden' }}>
            <div style={{ position:'absolute', right:-20, bottom:-20, opacity:.2 }}>{I.bell({s:100})}</div>
            <div style={{ fontSize:11, fontWeight:800, letterSpacing:'.08em', opacity:.9 }}>INTERVIR AGORA</div>
            <div style={{ fontSize:42, fontWeight:900, letterSpacing:'-0.04em', lineHeight:1, marginTop:4 }}>8</div>
            <div style={{ fontSize:12, fontWeight:700, marginTop:4 }}>recuperáveis com ajuda</div>
          </div>
        </div>

        {/* Predictions list */}
        <div style={{ flex:1, overflow:'auto', display:'flex', flexDirection:'column', gap:8 }}>
          {preds.map((p,i)=>{
            const dirMap = {
              up:   { ic:I.up,   c:'#059669', bg:'#D1FAE5', lbl:'Vai melhorar' },
              down: { ic:I.down, c:'#DC2626', bg:'#FEE2E2', lbl:'Vai piorar' },
              flat: { ic:I.target, c:'#D97706', bg:'#FEF3C7', lbl:'Estável' },
            };
            const d = dirMap[p.dir];
            return (
              <div key={i} style={{ background:A_CARD, border:`1px solid ${A_BORDER}`, borderRadius:A_RADIUS, padding:'12px 16px', display:'flex', alignItems:'center', gap:14 }}>
                <Avatar a={p.a} size={44} ring ringColor={d.c}/>
                <div style={{ flex:1, minWidth:0 }}>
                  <div style={{ fontSize:14, fontWeight:900 }}>{p.a.nome}</div>
                  <div style={{ fontSize:12, color:'#64748B' }}>{p.motivo}</div>
                </div>
                <div style={{ display:'flex', flexDirection:'column', alignItems:'flex-end' }}>
                  <div style={{ fontSize:11, fontWeight:700, color:'#94A3B8' }}>FOCO</div>
                  <div style={{ fontSize:13, fontWeight:800 }}>{p.mat}</div>
                </div>
                <div style={{ width:1, height:30, background:A_BORDER }}/>
                <div style={{ display:'flex', alignItems:'center', gap:8, padding:'6px 14px', borderRadius:999, background:d.bg, color:d.c, fontWeight:900, fontSize:13 }}>{d.ic({s:16})} {d.lbl}</div>
                <Ring value={p.conf} max={100} size={48} stroke={5} color={d.c} track="#F1F5F9">
                  <span style={{ fontSize:11, color:d.c }}>{p.conf}%</span>
                </Ring>
                <div style={{ color:'#94A3B8' }}>{I.chev({s:18})}</div>
              </div>
            );
          })}
        </div>
      </div>
    </APP_A>
  );
}

// ============ RELATÓRIO A ============
function A_Relatorio() {
  const rows = [];
  const statuses = ['Aprovado','Recuperação','Reprovado'];
  let seed = 1;
  const rand = () => { seed = (seed*9301+49297)%233280; return seed/233280; };
  ALUNOS.slice(0,8).forEach(a=>{
    MATERIAS.slice(0,4).forEach(m=>{
      const n = [3+rand()*7, 3+rand()*7, 3+rand()*7, 3+rand()*7].map(v=>Math.round(v*10)/10);
      const med = n.reduce((s,v)=>s+v,0)/4;
      const st = med>=7?0: med>=5?1:2;
      rows.push({ a, m, n, med, st });
    });
  });
  return (
    <APP_A sidebar="rel" kicker="ANÁLISE" title="Relatório" subtitle="Visão completa de notas e desempenho"
      headRight={<>
        <div style={{ background:'#fff', border:`1px solid ${A_BORDER}`, color:'#475569', padding:'9px 14px', borderRadius:10, fontWeight:700, fontSize:13, display:'flex', alignItems:'center', gap:6 }}>{I.download({s:14})} Exportar PDF</div>
        <div style={{ background:'#1B1D2A', color:'#fff', padding:'9px 14px', borderRadius:10, fontWeight:800, fontSize:13, display:'flex', alignItems:'center', gap:6 }}>{I.download({s:14})} Excel</div>
      </>}>
      <div style={{ padding:'20px 28px', display:'flex', flexDirection:'column', gap:14, height:'100%', overflow:'hidden' }}>
        <div style={{ display:'grid', gridTemplateColumns:'repeat(4,1fr)', gap:12 }}>
          {[
            { l:'Total de notas', v:'1.846', c:'#4F46E5' },
            { l:'Média geral', v:'7.2', c:'#10B981' },
            { l:'Taxa de aprovação', v:'76%', c:'#0EA5E9' },
            { l:'Em recuperação', v:'17%', c:'#F59E0B' },
          ].map((s,i)=>(
            <div key={i} style={{ background:A_CARD, border:`1px solid ${A_BORDER}`, borderRadius:14, padding:'12px 16px', display:'flex', alignItems:'center', gap:10 }}>
              <div style={{ width:6, height:30, background:s.c, borderRadius:3 }}/>
              <div>
                <div style={{ fontSize:22, fontWeight:900, color:s.c, letterSpacing:'-0.02em' }}>{s.v}</div>
                <div style={{ fontSize:11, color:'#64748B', fontWeight:700 }}>{s.l}</div>
              </div>
            </div>
          ))}
        </div>
        <div style={{ display:'flex', gap:8, alignItems:'center' }}>
          {['Todas','6F','7F','8F','9F','1M','2M','3M'].map((t,i)=>(
            <div key={t} style={{ padding:'6px 12px', borderRadius:999, fontSize:12, fontWeight:800, background: i===0?'#1B1D2A':'#fff', color:i===0?'#fff':'#475569', border:`1px solid ${i===0?'#1B1D2A':A_BORDER}` }}>{t}</div>
          ))}
          <div style={{ flex:1 }}/>
          <div style={{ padding:'6px 12px', borderRadius:999, fontSize:12, fontWeight:700, background:'#fff', border:`1px solid ${A_BORDER}`, display:'flex', alignItems:'center', gap:5, color:'#475569' }}>{I.search({s:12})} Buscar aluno</div>
        </div>
        <div style={{ flex:1, background:A_CARD, border:`1px solid ${A_BORDER}`, borderRadius:A_RADIUS, overflow:'hidden', display:'flex', flexDirection:'column' }}>
          <div style={{ display:'grid', gridTemplateColumns:'1.6fr 0.7fr 1.2fr repeat(4,0.7fr) 0.8fr 1.1fr', gap:0, fontSize:11, fontWeight:800, color:'#94A3B8', letterSpacing:'.06em', padding:'12px 16px', background:'#F8FAFC', borderBottom:`1px solid ${A_BORDER}` }}>
            <div>ALUNO</div><div>TURMA</div><div>MATÉRIA</div><div>N1</div><div>N2</div><div>N3</div><div>N4</div><div>MÉDIA</div><div style={{ textAlign:'right' }}>STATUS</div>
          </div>
          <div style={{ flex:1, overflow:'auto' }}>
            {rows.map((r,i)=>{
              const map = [
                { bg:'#D1FAE5', fg:'#047857', lbl:'Aprovado' },
                { bg:'#FEF3C7', fg:'#92400E', lbl:'Recuperação' },
                { bg:'#FEE2E2', fg:'#B91C1C', lbl:'Reprovado' },
              ];
              const s = map[r.st];
              return (
                <div key={i} style={{ display:'grid', gridTemplateColumns:'1.6fr 0.7fr 1.2fr repeat(4,0.7fr) 0.8fr 1.1fr', gap:0, fontSize:13, alignItems:'center', padding:'8px 16px', borderBottom:`1px solid ${A_BORDER}`, background: i%2?'#FCFCFA':'#fff' }}>
                  <div style={{ display:'flex', alignItems:'center', gap:8 }}>
                    <Avatar a={r.a} size={26}/>
                    <span style={{ fontWeight:700 }}>{r.a.nome}</span>
                  </div>
                  <div style={{ fontWeight:700, color:'#64748B' }}>{r.a.turma}</div>
                  <div style={{ fontWeight:700 }}>{r.m}</div>
                  {r.n.map((v,k)=>(
                    <div key={k} style={{ fontWeight:700, color: v<5?'#EF4444':v<7?'#F59E0B':'#10B981' }}>{v.toFixed(1)}</div>
                  ))}
                  <div style={{ fontWeight:900 }}>{r.med.toFixed(1)}</div>
                  <div style={{ textAlign:'right' }}><span style={{ fontSize:11, padding:'3px 10px', borderRadius:999, background:s.bg, color:s.fg, fontWeight:800 }}>● {s.lbl}</span></div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </APP_A>
  );
}

// ============ MACHINE LEARNING A ============
function A_ML() {
  const models = [
    { name:'RF_M1', desc:'100 árvores • prof. 5', acc:85.2, date:'20/05 19:23', active:false, color:'#94A3B8' },
    { name:'RF_M2', desc:'150 árvores • prof. 10', acc:90.4, date:'20/05 19:23', active:false, color:'#0EA5E9' },
    { name:'RF_M3', desc:'200 árvores • PRODUÇÃO', acc:91.3, date:'20/05 19:24', active:true, color:'#10B981' },
  ];
  return (
    <APP_A sidebar="ml" kicker="IA AVANÇADA" title="Machine Learning" subtitle="Treine e analise modelos de predição de desempenho"
      headRight={<>
        <div style={{ background:'#fff', border:`1px solid ${A_BORDER}`, color:'#475569', padding:'9px 14px', borderRadius:10, fontWeight:700, fontSize:13, display:'flex', alignItems:'center', gap:6 }}>{I.sparkle({s:14})} Gerar features</div>
        <div style={{ background:'#10B981', color:'#fff', padding:'9px 14px', borderRadius:10, fontWeight:800, fontSize:13, display:'flex', alignItems:'center', gap:6 }}>▶ Treinar produção</div>
      </>}>
      <div style={{ padding:'22px 28px', display:'flex', flexDirection:'column', gap:16, height:'100%', overflow:'hidden' }}>
        {/* Models */}
        <div>
          <div style={{ fontSize:11, fontWeight:900, color:'#94A3B8', letterSpacing:'.1em', marginBottom:10 }}>MODELOS TREINADOS</div>
          <div style={{ display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:14 }}>
            {models.map((m,i)=>(
              <div key={m.name} style={{ background: m.active?'linear-gradient(135deg,#064E3B,#10B981)':A_CARD, color: m.active?'#fff':'#1B1D2A', border:`1px solid ${m.active?'#10B981':A_BORDER}`, borderRadius:A_RADIUS, padding:'16px 18px', position:'relative', overflow:'hidden' }}>
                {m.active && <div style={{ position:'absolute', top:12, right:12, fontSize:10, padding:'3px 8px', borderRadius:999, background:'rgba(255,255,255,.2)', fontWeight:800 }}>● EM PRODUÇÃO</div>}
                <div style={{ display:'flex', alignItems:'center', gap:10, marginBottom:10 }}>
                  <div style={{ width:36, height:36, borderRadius:10, background: m.active?'rgba(255,255,255,.15)':'#F1F5F9', color: m.active?'#fff':m.color, display:'grid', placeItems:'center' }}>{I.brain({s:18})}</div>
                  <div>
                    <div style={{ fontSize:16, fontWeight:900 }}>{m.name}</div>
                    <div style={{ fontSize:11, opacity:.7, fontWeight:600 }}>{m.desc}</div>
                  </div>
                </div>
                <div style={{ display:'flex', alignItems:'baseline', gap:8 }}>
                  <div style={{ fontSize:36, fontWeight:900, letterSpacing:'-0.03em', lineHeight:1 }}>{m.acc}<span style={{ fontSize:18 }}>%</span></div>
                  <div style={{ fontSize:11, opacity:.7, fontWeight:600 }}>acurácia</div>
                </div>
                <div style={{ height:6, background: m.active?'rgba(255,255,255,.2)':'#F1F5F9', borderRadius:999, marginTop:10, overflow:'hidden' }}>
                  <div style={{ width:`${m.acc}%`, height:'100%', background: m.active?'#FBBF24':m.color, borderRadius:999 }}/>
                </div>
                <div style={{ fontSize:11, opacity:.7, marginTop:8, fontWeight:600 }}>Treinado em {m.date}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Two columns */}
        <div style={{ flex:1, display:'grid', gridTemplateColumns:'1fr 1.2fr', gap:14, minHeight:0 }}>
          {/* Feature importance */}
          <div style={{ background:A_CARD, border:`1px solid ${A_BORDER}`, borderRadius:A_RADIUS, padding:'16px 20px', display:'flex', flexDirection:'column' }}>
            <div style={{ display:'flex', alignItems:'center', gap:8, marginBottom:14 }}>
              <span style={{ width:30, height:30, borderRadius:8, background:'#EEF2FF', color:'#4F46E5', display:'grid', placeItems:'center' }}>{I.chart({s:18})}</span>
              <div style={{ fontSize:15, fontWeight:900 }}>Importância das Features</div>
            </div>
            {[
              { l:'Média anterior',      v:34, c:'#4F46E5' },
              { l:'Streak de aprovação', v:22, c:'#F97316' },
              { l:'Variação trimestral', v:18, c:'#0EA5E9' },
              { l:'Frequência (presença)',v:14, c:'#10B981' },
              { l:'Idade × série',       v:8,  c:'#EC4899' },
              { l:'Outros',              v:4,  c:'#94A3B8' },
            ].map(f=>(
              <div key={f.l} style={{ marginBottom:11 }}>
                <div style={{ display:'flex', justifyContent:'space-between', fontSize:12, marginBottom:5 }}>
                  <span style={{ fontWeight:700 }}>{f.l}</span>
                  <span style={{ fontWeight:900, color:f.c }}>{f.v}%</span>
                </div>
                <div style={{ height:8, background:'#F1F5F9', borderRadius:999, overflow:'hidden' }}>
                  <div style={{ width:`${f.v*2.5}%`, height:'100%', background:f.c, borderRadius:999 }}/>
                </div>
              </div>
            ))}
          </div>

          {/* Decision analysis */}
          <div style={{ background:A_CARD, border:`1px solid ${A_BORDER}`, borderRadius:A_RADIUS, padding:'16px 20px', display:'flex', flexDirection:'column' }}>
            <div style={{ display:'flex', alignItems:'center', gap:8, marginBottom:12 }}>
              <span style={{ width:30, height:30, borderRadius:8, background:'#FEF3C7', color:'#D97706', display:'grid', placeItems:'center' }}>{I.search({s:18})}</span>
              <div>
                <div style={{ fontSize:15, fontWeight:900 }}>Analisar Decisão do Modelo</div>
                <div style={{ fontSize:11, color:'#94A3B8', fontWeight:600 }}>Entenda por que a IA fez uma previsão</div>
              </div>
            </div>
            <div style={{ display:'flex', gap:8, marginBottom:14 }}>
              <div style={{ flex:1, padding:'8px 12px', background:'#F1F5F9', borderRadius:10, fontSize:13, fontWeight:700, display:'flex', justifyContent:'space-between', alignItems:'center' }}>Gabriel Sá {I.down({s:12})}</div>
              <div style={{ flex:1, padding:'8px 12px', background:'#F1F5F9', borderRadius:10, fontSize:13, fontWeight:700, display:'flex', justifyContent:'space-between', alignItems:'center' }}>Matemática {I.down({s:12})}</div>
            </div>
            <div style={{ flex:1, background:'#0F172A', borderRadius:14, padding:'16px', color:'#fff', overflow:'auto', fontFamily:"'JetBrains Mono', monospace", fontSize:11.5, lineHeight:1.7 }}>
              <div style={{ color:'#94A3B8' }}>{'> '} Aluno: <span style={{ color:'#A5B4FC' }}>Gabriel Sá (#2026008)</span></div>
              <div style={{ color:'#94A3B8' }}>{'> '} Matéria: <span style={{ color:'#A5B4FC' }}>Matemática</span></div>
              <div style={{ color:'#94A3B8' }}>{'> '} Modelo: <span style={{ color:'#34D399' }}>RF_M3 (200 árvores)</span></div>
              <div style={{ marginTop:8, color:'#FBBF24' }}>━━━ ANÁLISE ━━━</div>
              <div>Predição: <span style={{ color:'#F87171', fontWeight:700 }}>VAI PIORAR</span> (confiança 92%)</div>
              <div style={{ marginTop:8, color:'#FBBF24' }}>Fatores principais:</div>
              <div>  ↓ Média anterior 3.9/10 <span style={{ color:'#F87171' }}>(-2.4 σ)</span></div>
              <div>  ↓ Streak quebrada há 4 semanas</div>
              <div>  ↓ N3 e N4 abaixo da turma <span style={{ color:'#F87171' }}>(-31%)</span></div>
              <div>  ↑ Variação positiva em Português <span style={{ color:'#34D399' }}>(+1.1)</span></div>
              <div style={{ marginTop:8, color:'#FBBF24' }}>Recomendação:</div>
              <div>  • Reforço em álgebra básica</div>
              <div>  • Tutoria 2× por semana</div>
              <div>  • Reativar streak com tarefas curtas</div>
            </div>
          </div>
        </div>
      </div>
    </APP_A>
  );
}

window.A_Dashboard = A_Dashboard;
window.A_Alunos = A_Alunos;
window.A_Salas = A_Salas;
window.A_Materias = A_Materias;
window.A_Notas = A_Notas;
window.A_Predicoes = A_Predicoes;
window.A_Relatorio = A_Relatorio;
window.A_ML = A_ML;
