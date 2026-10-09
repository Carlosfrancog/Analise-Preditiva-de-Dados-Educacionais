// Shared tokens, icons, and primitives for both variations

const TOKENS = {
  indigo: '#4F46E5',
  indigoDark: '#3730A3',
  indigoSoft: '#EEF2FF',
  amber: '#FBBF24',
  amberSoft: '#FEF3C7',
  emerald: '#10B981',
  emeraldSoft: '#D1FAE5',
  red: '#EF4444',
  redSoft: '#FEE2E2',
  sky: '#0EA5E9',
  skySoft: '#E0F2FE',
  violet: '#8B5CF6',
  violetSoft: '#EDE9FE',
  pink: '#EC4899',
  ink: '#0F172A',
  ink2: '#1E293B',
  slate: '#475569',
  slate2: '#64748B',
  slate3: '#94A3B8',
  line: '#E2E8F0',
  line2: '#F1F5F9',
  bg: '#F8FAFC',
  bgWarm: '#FAFAF7',
  white: '#FFFFFF',
};

// Icon set — clean stroke icons, no emoji
const I = {
  home: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 12 12 3l9 9"/><path d="M5 10v10h14V10"/></svg>,
  users: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="9" cy="8" r="3.5"/><path d="M2 21c0-3.5 3-6 7-6s7 2.5 7 6"/><path d="M16 11a3 3 0 0 0 0-6"/><path d="M22 21c0-3-2-5-5-5.5"/></svg>,
  school: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 10 12 5l9 5-9 5z"/><path d="M7 12v5c0 1 2 2.5 5 2.5s5-1.5 5-2.5v-5"/><path d="M21 10v6"/></svg>,
  book: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 4h11a3 3 0 0 1 3 3v13H7a3 3 0 0 1-3-3z"/><path d="M4 17a3 3 0 0 1 3-3h11"/></svg>,
  edit: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4z"/></svg>,
  target: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/></svg>,
  chart: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 3v18h18"/><rect x="7" y="12" width="3" height="6"/><rect x="12" y="8" width="3" height="10"/><rect x="17" y="4" width="3" height="14"/></svg>,
  brain: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 4a3 3 0 0 0-3 3v1a3 3 0 0 0-2 5 3 3 0 0 0 2 5v1a3 3 0 0 0 3 3z"/><path d="M15 4a3 3 0 0 1 3 3v1a3 3 0 0 1 2 5 3 3 0 0 1-2 5v1a3 3 0 0 1-3 3"/><path d="M9 4v18M15 4v18"/></svg>,
  upload: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M17 8 12 3 7 8"/><path d="M12 3v13"/></svg>,
  download: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/></svg>,
  search: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>,
  plus: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M12 5v14M5 12h14"/></svg>,
  trash: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M5 6l1 14a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2l1-14"/></svg>,
  fire: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="currentColor"><path d="M12 2s4 4 4 8a4 4 0 0 1-1 2.5C16.5 14 18 12 18 9c2 2 3 5 3 8a9 9 0 0 1-18 0c0-4 2-7 5-9 0 2 1 3 2 3 0-3 0-6 2-9z"/></svg>,
  bolt: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="currentColor"><path d="M13 2 4 14h6l-1 8 9-12h-6z"/></svg>,
  star: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3 6.5 7 1-5 5 1.5 7L12 18l-6.5 3.5L7 14.5 2 9.5l7-1z"/></svg>,
  trophy: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M7 4h10v6a5 5 0 0 1-10 0z"/><path d="M5 4h2v3a2 2 0 0 1-2-2zM19 4h-2v3a2 2 0 0 0 2-2z"/><path d="M9 15h6v2H9zM8 19h8v2H8z"/></svg>,
  shield: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/></svg>,
  check: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M4 12l5 5 11-12"/></svg>,
  warn: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 3 2 21h20z"/><path d="M12 10v5M12 18v.5"/></svg>,
  up: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M5 15l7-7 7 7"/></svg>,
  down: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M5 9l7 7 7-7"/></svg>,
  chev: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m9 6 6 6-6 6"/></svg>,
  bell: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 7 3 9H3c0-2 3-2 3-9"/><path d="M10 21a2 2 0 0 0 4 0"/></svg>,
  filter: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 5h18l-7 9v6l-4-2v-4z"/></svg>,
  sparkle: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l1.6 5.4L19 9l-5.4 1.6L12 16l-1.6-5.4L5 9l5.4-1.6z"/><path d="M19 14l.8 2.2L22 17l-2.2.8L19 20l-.8-2.2L16 17l2.2-.8z"/></svg>,
  menu: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 12h18M3 6h18M3 18h18"/></svg>,
  dots: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="currentColor"><circle cx="5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/></svg>,
  pencil: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 21h4l11-11-4-4L3 17z"/><path d="M14 6l4 4"/></svg>,
  globe: (p={}) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/></svg>,
};

// Demo data
const TURMAS = [
  { name: '6º Fundamental', code: '6F', qtd: 28, risco: 4 },
  { name: '7º Fundamental', code: '7F', qtd: 31, risco: 6 },
  { name: '8º Fundamental', code: '8F', qtd: 29, risco: 3 },
  { name: '9º Fundamental', code: '9F', qtd: 27, risco: 5 },
  { name: '1º Médio', code: '1M', qtd: 32, risco: 7 },
  { name: '2º Médio', code: '2M', qtd: 30, risco: 4 },
  { name: '3º Médio', code: '3M', qtd: 25, risco: 2 },
];

