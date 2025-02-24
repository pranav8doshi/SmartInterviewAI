import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Select } from "@/components/ui/select"

export default function InterviewStatus() {
  const interviews = [
    { id: 1, candidate: "John Doe", role: "Frontend Developer", status: "Completed" },
    { id: 2, candidate: "Jane Smith", role: "UI/UX Designer", status: "Scheduled" },
    { id: 3, candidate: "Mike Johnson", role: "Backend Developer", status: "Pending" },
  ]

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">Interview Status</h2>
      <Card>
        <CardHeader>
          <CardTitle>All Interviews</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="mb-4">
            <Select>
              <option value="all">All</option>
              <option value="pending">Pending</option>
              <option value="scheduled">Scheduled</option>
              <option value="completed">Completed</option>
            </Select>
          </div>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Candidate</TableHead>
                <TableHead>Role</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {interviews.map((interview) => (
                <TableRow key={interview.id}>
                  <TableCell>{interview.candidate}</TableCell>
                  <TableCell>{interview.role}</TableCell>
                  <TableCell>{interview.status}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}

