"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Video } from "lucide-react"

export default function StudentLogin() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const router = useRouter()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Here you would typically handle the login logic
    console.log("Student login attempt", { email, password })
    // For now, we'll just redirect to the student dashboard
    router.push("/dashboard")
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#1B2A4E] to-[#19A5A2] flex flex-col justify-center items-center p-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
        <div className="flex justify-center mb-8">
          <Video className="h-12 w-12 text-[#19A5A2]" />
        </div>
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">Student Login</h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <Button type="submit" className="w-full bg-[#19A5A2] hover:bg-[#19A5A2]/90">
            Sign In
          </Button>
        </form>
        <div className="mt-6 text-center">
          <Link href="/login/hr" className="text-sm text-[#19A5A2] hover:underline">
            HR Login
          </Link>
          {" | "}
          <Link href="/login/super-admin" className="text-sm text-[#19A5A2] hover:underline">
            Super Admin Login
          </Link>
        </div>
      </div>
    </div>
  )
}

