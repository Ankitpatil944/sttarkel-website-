import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Index from "./pages/Index";
import AptitudeTest from "./pages/AptitudeTest";
import Analytics from "./pages/Analytics";
import Interview from "./pages/Interview";
import Companies from "./pages/Companies";
import NotFound from "./pages/NotFound";

// New pages
import Blogs from "./pages/Blogs";
import About from "./pages/About";
import Services from "./pages/Services";
import Mentorship from "./pages/Mentorship";
import FindMentor from "./pages/FindMentor";
import BecomeMentor from "./pages/BecomeMentor";
import AIAssessment from "./pages/AIAssessment";
import ResumeBuilder from "./pages/ResumeBuilder";
import JobListing from "./pages/JobListing";
import CareerRoadmap from "./pages/CareerRoadmap";
import Placement from "./pages/Placement";
import AssessmentPage from "./pages/AssessmentPage";
import InterviewPage from "./pages/InterviewPage";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/assessment/aptitude" element={<AptitudeTest />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/interview" element={<Interview />} />
          <Route path="/companies" element={<Companies />} />
          
          {/* New navbar routes */}
          <Route path="/blogs" element={<Blogs />} />
          <Route path="/about" element={<About />} />
          <Route path="/services" element={<Services />} />
          <Route path="/mentorship" element={<Mentorship />} />
          <Route path="/find-mentor" element={<FindMentor />} />
          <Route path="/become-mentor" element={<BecomeMentor />} />
          
          {/* Service sub-routes */}
          <Route path="/services/ai-assessment" element={<AIAssessment />} />
          <Route path="/ai-assessment" element={<AIAssessment />} />
          <Route path="/services/resume-builder" element={<ResumeBuilder />} />
          <Route path="/services/jobs" element={<JobListing />} />
          <Route path="/services/career-roadmap" element={<CareerRoadmap />} />
          <Route path="/services/placement" element={<Placement />} />

          {/* New assessment and interview routes */}
          <Route path="/assessment" element={<AssessmentPage />} />
          <Route path="/interview-page" element={<InterviewPage />} />
          
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
