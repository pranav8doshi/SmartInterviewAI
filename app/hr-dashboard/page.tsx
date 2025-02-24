import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { BarChart, Bell, Calendar, FileText, Users } from "lucide-react"

export default function HRDashboard() {
  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">HR Dashboard</h2>

      {/* Dashboard Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Applications</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">50</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Scheduled Interviews</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">10</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Completed Interviews</CardTitle>
            <BarChart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">25</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pending Feedback</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">5</div>
          </CardContent>
        </Card>
      </div>

      {/* Upcoming Interviews */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Upcoming Interviews</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2">
            <li className="flex items-center justify-between">
              <span>John Doe - Frontend Developer</span>
              <span>June 15, 2023 at 2:00 PM</span>
              <Button className="bg-[#FF9E46] hover:bg-[#19A5A2]/90">Join</Button>
            </li>
            <li className="flex items-center justify-between">
              <span>Jane Smith - UI/UX Designer</span>
              <span>June 16, 2023 at 10:00 AM</span>
              <Button className="bg-[#FF9E46] hover:bg-[#19A5A2]/90">Join</Button>
            </li>
          </ul>
        </CardContent>
      </Card>

      {/* Recent Notifications */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Notifications</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2">
            <li className="flex items-center space-x-2">
              <Bell className="h-4 w-4 text-[#19A5A2]" />
              <span>New application received for Backend Developer position</span>
            </li>
            <li className="flex items-center space-x-2">
              <Bell className="h-4 w-4 text-[#19A5A2]" />
              <span>Reminder: Provide feedback for yesterday's interviews</span>
            </li>
            <li className="flex items-center space-x-2">
              <Bell className="h-4 w-4 text-[#19A5A2]" />
              <span>System update scheduled for this weekend</span>
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  )
}

