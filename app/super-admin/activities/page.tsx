import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export default function HRCandidateActivities() {
  const hrActivities = [
    { id: 1, hr: "John Doe", action: "Scheduled interview", candidate: "Alice Smith", timestamp: "2023-06-15 14:30" },
    { id: 2, hr: "Jane Doe", action: "Provided feedback", candidate: "Bob Johnson", timestamp: "2023-06-15 16:00" },
    { id: 3, hr: "Mike Smith", action: "Created new job posting", candidate: "N/A", timestamp: "2023-06-16 09:15" },
  ]

  const candidateActivities = [
    {
      id: 1,
      candidate: "Alice Smith",
      action: "Submitted application",
      role: "Frontend Developer",
      timestamp: "2023-06-14 10:00",
    },
    {
      id: 2,
      candidate: "Bob Johnson",
      action: "Completed interview",
      role: "UI/UX Designer",
      timestamp: "2023-06-15 15:30",
    },
    { id: 3, candidate: "Charlie Brown", action: "Updated profile", role: "N/A", timestamp: "2023-06-16 11:45" },
  ]

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">HR & Candidate Activities</h2>
      <Tabs defaultValue="hr" className="w-full">
        <TabsList>
          <TabsTrigger value="hr">HR Activities</TabsTrigger>
          <TabsTrigger value="candidate">Candidate Activities</TabsTrigger>
        </TabsList>
        <TabsContent value="hr">
          <Card>
            <CardHeader>
              <CardTitle>HR Activities</CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>HR Name</TableHead>
                    <TableHead>Action</TableHead>
                    <TableHead>Candidate</TableHead>
                    <TableHead>Timestamp</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {hrActivities.map((activity) => (
                    <TableRow key={activity.id}>
                      <TableCell>{activity.hr}</TableCell>
                      <TableCell>{activity.action}</TableCell>
                      <TableCell>{activity.candidate}</TableCell>
                      <TableCell>{activity.timestamp}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="candidate">
          <Card>
            <CardHeader>
              <CardTitle>Candidate Activities</CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Candidate Name</TableHead>
                    <TableHead>Action</TableHead>
                    <TableHead>Role</TableHead>
                    <TableHead>Timestamp</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {candidateActivities.map((activity) => (
                    <TableRow key={activity.id}>
                      <TableCell>{activity.candidate}</TableCell>
                      <TableCell>{activity.action}</TableCell>
                      <TableCell>{activity.role}</TableCell>
                      <TableCell>{activity.timestamp}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

