'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

type Problem = {
  id: string;
  title: string;
  short_description: string;
  difficulty: string;
};

export default function ProblemsPage() {
  const [problems, setProblems] = useState<Problem[]>([]);

  useEffect(() => {
    fetch('/data/problems.json')
      .then(res => res.json())
      .then(data => setProblems(data));
  }, []);

  return (
    <main className="min-h-screen bg-white px-6 py-10">
      <div className="text-center mb-10">
        <h1 className="text-4xl font-extrabold text-blue-700 mb-2">Let’s Start Coding 💻</h1>
        <p className="text-gray-600 text-lg">
          Choose a coding problem and start your journey with AI-assisted feedback.
        </p>
      </div>

      <div className="space-y-6 max-w-3xl mx-auto">
        {problems.map((problem, index) => (
          <div
            key={problem.id}
            className="bg-blue-50 border border-blue-200 rounded-xl p-6 shadow hover:shadow-md transition"
          >
            <h2 className="text-xl font-bold text-blue-900 mb-2">{problem.title}</h2>
            <p className="text-gray-700 mb-2">{problem.short_description}</p>
            <p className="text-sm text-blue-600 font-semibold mb-4">Difficulty: {problem.difficulty}</p>
            <Link
              href={`/problems/${index}`}
              className="inline-block bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg text-sm"
            >
              Solve Now →
            </Link>
          </div>
        ))}
      </div>
    </main>
  );
}
