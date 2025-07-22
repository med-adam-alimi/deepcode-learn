'use client'

import { useState } from 'react'
import { sendPasswordResetEmail } from 'firebase/auth'
import { auth } from '../lib/firebase'

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('')
  const [status, setStatus] = useState('')
  const [error, setError] = useState('')

  const handleReset = async () => {
    try {
      await sendPasswordResetEmail(auth, email)
      setStatus('✅ Check your inbox for the reset link.')
      setError('')
    } catch (err: any) {
      console.error(err.message)
      setError('❌ Unable to send reset email.')
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center p-6 bg-white">
      <div className="max-w-md w-full space-y-6 text-center">
        <h2 className="text-2xl font-bold text-blue-700">Reset Password</h2>
        <input
          type="email"
          placeholder="Your email"
          className="w-full border p-3 rounded"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <button
          onClick={handleReset}
          className="w-full bg-blue-600 text-white py-2 rounded"
        >
          Send Reset Link
        </button>
        {status && <p className="mt-4 text-green-600 text-sm">{status}</p>}
        {error && <p className="mt-4 text-red-600 text-sm">{error}</p>}
      </div>
    </main>
  )
}
