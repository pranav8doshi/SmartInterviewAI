import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

export default function CandidateApplications() {
  const applications = [
    { id: 1, name: "John Doe", role: "Frontend Developer", status: "Pending" },
    { id: 2, name: "Jane Smith", role: "UI/UX Designer", status: "Accepted" },
    { id: 3, name: "Mike Johnson", role: "Backend Developer", status: "Rejected" },
  ]

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">Candidate Applications</h2>
      <Card>
        <CardHeader>
          <CardTitle>All Applications</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Role</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {applications.map((application) => (
                <TableRow key={application.id}>
                  <TableCell>{application.name}</TableCell>
                  <TableCell>{application.role}</TableCell>
                  <TableCell>{application.status}</TableCell>
                  <TableCell>
                    <Button className="bg-[#FF9E46] hover:bg-[#19A5A2]/90 mr-2">View Details</Button>
                    {application.status === "Pending" && (
                      <>
                        <Button className="bg-green-500 hover:bg-green-600 mr-2">Accept</Button>
                        <Button className="bg-red-500 hover:bg-red-600">Reject</Button>
                      </>
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

