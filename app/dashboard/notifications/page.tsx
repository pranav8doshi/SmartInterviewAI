import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Bell } from "lucide-react"

export default function Notifications() {
  const notifications = [
    {
      id: 1,
      type: "Interview Update",
      message: "Your interview for Frontend Developer is scheduled for June 25, 2023.",
    },
    { id: 2, type: "HR Message", message: "Please submit your updated resume before the interview." },
    { id: 3, type: "System Alert", message: "The platform will be undergoing maintenance on June 30, 2023." },
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

