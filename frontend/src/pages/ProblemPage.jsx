import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import Editor from '@monaco-editor/react';

const API = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// ─── Difficulty badge colors ─────────────────────────────────────────────────
const DIFF_COLORS = {
  easy:   { bg: 'rgba(16,185,129,0.15)', color: '#34d399', border: '#10b981' },
  medium: { bg: 'rgba(245,158,11,0.15)',  color: '#fbbf24', border: '#f59e0b' },
  hard:   { bg: 'rgba(239,68,68,0.15)',   color: '#f87171', border: '#ef4444' },
};

// ─── Mistake type titles ──────────────────────────────────────────────────────
const MISTAKE_TITLES = {
  syntax_error:                "Syntax Error",
  index_error:                 "Index Out of Bounds",
  recursion_error:             "Infinite Recursion",
  logic_error:                 "Algorithm Logic Issue",
  potential_missing_base_case: "Missing Base Case",
  shadowing_builtin:           "Shadowing Built-in",
  invalid_len_method:          "Invalid .length() / .size()",
  invalid_keyword_elsif:       "Invalid 'elsif' Keyword",
  incorrect_none_comparison:   "Wrong None Comparison",
};

// ─── DNA chart colors ────────────────────────────────────────────────────────
const MISTAKE_BAR_COLORS = {
  syntax_error:                '#ef4444',
  index_error:                 '#f97316',
  recursion_error:             '#a855f7',
  logic_error:                 '#3b82f6',
  potential_missing_base_case: '#ec4899',
  shadowing_builtin:           '#f59e0b',
  invalid_len_method:          '#06b6d4',
  invalid_keyword_elsif:       '#84cc16',
  incorrect_none_comparison:   '#6366f1',
};

const TOPIC_COLORS = ['#38bdf8','#818cf8','#c084fc','#34d399','#fbbf24','#f87171','#fb923c'];

// ─── Helper ───────────────────────────────────────────────────────────────────
function Badge({ label, type = 'topic' }) {
  const dc = DIFF_COLORS[label] || { bg: 'rgba(99,102,241,0.15)', color: '#a5b4fc', border: '#6366f1' };
  return (
    <span style={{
      padding: '2px 8px', borderRadius: 4, fontSize: '0.65rem', fontWeight: 700,
      textTransform: 'uppercase', letterSpacing: '0.04em',
      background: dc.bg, color: dc.color, border: `1px solid ${dc.border}`,
    }}>
      {label}
    </span>
  );
}

// ─── Auth Screen ──────────────────────────────────────────────────────────────
function AuthScreen({ onAuth }) {
  const [mode, setMode]       = useState('login');
  const [email, setEmail]     = useState('');
  const [name, setName]       = useState('');
  const [pass, setPass]       = useState('');
  const [err, setErr]         = useState('');
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setErr(''); setLoading(true);
    try {
      const endpoint = mode === 'login' ? 'login' : 'signup';
      const payload  = mode === 'login' ? { email, password: pass } : { email, name, password: pass };
      const res = await axios.post(`${API}/api/auth/${endpoint}`, payload);
      localStorage.setItem('token',     res.data.token);
      localStorage.setItem('user_id',   res.data.user_id);
      localStorage.setItem('user_name', res.data.name);
      onAuth(res.data);
    } catch (ex) {
      setErr(ex.response?.data?.detail || 'Authentication failed.');
    } finally { setLoading(false); }
  };

  return (
    <div style={{
      minHeight:'100vh', display:'flex', alignItems:'center', justifyContent:'center',
      background:'#05070c',
      backgroundImage:'radial-gradient(at 0% 0%, hsla(244,70%,20%,0.4) 0,transparent 55%), radial-gradient(at 100% 100%, hsla(266,70%,20%,0.3) 0,transparent 55%)',
      fontFamily:"'Outfit',sans-serif",
    }}>
      <div style={{
        width: 400, padding:'36px 40px', borderRadius:16,
        background:'rgba(15,23,42,0.65)', backdropFilter:'blur(18px)',
        border:'1px solid rgba(255,255,255,0.08)',
        boxShadow:'0 24px 48px rgba(0,0,0,0.55)',
      }}>
        {/* Logo */}
        <div style={{
          fontSize:'2rem', fontWeight:700, textAlign:'center', marginBottom:4,
          background:'linear-gradient(135deg,#38bdf8 0%,#818cf8 50%,#c084fc 100%)',
          WebkitBackgroundClip:'text', WebkitTextFillColor:'transparent',
        }}>Coding Tutor AI</div>
        <p style={{textAlign:'center', color:'#94a3b8', fontSize:'0.85rem', marginBottom:24}}>
          Learn Python with AI-powered mistake detection
        </p>

        {err && (
          <div style={{
            background:'rgba(239,68,68,0.1)', border:'1px solid #ef4444',
            color:'#f87171', padding:'10px 14px', borderRadius:8, fontSize:'0.85rem',
            textAlign:'center', marginBottom:14,
          }}>{err}</div>
        )}

        <form onSubmit={submit} style={{display:'flex', flexDirection:'column', gap:14}}>
          {mode === 'signup' && (
            <label style={{display:'flex', flexDirection:'column', gap:5}}>
              <span style={{fontSize:'0.8rem', color:'#94a3b8'}}>Your Name</span>
              <input value={name} onChange={e=>setName(e.target.value)} required
                placeholder="e.g. John Doe" style={inputStyle} />
            </label>
          )}
          <label style={{display:'flex', flexDirection:'column', gap:5}}>
            <span style={{fontSize:'0.8rem', color:'#94a3b8'}}>Email</span>
            <input type="email" value={email} onChange={e=>setEmail(e.target.value)} required
              placeholder="email@example.com" style={inputStyle} />
          </label>
          <label style={{display:'flex', flexDirection:'column', gap:5}}>
            <span style={{fontSize:'0.8rem', color:'#94a3b8'}}>Password</span>
            <input type="password" value={pass} onChange={e=>setPass(e.target.value)} required
              placeholder="••••••••" style={inputStyle} />
          </label>
          <button type="submit" disabled={loading} style={{
            marginTop:8, padding:'12px', borderRadius:8, border:'none', cursor:loading?'not-allowed':'pointer',
            background: loading ? '#334155' : 'linear-gradient(135deg,#6366f1,#a855f7)',
            color:'#fff', fontWeight:700, fontSize:'0.95rem',
            boxShadow:'0 4px 15px rgba(99,102,241,0.3)', transition:'opacity 0.2s',
          }}>
            {loading ? 'Authenticating…' : mode === 'login' ? 'Log In' : 'Create Account'}
          </button>
        </form>

        <p style={{textAlign:'center', fontSize:'0.85rem', color:'#94a3b8', marginTop:16}}>
          {mode === 'login'
            ? <>Don't have an account? <span onClick={()=>{setMode('signup');setErr('');}} style={linkStyle}>Sign Up</span></>
            : <>Already have an account? <span onClick={()=>{setMode('login');setErr('');}} style={linkStyle}>Log In</span></>}
        </p>
      </div>
    </div>
  );
}

