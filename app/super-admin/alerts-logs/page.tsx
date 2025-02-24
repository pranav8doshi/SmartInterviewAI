import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

export default function AlertsLogs() {
  const systemLogs = [
    { id: 1, type: "Info", message: "System update completed successfully", timestamp: "2023-06-15 10:30:00" },
    { id: 2, type: "Warning", message: "High server load detected", timestamp: "2023-06-15 14:45:00" },
    { id: 3, type: "Error", message: "Database connection failed", timestamp: "2023-06-16 09:15:00" },
  ]

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">Manage Alerts & Logs</h2>
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Send System-wide Message</CardTitle>
        </CardHeader>
        <CardContent>
          <form className="space-y-4">
            <div>
              <Label htmlFor="message-title">Message Title</Label>
              <Input id="message-title" placeholder="Enter message title" />
            </div>
            <div>
              <Label htmlFor="message-content">Message Content</Label>
              <Textarea id="message-content" placeholder="Enter your message here" />
            </div>
            <Button type="submit" className="bg-[#FF9E46] hover:bg-[#19A5A2]/90">
              Send Message
            </Button>
          </form>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>System Logs</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Type</TableHead>
                <TableHead>Message</TableHead>
                <TableHead>Timestamp</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {systemLogs.map((log) => (
                <TableRow key={log.id}>
                  <TableCell>{log.type}</TableCell>
                  <TableCell>{log.message}</TableCell>
                  <TableCell>{log.timestamp}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}

