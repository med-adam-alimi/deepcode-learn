'use client'


import { auth } from '../lib/firebase'

import { createUserWithEmailAndPassword } from 'firebase/auth'
import { useRouter } from 'next/navigation'
import { useState } from 'react'

export default function SignupPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState<'student' | 'professor'>('student')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const handleSignup = async () => {
    setError('')
    setSuccess('')
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password)

      // Optional: Save user role in Firestore or backend
      await fetch('http://127.0.0.1:8000/register-role', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${await userCredential.user.getIdToken()}`,
        },
        body: JSON.stringify({ role }),
      })

      setSuccess('✅ Account created successfully!')
      setTimeout(() => router.push('/login'), 1500)
    } catch (err: any) {
      setError(err.message)
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-50 to-white p-6">
      <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-md space-y-6">
        <h2 className="text-3xl font-bold text-center text-blue-700">Sign Up</h2>

        <input
          type="email"
          placeholder="Email"
          className="w-full border border-gray-300 p-3 rounded-lg"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full border border-gray-300 p-3 rounded-lg"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <div className="flex justify-between items-center gap-3">
          <label className="text-sm font-medium text-gray-700">Account Type:</label>
          <select
            className="flex-1 border p-2 rounded-lg"
            value={role}
            onChange={(e) => setRole(e.target.value as 'student' | 'professor')}
          >
            <option value="student">Student</option>
            <option value="professor">Professor</option>
          </select>
        </div>

        {error && <p className="text-red-600 text-sm">{error}</p>}
        {success && <p className="text-green-600 text-sm">{success}</p>}

        <button
          onClick={handleSignup}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg text-lg font-semibold"
        >
          Create Account
        </button>
      </div>
    </main>
  )
}
