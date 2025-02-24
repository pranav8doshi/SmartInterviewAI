import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { BarChart, Users, UserCheck, Video, AlertTriangle } from "lucide-react"

export default function SuperAdminDashboard() {
  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">Super Admin Dashboard</h2>

      {/* Dashboard Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total HRs</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">25</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Candidates</CardTitle>
            <UserCheck className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">150</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Ongoing Interviews</CardTitle>
            <Video className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">5</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">System Alerts</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">2</div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex space-x-4">
            <Button className="bg-[#FF9E46] hover:bg-[#19A5A2]/90">Add New HR</Button>
            <Button className="bg-[#FF9E46] hover:bg-[#19A5A2]/90">Generate Report</Button>
            <Button className="bg-[#FF9E46] hover:bg-[#19A5A2]/90">System Settings</Button>
          </div>
        </CardContent>
      </Card>

      {/* Recent Activities */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Activities</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2">
            <li className="flex items-center space-x-2">
              <Users className="h-4 w-4 text-[#19A5A2]" />
              <span>New HR account created: John Doe</span>
            </li>
            <li className="flex items-center space-x-2">
              <Video className="h-4 w-4 text-[#19A5A2]" />
              <span>Interview completed: Frontend Developer position</span>
            </li>
            <li className="flex items-center space-x-2">
              <BarChart className="h-4 w-4 text-[#19A5A2]" />
              <span>Monthly analytics report generated</span>
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  )
}

