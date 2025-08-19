import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { motion } from 'framer-motion';
import { 
  FileText, 
  Search, 
  Bot, 
  Map, 
  Users,
  ArrowRight,
  Sparkles,
  CheckCircle,
  Star,
  Clock,
  Zap,
  Target,
  Lightbulb,
  Shield
} from "lucide-react";
import { Link } from "react-router-dom";
import Footer from "@/components/Footer";
import './OutlinedText.css';

const Services = () => {
  const services = [
    {
      id: "resume-builder",
      title: "Resume Builder",
      description: "Create professional, ATS-optimized resumes that stand out to hiring managers and pass through applicant tracking systems.",
      icon: FileText,
      features: [
        "AI-powered content suggestions",
        "ATS optimization",
        "Multiple professional templates",
        "Real-time feedback and scoring",
        "Export to PDF/Word formats"
      ],
      price: "Free",
      cta: "Build Resume",
      path: "/services/resume-builder",
      color: "from-blue-500/10 to-blue-600/10"
    },
    {
      id: "job-listing",
      title: "Job Listing",
      description: "Access curated job opportunities from top companies, filtered by your skills, experience, and career goals.",
      icon: Search,
      features: [
        "Curated job recommendations",
        "Advanced filtering options",
        "Company insights and reviews",
        "One-click application tracking",
        "Salary insights and negotiations"
      ],
      price: "Free",
      cta: "Browse Jobs",
      path: "/services/jobs",
      color: "from-green-500/10 to-green-600/10"
    },
    {
      id: "ai-assessment",
      title: "AI Assessment",
      description: "Take comprehensive skill assessments powered by AI to evaluate your technical and soft skills with detailed feedback.",
      icon: Bot,
      features: [
        "Adaptive difficulty testing",
        "Real-time performance analysis",
        "Detailed skill breakdown",
        "Personalized improvement plans",
        "Industry benchmarking"
      ],
      price: "From $29",
      cta: "Start Assessment",
      path: "/services/ai-assessment",
      color: "from-purple-500/10 to-purple-600/10"
    },
    {
      id: "career-roadmap",
      title: "Career Roadmap",
      description: "Get personalized career guidance with AI-driven roadmaps that help you plan your professional development journey.",
      icon: Map,
      features: [
        "Personalized career planning",
        "Skill gap analysis",
        "Learning path recommendations",
        "Industry trend insights",
        "Progress tracking and milestones"
      ],
      price: "From $49",
      cta: "Plan Career",
      path: "/services/career-roadmap",
      color: "from-orange-500/10 to-orange-600/10"
    },
    {
      id: "placement",
      title: "Placement",
      description: "Connect with our network of hiring partners and get direct placement opportunities with top companies.",
      icon: Users,
      features: [
        "Direct company connections",
        "Priority candidate status",
        "Interview preparation support",
        "Negotiation guidance",
        "Ongoing career support"
      ],
      price: "From $99",
      cta: "Get Placed",
      path: "/services/placement",
      color: "from-red-500/10 to-red-600/10"
    }
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        ease: "easeOut" as const
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-bg">
      <div className="min-h-screen max-w-screen-2xl mx-auto px-4 sm:px-6 lg:px-8 
                    m-4 sm:m-6 lg:m-10 bg-gradient-bg border border-blue-300 rounded-3xl overflow-hidden bg-gradient-to-b from-slate-100 to-cyan-50
                    animate-fade-in mt-20" style={{ marginTop: '5rem' }}>
        
        {/* Hero Section */}
        <section className="relative pt-20 mt-10 pb-20">
          <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div 
              className="text-center max-w-4xl mx-auto"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
            >
              <div className="inline-flex items-center space-x-2 bg-card/50 backdrop-blur-sm rounded-full px-4 py-2 mb-8 border border-primary/20 animate-fade-in">
                <Sparkles className="h-4 w-4 text-primary animate-pulse" />
                <span className="text-sm font-medium">Comprehensive Career Services</span>
              </div>
              
              <h1 className="text-3xl sm:text-4xl md:text-6xl lg:text-7xl font-normal mb-6 leading-tight animate-fade-in text-[#2D3253]">
                Everything You Need to
                <span className="bg-gradient-primary bg-clip-text text-transparent block">Succeed in Your Career</span>
              </h1>
              
              <p className="text-xl text-muted-foreground mb-10 max-w-3xl mx-auto leading-relaxed animate-fade-in">
                From resume building to job placement, we provide comprehensive tools and services 
                to help you navigate every step of your professional journey.
              </p>
            </motion.div>
          </div>
        </section>

        {/* Services Grid */}
        <section className="py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div 
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
              variants={containerVariants}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
            >
              {services.map((service, index) => (
                <motion.div key={service.id} variants={itemVariants}>
                  <Card className="p-8 bg-gradient-card border-primary/10 hover:border-primary/30 transition-all duration-300 hover:shadow-glow-accent group hover-scale animate-fade-in h-full">
                    <div className="text-center mb-6">
                      <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:bg-primary/20 transition-colors group-hover:animate-pulse">
                        <service.icon className="h-8 w-8 text-primary" />
                      </div>
                      <h3 className="text-2xl font-bold mb-2 group-hover:text-primary transition-colors">
                        {service.title}
                      </h3>
                      <p className="text-muted-foreground leading-relaxed mb-4">
                        {service.description}
                      </p>
                      <div className="text-2xl font-bold text-primary mb-4">
                        {service.price}
                      </div>
                    </div>
                    
                    <div className="space-y-3 mb-6">
                      {service.features.map((feature, featureIndex) => (
                        <div key={featureIndex} className="flex items-start gap-3">
                          <CheckCircle className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
                          <span className="text-sm text-muted-foreground">{feature}</span>
                        </div>
                      ))}
                    </div>
                    
                    <Link to={service.path} className="block">
                      <Button className="w-full group hover-scale">
                        {service.cta}
                        <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                      </Button>
                    </Link>
                  </Card>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </section>

        {/* Why Choose Us Section */}
        <section className="py-20 bg-muted/30">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div 
              className="text-center mb-16 animate-fade-in"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl md:text-5xl font-bold mb-4">
                Why Choose 
                <span className="bg-gradient-primary bg-clip-text text-transparent"> Our Services?</span>
              </h2>
              <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                We combine cutting-edge technology with human expertise to deliver results
              </p>
            </motion.div>
            
            <motion.div 
              className="grid md:grid-cols-3 gap-8"
              variants={containerVariants}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
            >
              <motion.div variants={itemVariants}>
                <Card className="p-8 bg-gradient-card border-primary/10 hover:border-primary/30 hover:shadow-glow-accent transition-all duration-300 text-center">
                  <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <Zap className="h-8 w-8 text-primary" />
                  </div>
                  <h3 className="text-xl font-semibold mb-3">AI-Powered</h3>
                  <p className="text-muted-foreground leading-relaxed">
                    Leverage advanced AI technology for personalized insights and recommendations
                  </p>
                </Card>
              </motion.div>
              
              <motion.div variants={itemVariants}>
                <Card className="p-8 bg-gradient-card border-primary/10 hover:border-primary/30 hover:shadow-glow-accent transition-all duration-300 text-center">
                  <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <Target className="h-8 w-8 text-primary" />
                  </div>
                  <h3 className="text-xl font-semibold mb-3">Results-Driven</h3>
                  <p className="text-muted-foreground leading-relaxed">
                    Focus on outcomes with proven strategies that lead to career success
                  </p>
                </Card>
              </motion.div>
              
              <motion.div variants={itemVariants}>
                <Card className="p-8 bg-gradient-card border-primary/10 hover:border-primary/30 hover:shadow-glow-accent transition-all duration-300 text-center">
                  <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <Shield className="h-8 w-8 text-primary" />
                  </div>
                  <h3 className="text-xl font-semibold mb-3">Trusted & Secure</h3>
                  <p className="text-muted-foreground leading-relaxed">
                    Your data is protected with enterprise-grade security and privacy controls
                  </p>
                </Card>
              </motion.div>
            </motion.div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20">
          <div className="max-w-4xl mx-auto text-center">
            <motion.div 
              className="bg-gradient-to-r from-primary/10 to-primary/5 rounded-3xl p-12"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
                Ready to Accelerate Your Career?
              </h2>
              <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
                Start with any of our services and see the difference professional tools can make. 
                Your success journey begins here.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button size="lg" className="text-lg px-8 py-6 group hover-scale">
                  Explore Services
                  <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                </Button>
                <Button variant="outline" size="lg" className="text-lg px-8 py-6 hover-scale">
                  Schedule Consultation
                </Button>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Footer */}
        <Footer />

        <div className="px-4 sm:px-6 lg:px-8 text-center">
          <h1
            className="outlined-text text-[3.5rem] sm:text-[6rem] md:text-[8rem] lg:text-[10rem] xl:text-[12rem] 2xl:text-[14rem] leading-none tracking-widest"
          >
            STTARKEL
          </h1>
        </div>
      </div>
    </div>
  );
};

export default Services; 