const MATERIAS = ['Português', 'Matemática', 'Ciências', 'História', 'Geografia', 'Inglês', 'Arte', 'Ed. Física', 'Física', 'Química', 'Biologia', 'Filosofia', 'Sociologia'];

const ALUNOS = [
  { mat: '2026001', nome: 'Ana Araújo',    turma: '6F', xp: 2340, lvl: 12, streak: 18, status: 'on',   media: 8.4, avatar: 'AA', color: '#F472B6' },
  { mat: '2026002', nome: 'Ana Cardoso',   turma: '6F', xp: 980,  lvl: 6,  streak: 3,  status: 'risk', media: 5.2, avatar: 'AC', color: '#FBBF24' },
  { mat: '2026003', nome: 'Bruno Lima',    turma: '7F', xp: 3120, lvl: 15, streak: 27, status: 'on',   media: 9.1, avatar: 'BL', color: '#10B981' },
  { mat: '2026004', nome: 'Carlos Mota',   turma: '7F', xp: 1450, lvl: 8,  streak: 0,  status: 'risk', media: 4.7, avatar: 'CM', color: '#EF4444' },
  { mat: '2026005', nome: 'Diana Souza',   turma: '8F', xp: 2890, lvl: 14, streak: 22, status: 'on',   media: 8.8, avatar: 'DS', color: '#8B5CF6' },
  { mat: '2026006', nome: 'Eduardo Reis',  turma: '8F', xp: 1670, lvl: 9,  streak: 6,  status: 'warn', media: 6.4, avatar: 'ER', color: '#0EA5E9' },
  { mat: '2026007', nome: 'Fernanda Pinto',turma: '9F', xp: 3450, lvl: 17, streak: 31, status: 'on',   media: 9.4, avatar: 'FP', color: '#F97316' },
  { mat: '2026008', nome: 'Gabriel Sá',    turma: '9F', xp: 720,  lvl: 4,  streak: 0,  status: 'risk', media: 3.9, avatar: 'GS', color: '#EC4899' },
  { mat: '2026009', nome: 'Helena Vaz',    turma: '1M', xp: 2110, lvl: 11, streak: 14, status: 'on',   media: 7.9, avatar: 'HV', color: '#14B8A6' },
  { mat: '2026010', nome: 'Igor Brandão',  turma: '1M', xp: 1990, lvl: 10, streak: 9,  status: 'warn', media: 6.8, avatar: 'IB', color: '#A855F7' },
  { mat: '2026011', nome: 'Júlia Nunes',   turma: '2M', xp: 2780, lvl: 13, streak: 19, status: 'on',   media: 8.6, avatar: 'JN', color: '#06B6D4' },
  { mat: '2026012', nome: 'Lucas Fonseca', turma: '3M', xp: 3680, lvl: 18, streak: 35, status: 'on',   media: 9.6, avatar: 'LF', color: '#84CC16' },
];

// SparkBar — small bar chart
function SparkBar({ data, max, color, h=44, gap=4 }) {
  const m = max || Math.max(...data);
  return (
    <div style={{ display:'flex', alignItems:'flex-end', gap, height:h }}>
      {data.map((v,i)=>(
        <div key={i} style={{ flex:1, height:`${(v/m)*100}%`, background:color, borderRadius:'3px 3px 0 0', minHeight:2 }}/>
      ))}
    </div>
  );
}

// Ring — circular progress
function Ring({ value, max=100, size=64, stroke=6, color='#4F46E5', track='#E2E8F0', children }) {
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const off = c - (value/max) * c;
  return (
    <div style={{ position:'relative', width:size, height:size }}>
      <svg width={size} height={size} style={{ transform:'rotate(-90deg)' }}>
        <circle cx={size/2} cy={size/2} r={r} fill="none" stroke={track} strokeWidth={stroke}/>
        <circle cx={size/2} cy={size/2} r={r} fill="none" stroke={color} strokeWidth={stroke} strokeDasharray={c} strokeDashoffset={off} strokeLinecap="round"/>
      </svg>
      <div style={{ position:'absolute', inset:0, display:'grid', placeItems:'center', fontWeight:700 }}>{children}</div>
    </div>
  );
}

// Avatar component
function Avatar({ a, size=40, ring=false, ringColor }) {
  const s = { width:size, height:size, borderRadius:'50%', background:a.color, color:'#fff', display:'grid', placeItems:'center', fontWeight:800, fontSize:size*0.36, letterSpacing:'-0.02em', flexShrink:0 };
  if (ring) {
    return (
      <div style={{ position:'relative', padding:3, borderRadius:'50%', background:`conic-gradient(${ringColor||'#FBBF24'} ${(a.lvl/20)*360}deg, #E2E8F0 0)`, display:'inline-block' }}>
        <div style={{ background:'#fff', padding:2, borderRadius:'50%' }}>
          <div style={s}>{a.avatar}</div>
        </div>
      </div>
    );
  }
  return <div style={s}>{a.avatar}</div>;
}

Object.assign(window, { TOKENS, I, TURMAS, MATERIAS, ALUNOS, SparkBar, Ring, Avatar });
