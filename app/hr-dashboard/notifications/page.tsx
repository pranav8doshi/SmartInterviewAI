import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Bell } from "lucide-react"

export default function Notifications() {
  const notifications = [
    {
      id: 1,
      type: "Interview Reminder",
      message: "Upcoming interview with John Doe for Frontend Developer position at 2:00 PM.",
    },
    {
      id: 2,
      type: "Candidate Update",
      message: "Jane Smith has uploaded a new resume for the UI/UX Designer position.",
    },
    { id: 3, type: "System Message", message: "New feature added: Video recording for interviews is now available." },
  ]

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">Notifications & Alerts</h2>
      {notifications.map((notification) => (
        <Card key={notification.id} className="mb-4">
          <CardHeader>
            <CardTitle className="flex items-center">
              <Bell className="w-5 h-5 mr-2" />
              {notification.type}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p>{notification.message}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

