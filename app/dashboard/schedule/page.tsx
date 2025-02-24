import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

export default function InterviewSchedule() {
  const interviews = [
    { id: 1, date: "2023-06-20", time: "14:00", role: "Frontend Developer", status: "Scheduled" },
    { id: 2, date: "2023-06-22", time: "10:00", role: "Backend Developer", status: "Pending" },
    { id: 3, date: "2023-06-25", time: "15:30", role: "UI/UX Designer", status: "Completed" },
  ]

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">Interview Schedule</h2>
      <Card>
        <CardHeader>
          <CardTitle>Upcoming Interviews</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Date</TableHead>
                <TableHead>Time</TableHead>
                <TableHead>Job Role</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {interviews.map((interview) => (
                <TableRow key={interview.id}>
                  <TableCell>{interview.date}</TableCell>
                  <TableCell>{interview.time}</TableCell>
                  <TableCell>{interview.role}</TableCell>
                  <TableCell>{interview.status}</TableCell>
                  <TableCell>
                    {interview.status === "Scheduled" && (
                      <Button className="bg-[#FF9E46] hover:bg-[#19A5A2]/90">Join</Button>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}

