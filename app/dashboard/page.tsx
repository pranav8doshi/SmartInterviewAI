import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { BarChart, Bell, Calendar, FileText } from "lucide-react"

export default function CandidateDashboard() {
  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">Candidate Dashboard</h2>

      {/* Dashboard Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Upcoming Interviews</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">2</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Applications</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">5</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Latest Interview Status</CardTitle>
            <BarChart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Scheduled</div>
          </CardContent>
        </Card>
      </div>

      {/* Next Interview */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Next Interview</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="mb-2">
            <strong>Date & Time:</strong> June 15, 2023 at 2:00 PM
          </p>
          <p className="mb-2">
            <strong>Job Role:</strong> Frontend Developer
          </p>
          <p className="mb-4">
            <strong>Interviewer:</strong> John Doe
          </p>
          <Button className="bg-[#FF9E46] hover:bg-[#FF9E46]/90">Join Interview</Button>
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
              <Bell className="h-4 w-4 text-[#FF9E46]" />
              <span>New interview scheduled for June 20, 2023</span>
            </li>
            <li className="flex items-center space-x-2">
              <Bell className="h-4 w-4 text-[#FF9E46]" />
              <span>Feedback received for your last interview</span>
            </li>
            <li className="flex items-center space-x-2">
              <Bell className="h-4 w-4 text-[#FF9E46]" />
              <span>Reminder: Update your profile information</span>
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  )
}

