import type React from "react"
import Link from "next/link"
import { BarChart, Bell, Calendar, FileText, Home, Settings, User, Clock } from "lucide-react"

const sidebarItems = [
  { icon: Home, label: "Dashboard", href: "/dashboard" },
  { icon: FileText, label: "Apply for Interview", href: "/dashboard/apply" },
  { icon: Calendar, label: "Interview Schedule", href: "/dashboard/schedule" },
  { icon: BarChart, label: "Feedback & Results", href: "/dashboard/feedback" },
  { icon: Bell, label: "Notifications", href: "/dashboard/notifications" },
  { icon: Clock, label: "Interview History", href: "/dashboard/history" },
  { icon: User, label: "Profile", href: "/dashboard/profile" },
  { icon: Settings, label: "Settings", href: "/dashboard/settings" },
]

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-[#FF9E46] text-white">
        <div className="p-4">
          <h1 className="text-2xl font-bold">InterviewAI</h1>
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

