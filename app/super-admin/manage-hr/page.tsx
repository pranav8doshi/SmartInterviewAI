import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Select } from "@/components/ui/select"

export default function ManageHRAccounts() {
  const hrAccounts = [
    { id: 1, name: "John Doe", email: "john@example.com", role: "Senior HR" },
    { id: 2, name: "Jane Smith", email: "jane@example.com", role: "HR Manager" },
    { id: 3, name: "Mike Johnson", email: "mike@example.com", role: "Junior HR" },
  ]

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">Manage HR Accounts</h2>
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Add New HR</CardTitle>
        </CardHeader>
        <CardContent>
          <form className="space-y-4">
            <div>
              <Label htmlFor="name">Name</Label>
              <Input id="name" placeholder="Enter HR name" />
            </div>
            <div>
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" placeholder="Enter HR email" />
            </div>
            <div>
              <Label htmlFor="role">Role</Label>
              <Select id="role">
                <option>Junior HR</option>
                <option>Senior HR</option>
                <option>HR Manager</option>
              </Select>
            </div>
            <Button type="submit" className="bg-[#FF9E46] hover:bg-[#19A5A2]/90">
              Add HR
            </Button>
          </form>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>HR Accounts</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Email</TableHead>
                <TableHead>Role</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {hrAccounts.map((account) => (
                <TableRow key={account.id}>
                  <TableCell>{account.name}</TableCell>
                  <TableCell>{account.email}</TableCell>
                  <TableCell>{account.role}</TableCell>
                  <TableCell>
                    <Button className="bg-blue-500 hover:bg-blue-600 mr-2">Edit</Button>
                    <Button className="bg-red-500 hover:bg-red-600">Remove</Button>
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

