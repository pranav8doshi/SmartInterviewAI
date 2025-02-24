import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select } from "@/components/ui/select"

export default function ApplyForInterview() {
  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">Apply for Interview</h2>
      <Card>
        <CardHeader>
          <CardTitle>Submit Application</CardTitle>
        </CardHeader>
        <CardContent>
          <form className="space-y-4">
            <div>
              <Label htmlFor="job-role">Job Role / Department</Label>
              <Select id="job-role">
                <option>Frontend Developer</option>
                <option>Backend Developer</option>
                <option>Full Stack Developer</option>
                <option>UI/UX Designer</option>
              </Select>
            </div>
            <div>
              <Label htmlFor="resume">Upload Resume (PDF/DOC)</Label>
              <Input id="resume" type="file" accept=".pdf,.doc,.docx" />
            </div>
            <div>
              <Label htmlFor="availability">Provide Availability</Label>
              <Input id="availability" type="datetime-local" />
            </div>
            <Button type="submit" className="bg-[#FF9E46] hover:bg-[#FF9E46]/90">
              Submit Application
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

