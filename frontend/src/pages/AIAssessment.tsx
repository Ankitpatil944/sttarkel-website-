import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { 
  Bot, 
  Brain, 
  Target, 
  BarChart, 
  Clock,
  CheckCircle,
  Play,
  Mic,
  Video,
  FileText,
  Users,
  Star,
  ArrowRight,
  Sparkles,
  Zap,
  Shield,
  TrendingUp,
  MessageSquare,
  Lightbulb
} from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from 'framer-motion';
import Footer from "@/components/Footer";
import './OutlinedText.css';

const AIAssessment = () => {
  const [activeTab, setActiveTab] = useState<'assessment' | 'interview'>('assessment');
  const navigate = useNavigate();

  const assessmentFeatures = [
    {
      icon: Brain,
      title: "Adaptive Testing",
      description: "Questions adjust to your skill level in real-time for accurate assessment"
    },
    {
      icon: BarChart,
      title: "Detailed Analytics",
      description: "Comprehensive performance breakdown with skill-specific insights"
    },
    {
      icon: Target,
      title: "Industry Benchmarking",
      description: "Compare your performance against industry standards and peers"
    },
    {
      icon: Clock,
      title: "Time Management",
      description: "Practice under realistic time constraints to improve efficiency"
    }
  ];

  const interviewFeatures = [
    {
      icon: Video,
      title: "Video Recording",
      description: "Record your responses and analyze body language and presentation"
    },
    {
      icon: Mic,
      title: "Voice Analysis",
      description: "AI analyzes tone, pace, and clarity of your verbal responses"
    },
    {
      icon: MessageSquare,
      title: "Real-time Feedback",
      description: "Get instant feedback on your answers and communication style"
    },
    {
      icon: Users,
      title: "Behavioral Questions",
      description: "Practice with common behavioral and situational questions"
    }
  ];

  const assessmentTypes = [
    {
      name: "Technical Skills",
      description: "Programming, data analysis, design tools",
      duration: "45-60 min",
      questions: "30-40",
      difficulty: "Adaptive"
    },
    {
      name: "Soft Skills",
      description: "Communication, leadership, problem-solving",
      duration: "30-45 min",
      questions: "20-25",
      difficulty: "Adaptive"
    },
    {
      name: "Domain Knowledge",
      description: "Industry-specific knowledge and expertise",
      duration: "60-90 min",
      questions: "40-50",
      difficulty: "Adaptive"
    },
    {
      name: "Cognitive Ability",
      description: "Logical reasoning, analytical thinking",
      duration: "30-45 min",
      questions: "25-30",
      difficulty: "Adaptive"
    }
  ];

  const interviewTypes = [
    {
      name: "Behavioral Interview",
      description: "STAR method questions about past experiences",
      duration: "20-30 min",
      questions: "5-8",
      focus: "Experience & Skills"
    },
    {
      name: "Technical Interview",
      description: "Problem-solving and technical discussion",
      duration: "30-45 min",
      questions: "3-5",
      focus: "Technical Skills"
    },
    {
      name: "Case Study",
      description: "Real-world scenarios and business problems",
      duration: "45-60 min",
      questions: "1-2",
      focus: "Problem Solving"
    },
    {
      name: "Cultural Fit",
      description: "Values, work style, and team collaboration",
      duration: "15-25 min",
      questions: "4-6",
      focus: "Personality & Values"
    }
  ];

  const testimonials = [
    {
      name: "Sarah Chen",
      role: "Software Engineer",
      company: "Google",
      quote: "The AI assessment accurately identified my weak areas in system design. The targeted practice helped me improve significantly.",
      score: "92%",
      improvement: "+18%"
    },
    {
      name: "Michael Rodriguez",
      role: "Product Manager",
      company: "Microsoft",
      quote: "The AI interview simulation was incredibly realistic. It helped me practice my responses and build confidence for real interviews.",
      score: "88%",
      improvement: "+15%"
    },
    {
      name: "Priya Sharma",
      role: "Data Scientist",
      company: "Amazon",
      quote: "The detailed feedback on my communication style was eye-opening. I learned to be more concise and impactful in my responses.",
      score: "95%",
      improvement: "+22%"
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
          <div className="text-center mb-12">
            <div className="inline-flex items-center space-x-2 bg-card/50 backdrop-blur-sm rounded-full px-4 py-2 mb-6 border border-primary/20">
              <Sparkles className="h-4 w-4 text-primary" />
              <span className="text-sm font-medium">AI-Powered Evaluation</span>
            </div>
            <h1 className="text-3xl sm:text-4xl md:text-6xl lg:text-7xl font-normal mb-6 leading-tight animate-fade-in text-[#2D3253]">
              AI <span className="bg-gradient-primary bg-clip-text text-transparent">Assessment</span>
            </h1>
            <p className="text-xl text-muted-foreground mb-10 max-w-3xl mx-auto leading-relaxed animate-fade-in">
              Evaluate your skills with AI-powered assessments and practice interviews. Get detailed feedback and personalized improvement plans.
            </p>
          </div>

          {/* Tab Navigation */}
          <div className="flex justify-center mb-12">
            <div className="bg-card/50 backdrop-blur-sm rounded-lg p-1 border border-primary/20">
              <button
                onClick={() => setActiveTab('assessment')}
                className={`px-6 py-3 rounded-md font-medium transition-all ${
                  activeTab === 'assessment'
                    ? 'bg-primary text-primary-foreground shadow-sm'
                    : 'text-muted-foreground hover:text-foreground'
                }`}
              >
                <Brain className="h-4 w-4 inline mr-2" />
                AI Assessment
              </button>
              <button
                onClick={() => setActiveTab('interview')}
                className={`px-6 py-3 rounded-md font-medium transition-all ${
                  activeTab === 'interview'
                    ? 'bg-primary text-primary-foreground shadow-sm'
                    : 'text-muted-foreground hover:text-foreground'
                }`}
              >
                <Video className="h-4 w-4 inline mr-2" />
                AI Interview
              </button>
            </div>
          </div>

          {/* Assessment Section */}
          {activeTab === 'assessment' && (
            <div className="space-y-16">
              {/* Features */}
              <div>
                <h2 className="text-3xl font-bold text-center mb-12">Assessment Features</h2>
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {assessmentFeatures.map((feature) => (
                    <Card key={feature.title} className="p-6 text-center border-primary/10">
                      <feature.icon className="h-12 w-12 mx-auto mb-4 text-primary" />
                      <h3 className="font-bold text-lg mb-2">{feature.title}</h3>
                      <p className="text-muted-foreground text-sm">{feature.description}</p>
                    </Card>
                  ))}
                </div>
              </div>

              {/* Assessment Types */}
              <div>
                <h2 className="text-3xl font-bold text-center mb-12">Assessment Types</h2>
                <div className="grid md:grid-cols-2 gap-6">
                  {assessmentTypes.map((type) => (
                    <Card key={type.name} className="p-6 border-primary/10">
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <h3 className="font-bold text-xl mb-2">{type.name}</h3>
                          <p className="text-muted-foreground mb-3">{type.description}</p>
                        </div>
                        <Badge variant="secondary">{type.difficulty}</Badge>
                      </div>
                      <div className="grid grid-cols-3 gap-4 text-sm">
                        <div>
                          <p className="text-muted-foreground">Duration</p>
                          <p className="font-medium">{type.duration}</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Questions</p>
                          <p className="font-medium">{type.questions}</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Format</p>
                          <p className="font-medium">Multiple Choice</p>
                        </div>
                      </div>
                      <Button className="w-full mt-4" onClick={() => navigate('/assessment')}>
                        Start Assessment
                        <ArrowRight className="ml-2 h-4 w-4" />
                      </Button>
                    </Card>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Interview Section */}
          {activeTab === 'interview' && (
            <div className="space-y-16">
              {/* Features */}
              <div>
                <h2 className="text-3xl font-bold text-center mb-12">Interview Features</h2>
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {interviewFeatures.map((feature) => (
                    <Card key={feature.title} className="p-6 text-center border-primary/10">
                      <feature.icon className="h-12 w-12 mx-auto mb-4 text-primary" />
                      <h3 className="font-bold text-lg mb-2">{feature.title}</h3>
                      <p className="text-muted-foreground text-sm">{feature.description}</p>
                    </Card>
                  ))}
                </div>
              </div>

              {/* Interview Types */}
              <div>
                <h2 className="text-3xl font-bold text-center mb-12">Interview Types</h2>
                <div className="grid md:grid-cols-2 gap-6">
                  {interviewTypes.map((type) => (
                    <Card key={type.name} className="p-6 border-primary/10">
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <h3 className="font-bold text-xl mb-2">{type.name}</h3>
                          <p className="text-muted-foreground mb-3">{type.description}</p>
                        </div>
                        <Badge variant="outline">{type.focus}</Badge>
                      </div>
                      <div className="grid grid-cols-3 gap-4 text-sm">
                        <div>
                          <p className="text-muted-foreground">Duration</p>
                          <p className="font-medium">{type.duration}</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Questions</p>
                          <p className="font-medium">{type.questions}</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Format</p>
                          <p className="font-medium">Video/Audio</p>
                        </div>
                      </div>
                      <Button className="w-full mt-4" onClick={() => navigate('/interview')}>
                        Start Interview
                        <Play className="ml-2 h-4 w-4" />
                      </Button>
                    </Card>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* How It Works */}
          <div className="mt-16">
            <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
            <div className="grid md:grid-cols-3 gap-8">
              <Card className="p-6 text-center border-primary/10">
                <div className="h-12 w-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-primary font-bold text-xl">1</span>
                </div>
                <h3 className="font-bold text-lg mb-2">Choose Your Test</h3>
                <p className="text-muted-foreground text-sm">
                  Select from our range of assessments or interview simulations based on your needs.
                </p>
              </Card>
              <Card className="p-6 text-center border-primary/10">
                <div className="h-12 w-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-primary font-bold text-xl">2</span>
                </div>
                <h3 className="font-bold text-lg mb-2">Take the Assessment</h3>
                <p className="text-muted-foreground text-sm">
                  Complete the test in a distraction-free environment with our AI monitoring your performance.
                </p>
              </Card>
              <Card className="p-6 text-center border-primary/10">
                <div className="h-12 w-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-primary font-bold text-xl">3</span>
                </div>
                <h3 className="font-bold text-lg mb-2">Get Detailed Feedback</h3>
                <p className="text-muted-foreground text-sm">
                  Receive comprehensive analysis with actionable insights and improvement recommendations.
                </p>
              </Card>
            </div>
          </div>

          {/* Testimonials */}
          <div className="mt-16">
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
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-sm text-muted-foreground">Score:</span>
                      <span className="font-bold text-primary">{testimonial.score}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <TrendingUp className="h-4 w-4 text-green-500" />
                      <span className="text-sm text-green-500 font-medium">{testimonial.improvement}</span>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>

          {/* CTA Section */}
          <div className="mt-16 text-center">
            <Card className="p-8 bg-gradient-card border-primary/10">
              <h3 className="text-2xl font-bold mb-3">Ready to Test Your Skills?</h3>
              <p className="text-muted-foreground mb-6 max-w-md mx-auto">
                Start with a free assessment or interview simulation and see how AI can help you improve.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button size="lg" onClick={() => navigate('/assessment')}>
                  Start Free Assessment
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
                <Button variant="outline" size="lg" onClick={() => navigate('/interview')}>
                  Try AI Interview
                  <Video className="ml-2 h-4 w-4" />
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

export default AIAssessment; 