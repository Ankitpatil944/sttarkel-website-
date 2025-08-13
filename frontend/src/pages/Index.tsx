import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Link } from "react-router-dom";
import { 
  Brain, 
  Target, 
  BarChart, 
  Users, 
  CheckCircle, 
  ArrowRight,
  Sparkles,
  Zap,
  Trophy,
  FileUp,
  ClipboardCheck,
  Bot,
  MessageSquare,
  Briefcase,
  Shield,
  Lock,
  Star,
  Quote,
  Mail
} from "lucide-react";
// import heroBg from "@/assets/hero-bg.jpg";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "@/components/ui/accordion";
import Footer from "@/components/Footer";

const Index = () => {
  const features = [
    {
      icon: Brain,
      title: "Smart Assessments",
      description: "Intelligent evaluation system designed for comprehensive skill assessment",
    },
    {
      icon: Target,
      title: "Focused Preparation",
      description: "Structured approach to help you excel in your professional journey",
    },
    {
      icon: BarChart,
      title: "Progress Tracking",
      description: "Monitor your development with detailed insights and analytics",
    },
    {
      icon: Users,
      title: "Professional Network",
      description: "Connect with opportunities and build your career foundation",
    },
  ];

  const flowSteps = [
    { icon: FileUp, label: "Resume Upload" },
    { icon: ClipboardCheck, label: "Assessment" },
    { icon: Bot, label: "AI Interview" },
    { icon: MessageSquare, label: "Feedback" },
    { icon: Briefcase, label: "Job Openings" },
  ];

  const stats = [
    { label: "Candidates Assessed", value: "25k+" },
    { label: "Avg. Score Improvement", value: "18%" },
    { label: "Interview Qs Practiced", value: "350k+" },
    { label: "Hiring Partners", value: "120+" },
  ];

  const testimonials = [
    {
      name: "Aarav", role: "SWE, Bengaluru", initials: "AR", quote:
        "The assessments felt practical and the feedback was specific. I landed two interviews in a week.",
    },
    {
      name: "Meera", role: "Data Analyst, Pune", initials: "MR", quote:
        "Loved the AI interview. It highlighted how I speak under pressure and what to fix before the real thing.",
    },
    {
      name: "Karthik", role: "Full‑stack Dev, Chennai", initials: "KT", quote:
        "No fluff. Clear steps, clean UI, and helpful insights. It kept me focused on what matters.",
    },
  ];

  const faqs = [
    {
      q: "Do I need prior experience to start?",
      a: "No. The platform adapts to your level and guides you from basics to advanced topics.",
    },
    {
      q: "Can I retake assessments?",
      a: "Yes. You can retake assessments and track improvement across attempts.",
    },
    {
      q: "How does the AI interview work?",
      a: "You answer realistic questions on camera/mic. We analyze content, clarity, and confidence to give actionable feedback.",
    },
    {
      q: "Is my data secure?",
      a: "We use encrypted storage and strict access controls. You can delete your data anytime from settings.",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-bg">
      
      {/* Hero Section */}
      <section className="relative pt-24 pb-20">
        {/* Removed background image and overlay */}
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-4xl mx-auto">
            <div className="inline-flex items-center space-x-2 bg-card/50 backdrop-blur-sm rounded-full px-4 py-2 mb-8 border border-primary/20 animate-fade-in">
              <Sparkles className="h-4 w-4 text-primary animate-pulse" />
              <span className="text-sm font-medium">Professional Assessment Platform</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight animate-fade-in">
              Build Your
              <span className="bg-gradient-primary bg-clip-text text-transparent block animate-scale-in">
                Future Today
              </span>
            </h1>
            
            <p className="text-xl text-muted-foreground mb-10 max-w-2xl mx-auto leading-relaxed animate-fade-in">
              Take the next step in your career with our comprehensive assessment and preparation platform. 
              Designed to help you succeed in your professional goals.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center animate-fade-in">
              <Link to="/difficulty">
                <Button variant="default" size="lg" className="group hover-scale">
                  Start Assessment
                  <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Link>
              <Button variant="outline" size="lg" className="hover-scale">
                Learn More
              </Button>
            </div>

            {/* Process Flow */}
            <div className="mt-12 animate-fade-in" style={{ animationDelay: '0.1s' }}>
              <div className="flex flex-col md:flex-row items-center md:items-stretch gap-6 md:gap-4">
                {flowSteps.map((step, index) => (
                  <div key={step.label} className="flex items-center w-full md:w-auto">
                    <div className="flex flex-col items-center text-center">
                      <div className="w-14 h-14 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center mb-3">
                        <step.icon className="h-6 w-6 text-primary" />
                      </div>
                      <span className="text-sm font-medium text-foreground/90">{step.label}</span>
                    </div>
                    {index < flowSteps.length - 1 && (
                      <div className="hidden md:flex flex-1 mx-4">
                        <div className="h-px w-24 bg-primary/30 self-center" />
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {/* Mobile connectors */}
              <div className="md:hidden mt-4 flex flex-col items-center gap-3">
                {flowSteps.slice(0, flowSteps.length - 1).map((_, idx) => (
                  <div key={idx} className="w-px h-4 bg-primary/30" />
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Social Proof */}
      <section className="py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-wrap items-center justify-center gap-3 text-muted-foreground/80">
            <Badge variant="secondary" className="bg-card/60 border-primary/10">Trusted by early‑career and experienced professionals</Badge>
            <Badge variant="outline">Tech • Product • Data • Cloud</Badge>
            <Badge variant="outline">Interview‑ready in weeks</Badge>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16 animate-fade-in">
            <h2 className="text-3xl md:text-5xl font-bold mb-4">
              Why Choose 
              <span className="bg-gradient-primary bg-clip-text text-transparent"> Sttarkel</span>
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Comprehensive platform designed to help you succeed in your professional journey
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {features.map((feature, index) => (
              <Card 
                key={index} 
                className="p-8 bg-gradient-card border-primary/10 hover:border-primary/30 transition-all duration-300 hover:shadow-glow-accent group hover-scale animate-fade-in"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0">
                    <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center group-hover:bg-primary/20 transition-colors group-hover:animate-pulse">
                      <feature.icon className="h-6 w-6 text-primary" />
                    </div>
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-3 group-hover:text-primary transition-colors">
                      {feature.title}
                    </h3>
                    <p className="text-muted-foreground leading-relaxed">
                      {feature.description}
                    </p>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Stats strip */}
      <section className="py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {stats.map((s) => (
              <Card key={s.label} className="p-6 text-center bg-gradient-card border-primary/10">
                <div className="text-3xl font-bold">{s.value}</div>
                <div className="text-sm text-muted-foreground mt-1">{s.label}</div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Trust & Security */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-8 items-stretch">
            <Card className="p-8 bg-gradient-card border-primary/10">
              <div className="flex items-center gap-3 mb-4">
                <Shield className="h-6 w-6 text-primary" />
                <h3 className="text-xl font-semibold">Built for privacy and trust</h3>
              </div>
              <ul className="space-y-3 text-sm text-muted-foreground">
                <li className="flex items-start gap-2"><CheckCircle className="h-4 w-4 text-primary mt-0.5" /> Data encryption at rest and in transit</li>
                <li className="flex items-start gap-2"><CheckCircle className="h-4 w-4 text-primary mt-0.5" /> Role‑based access and secure storage</li>
                <li className="flex items-start gap-2"><CheckCircle className="h-4 w-4 text-primary mt-0.5" /> You control what to share with employers</li>
              </ul>
            </Card>
            <Card className="p-8 bg-gradient-card border-primary/10">
              <div className="flex items-center gap-3 mb-4">
                <Lock className="h-6 w-6 text-primary" />
                <h3 className="text-xl font-semibold">Clear, practical outcomes</h3>
              </div>
              <ul className="space-y-3 text-sm text-muted-foreground">
                <li className="flex items-start gap-2"><CheckCircle className="h-4 w-4 text-primary mt-0.5" /> Actionable feedback after every step</li>
                <li className="flex items-start gap-2"><CheckCircle className="h-4 w-4 text-primary mt-0.5" /> Skill‑gap insights with next‑step guidance</li>
                <li className="flex items-start gap-2"><CheckCircle className="h-4 w-4 text-primary mt-0.5" /> Connect with relevant job openings</li>
              </ul>
            </Card>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h3 className="text-2xl md:text-4xl font-bold">What candidates say</h3>
            <p className="text-muted-foreground mt-2">Honest words from people who used the platform</p>
          </div>
          <div className="grid md:grid-cols-3 gap-6">
            {testimonials.map((t, idx) => (
              <Card key={idx} className="p-6 bg-gradient-card border-primary/10">
                <div className="flex items-center gap-3 mb-4">
                  <Avatar className="h-10 w-10">
                    <AvatarFallback>{t.initials}</AvatarFallback>
                  </Avatar>
                  <div>
                    <div className="font-medium">{t.name}</div>
                    <div className="text-xs text-muted-foreground">{t.role}</div>
                  </div>
                </div>
                <div className="flex items-start gap-2 text-foreground/90">
                  <Quote className="h-4 w-4 mt-1 text-primary" />
                  <p className="leading-relaxed">{t.quote}</p>
                </div>
                <div className="flex gap-1 mt-4 text-primary">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="h-4 w-4 fill-primary" />
                  ))}
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-16">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
          <h3 className="text-2xl md:text-4xl font-bold text-center mb-8">Questions, answered</h3>
          <Card className="p-4 md:p-6 bg-gradient-card border-primary/10">
            <Accordion type="single" collapsible className="w-full">
              {faqs.map((item, idx) => (
                <AccordionItem key={idx} value={`item-${idx}`}>
                  <AccordionTrigger>{item.q}</AccordionTrigger>
                  <AccordionContent>{item.a}</AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </Card>
        </div>
      </section>

      {/* Newsletter / Job alerts */}
      <section className="py-16">
        <div className="max-w-xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h3 className="text-2xl md:text-4xl font-bold mb-3">Get updates that matter</h3>
          <p className="text-muted-foreground mb-6">Occasional tips, mock interview invites, and relevant roles. No spam.</p>
          <div className="flex gap-2">
            <Input type="email" placeholder="you@example.com" className="bg-card/60 border-primary/20" />
            <Button className="whitespace-nowrap"><Mail className="h-4 w-4 mr-2" /> Notify me</Button>
          </div>
          <div className="text-xs text-muted-foreground mt-3">By subscribing, you agree to our updates. Unsubscribe anytime.</div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-primary relative overflow-hidden animate-fade-in">
        <div className="absolute inset-0 bg-black/20" />
        <div className="relative max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <Trophy className="h-16 w-16 text-white mx-auto mb-6 animate-pulse" />
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-6 animate-scale-in">
            Ready to Get Started?
          </h2>
          <p className="text-xl text-white/90 mb-10 max-w-2xl mx-auto animate-fade-in">
            Take the first step towards your professional goals with our comprehensive assessment platform
          </p>
          <Link to="/difficulty">
            <Button 
              variant="outline" 
              size="lg" 
              className="bg-white text-primary hover:bg-white/90 border-white hover-scale animate-fade-in"
            >
              <Zap className="mr-2 h-5 w-5" />
              Begin Assessment
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default Index;
