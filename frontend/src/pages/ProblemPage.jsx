import { useState, useEffect } from 'react';
import axios from 'axios';

// Hardcode a user ID for now
const USER_ID = '1fdc2d9c-07f2-4627-b2b6-20808a438380'; // from my create_test_user.py

export default function ProblemPage() {
  const [problem, setProblem] = useState(null);
  const [code, setCode] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const [progress, setProgress] = useState(null);
  const [showProgress, setShowProgress] = useState(false);
  
  // Fetch a problem when component loads
  useEffect(() => {
    fetchProblem('prob_easy_1');
    fetchProgress();
  }, []);

  const fetchProblem = async (problemId) => {
    try {
      const res = await axios.get(`http://localhost:8000/api/problems/${problemId}`);
      setProblem(res.data);
      setCode(res.data.starter_code);
      setResult(null);
    } catch (err) {
      console.error('Failed to fetch problem', err);
    }
  };

  const fetchProgress = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/api/progress/user/${USER_ID}`);
      setProgress(res.data);
    } catch (err) {
      console.error("Failed to fetch progress", err);
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:8000/api/execute', {
        code: code,
        problem_id: problem.id,
        user_id: USER_ID
      });
      setResult(res.data);
      fetchProgress(); // Refresh progress immediately after submission
    } catch (err) {
      setResult({ error: err.response?.data?.detail || err.message });
    }
    setLoading(false);
  };

  const getMistakeTitle = (type) => {
    const titles = {
      "syntax_error": "Syntax Error Detected",
      "index_error": "Index Error (Out of Bounds)",
      "recursion_error": "Infinite Recursion / Call Stack Overflow",
      "logic_error": "Algorithm Logic Issue",
      "potential_missing_base_case": "Missing Base Case in Recursion",
      "shadowing_builtin": "Shadowing a Built-in Function/Variable",
      "invalid_len_method": "Invalid Length/Size Method call",
      "invalid_keyword_elsif": "Invalid Keyword ('elsif')",
      "incorrect_none_comparison": "Incorrect Comparison with None"
    };
    return titles[type] || type.replace(/_/g, ' ');
  };

  if (!problem) return <div style={{ color: '#94a3b8', padding: '40px', textAlign: 'center' }}>Loading problem...</div>;

  return (
    <div className="tutor-container">
      {/* Injecting CSS styles dynamically in style block */}
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');

        .tutor-container {
          font-family: 'Outfit', sans-serif;
          background-color: #0b0f19;
          color: #f1f5f9;
          min-height: 100vh;
          padding: 40px 20px;
          box-sizing: border-box;
        }

        .tutor-header {
          text-align: center;
          margin-bottom: 40px;
        }

        .tutor-title {
          font-size: 2.8rem;
          font-weight: 700;
          background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          margin-bottom: 10px;
        }

        .tutor-subtitle {
          color: #94a3b8;
          font-size: 1.1rem;
        }

        .problem-description-card {
          background: #1e293b;
          border: 1px solid #334155;
          border-radius: 12px;
          padding: 24px;
          margin-bottom: 30px;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }

        .problem-description-card h2 {
          margin-top: 0;
          font-size: 1.8rem;
          color: #38bdf8;
          border-bottom: 1px solid #334155;
          padding-bottom: 10px;
        }

        .problem-description-card p {
          line-height: 1.6;
          color: #cbd5e1;
        }

        .workspace-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 30px;
        }

        @media (max-width: 900px) {
          .workspace-grid {
            grid-template-columns: 1fr;
          }
        }

        .card-title {
          font-size: 1.3rem;
          font-weight: 600;
          margin-bottom: 15px;
          color: #94a3b8;
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .editor-textarea {
          width: 100%;
          height: 420px;
          background-color: #0f172a;
          color: #e2e8f0;
          border: 1px solid #334155;
          border-radius: 12px;
          font-family: 'Fira Code', 'Courier New', monospace;
          font-size: 0.95rem;
          padding: 16px;
          box-sizing: border-box;
          resize: vertical;
          line-height: 1.5;
          outline: none;
          transition: border-color 0.2s, box-shadow 0.2s;
        }

        .editor-textarea:focus {
          border-color: #6366f1;
          box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
        }

        .submit-btn {
          background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
          color: #ffffff;
          border: none;
          border-radius: 8px;
          padding: 12px 28px;
          font-size: 1rem;
          font-weight: 600;
          cursor: pointer;
          margin-top: 15px;
          transition: transform 0.1s active, opacity 0.2s, box-shadow 0.2s;
          box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        }

        .submit-btn:hover {
          opacity: 0.9;
          box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
        }

        .submit-btn:active {
          transform: scale(0.98);
        }

        .submit-btn:disabled {
          background: #334155;
          color: #64748b;
          cursor: not-allowed;
          box-shadow: none;
        }

        .results-panel {
          background: #1e293b;
          border: 1px solid #334155;
          border-radius: 12px;
          padding: 24px;
          box-sizing: border-box;
          min-height: 420px;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
          overflow-y: auto;
        }

        .status-alert {
          padding: 14px 20px;
          border-radius: 8px;
          margin-bottom: 20px;
          font-weight: 600;
          display: flex;
          align-items: center;
          gap: 10px;
        }

        .status-alert.success {
          background-color: rgba(16, 185, 129, 0.15);
          border: 1px solid #10b981;
          color: #34d399;
        }

        .status-alert.failed {
          background-color: rgba(239, 68, 68, 0.15);
          border: 1px solid #ef4444;
          color: #f87171;
        }

        .testcase-card {
          background: #0f172a;
          border: 1px solid #334155;
          border-radius: 8px;
          padding: 14px 18px;
          margin-bottom: 12px;
          font-size: 0.9rem;
        }

        .testcase-header {
          display: flex;
          justify-content: space-between;
          margin-bottom: 8px;
          font-weight: 600;
        }

        .testcase-io {
          font-family: monospace;
          background: #1e293b;
          padding: 4px 8px;
          border-radius: 4px;
          font-size: 0.85rem;
          color: #cbd5e1;
        }

        .mistakes-container {
          margin-top: 25px;
        }

        .mistake-card {
          background-color: rgba(245, 158, 11, 0.08);
          border-left: 4px solid #f59e0b;
          border-top: 1px solid rgba(245, 158, 11, 0.15);
          border-right: 1px solid rgba(245, 158, 11, 0.15);
          border-bottom: 1px solid rgba(245, 158, 11, 0.15);
          border-radius: 0 8px 8px 0;
          padding: 16px 20px;
          margin-bottom: 12px;
          box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
        }

        .mistake-card.syntax {
          background-color: rgba(239, 68, 68, 0.08);
          border-left-color: #ef4444;
          border-top-color: rgba(239, 68, 68, 0.15);
          border-right-color: rgba(239, 68, 68, 0.15);
          border-bottom-color: rgba(239, 68, 68, 0.15);
        }

        .mistake-title {
          font-weight: 700;
          font-size: 1rem;
          color: #f59e0b;
          margin-bottom: 6px;
          text-transform: capitalize;
          display: flex;
          align-items: center;
          gap: 6px;
        }

        .mistake-card.syntax .mistake-title {
          color: #ef4444;
        }

        .mistake-message {
          font-size: 0.92rem;
          line-height: 1.5;
          color: #cbd5e1;
        }

        .progress-section {
          margin-top: 40px;
          background: #1e293b;
          border: 1px solid #334155;
          border-radius: 12px;
          padding: 24px;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }

        .toggle-progress-btn {
          background: #334155;
          color: #f1f5f9;
          border: 1px solid #475569;
          border-radius: 8px;
          padding: 10px 20px;
          font-weight: 600;
          cursor: pointer;
          transition: background 0.2s;
          display: inline-flex;
          align-items: center;
          gap: 8px;
        }

        .toggle-progress-btn:hover {
          background: #475569;
        }

        .progress-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
          gap: 20px;
          margin-top: 20px;
        }

        .progress-stats-box {
          background: #0f172a;
          border: 1px solid #334155;
          padding: 16px;
          border-radius: 8px;
          text-align: center;
        }

        .progress-stats-value {
          font-size: 2.2rem;
          font-weight: 700;
          color: #38bdf8;
          margin-bottom: 5px;
        }

        .topic-mastery-card {
          background: #0f172a;
          border: 1px solid #334155;
          padding: 16px 20px;
          border-radius: 8px;
        }

        .topic-header {
          display: flex;
          justify-content: space-between;
          margin-bottom: 10px;
          font-weight: 600;
          text-transform: capitalize;
        }

        .mastery-bar-container {
          background-color: #334155;
          height: 8px;
          border-radius: 4px;
          overflow: hidden;
          margin-bottom: 8px;
        }

        .mastery-bar-fill {
          background: linear-gradient(90deg, #38bdf8 0%, #6366f1 100%);
          height: 100%;
          border-radius: 4px;
          transition: width 0.5s ease-in-out;
        }

        .topic-details {
          font-size: 0.8rem;
          color: #94a3b8;
        }
      `}</style>

      {/* Header */}
      <div className="tutor-header">
        <h1 className="tutor-title">Coding Tutor AI</h1>
        <p className="tutor-subtitle">Learn to code with interactive, mistake-analyzing feedback.</p>
      </div>

      {/* Problem Description */}
      <div className="problem-description-card">
        <h2>{problem.title}</h2>
        <p>{problem.description}</p>
      </div>

      {/* Workspace */}
      <div className="workspace-grid">
        {/* Code Editor */}
        <div>
          <div className="card-title">
            <span>💻</span> Your Editor
          </div>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="editor-textarea"
            placeholder="Write your code here..."
          />
          <button
            onClick={handleSubmit}
            disabled={loading}
            className="submit-btn"
          >
            {loading ? 'Running Tests...' : 'Submit Code'}
          </button>
        </div>

        {/* Results Panel */}
        <div className="results-panel">
          <div className="card-title">
            <span>📊</span> Execution Results
          </div>
          
          {!result && (
            <div style={{ color: '#64748b', textAlign: 'center', paddingTop: '60px' }}>
              Submit your code to see results and analysis.
            </div>
          )}

          {result && (
            <div>
              {result.error ? (
                <div className="status-alert failed">
                  <span>⚠️</span> {result.error}
                </div>
              ) : (
                <>
                  {/* Status Banner */}
                  {result.passed ? (
                    <div className="status-alert success">
                      <span>✓</span> All tests passed! Great job!
                    </div>
                  ) : (
                    <div className="status-alert failed">
                      <span>✗</span> Failed {result.total_count - result.passed_count} of {result.total_count} tests.
                    </div>
                  )}

                  {/* Mistake DNA Alerts */}
                  {result.mistake_details && result.mistake_details.length > 0 && (
                    <div className="mistakes-container">
                      <div className="card-title" style={{ fontSize: '1rem', color: '#f59e0b' }}>
                        <span>🧠</span> Tutor Insights (Mistake DNA Analysis)
                      </div>
                      {result.mistake_details.map((m, i) => {
                        const isSyntax = m.type === 'syntax_error' || m.type === 'recursion_error';
                        return (
                          <div key={i} className={`mistake-card ${isSyntax ? 'syntax' : ''}`}>
                            <div className="mistake-title">
                              <span>{isSyntax ? '⚠️' : '💡'}</span> {getMistakeTitle(m.type)}
                            </div>
                            <div className="mistake-message">{m.message}</div>
                          </div>
                        );
                      })}
                    </div>
                  )}

                  {/* Test Cases Output */}
                  <div style={{ marginTop: '20px' }}>
                    <div className="card-title" style={{ fontSize: '1rem' }}>
                      <span>📂</span> Test Cases
                    </div>
                    {result.results.map((r, i) => (
                      <div key={i} className="testcase-card">
                        <div className="testcase-header">
                          <span>Test Case {i + 1}</span>
                          <span style={{ color: r.passed ? '#34d399' : '#f87171' }}>
                            {r.passed ? 'Passed' : 'Failed'}
                          </span>
                        </div>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginTop: '6px' }}>
                          <div>
                            <span style={{ color: '#64748b', display: 'block', fontSize: '0.75rem' }}>INPUT</span>
                            <span className="testcase-io">{r.input}</span>
                          </div>
                          <div>
                            <span style={{ color: '#64748b', display: 'block', fontSize: '0.75rem' }}>EXPECTED</span>
                            <span className="testcase-io">{r.expected}</span>
                          </div>
                        </div>
                        <div style={{ marginTop: '8px' }}>
                          <span style={{ color: '#64748b', display: 'block', fontSize: '0.75rem' }}>GOT</span>
                          <span className="testcase-io" style={{ color: r.passed ? '#34d399' : '#f87171', background: '#090d16' }}>
                            {r.actual || '(no output)'}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Progress & topic tracking */}
      <div className="progress-section">
        <button
          onClick={() => setShowProgress(!showProgress)}
          className="toggle-progress-btn"
        >
          <span>{showProgress ? '🔼' : '🔽'}</span> {showProgress ? 'Hide My Progress' : 'Show My Progress'}
        </button>

        {showProgress && progress && (
          <div>
            <div className="progress-grid">
              <div className="progress-stats-box">
                <div className="progress-stats-value">{progress.problems_solved}</div>
                <div style={{ color: '#64748b', fontSize: '0.9rem' }}>Problems Solved</div>
              </div>
              <div className="progress-stats-box">
                <div className="progress-stats-value">{progress.total_attempts}</div>
                <div style={{ color: '#64748b', fontSize: '0.9rem' }}>Total Attempts</div>
              </div>
            </div>

            {progress.topics && Object.keys(progress.topics).length > 0 && (
              <div style={{ marginTop: '30px' }}>
                <div className="card-title" style={{ fontSize: '1.1rem' }}>
                  <span>📈</span> Topic Mastery
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', marginTop: '15px' }}>
                  {Object.entries(progress.topics).map(([topic, stats]) => (
                    <div key={topic} className="topic-mastery-card">
                      <div className="topic-header">
                        <span>{topic}</span>
                        <span style={{ color: '#38bdf8' }}>{stats.mastery}% Mastery</span>
                      </div>
                      <div className="mastery-bar-container">
                        <div
                          className="mastery-bar-fill"
                          style={{ width: `${stats.mastery}%` }}
                        />
                      </div>
                      <div className="topic-details">
                        Solved {stats.solved} of {stats.attempts} attempts
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}