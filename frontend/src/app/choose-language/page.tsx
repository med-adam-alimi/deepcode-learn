'use client'

import { useRouter } from 'next/navigation'

export default function ChooseLanguage() {
  const router = useRouter()

  const goToLanguage = (lang: string) => {
    router.push(`/problems?lang=${lang}`)
  }

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-white p-6 text-center">
      <h1 className="text-3xl font-bold mb-6 text-blue-700">Choose a Language</h1>
      <div className="grid grid-cols-2 gap-4 w-64">
        <button onClick={() => goToLanguage('python')} className="bg-yellow-500 hover:bg-yellow-600 text-white py-2 rounded">
          Python 🐍
        </button>
        <button onClick={() => goToLanguage('java')} className="bg-red-500 hover:bg-red-600 text-white py-2 rounded">
          Java ☕
        </button>
        <button onClick={() => goToLanguage('c')} className="bg-blue-500 hover:bg-blue-600 text-white py-2 rounded">
          C 🔵
        </button>
        <button onClick={() => goToLanguage('cpp')} className="bg-purple-500 hover:bg-purple-600 text-white py-2 rounded">
          C++ 💡
        </button>
      </div>
    </main>
  )
}
