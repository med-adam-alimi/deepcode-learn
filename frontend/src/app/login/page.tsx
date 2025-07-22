'use client'

import { useRouter } from 'next/navigation'
import { useState } from 'react'
import { signInWithEmailAndPassword, getAuth } from 'firebase/auth'
import { auth } from '../lib/firebase'

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const handleLogin = async () => {
    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password)
      const token = await userCredential.user.getIdToken()

      // Optional: call backend with token if needed
      // await fetch('http://127.0.0.1:8000/some-auth-route', {
      //   method: 'POST',
      //   headers: {
      //     'Authorization': `Bearer ${token}`
      //   }
      // })

      router.push('/choose-mode')
    } catch (err: any) {
      setError('❌ Invalid email or password')
      console.error(err.message)
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center bg-white p-6">
      <div className="max-w-md w-full space-y-6">
        <h2 className="text-3xl font-bold text-center text-blue-700">Sign In</h2>

        <input
          type="email"
          placeholder="Email"
          className="w-full border p-3 rounded"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full border p-3 rounded"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {error && <p className="text-red-600 text-sm text-center">{error}</p>}

        <button
          onClick={handleLogin}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white p-3 rounded"
        >
          Login
        </button>

        <button
          className="text-sm text-blue-600 underline block mx-auto"
          onClick={() => router.push('/forgot-password')}
        >
          Forgot Password?
        </button>
      </div>
    </main>
  )
}
