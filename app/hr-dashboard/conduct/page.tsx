import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function ConductInterviews() {
  const upcomingInterviews = [
    { id: 1, name: "John Doe", role: "Frontend Developer", time: "2:00 PM" },
    { id: 2, name: "Jane Smith", role: "UI/UX Designer", time: "3:30 PM" },
  ]

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">Conduct Interviews</h2>
      <Card>
        <CardHeader>
          <CardTitle>Today's Interviews</CardTitle>
        </CardHeader>
        <CardContent>
          {upcomingInterviews.map((interview) => (
            <div key={interview.id} className="flex items-center justify-between mb-4">
              <div>
                <h3 className="font-bold">{interview.name}</h3>
                <p>
                  {interview.role} - {interview.time}
                </p>
              </div>
              <Button className="bg-[#FF9E46] hover:bg-[#19A5A2]/90">Join Interview</Button>
            </div>
          ))}
        </CardContent>
      </Card>
      {/* Here you would integrate your video conferencing solution */}
    </div>
  )
}

