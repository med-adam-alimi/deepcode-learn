"use client";

import { useRouter } from "next/navigation";
import { useState } from "react"; // Added for click animation

export default function Home() {
  const router = useRouter();
  const [isClicked, setIsClicked] = useState(false); // Track button click state

  const handleStart = () => {
    setIsClicked(true); // Trigger animation
    setTimeout(() => {
      router.push("/problems");
    }, 200); // Short delay to show animation
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gray-50 text-center p-6">
      <img src="/logo.PNG" alt="Logo" className="w-24 h-24 mb-4" />

      <h1 className="text-4xl font-bold">
        Welcome to <span className="text-blue-600">DeepCode Learn</span>
      </h1>
      <p className="text-gray-600 mt-2 mb-6 max-w-md">
        Master coding by solving real problems, submitting your code, and
        getting instant feedback — powered by AI.
      </p>

      <button
        onClick={handleStart}
        className={`bg-blue-600 hover:bg-blue-700 text-white font-semibold py-1 px-4 rounded-lg shadow-md transition-all duration-200 ${
          isClicked ? "transform scale-95" : ""
        }`}
      >
        Let’s Start Learning →
      </button>
    </main>
  );
}