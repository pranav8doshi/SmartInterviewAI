import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Calendar, Video, Bell, CheckCircle, ArrowRight } from "lucide-react"

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Header/Navbar */}
      <header className="sticky top-0 z-50 w-full border-b bg-gradient-to-r from-[#1f465e] to-[#1f465e]">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center space-x-2">
          <img src = "download.png"
           alt="AI Avatar" width="100" height="50"/>
            
            <span className="text-2xl font-bold text-white">InterviewAI</span>
            <Video className="h-8 w-8 text-white" />
          </div>
          <nav className="hidden md:flex items-center space-x-6">
            <Link href="/" className="text-sm font-medium text-white hover:text-white/80">
              Home
            </Link>
            <Link href="#about" className="text-sm font-medium text-white hover:text-white/80">
              About Us
            </Link>
            <Link href="#features" className="text-sm font-medium text-white hover:text-white/80">
              Features
            </Link>
            <Link href="#contact" className="text-sm font-medium text-white hover:text-white/80">
              Contact
            </Link>
            <Link href="/login">
  <Button className="bg-[#ffab3fe6] text-white hover:bg-white hover:text-black">
    Login
  </Button>
</Link>
          </nav>
        </div>
      </header>

      <main className="flex-1">
        {/* Hero Section */}
        <section className="w-full py-12 md:py-24 lg:py-32 bg-gradient-to-b from-[#E98300B3] to-[#E98300B3] text-white">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center space-y-4 text-center">
              <div className="inline-flex items-center rounded-lg bg-white/10 px-3 py-1 text-sm">
                <span className="text-white">✨ AI-Powered Interview Platform</span>
              </div>
              <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none xl:text-7xl/none">
                Prepare. Apply. <span className="text-[#F37021]">Get Hired.</span>
              </h1>
              <p className="mx-auto max-w-[700px] text-gray-200 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                Transform your interview process with AI-powered interviews. Practice, perfect, and land your dream job
                with our cutting-edge platform.
              </p>
              <div className="flex flex-col gap-4 min-[400px]:flex-row">
                <Button className="bg-[#E98300B3] text-white hover:bg-[#E98300B3]/90 h-11 px-8">
                  Get Started
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
                <Button
                  variant="outline"
                  className="border-white text-black hover:bg-orange hover:text-[#E98300B3] h-11 px-8"
                >
                  Learn More
                </Button>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="w-full py-12 md:py-24 lg:py-32 bg-gray-50">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <div className="inline-flex items-center rounded-lg bg-[#E98300B3]/10 px-3 py-1 text-sm text-[#E98300B3]">
                  <span>Key Features</span>
                </div>
                <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">Everything you need</h2>
                <p className="mx-auto max-w-[900px] text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                  Our platform provides all the tools you need for a seamless interview experience.
                </p>
              </div>
            </div>
            <div className="mx-auto grid max-w-5xl grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4 mt-12">
              <div className="relative overflow-hidden rounded-lg border bg-white p-6 shadow-sm transition-all hover:shadow-lg">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-[#E98300B3]/10 text-[#E98300B3] mb-4">
                  <CheckCircle className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-bold">Apply for Interviews</h3>
                <p className="text-gray-500 mt-2">Submit applications and get matched with perfect opportunities.</p>
              </div>
              <div className="relative overflow-hidden rounded-lg border bg-white p-6 shadow-sm transition-all hover:shadow-lg">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-[#E98300B3]/10 text-[#E98300B3] mb-4">
                  <Calendar className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-bold">Schedule & Manage</h3>
                <p className="text-gray-500 mt-2">Easily schedule and manage your upcoming interviews.</p>
              </div>
              <div className="relative overflow-hidden rounded-lg border bg-white p-6 shadow-sm transition-all hover:shadow-lg">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-[#E98300B3]/10 text-[#E98300B3] mb-4">
                  <Video className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-bold">Video Interviews</h3>
                <p className="text-gray-500 mt-2">Conduct seamless video interviews with our integrated platform.</p>
              </div>
              <div className="relative overflow-hidden rounded-lg border bg-white p-6 shadow-sm transition-all hover:shadow-lg">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-[#E98300B3]/10 text-[#E98300B3] mb-4">
                  <Bell className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-bold">Notifications</h3>
                <p className="text-gray-500 mt-2">Stay updated with real-time notifications and reminders.</p>
              </div>
            </div>
          </div>
        </section>

        {/* How It Works Section */}
        <section className="w-full py-12 md:py-24 lg:py-32 bg-[#E98300B3]/5">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <div className="inline-flex items-center rounded-lg bg-[#E98300B3]/10 px-3 py-1 text-sm text-[#E98300B3]">
                  <span>Simple Process</span>
                </div>
                <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">How It Works</h2>
                <p className="mx-auto max-w-[900px] text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                  Get started with our platform in three simple steps
                </p>
              </div>
            </div>
            <div className="mx-auto grid max-w-5xl grid-cols-1 gap-6 md:grid-cols-3 mt-12">
              <div className="relative overflow-hidden rounded-lg border bg-white p-8 shadow-sm transition-all hover:shadow-lg">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-[#E98300B3] text-white text-xl font-bold mb-6">
                  1
                </div>
                <h3 className="text-xl font-bold">Create an Account</h3>
                <p className="text-gray-500 mt-2">Choose between HR or Candidate profile and get started.</p>
              </div>
              <div className="relative overflow-hidden rounded-lg border bg-white p-8 shadow-sm transition-all hover:shadow-lg">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-[#E98300B3] text-white text-xl font-bold mb-6">
                  2
                </div>
                <h3 className="text-xl font-bold">Apply & Schedule</h3>
                <p className="text-gray-500 mt-2">Browse opportunities and schedule your interviews.</p>
              </div>
              <div className="relative overflow-hidden rounded-lg border bg-white p-8 shadow-sm transition-all hover:shadow-lg">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-[#E98300B3] text-white text-xl font-bold mb-6">
                  3
                </div>
                <h3 className="text-xl font-bold">Join & Track</h3>
                <p className="text-gray-500 mt-2">Attend interviews and track your progress.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Testimonials Section */}
        <section className="w-full py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <div className="inline-flex items-center rounded-lg bg-[#E98300B3]/10 px-3 py-1 text-sm text-[#E98300B3]">
                  <span>Testimonials</span>
                </div>
                <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">Success Stories</h2>
                <p className="mx-auto max-w-[900px] text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                  Hear from our successful candidates and hiring managers
                </p>
              </div>
            </div>
            <div className="mx-auto grid max-w-5xl grid-cols-1 gap-6 md:grid-cols-3 mt-12">
              <div className="relative overflow-hidden rounded-lg border bg-gradient-to-b from-white to-gray-50 p-6 shadow-sm">
                <div className="flex flex-col gap-4">
                  <p className="text-gray-600">
                    "InterviewAI helped me prepare and land my dream job at a top tech company. The platform is
                    intuitive and effective."
                  </p>
                  <div className="mt-4">
                    <p className="font-semibold text-[#E98300B3]">Sarah K.</p>
                    <p className="text-sm text-gray-500">Software Engineer</p>
                  </div>
                </div>
              </div>
              <div className="relative overflow-hidden rounded-lg border bg-gradient-to-b from-white to-gray-50 p-6 shadow-sm">
                <div className="flex flex-col gap-4">
                  <p className="text-gray-600">
                    "As an HR manager, this platform has streamlined our entire interview process. It's a game-changer!"
                  </p>
                  <div className="mt-4">
                    <p className="font-semibold text-[#E98300B3]">Michael R.</p>
                    <p className="text-sm text-gray-500">HR Director</p>
                  </div>
                </div>
              </div>
              <div className="relative overflow-hidden rounded-lg border bg-gradient-to-b from-white to-gray-50 p-6 shadow-sm">
                <div className="flex flex-col gap-4">
                  <p className="text-gray-600">
                    "The AI-powered features have significantly improved our candidate evaluation process."
                  </p>
                  <div className="mt-4">
                    <p className="font-semibold text-[#E98300B3]">Emily T.</p>
                    <p className="text-sm text-gray-500">Recruitment Manager</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="w-full border-t bg-[#E98300B3] text-white">
        <div className="container px-4 py-12 md:px-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">TE Connectivity</h3>
              <p className="text-sm text-white">Transforming the interview process with AI technology.</p>
            </div>
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Contact</h3>
              <p className="text-sm text-white">Email: herinterview@gmail.com</p>
              <p className="text-sm text-white">Phone: 9022296054</p>
            </div>
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Legal</h3>
              <ul className="space-y-2 text-sm text-white">
                <li>
                  <Link href="/privacy" className="hover:text-[#E98300B3]">
                    Privacy Policy
                  </Link>
                </li>
                <li>
                  <Link href="/terms" className="hover:text-[#E98300B3]">
                    Terms of Service
                  </Link>
                </li>
              </ul>
            </div>
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Follow Us</h3>
              <div className="flex space-x-4 text-white">
                <Link href="#" className="hover:text-[#E98300B3]">
                  Twitter
                </Link>
                <Link href="#" className="hover:text-[#E98300B3]">
                  LinkedIn
                </Link>
                <Link href="#" className="hover:text-[#E98300B3]">
                  Facebook
                </Link>
              </div>
            </div>
          </div>
          <div className="mt-8 border-t border-gray-700 pt-8 text-center text-sm text-white">
            <p>&copy; {new Date().getFullYear()} InterviewAI. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

