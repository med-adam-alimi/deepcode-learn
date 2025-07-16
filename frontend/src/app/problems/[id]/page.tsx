'use client';

import { useParams } from 'next/navigation';
import { useEffect, useState } from 'react';

type Problem = {
  id: string;
  title: string;
  description: string;
  difficulty: string;
};

export default function ProblemPage() {
  const { id } = useParams();
  const [problem, setProblem] = useState<Problem | null>(null);
  const [code, setCode] = useState('');
  const [feedback, setFeedback] = useState<string | null>(null);
  const [score, setScore] = useState<number | null>(null);
  const [results, setResults] = useState<any[] | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch('/data/problems.json')
      .then(res => res.json())
      .then((data: Problem[]) => {
        const p = data[parseInt(id as string)];
        setProblem(p);
      });
  }, [id]);

  const handleSubmit = async () => {
    setLoading(true);
    setFeedback(null);
    setScore(null);
    setResults(null);

    try {
      const res = await fetch('http://127.0.0.1:8000/submit/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          problem_id: parseInt(id as string),
          student_code: code
        })
      });

      if (!res.ok) {
        const err = await res.text();
        alert(`Error: ${err}`);
        return;
      }

      const data = await res.json();
      setScore(data.score);
      setFeedback(data.feedback);
      setResults(data.results);
    } catch (err) {
      alert('⚠️ Cannot reach backend.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (!problem) return <div className="p-6">Loading...</div>;

  return (
    <main className="min-h-screen p-6 bg-white">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold text-blue-800 mb-1">{problem.title}</h1>
        <p className="text-sm text-blue-600 mb-4">Difficulty: {problem.difficulty}</p>
        <pre className="bg-blue-50 p-4 rounded border border-blue-100 text-gray-800 text-sm whitespace-pre-wrap mb-4 max-h-60 overflow-auto">
          {problem.description}
        </pre>

        <textarea
          placeholder="Write your solution here..."
          value={code}
          onChange={e => setCode(e.target.value)}
          className="w-full h-[400px] p-4 border border-blue-300 rounded-lg font-mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <button
          onClick={handleSubmit}
          className="mt-6 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg text-base"
          disabled={loading}
        >
          {loading ? '⏳ Submitting...' : 'Submit Solution'}
        </button>

        {score !== null && (
          <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded text-green-800">
            <strong>✅ Score:</strong> {score}%
          </div>
        )}

        {feedback && (
          <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded text-yellow-900 whitespace-pre-line">
            <strong>🧠 Feedback:</strong> {feedback}
          </div>
        )}

        {results && (
          <div className="mt-4">
            <h3 className="font-semibold text-lg mb-2">🧪 Test Results:</h3>
            <ul className="list-disc pl-6 text-sm text-gray-800">
              {results.map((r, i) => (
                <li key={i}>
                  {r.passed ? '✅' : '❌'} Test {i + 1}: input = <code>{r.input}</code>, expected = <code>{r.expected}</code>, got = <code>{r.actual}</code>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </main>
  );
}
