import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select } from "@/components/ui/select"

export default function RateAndFeedback() {
  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">Rate & Provide Feedback</h2>
      <Card>
        <CardHeader>
          <CardTitle>Interview Feedback</CardTitle>
        </CardHeader>
        <CardContent>
          <form className="space-y-4">
            <div>
              <Label htmlFor="candidate">Select Candidate</Label>
              <Select id="candidate">
                <option>John Doe - Frontend Developer</option>
                <option>Jane Smith - UI/UX Designer</option>
              </Select>
            </div>
            <div>
              <Label htmlFor="score">Score (1-10)</Label>
              <Input id="score" type="number" min="1" max="10" />
            </div>
            <div>
              <Label htmlFor="comments">Comments</Label>
              <Textarea id="comments" placeholder="Provide detailed feedback..." />
            </div>
            <div>
              <Label htmlFor="status">Interview Status</Label>
              <Select id="status">
                <option>Passed</option>
                <option>Failed</option>
              </Select>
            </div>
            <Button type="submit" className="bg-[#FF9E46] hover:bg-[#19A5A2]/90">
              Submit Feedback
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

