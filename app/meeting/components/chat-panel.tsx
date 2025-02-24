"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Send, X } from "lucide-react"
import { Switch } from "@/components/ui/switch"

interface Message {
  id: number
  sender: string
  text: string
  timestamp: Date
}

export function ChatPanel({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const [messages, setMessages] = useState<Message[]>([])
  const [newMessage, setNewMessage] = useState("")
  const [allowMessages, setAllowMessages] = useState(true)

  const sendMessage = (e: React.FormEvent) => {
    e.preventDefault()
    if (!newMessage.trim()) return

    setMessages([
      ...messages,
      {
        id: Date.now(),
        sender: "You",
        text: newMessage,
        timestamp: new Date(),
      },
    ])
    setNewMessage("")
  }

  if (!isOpen) return null

  return (
    <div className="w-[350px] bg-white text-black flex flex-col h-full">
      <div className="p-4 border-b flex justify-between items-center">
        <h2 className="text-xl font-medium">In-call messages</h2>
        <Button variant="ghost" size="icon" onClick={onClose}>
          <X className="h-4 w-4" />
        </Button>
      </div>

      <div className="p-4 bg-gray-50 flex items-center justify-between">
        <span>Let everyone send messages</span>
        <Switch checked={allowMessages} onCheckedChange={setAllowMessages} />
      </div>

      <div className="p-4 bg-gray-50 text-sm text-gray-600 text-center">
        You can pin a message to make it visible for people who join later. When you leave the call, you won&apos;t be
        able to access this chat.
      </div>

      <ScrollArea className="flex-1 p-4">
        <div className="space-y-4">
          {messages.map((message) => (
            <div key={message.id} className="flex flex-col">
              <div className="flex items-center gap-2">
                <span className="font-medium">{message.sender}</span>
                <span className="text-xs text-gray-400">{message.timestamp.toLocaleTimeString()}</span>
              </div>
              <p className="text-sm">{message.text}</p>
            </div>
          ))}
        </div>
      </ScrollArea>

      <form onSubmit={sendMessage} className="p-4 border-t">
        <div className="flex gap-2">
          <Input
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            placeholder="Send a message to everyone"
            className="flex-1"
          />
          <Button type="submit" size="icon" variant="ghost">
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </form>
    </div>
  )
}

