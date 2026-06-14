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
  
  // Fetch a problem when component loads (hardcode problem ID for now)
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

  // ========== NEW FUNCTION (Step 5) – ADD AFTER fetchProblem ==========
  const fetchProgress = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/api/progress/user/${USER_ID}`);
      setProgress(res.data);
    } catch (err) {
      console.error("Failed to fetch progress", err);
    }
  };
  // =====================================================================

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:8000/api/execute', {
        code: code,
        problem_id: problem.id,
        user_id: USER_ID
      });
      setResult(res.data);
      // ========== NEW LINE – refresh progress after submission ==========
      fetchProgress();  // so progress updates immediately
    } catch (err) {
      setResult({ error: err.response?.data?.detail || err.message });
    }
    setLoading(false);
  };

  if (!problem) return <div>Loading problem...</div>;

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>{problem.title}</h1>
      <p>{problem.description}</p>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        {/* Code Editor Section */}
        <div>
          <h3>Your Code</h3>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            style={{
              width: '100%',
              height: '400px',
              fontFamily: 'monospace',
              padding: '10px',
              border: '1px solid #ccc'
            }}
          />
          <button
            onClick={handleSubmit}
            disabled={loading}
            style={{
              marginTop: '10px',
              padding: '10px 20px',
              fontSize: '16px',
              cursor: loading ? 'not-allowed' : 'pointer'
            }}
          >
            {loading ? 'Running...' : 'Submit'}
          </button>
        </div>
        {/* Results Section */}
        <div>
          <h3>Results</h3>
          {result && (
            <div style={{ border: '1px solid #ccc', padding: '10px' }}>
              {result.error ? (
                <p style={{ color: 'red' }}>{result.error}</p>
              ) : (
                <>
                  <p style={{ color: result.passed ? 'green' : 'red' }}>
                    {result.passed ? '✓ All tests passed!' : `✗ ${result.passed_count}/${result.total_count} tests passed`}
                  </p>
                  {result.results.map((r, i) => (
                    <div key={i} style={{ marginTop: '10px', fontSize: '12px' }}>
                      <p><strong>Test {i + 1}:</strong></p>
                      <p>Input: {r.input}</p>
                      <p>Expected: {r.expected}</p>
                      <p>Got: {r.actual || '(no output)'}</p>
                      <p style={{ color: r.passed ? 'green' : 'red' }}>
                        {r.passed ? '✓ Passed' : '✗ Failed'}
                      </p>
                    </div>
                  ))}
                </>
              )}
            </div>
          )}
        </div>
      </div>

      {/*  ADDED BUTTON AND PROGRESS DISPLAY ========== */}
      <div style={{ marginTop: '20px' }}>
        <button onClick={() => setShowProgress(!showProgress)}>
          {showProgress ? 'Hide Progress' : 'Show Progress'}
        </button>

        {showProgress && progress && (
          <div style={{ border: '1px solid #ccc', padding: '10px', marginTop: '10px' }}>
            <h3>Your Progress</h3>
            <p>Problems Solved: {progress.problems_solved}</p>
            <p>Total Attempts: {progress.total_attempts}</p>
            <h4>By Topic:</h4>
            {Object.entries(progress.topics).map(([topic, stats]) => (
              <p key={topic}>
                <strong>{topic}:</strong> {stats.mastery}% mastery ({stats.solved}/{stats.attempts} solved)
              </p>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}