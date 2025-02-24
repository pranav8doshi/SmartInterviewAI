"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { X, Mic, Video, UserPlus } from "lucide-react"

interface Participant {
  id: number
  name: string
  isHost?: boolean
  audioEnabled: boolean
  videoEnabled: boolean
  role?: string
}

export function ParticipantsPanel({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const [participants] = useState<Participant[]>([
    {
      id: 1,
      name: "You",
      isHost: true,
      audioEnabled: true,
      videoEnabled: true,
      role: "Meeting host",
    },
  ])

  if (!isOpen) return null

  return (
    <div className="w-[350px] bg-white text-black flex flex-col h-full">
      <div className="p-4 border-b flex justify-between items-center">
        <h2 className="text-xl font-medium">People</h2>
        <Button variant="ghost" size="icon" onClick={onClose}>
          <X className="h-4 w-4" />
        </Button>
      </div>

      <div className="p-4">
        <Button variant="outline" className="w-full justify-start" onClick={() => {}}>
          <UserPlus className="mr-2 h-4 w-4" />
          Add people
        </Button>
      </div>

      <div className="px-4 pb-4">
        <Input placeholder="Search for people" />
      </div>

      <div className="px-4 py-2 text-sm text-gray-500">IN MEETING</div>

      <ScrollArea className="flex-1">
        <div className="p-4">
          <div className="font-medium mb-2 flex justify-between items-center">
            Contributors
            <span className="text-gray-500">{participants.length}</span>
          </div>
          {participants.map((participant) => (
            <div key={participant.id} className="flex items-center justify-between p-2 rounded-lg hover:bg-gray-100">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-purple-600 flex items-center justify-center text-white">
                  {participant.name[0]}
                </div>
                <div>
                  <p className="font-medium">
                    {participant.name}
                    {participant.isHost && <span className="text-sm text-gray-500 block">{participant.role}</span>}
                  </p>
                </div>
              </div>
              <div className="flex gap-1">
                <Button variant="ghost" size="icon" className={!participant.audioEnabled ? "text-red-500" : ""}>
                  <Mic className="h-4 w-4" />
                </Button>
                <Button variant="ghost" size="icon" className={!participant.videoEnabled ? "text-red-500" : ""}>
                  <Video className="h-4 w-4" />
                </Button>
              </div>
            </div>
          ))}
        </div>
      </ScrollArea>
    </div>
  )
}