const inputStyle = {
  padding:'10px 14px', background:'#090d16', border:'1px solid #334155',
  borderRadius:8, color:'#f1f5f9', outline:'none', fontSize:'0.9rem',
  transition:'border-color 0.2s', fontFamily:"'Outfit',sans-serif",
};
const linkStyle = { color:'#38bdf8', cursor:'pointer', fontWeight:600, textDecoration:'underline' };


// ─── Main App ─────────────────────────────────────────────────────────────────
export default function ProblemPage() {
  // Auth
  const [token,    setToken]    = useState(localStorage.getItem('token')     || '');
  const [userId,   setUserId]   = useState(localStorage.getItem('user_id')   || '');
  const [userName, setUserName] = useState(localStorage.getItem('user_name') || '');

  // Problems
  const [problems,  setProblems]  = useState([]);
  const [problem,   setProblem]   = useState(null);
  const [code,      setCode]      = useState('');

  // Submission
  const [result,   setResult]   = useState(null);
  const [loading,  setLoading]  = useState(false);

  // Hint & Explanation
  const [hint,              setHint]              = useState(null);
  const [loadingHint,       setLoadingHint]       = useState(false);
  const [explanation,       setExplanation]       = useState(null);
  const [loadingExplain,    setLoadingExplain]    = useState(false);
  const [explainMistake,    setExplainMistake]    = useState(null); // which mistake to explain

  // Dashboards
  const [progress,        setProgress]        = useState(null);
  const [mistakeDna,      setMistakeDna]      = useState(null);
  const [showProgress,    setShowProgress]    = useState(false);
  const [showDna,         setShowDna]         = useState(false);

  // Sidebar
  const [sidebarOpen,     setSidebarOpen]     = useState(true);
  const [mobileSidebar,   setMobileSidebar]   = useState(false);
  const [search,          setSearch]          = useState('');
  const [diffFilter,      setDiffFilter]      = useState('all');

  const hdrs = useCallback(() =>
    token ? { headers: { Authorization: `Bearer ${token}` } } : {}
  , [token]);

  // ── Data fetchers ──────────────────────────────────────────────────────────
  const loadProblems = useCallback(async () => {
    try {
      const r = await axios.get(`${API}/api/problems/`, hdrs());
      setProblems(r.data);
    } catch (e) { console.error(e); }
  }, [hdrs]);

  const loadProblem = useCallback(async (id) => {
    try {
      const r = await axios.get(`${API}/api/problems/${id}`, hdrs());
      setProblem(r.data);
      setCode(r.data.starter_code || '');
      setResult(null); setHint(null); setExplanation(null); setExplainMistake(null);
      setMobileSidebar(false); // close mobile drawer on selection
    } catch (e) { console.error(e); }
  }, [hdrs]);

  const loadProgress = useCallback(async () => {
    try {
      const r = await axios.get(`${API}/api/progress/user/${userId}`, hdrs());
      setProgress(r.data);
    } catch (e) { console.error(e); }
  }, [hdrs, userId]);

  const loadDna = useCallback(async () => {
    try {
      const r = await axios.get(`${API}/api/mistake-dna/user/${userId}`, hdrs());
      setMistakeDna(r.data);
    } catch (e) { console.error(e); }
  }, [hdrs, userId]);

  useEffect(() => {
    if (!userId || !token) return;
    loadProblems();
    loadProgress();
    loadDna();
    // Load recommended problem on first load
    axios.get(`${API}/api/problems/recommended/${userId}`, hdrs())
      .then(r => loadProblem(r.data.id))
      .catch(()  => loadProblem('prob_easy_1'));
  }, [userId, token]); // eslint-disable-line

  // ── Auth ──────────────────────────────────────────────────────────────────
  const handleAuth = ({ token: t, user_id: u, name: n }) => {
    setToken(t); setUserId(u); setUserName(n);
  };

  const handleLogout = () => {
    ['token','user_id','user_name'].forEach(k => localStorage.removeItem(k));
    setToken(''); setUserId(''); setUserName('');
    setProblems([]); setProblem(null); setProgress(null); setMistakeDna(null);
  };

  // ── Submit ────────────────────────────────────────────────────────────────
  const handleSubmit = async () => {
    setLoading(true); setHint(null); setExplanation(null); setExplainMistake(null);
    try {
      const r = await axios.post(`${API}/api/execute`, {
        code, problem_id: problem.id, user_id: userId,
      }, hdrs());
      setResult(r.data);
      loadProgress(); loadDna();
    } catch (ex) {
      setResult({ error: ex.response?.data?.detail || ex.message });
    } finally { setLoading(false); }
  };

  // ── Hint ──────────────────────────────────────────────────────────────────
  const handleHint = async () => {
    setLoadingHint(true);
    try {
      const r = await axios.post(`${API}/api/hints/generate`, {
        problem_description: problem.description,
        user_code:    code,
        test_results: result.results,
        mistakes:     result.mistakes || [],
      }, hdrs());
      setHint(r.data.hint);
    } catch (e) { setHint('Could not generate hint. Please try again.'); }
    setLoadingHint(false);
  };

  // ── Explain Mistake ───────────────────────────────────────────────────────
  const handleExplain = async (mistakeType) => {
    setLoadingExplain(true); setExplainMistake(mistakeType); setExplanation(null);
    try {
      const r = await axios.post(`${API}/api/hints/explain`, {
        problem_description: problem.description,
        user_code:    code,
        test_results: result.results,
        mistake_type: mistakeType,
      }, hdrs());
      setExplanation(r.data.explanation);
    } catch (e) { setExplanation('Could not generate explanation. Please try again.'); }
    setLoadingExplain(false);
  };

  // ── Sidebar filter ────────────────────────────────────────────────────────
  const filtered = problems.filter(p => {
    const matchSearch = p.title.toLowerCase().includes(search.toLowerCase());
    const matchDiff   = diffFilter === 'all' || p.difficulty === diffFilter;
    return matchSearch && matchDiff;
  });

  // ── Not logged in → Auth screen ───────────────────────────────────────────
  if (!token || !userId) return <AuthScreen onAuth={handleAuth} />;

  // ── Render ────────────────────────────────────────────────────────────────
  return (
    <>
      {/* ── Global CSS ── */}
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #090d16; color: #f1f5f9; font-family: 'Outfit', sans-serif; }

        :root {
          --bg0: #05070c;
          --bg1: #090d16;
          --bg2: #0f172a;
          --bg3: #1e293b;
          --border: #1e293b;
          --border2: #334155;
          --accent: #6366f1;
          --accent2: #a855f7;
          --text1: #f1f5f9;
          --text2: #94a3b8;
          --text3: #64748b;
          --success: #10b981;
          --error: #ef4444;
          --warn: #f59e0b;
        }

        /* ── Scrollbar ── */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }

        /* ── Layout ── */
        .app { display: flex; flex-direction: column; height: 100vh; overflow: hidden; }

        /* ── Header ── */
        .hdr {
          display: flex; align-items: center; justify-content: space-between;
          padding: 0 20px; height: 54px; flex-shrink: 0;
          background: rgba(15,23,42,0.85); backdrop-filter: blur(12px);
          border-bottom: 1px solid var(--border); position: relative; z-index: 100;
        }
        .hdr-left  { display: flex; align-items: center; gap: 10px; }
        .hdr-right { display: flex; align-items: center; gap: 12px; }
        .logo {
          font-size: 1.4rem; font-weight: 700;
          background: linear-gradient(135deg,#38bdf8 0%,#818cf8 50%,#c084fc 100%);
          -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .icon-btn {
          background: transparent; border: 1px solid var(--border2);
          color: var(--text1); border-radius: 6px; width: 32px; height: 32px;
          cursor: pointer; display: flex; align-items: center; justify-content: center;
          font-size: 1rem; transition: background 0.15s;
        }
        .icon-btn:hover { background: var(--bg3); }
        .user-chip { font-size: 0.85rem; color: var(--text2); }
        .user-chip strong { color: var(--text1); }
        .logout-btn {
          background: transparent; border: 1px solid var(--error); color: #f87171;
          padding: 5px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 600;
          cursor: pointer; transition: background 0.2s, color 0.2s;
        }
        .logout-btn:hover { background: var(--error); color: #fff; }

        /* ── Body ── */
        .body { display: flex; flex: 1; overflow: hidden; }

        /* ── Sidebar ── */
        .sidebar {
          width: 280px; flex-shrink: 0;
          background: var(--bg0); border-right: 1px solid var(--border);
          display: flex; flex-direction: column; overflow: hidden;
          transition: width 0.22s ease, opacity 0.22s ease;
        }
        .sidebar.collapsed { width: 0; opacity: 0; pointer-events: none; }
        .sidebar-inner {
          width: 280px; padding: 16px; display: flex; flex-direction: column;
          gap: 10px; overflow-y: auto; height: 100%;
        }
        .sb-title { font-size: 0.7rem; font-weight: 700; color: var(--text3); text-transform: uppercase; letter-spacing: 0.08em; }
        .sb-search {
          width: 100%; padding: 8px 12px; background: var(--bg2);
          border: 1px solid var(--border2); border-radius: 8px;
          color: var(--text1); font-size: 0.85rem; outline: none;
          transition: border-color 0.2s; font-family: 'Outfit', sans-serif;
        }
        .sb-search:focus { border-color: var(--accent); }
        .sb-filters { display: flex; gap: 5px; flex-wrap: wrap; }
        .sb-filter {
          padding: 3px 9px; border-radius: 5px; border: 1px solid var(--border2);
          background: var(--bg2); color: var(--text2); font-size: 0.7rem;
          font-weight: 700; text-transform: capitalize; cursor: pointer;
          transition: all 0.15s;
        }
        .sb-filter:hover { border-color: var(--text3); }
        .sb-filter.active { background: var(--accent); border-color: var(--accent); color: #fff; }
        .prob-list { display: flex; flex-direction: column; gap: 6px; }
        .prob-item {
          padding: 10px 12px; border: 1px solid var(--border); border-radius: 8px;
          background: var(--bg2); cursor: pointer; text-align: left; width: 100%;
          transition: border-color 0.15s, background 0.15s;
        }
        .prob-item:hover  { border-color: var(--accent); background: rgba(99,102,241,0.05); }
        .prob-item.active { border-color: var(--accent); background: rgba(99,102,241,0.1); }
        .prob-item-title  { font-size: 0.85rem; font-weight: 600; margin-bottom: 5px; color: var(--text1); }
        .prob-item-tags   { display: flex; gap: 5px; }

        /* Mobile sidebar overlay */
        .mob-overlay {
          display: none; position: fixed; inset: 0; z-index: 200;
          background: rgba(0,0,0,0.6); backdrop-filter: blur(4px);
        }
        .mob-drawer {
          position: fixed; top: 0; left: 0; bottom: 0; width: 300px; z-index: 201;
          background: var(--bg0); border-right: 1px solid var(--border);
          display: flex; flex-direction: column; transform: translateX(-100%);
          transition: transform 0.25s ease; overflow-y: auto;
        }
        .mob-drawer.open { transform: translateX(0); }

        /* ── Workspace ── */
        .workspace {
          flex: 1; overflow-y: auto; padding: 20px;
          display: flex; flex-direction: column; gap: 18px;
        }

        /* ── Cards ── */
        .card {
          background: var(--bg2); border: 1px solid var(--border);
          border-radius: 12px; padding: 18px 20px;
        }
        .card-title {
          font-size: 0.8rem; font-weight: 700; color: var(--text2);
          text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 12px;
          display: flex; align-items: center; gap: 6px;
        }
        .prob-hdr {
          display: flex; justify-content: space-between; align-items: flex-start;
          gap: 12px; flex-wrap: wrap; margin-bottom: 12px;
          border-bottom: 1px solid var(--border2); padding-bottom: 12px;
        }
        .prob-hdr h2 { font-size: 1.3rem; color: #38bdf8; }
        .prob-desc { font-size: 0.9rem; color: #cbd5e1; line-height: 1.65; white-space: pre-wrap; }

        /* ── Code grid ── */
        .code-grid {
          display: grid; grid-template-columns: 1fr 1fr; gap: 18px;
        }
        @media (max-width: 900px) {
          .code-grid { grid-template-columns: 1fr; }
          .sidebar { display: none; }
          .mob-overlay { display: block; }
        }

        /* ── Editor ── */
        .editor-wrap {
          border: 1px solid var(--border2); border-radius: 10px; overflow: hidden;
        }

        /* ── Buttons ── */
        .btn-primary {
          padding: 10px 22px; border-radius: 8px; border: none; cursor: pointer;
          font-weight: 700; font-size: 0.9rem; color: #fff;
          background: linear-gradient(135deg, #6366f1, #a855f7);
          box-shadow: 0 4px 14px rgba(99,102,241,0.3);
          transition: opacity 0.2s, transform 0.1s, box-shadow 0.2s;
        }
        .btn-primary:hover { opacity: 0.9; box-shadow: 0 6px 20px rgba(99,102,241,0.4); }
        .btn-primary:active { transform: scale(0.97); }
        .btn-primary:disabled { background: var(--bg3); color: var(--text3); cursor: not-allowed; box-shadow: none; }

        .btn-warn {
          padding: 9px 18px; border-radius: 8px; border: none; cursor: pointer;
          font-weight: 700; font-size: 0.85rem; color: #fff;
          background: linear-gradient(135deg,#f59e0b,#f97316);
          box-shadow: 0 4px 12px rgba(245,158,11,0.25);
          transition: opacity 0.2s, box-shadow 0.2s;
        }
        .btn-warn:hover { opacity: 0.9; box-shadow: 0 6px 18px rgba(245,158,11,0.35); }
        .btn-warn:disabled { background: var(--bg3); color: var(--text3); cursor: not-allowed; box-shadow: none; }

        .btn-purple {
          padding: 9px 18px; border-radius: 8px; border: none; cursor: pointer;
          font-weight: 700; font-size: 0.85rem; color: #fff;
          background: linear-gradient(135deg,#a855f7,#ec4899);
          box-shadow: 0 4px 12px rgba(168,85,247,0.25);
          transition: opacity 0.2s, box-shadow 0.2s;
        }
        .btn-purple:hover { opacity: 0.9; }
        .btn-purple:disabled { background: var(--bg3); color: var(--text3); cursor: not-allowed; box-shadow: none; }

        .btn-ghost {
          padding: 5px 12px; border-radius: 6px; border: 1px solid var(--border2);
          background: transparent; color: var(--text2); cursor: pointer; font-size: 0.75rem;
          font-weight: 600; transition: background 0.15s, color 0.15s;
        }
        .btn-ghost:hover { background: var(--bg3); color: var(--text1); }

        /* ── Alerts ── */
        .alert {
          padding: 12px 18px; border-radius: 8px; font-weight: 600;
          display: flex; align-items: center; gap: 10px; font-size: 0.9rem;
          margin-bottom: 16px;
        }
        .alert.success { background: rgba(16,185,129,0.12); border: 1px solid #10b981; color: #34d399; }
        .alert.error   { background: rgba(239,68,68,0.12);  border: 1px solid #ef4444; color: #f87171; }

        /* ── Test cases ── */
        .tc-card {
          background: var(--bg1); border: 1px solid var(--border); border-radius: 8px;
          padding: 12px 14px; margin-bottom: 10px;
        }
        .tc-hdr { display: flex; justify-content: space-between; font-weight: 600; font-size: 0.85rem; margin-bottom: 8px; }
        .tc-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
        .tc-label { font-size: 0.65rem; color: var(--text3); text-transform: uppercase; margin-bottom: 3px; }
        .tc-val {
          font-family: 'Fira Code', monospace; font-size: 0.78rem;
          background: var(--bg2); padding: 4px 8px; border-radius: 4px; color: #cbd5e1;
          display: block; word-break: break-all;
        }

        /* ── Mistake card ── */
        .mistake-card {
          border-radius: 0 8px 8px 0; padding: 14px 16px; margin-bottom: 10px;
          background: rgba(245,158,11,0.07);
          border: 1px solid rgba(245,158,11,0.18); border-left: 4px solid #f59e0b;
        }
        .mistake-card.critical {
          background: rgba(239,68,68,0.07);
          border: 1px solid rgba(239,68,68,0.18); border-left: 4px solid #ef4444;
        }
        .mistake-title { font-weight: 700; font-size: 0.88rem; color: #f59e0b; margin-bottom: 5px; display: flex; align-items: center; gap: 6px; }
        .mistake-card.critical .mistake-title { color: #f87171; }
        .mistake-msg { font-size: 0.85rem; color: #cbd5e1; line-height: 1.5; }

        /* ── Hint / Explanation boxes ── */
        .hint-box {
          margin-top: 14px; padding: 14px 16px; border-radius: 8px;
          background: rgba(245,158,11,0.06); border: 1px solid rgba(245,158,11,0.2);
          color: #fde68a; font-size: 0.87rem; line-height: 1.65;
        }
        .explain-box {
          margin-top: 14px; padding: 14px 16px; border-radius: 8px;
          background: rgba(168,85,247,0.07); border: 1px solid rgba(168,85,247,0.25);
          color: #e9d5ff; font-size: 0.87rem; line-height: 1.65;
        }
        .explain-box strong { color: #c084fc; }

        /* ── Progress Section ── */
        .prog-section { }
        .toggle-row { display: flex; gap: 8px; flex-wrap: wrap; }
        .stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px,1fr)); gap: 12px; margin-top: 14px; }
        .stat-box { background: var(--bg1); border: 1px solid var(--border); border-radius: 8px; padding: 14px; text-align: center; }
        .stat-num { font-size: 2rem; font-weight: 700; color: #38bdf8; }
        .stat-lbl { font-size: 0.78rem; color: var(--text2); margin-top: 3px; }

        /* ── Topic mastery bars ── */
        .mastery-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px,1fr)); gap: 10px; margin-top: 14px; }
        .mastery-item { background: var(--bg1); border: 1px solid var(--border); border-radius: 8px; padding: 12px 14px; }
        .mastery-hdr  { display: flex; justify-content: space-between; font-size: 0.82rem; font-weight: 600; text-transform: capitalize; margin-bottom: 7px; }
        .bar-track { height: 6px; border-radius: 3px; background: var(--bg3); overflow: hidden; margin-bottom: 5px; }
        .bar-fill  { height: 100%; border-radius: 3px; transition: width 0.6s ease; }
        .mastery-sub { font-size: 0.72rem; color: var(--text3); }

        /* ── DNA section ── */
        .dna-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-top: 12px; }
        @media (max-width: 700px) { .dna-grid { grid-template-columns: 1fr; } }
        .dna-col-title { font-size: 0.75rem; font-weight: 700; color: var(--text2); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 10px; }

        /* Mastery ring placeholder (circle) */
        .ring-row { display: flex; flex-wrap: wrap; gap: 10px; }
        .ring-item {
          display: flex; flex-direction: column; align-items: center; gap: 4px;
          background: var(--bg1); border: 1px solid var(--border); border-radius: 8px;
          padding: 10px 12px; min-width: 80px; flex: 1;
        }
        .ring-circle {
          width: 48px; height: 48px; border-radius: 50%; display: flex;
          align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 700;
          color: #fff; position: relative;
        }
        .ring-label { font-size: 0.68rem; color: var(--text2); text-transform: capitalize; }

        /* Mistake bar chart */
        .mistake-bar-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
        .mistake-bar-label { font-size: 0.72rem; color: var(--text2); width: 150px; flex-shrink: 0; text-transform: capitalize; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .mistake-bar-track { flex: 1; height: 8px; border-radius: 4px; background: var(--bg3); overflow: hidden; }
        .mistake-bar-fill  { height: 100%; border-radius: 4px; transition: width 0.5s ease; }
        .mistake-bar-count { font-size: 0.72rem; color: var(--text3); width: 24px; text-align: right; }

        .dna-recommend {
          margin-top: 14px; padding: 12px 16px; border-radius: 8px;
          background: rgba(99,102,241,0.08); border: 1px solid rgba(99,102,241,0.25);
          color: #cbd5e1; font-size: 0.85rem; line-height: 1.55;
        }
        .dna-recommend strong { color: #a5b4fc; }

        /* ── Empty state ── */
        .empty-state { color: var(--text3); text-align: center; padding: 80px 20px; font-size: 0.9rem; }

        /* ── Responsive ── */
        @media (max-width: 640px) {
          .workspace { padding: 12px; gap: 14px; }
          .card { padding: 14px 14px; }
          .prob-hdr h2 { font-size: 1.1rem; }
          .hdr { padding: 0 12px; }
          .logo { font-size: 1.1rem; }
          .user-chip { display: none; }
          .dna-grid { grid-template-columns: 1fr; }
          .code-grid { grid-template-columns: 1fr; }
        }
      `}</style>

      <div className="app">
        {/* ─── Header ──────────────────────────────────────────────────── */}
        <header className="hdr">
          <div className="hdr-left">
            {/* Desktop sidebar toggle */}
            <button className="icon-btn" onClick={() => setSidebarOpen(o => !o)} title="Toggle sidebar" style={{display:'flex'}}>
              {sidebarOpen ? '◀' : '▶'}
            </button>
            {/* Mobile hamburger — only visible on small screens via CSS */}
            <button className="icon-btn"
              onClick={() => setMobileSidebar(true)}
              title="Problems"
              style={{display:'none'}}
              id="mob-menu-btn"
            >☰</button>
            <span className="logo">Coding Tutor AI</span>
          </div>
          <div className="hdr-right">
            <span className="user-chip">👋 <strong>{userName}</strong></span>
            <button className="logout-btn" onClick={handleLogout}>Log Out</button>
          </div>
        </header>

        {/* Inject mobile menu btn visibility via a style block — avoids media query in JS */}
        <style>{`
          @media (max-width: 900px) {
            #mob-menu-btn { display: flex !important; }
          }
        `}</style>

        {/* ─── Mobile sidebar overlay + drawer ────────────────────────── */}
        <div className="mob-overlay" onClick={() => setMobileSidebar(false)}
          style={{display: mobileSidebar ? 'block' : 'none'}} />
        <div className={`mob-drawer ${mobileSidebar ? 'open' : ''}`}>
          <div style={{padding:'16px', borderBottom:'1px solid var(--border)', display:'flex', justifyContent:'space-between', alignItems:'center'}}>
            <span style={{fontWeight:700, fontSize:'0.9rem', color:'var(--text2)'}}>Problem Bank</span>
            <button className="icon-btn" onClick={() => setMobileSidebar(false)}>✕</button>
          </div>
          <SidebarContents
            search={search} setSearch={setSearch}
            diffFilter={diffFilter} setDiffFilter={setDiffFilter}
            filtered={filtered} problem={problem} loadProblem={loadProblem}
          />
        </div>

        <div className="body">
          {/* ─── Desktop sidebar ──────────────────────────────────────── */}
          <aside className={`sidebar ${sidebarOpen ? '' : 'collapsed'}`}>
            <div className="sidebar-inner">
              <SidebarContents
                search={search} setSearch={setSearch}
                diffFilter={diffFilter} setDiffFilter={setDiffFilter}
                filtered={filtered} problem={problem} loadProblem={loadProblem}
              />
            </div>
          </aside>

          {/* ─── Workspace ───────────────────────────────────────────── */}
          <main className="workspace">
            {problem ? (
              <>
                {/* Problem description */}
                <div className="card">
                  <div className="prob-hdr">
                    <h2>{problem.title}</h2>
                    <div style={{display:'flex', gap:6, flexShrink:0}}>
                      <Badge label={problem.difficulty} />
                      <Badge label={problem.topic} />
                    </div>
                  </div>
                  <p className="prob-desc">{problem.description}</p>
                </div>

                {/* Editor + Results */}
                <div className="code-grid">
                  {/* Editor column */}
                  <div style={{display:'flex', flexDirection:'column', gap:10}}>
                    <div className="card-title">💻 Code Editor (Python)</div>
                    <div className="editor-wrap">
                      <Editor
                        height="420px"
                        defaultLanguage="python"
                        theme="vs-dark"
                        value={code}
                        onChange={v => setCode(v || '')}
                        options={{
                          fontSize: 16,
                          fontFamily: "'Fira Code', 'Cascadia Code', 'Consolas', 'Monaco', monospace",
                          fontLigatures: true,
                          minimap: {enabled: false},
                          scrollBeyondLastLine: false,
                          lineNumbers: 'on',
                          automaticLayout: true,
                          tabSize: 4,
                          padding: {top: 12, bottom: 12},
                          wordWrap: 'on',
                        }}
                      />
                    </div>
                    <button onClick={handleSubmit} disabled={loading} className="btn-primary" style={{alignSelf:'flex-start'}}>
                      {loading ? '⏳ Running Tests…' : '🚀 Submit Code'}
                    </button>
                  </div>

                  {/* Results column */}
                  <div style={{display:'flex', flexDirection:'column', gap:10}}>
                    <div className="card-title">📊 Output & Feedback</div>
                    <div className="card" style={{flex:1, minHeight:420, overflowY:'auto'}}>
                      {!result ? (
                        <div className="empty-state">Submit your solution to see results here.</div>
                      ) : result.error ? (
                        <div className="alert error">⚠️ {result.error}</div>
                      ) : (
                        <>
                          {/* Pass / fail banner */}
                          <div className={`alert ${result.passed ? 'success' : 'error'}`}>
                            {result.passed ? '✓ All tests passed! Great work!' : `✗ Failed ${result.total_count - result.passed_count} of ${result.total_count} tests.`}
                          </div>

                          {/* Mistake cards */}
                          {result.mistake_details?.length > 0 && (
                            <div style={{marginBottom:14}}>
                              <div className="card-title" style={{color:'#f59e0b'}}>🧠 Mistake DNA Insights</div>
                              {result.mistake_details.map((m, i) => {
                                const isCritical = ['syntax_error','recursion_error'].includes(m.type);
                                return (
                                  <div key={i} className={`mistake-card ${isCritical ? 'critical' : ''}`}>
                                    <div className="mistake-title">
                                      {isCritical ? '⚠️' : '💡'} {MISTAKE_TITLES[m.type] || m.type}
                                    </div>
                                    <div className="mistake-msg">{m.message}</div>
                                    {/* Per-mistake explain button */}
                                    <button
                                      className="btn-ghost"
                                      style={{marginTop:8}}
                                      disabled={loadingExplain && explainMistake === m.type}
                                      onClick={() => handleExplain(m.type)}
                                    >
                                      {loadingExplain && explainMistake === m.type ? '⏳ Explaining…' : '🔍 Explain This'}
                                    </button>
                                    {explanation && explainMistake === m.type && (
                                      <div className="explain-box" style={{marginTop:8}}>
                                        <strong>Explanation:</strong> {explanation}
                                      </div>
                                    )}
                                  </div>
                                );
                              })}
                            </div>
                          )}

                          {/* Test cases */}
                          <div className="card-title" style={{marginBottom:8}}>📂 Test Cases</div>
                          {result.results.map((r, i) => (
                            <div key={i} className="tc-card">
                              <div className="tc-hdr">
                                <span>Test {i + 1}</span>
                                <span style={{color: r.passed ? '#34d399' : '#f87171'}}>{r.passed ? '✓ Passed' : '✗ Failed'}</span>
                              </div>
                              <div className="tc-grid">
                                <div>
                                  <div className="tc-label">Input</div>
                                  <span className="tc-val">{r.input || '(none)'}</span>
                                </div>
                                <div>
                                  <div className="tc-label">Expected</div>
                                  <span className="tc-val">{r.expected}</span>
                                </div>
                              </div>
                              <div style={{marginTop:6}}>
                                <div className="tc-label">Got</div>
                                <span className="tc-val" style={{color: r.passed ? '#34d399' : '#f87171', background:'var(--bg0)'}}>
                                  {r.actual !== undefined && r.actual !== null ? String(r.actual) : '(no output)'}
                                </span>
                              </div>
                            </div>
                          ))}

                          {/* Hint + Explain buttons */}
                          {!result.passed && (
                            <div style={{display:'flex', gap:8, flexWrap:'wrap', marginTop:12}}>
                              <button className="btn-warn" onClick={handleHint} disabled={loadingHint}>
                                {loadingHint ? '⏳ Generating…' : '💡 Get AI Hint'}
                              </button>
                              {result.primary_mistake && result.primary_mistake !== 'no_mistake' && (
                                <button className="btn-purple" onClick={() => handleExplain(result.primary_mistake)} disabled={loadingExplain}>
                                  {loadingExplain ? '⏳ Explaining…' : '🔍 Explain My Mistake'}
                                </button>
                              )}
                            </div>
                          )}
                          {hint && <div className="hint-box"><strong>💡 AI Hint:</strong> {hint}</div>}
                          {explanation && !result.mistake_details?.some(m => m.type === explainMistake) && (
                            <div className="explain-box">
                              <strong>🔍 Explanation ({MISTAKE_TITLES[explainMistake] || explainMistake}):</strong><br />{explanation}
                            </div>
                          )}
                        </>
                      )}
                    </div>
                  </div>
                </div>

                {/* Progress & DNA */}
                <div className="card prog-section">
                  <div className="toggle-row">
                    <button className="btn-ghost" onClick={() => setShowProgress(o => !o)}>
                      {showProgress ? '🔼 Hide Stats' : '📈 My Progress'}
                    </button>
                    <button className="btn-ghost" onClick={() => setShowDna(o => !o)}>
                      {showDna ? '🔼 Hide DNA' : '🧬 Mistake DNA'}
                    </button>
                  </div>

                  {/* Progress stats */}
                  {showProgress && progress && (
                    <>
                      <div className="stat-grid">
                        <div className="stat-box">
                          <div className="stat-num">{progress.problems_solved}</div>
                          <div className="stat-lbl">Problems Solved</div>
                        </div>
                        <div className="stat-box">
                          <div className="stat-num">{progress.total_attempts}</div>
                          <div className="stat-lbl">Total Submissions</div>
                        </div>
                        <div className="stat-box">
                          <div className="stat-num" style={{fontSize:'1.5rem'}}>
                            {progress.total_attempts > 0
                              ? Math.round((progress.problems_solved / progress.total_attempts) * 100)
                              : 0}%
                          </div>
                          <div className="stat-lbl">Success Rate</div>
                        </div>
                      </div>

                      {progress.topics && Object.keys(progress.topics).length > 0 && (
                        <>
                          <div className="card-title" style={{marginTop:18, marginBottom:4}}>Topic Mastery</div>
                          <div className="mastery-grid">
                            {Object.entries(progress.topics).map(([topic, stats], idx) => {
                              const color = TOPIC_COLORS[idx % TOPIC_COLORS.length];
                              return (
                                <div key={topic} className="mastery-item">
                                  <div className="mastery-hdr">
                                    <span>{topic}</span>
                                    <span style={{color}}>{stats.mastery}%</span>
                                  </div>
                                  <div className="bar-track">
                                    <div className="bar-fill" style={{width:`${stats.mastery}%`, background:`linear-gradient(90deg, ${color}aa, ${color})`}} />
                                  </div>
                                  <div className="mastery-sub">{stats.solved}/{stats.attempts} solved</div>
                                </div>
                              );
                            })}
                          </div>
                        </>
                      )}
                    </>
                  )}

                  {/* Mistake DNA */}
                  {showDna && mistakeDna && (
                    <>
                      <div className="card-title" style={{marginTop:18, color:'#c084fc'}}>🧬 Mistake DNA Profile</div>
                      <div className="dna-grid">
                        {/* Mastery rings */}
                        <div>
                          <div className="dna-col-title">Topic Mastery</div>
                          <div className="ring-row">
                            {Object.entries(mistakeDna.mastery).map(([topic, score], idx) => {
                              const color = TOPIC_COLORS[idx % TOPIC_COLORS.length];
                              // gradient-conic not universally supported; use solid color background + text
                              const bg = `conic-gradient(${color} ${score}%, var(--bg3) 0)`;
                              return (
                                <div key={topic} className="ring-item">
                                  <div className="ring-circle" style={{background: bg}}>
                                    <div style={{
                                      position:'absolute', width:34, height:34, borderRadius:'50%',
                                      background:'var(--bg2)', display:'flex', alignItems:'center',
                                      justifyContent:'center', fontSize:'0.72rem', fontWeight:700, color,
                                    }}>{score}%</div>
                                  </div>
                                  <span className="ring-label">{topic}</span>
                                </div>
                              );
                            })}
                          </div>
                        </div>

                        {/* Mistake bars */}
                        <div>
                          <div className="dna-col-title">Mistake Patterns</div>
                          {(() => {
                            const entries = Object.entries(mistakeDna.mistakes).filter(([,v]) => v > 0);
                            const maxVal  = Math.max(1, ...entries.map(([,v]) => v));
                            if (entries.length === 0)
                              return <div style={{color:'var(--text3)', fontSize:'0.82rem'}}>No mistakes logged yet! 🎉</div>;
                            return entries.map(([type, count]) => {
                              const cleanKey = type.replace(/_errors$/, '');
                              const color    = MISTAKE_BAR_COLORS[cleanKey] || '#6366f1';
                              return (
                                <div key={type} className="mistake-bar-row">
                                  <div className="mistake-bar-label">{cleanKey.replace(/_/g,' ')}</div>
                                  <div className="mistake-bar-track">
                                    <div className="mistake-bar-fill" style={{width:`${(count/maxVal)*100}%`, background: color}} />
                                  </div>
                                  <div className="mistake-bar-count">{count}</div>
                                </div>
                              );
                            });
                          })()}
                        </div>
                      </div>

                      {mistakeDna.recommendation && (
                        <div className="dna-recommend">
                          <strong>📌 Adaptive Recommendation:</strong> {mistakeDna.recommendation.replace(/\*\*/g,'')}
                        </div>
                      )}
                    </>
                  )}
                </div>
              </>
            ) : (
              <div className="empty-state">Loading your personalised problem…</div>
            )}
          </main>
        </div>
      </div>
    </>
  );
}

// ─── Sidebar contents component (shared between desktop + mobile drawer) ──────
function SidebarContents({ search, setSearch, diffFilter, setDiffFilter, filtered, problem, loadProblem }) {
  return (
    <>
      <div className="sb-title">📑 Problem Bank</div>
      <input
        className="sb-search"
        placeholder="Search problems…"
        value={search}
        onChange={e => setSearch(e.target.value)}
      />
      <div className="sb-filters">
        {['all','easy','medium','hard'].map(d => (
          <button key={d} className={`sb-filter ${diffFilter === d ? 'active' : ''}`} onClick={() => setDiffFilter(d)}>
            {d}
          </button>
        ))}
      </div>
      <div className="prob-list">
        {filtered.length === 0 ? (
          <div style={{color:'var(--text3)', fontSize:'0.8rem', textAlign:'center', paddingTop:12}}>No problems match.</div>
        ) : filtered.map(p => (
          <button key={p.id} className={`prob-item ${problem?.id === p.id ? 'active' : ''}`} onClick={() => loadProblem(p.id)}>
            <div className="prob-item-title">{p.title}</div>
            <div className="prob-item-tags">
              <Badge label={p.difficulty} />
              <Badge label={p.topic} />
            </div>
          </button>
        ))}
      </div>
    </>
  );
}