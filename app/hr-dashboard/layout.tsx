import type React from "react"
import Link from "next/link"
import { BarChart, Bell, Calendar, FileText, Home, Settings, Clock, Users, Video } from "lucide-react"

const sidebarItems = [
  { icon: Home, label: "Dashboard", href: "/hr-dashboard" },
  { icon: Users, label: "Candidate Applications", href: "/hr-dashboard/applications" },
  { icon: Calendar, label: "Schedule Interviews", href: "/hr-dashboard/schedule" },
  { icon: Video, label: "Conduct Interviews", href: "/hr-dashboard/conduct" },
  { icon: BarChart, label: "Rate & Feedback", href: "/hr-dashboard/feedback" },
  { icon: Clock, label: "Interview Status", href: "/hr-dashboard/status" },
  { icon: FileText, label: "Candidate History", href: "/hr-dashboard/history" },
  { icon: Bell, label: "Notifications", href: "/hr-dashboard/notifications" },
  { icon: Settings, label: "Settings", href: "/hr-dashboard/settings" },
]

export default function HRDashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-[#FF9E46] text-white">
        <div className="p-4">
          <h1 className="text-2xl font-bold">InterviewAI HR</h1>
        </div>
        <nav className="mt-8">
          {sidebarItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="flex items-center px-4 py-2 mt-2 text-gray-100 hover:bg-[#19A5A2]/50"
            >
              <item.icon className="w-5 h-5 mr-3" />
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8 overflow-y-auto">{children}</main>
    </div>
  )
}

