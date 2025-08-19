import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { 
  FileText, 
  Download, 
  Eye, 
  Edit, 
  CheckCircle,
  Sparkles,
  ArrowRight,
  Star,
  Users,
  Target,
  Zap,
  Shield,
  Palette,
  FileUp,
  Copy,
  Share2,
  TrendingUp
} from "lucide-react";
import { useState } from "react";
import { motion } from 'framer-motion';
import Footer from "@/components/Footer";
import './OutlinedText.css';

const ResumeBuilder = () => {
  const [activeStep, setActiveStep] = useState(1);

  const templates = [
    {
      id: 1,
      name: "Professional",
      category: "Corporate",
      image: "/Images/resume-template-1.jpg",
      popular: true
    },
    {
      id: 2,
      name: "Creative",
      category: "Design",
      image: "/Images/resume-template-2.jpg",
      popular: false
    },
    {
      id: 3,
      name: "Minimal",
      category: "Tech",
      image: "/Images/resume-template-3.jpg",
      popular: false
    },
    {
      id: 4,
      name: "Executive",
      category: "Leadership",
      image: "/Images/resume-template-4.jpg",
      popular: true
    }
  ];

  const features = [
    {
      icon: Target,
      title: "ATS Optimized",
      description: "Built to pass Applicant Tracking Systems and reach human recruiters"
    },
    {
      icon: Palette,
      title: "Professional Templates",
      description: "Choose from 20+ industry-specific templates designed by experts"
    },
    {
      icon: Zap,
      title: "AI Content Suggestions",
      description: "Get intelligent suggestions to improve your resume content and impact"
    },
    {
      icon: Shield,
      title: "Privacy Protected",
      description: "Your data is secure and never shared with third parties"
    }
  ];

  const steps = [
    {
      number: 1,
      title: "Choose Template",
      description: "Select from our professional templates"
    },
    {
      number: 2,
      title: "Add Information",
      description: "Fill in your details and experience"
    },
    {
      number: 3,
      title: "AI Enhancement",
      description: "Get AI-powered suggestions and improvements"
    },
    {
      number: 4,
      title: "Download & Share",
      description: "Export in multiple formats and share"
    }
  ];

  const testimonials = [
    {
      name: "Sarah Chen",
      role: "Software Engineer",
      company: "Google",
      quote: "The ATS optimization feature helped me get past screening systems. I received 3x more interview calls!",
      improvement: "+300%"
    },
    {
      name: "Michael Rodriguez",
      role: "Marketing Manager",
      company: "Microsoft",
      quote: "The AI suggestions made my resume much more impactful. I landed my dream job within 2 weeks.",
      improvement: "+150%"
    },
    {
      name: "Priya Sharma",
      role: "Data Analyst",
      company: "Amazon",
      quote: "Professional templates and easy customization. My resume now stands out from the crowd.",
      improvement: "+200%"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-bg">
      <div
        className="min-h-screen max-w-screen-2xl mx-auto px-4 sm:px-6 lg:px-8 
                    m-4 sm:m-6 lg:m-10 bg-gradient-bg border border-blue-300 rounded-3xl overflow-hidden bg-gradient-to-b from-slate-100 to-cyan-50
                    animate-fade-in mt-20"
        style={{ marginTop: '5rem' }}
      >
        {/* Hero Section */}
        <div className="pt-20 mt-10 pb-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <div className="inline-flex items-center space-x-2 bg-card/50 backdrop-blur-sm rounded-full px-4 py-2 mb-6 border border-primary/20">
              <Sparkles className="h-4 w-4 text-primary" />
              <span className="text-sm font-medium">ATS-Optimized Resumes</span>
            </div>
            <h1 className="text-3xl sm:text-4xl md:text-6xl lg:text-7xl font-normal mb-6 leading-tight animate-fade-in text-[#2D3253]">
              Resume <span className="bg-gradient-primary bg-clip-text text-transparent">Builder</span>
            </h1>
            <p className="text-xl text-muted-foreground mb-10 max-w-3xl mx-auto leading-relaxed animate-fade-in">
              Create professional, ATS-optimized resumes that stand out to hiring managers. Get AI-powered suggestions and industry-specific templates.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg">
                Start Building
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
              <Button variant="outline" size="lg">
                View Templates
              </Button>
            </div>
          </div>

          {/* Features */}
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
            {features.map((feature) => (
              <Card key={feature.title} className="p-6 text-center border-primary/10">
                <feature.icon className="h-12 w-12 mx-auto mb-4 text-primary" />
                <h3 className="font-bold text-lg mb-2">{feature.title}</h3>
                <p className="text-muted-foreground text-sm">{feature.description}</p>
              </Card>
            ))}
          </div>

          {/* Templates */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-center mb-12">Professional Templates</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {templates.map((template) => (
                <Card key={template.id} className="overflow-hidden hover:shadow-lg transition-shadow border-primary/10 group cursor-pointer">
                  <div className="aspect-[3/4] bg-gradient-to-br from-primary/10 to-primary/5 flex items-center justify-center">
                    <FileText className="h-16 w-16 text-primary/50" />
                  </div>
                  <div className="p-4">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-bold">{template.name}</h3>
                      {template.popular && (
                        <Badge variant="secondary" className="text-xs">Popular</Badge>
                      )}
                    </div>
                    <p className="text-sm text-muted-foreground mb-3">{template.category}</p>
                    <Button className="w-full" variant="outline">
                      Use Template
                    </Button>
                  </div>
                </Card>
              ))}
            </div>
          </div>

          {/* How It Works */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
            <div className="grid md:grid-cols-4 gap-8">
              {steps.map((step) => (
                <Card key={step.number} className="p-6 text-center border-primary/10">
                  <div className="h-12 w-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-primary font-bold text-xl">{step.number}</span>
                  </div>
                  <h3 className="font-bold text-lg mb-2">{step.title}</h3>
                  <p className="text-muted-foreground text-sm">{step.description}</p>
                </Card>
              ))}
            </div>
          </div>

          {/* Resume Builder Interface */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-center mb-12">Start Building Your Resume</h2>
            <div className="grid lg:grid-cols-2 gap-8">
              {/* Form */}
              <Card className="p-6 border-primary/10">
                <h3 className="font-bold text-xl mb-6">Personal Information</h3>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-sm font-medium mb-2 block">First Name</label>
                      <Input placeholder="John" />
                    </div>
                    <div>
                      <label className="text-sm font-medium mb-2 block">Last Name</label>
                      <Input placeholder="Doe" />
                    </div>
                  </div>
                  <div>
                    <label className="text-sm font-medium mb-2 block">Email</label>
                    <Input placeholder="john.doe@email.com" type="email" />
                  </div>
                  <div>
                    <label className="text-sm font-medium mb-2 block">Phone</label>
                    <Input placeholder="+1 (555) 123-4567" />
                  </div>
                  <div>
                    <label className="text-sm font-medium mb-2 block">Location</label>
                    <Input placeholder="San Francisco, CA" />
                  </div>
                  <div>
                    <label className="text-sm font-medium mb-2 block">Professional Summary</label>
                    <Textarea 
                      placeholder="Brief overview of your professional background and career objectives..."
                      rows={4}
                    />
                  </div>
                  <Button className="w-full">
                    Continue to Experience
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </div>
              </Card>

              {/* Preview */}
              <Card className="p-6 border-primary/10">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="font-bold text-xl">Resume Preview</h3>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm">
                      <Eye className="h-4 w-4 mr-2" />
                      Preview
                    </Button>
                    <Button variant="outline" size="sm">
                      <Download className="h-4 w-4 mr-2" />
                      Download
                    </Button>
                  </div>
                </div>
                <div className="aspect-[3/4] bg-white border rounded-lg p-6 shadow-sm">
                  <div className="text-center mb-6">
                    <h2 className="text-2xl font-bold text-gray-800">John Doe</h2>
                    <p className="text-gray-600">Software Engineer</p>
                    <p className="text-sm text-gray-500">john.doe@email.com • +1 (555) 123-4567</p>
                    <p className="text-sm text-gray-500">San Francisco, CA</p>
                  </div>
                  <div>
                    <h3 className="font-bold text-lg text-gray-800 mb-2">Professional Summary</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      Experienced software engineer with 5+ years developing scalable web applications...
                    </p>
                    <div className="text-center text-gray-400 text-sm">
                      Continue building to see more sections
                    </div>
                  </div>
                </div>
              </Card>
            </div>
          </div>

          {/* Testimonials */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-center mb-12">Success Stories</h2>
            <div className="grid md:grid-cols-3 gap-6">
              {testimonials.map((testimonial, index) => (
                <Card key={index} className="p-6 border-primary/10">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="h-10 w-10 bg-primary/10 rounded-full flex items-center justify-center">
                      <span className="text-primary font-bold text-sm">
                        {testimonial.name.split(' ').map(n => n[0]).join('')}
                      </span>
                    </div>
                    <div>
                      <p className="font-medium">{testimonial.name}</p>
                      <p className="text-xs text-muted-foreground">{testimonial.role} at {testimonial.company}</p>
                    </div>
                  </div>
                  <p className="text-muted-foreground mb-4 italic">"{testimonial.quote}"</p>
                  <div className="flex items-center gap-2">
                    <TrendingUp className="h-4 w-4 text-green-500" />
                    <span className="text-sm text-green-500 font-medium">{testimonial.improvement} more interviews</span>
                  </div>
                </Card>
              ))}
            </div>
          </div>

          {/* CTA Section */}
          <div className="text-center">
            <Card className="p-8 bg-gradient-card border-primary/10">
              <h3 className="text-2xl font-bold mb-3">Ready to Create Your Professional Resume?</h3>
              <p className="text-muted-foreground mb-6 max-w-md mx-auto">
                Join thousands of professionals who have landed their dream jobs with our AI-powered resume builder.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button size="lg">
                  Start Building Free
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
                <Button variant="outline" size="lg">
                  View All Templates
                </Button>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>

    <Footer />

    <div className="px-4 sm:px-6 lg:px-8 text-center">
      <h1
        className="outlined-text text-[3.5rem] sm:text-[6rem] md:text-[8rem] lg:text-[10rem] xl:text-[12rem] 2xl:text-[14rem] leading-none tracking-widest"
      >
        STTARKEL
      </h1>
    </div>
  </div>
  );
};

export default ResumeBuilder; 