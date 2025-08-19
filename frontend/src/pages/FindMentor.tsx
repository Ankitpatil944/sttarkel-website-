import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { motion } from 'framer-motion';
import AIspireVerifiedBadge from "@/components/AIspireVerifiedBadge";
import { 
  Search, 
  Star, 
  Award, 
  Trophy, 
  Medal,
  ChevronLeft,
  ChevronRight,
  Filter,
  MapPin,
  Clock,
  Users,
  MessageCircle,
  ArrowRight,
  Sparkles,
  CheckCircle,
  Zap,
  TrendingUp
} from "lucide-react";

const FindMentor = () => {
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [selectedSubcategory, setSelectedSubcategory] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState<string>("");

  // Tech categories and their subcategories
  const techCategories = {
    "Python": [
      "Web Development (Django/Flask)",
      "Data Science & Analytics",
      "Machine Learning & AI",
      "Automation & Scripting",
      "DevOps & Infrastructure",
      "Game Development",
      "Desktop Applications",
      "API Development"
    ],
    "JavaScript": [
      "Frontend Development (React/Vue/Angular)",
      "Backend Development (Node.js)",
      "Full Stack Development",
      "Mobile Development (React Native)",
      "Game Development",
      "Desktop Applications (Electron)",
      "Testing & QA"
    ],
    "Java": [
      "Enterprise Development",
      "Android Development",
      "Spring Framework",
      "Microservices",
      "Big Data Processing",
      "Cloud Development",
      "Performance Optimization"
    ],
    "Data Science": [
      "Machine Learning",
      "Deep Learning",
      "Statistical Analysis",
      "Data Visualization",
      "Natural Language Processing",
      "Computer Vision",
      "Big Data Analytics"
    ],
    "DevOps": [
      "CI/CD Pipelines",
      "Cloud Infrastructure (AWS/Azure/GCP)",
      "Containerization (Docker/Kubernetes)",
      "Monitoring & Logging",
      "Security & Compliance",
      "Infrastructure as Code",
      "Performance Tuning"
    ],
    "Mobile Development": [
      "iOS Development (Swift)",
      "Android Development (Kotlin/Java)",
      "Cross-platform (Flutter/React Native)",
      "Mobile UI/UX Design",
      "App Store Optimization",
      "Mobile Testing",
      "Performance Optimization"
    ]
  };

  // Top performers and awards slideshow data
  const topPerformers = [
    {
      id: 1,
      name: "Dr. Priya Sharma",
      role: "Senior Software Engineer",
      company: "TCS",
      achievement: "Best Mentor 2024",
      rating: 4.9,
      sessions: 150,
      image: "/Images/Sttarkel_Student.png",
      badge: "🏆"
    },
    {
      id: 2,
      name: "Rajesh Kumar",
      role: "Product Manager",
      company: "Infosys",
      achievement: "Excellence in Leadership",
      rating: 4.8,
      sessions: 120,
      image: "/Images/Sttarkel_Student.png",
      badge: "🥇"
    },
    {
      id: 3,
      name: "Anjali Patel",
      role: "Data Scientist",
      company: "Wipro",
      achievement: "Innovation Award",
      rating: 4.9,
      sessions: 95,
      image: "/Images/Sttarkel_Student.png",
      badge: "💎"
    },
    {
      id: 4,
      name: "Vikram Singh",
      role: "Tech Lead",
      company: "HCL",
      achievement: "Most Helpful Mentor",
      rating: 4.7,
      sessions: 180,
      image: "/Images/Sttarkel_Student.png",
      badge: "⭐"
    },
    {
      id: 5,
      name: "Meera Reddy",
      role: "Senior Developer",
      company: "Tech Mahindra",
      achievement: "Student Success Champion",
      rating: 4.8,
      sessions: 110,
      image: "/Images/Sttarkel_Student.png",
      badge: "🎯"
    }
  ];

  // All mentors data
  const allMentors = [
    {
      id: 1,
      name: "Dr. Priya Sharma",
      role: "Senior Software Engineer",
      company: "TCS",
      experience: "8+ years",
      category: "Python",
      subcategory: "Machine Learning & AI",
      rating: 4.9,
      sessions: 150,
      hourlyRate: "₹2,500",
      location: "Bangalore",
      image: "/Images/Sttarkel_Student.png",
      expertise: ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch"],
      availability: "Weekdays 6-9 PM",
      isVerified: true,
      verificationDate: "2024-01-15",
      responseTime: "< 2 hours",
      successRate: "98%"
    },
    {
      id: 2,
      name: "Rajesh Kumar",
      role: "Product Manager",
      company: "Infosys",
      experience: "6+ years",
      category: "JavaScript",
      subcategory: "Full Stack Development",
      rating: 4.8,
      sessions: 120,
      hourlyRate: "₹2,000",
      location: "Mumbai",
      image: "/Images/Sttarkel_Student.png",
      expertise: ["JavaScript", "React", "Node.js", "MongoDB", "AWS"],
      availability: "Weekends 10 AM-6 PM",
      isVerified: true,
      verificationDate: "2024-02-20",
      responseTime: "< 4 hours",
      successRate: "95%"
    },
    {
      id: 3,
      name: "Anjali Patel",
      role: "Data Scientist",
      company: "Wipro",
      experience: "5+ years",
      category: "Data Science",
      subcategory: "Machine Learning",
      rating: 4.9,
      sessions: 95,
      hourlyRate: "₹2,200",
      location: "Hyderabad",
      image: "/Images/Sttarkel_Student.png",
      expertise: ["Python", "R", "SQL", "Scikit-learn", "Pandas"],
      availability: "Weekdays 7-10 PM",
      isVerified: true,
      verificationDate: "2024-03-10",
      responseTime: "< 1 hour",
      successRate: "99%"
    },
    {
      id: 4,
      name: "Vikram Singh",
      role: "Tech Lead",
      company: "HCL",
      experience: "10+ years",
      category: "DevOps",
      subcategory: "Cloud Infrastructure",
      rating: 4.7,
      sessions: 180,
      hourlyRate: "₹3,000",
      location: "Delhi",
      image: "/Images/Sttarkel_Student.png",
      expertise: ["AWS", "Docker", "Kubernetes", "Terraform", "Jenkins"],
      availability: "Flexible",
      isVerified: true,
      verificationDate: "2024-01-05",
      responseTime: "< 3 hours",
      successRate: "97%"
    },
    {
      id: 5,
      name: "Meera Reddy",
      role: "Senior Developer",
      company: "Tech Mahindra",
      experience: "7+ years",
      category: "Mobile Development",
      subcategory: "Android Development",
      rating: 4.8,
      sessions: 110,
      hourlyRate: "₹2,300",
      location: "Chennai",
      image: "/Images/Sttarkel_Student.png",
      expertise: ["Kotlin", "Java", "Android Studio", "Firebase", "REST APIs"],
      availability: "Weekdays 6-9 PM",
      isVerified: false,
      responseTime: "< 6 hours",
      successRate: "92%"
    },
    {
      id: 6,
      name: "Arjun Mehta",
      role: "Backend Developer",
      company: "Mindtree",
      experience: "4+ years",
      category: "Java",
      subcategory: "Microservices",
      rating: 4.6,
      sessions: 85,
      hourlyRate: "₹1,800",
      location: "Pune",
      image: "/Images/Sttarkel_Student.png",
      expertise: ["Java", "Spring Boot", "Microservices", "Kafka", "Redis"],
      availability: "Weekends 2-8 PM",
      isVerified: false,
      responseTime: "< 8 hours",
      successRate: "89%"
    }
  ];

  // Filter mentors based on selection
  const filteredMentors = allMentors.filter(mentor => {
    const matchesCategory = selectedCategory === "all" || mentor.category === selectedCategory;
    const matchesSubcategory = selectedSubcategory === "all" || mentor.subcategory === selectedSubcategory;
    const matchesSearch = !searchQuery || 
      mentor.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      mentor.role.toLowerCase().includes(searchQuery.toLowerCase()) ||
      mentor.company.toLowerCase().includes(searchQuery.toLowerCase()) ||
      mentor.expertise.some(skill => skill.toLowerCase().includes(searchQuery.toLowerCase()));
    
    return matchesCategory && matchesSubcategory && matchesSearch;
  });

  const handleCategoryChange = (category: string) => {
    setSelectedCategory(category);
    setSelectedSubcategory("all"); // Reset subcategory when category changes
  };

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
        <section className="relative pt-20 mt-10 pb-16">
          <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div 
              className="text-center max-w-4xl mx-auto"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
            >
              <div className="inline-flex items-center space-x-2 bg-card/50 backdrop-blur-sm rounded-full px-4 py-2 mb-8 border border-primary/20 animate-fade-in">
                <Sparkles className="h-4 w-4 text-primary animate-pulse" />
                <span className="text-sm font-medium">Find Your Perfect Tech Mentor</span>
              </div>
              
              <h1 className="text-3xl sm:text-4xl md:text-6xl lg:text-7xl font-normal mb-6 leading-tight animate-fade-in text-[#2D3253]">
                Find Your Perfect
                <span className="bg-gradient-primary bg-clip-text text-transparent block">Tech Mentor</span>
              </h1>
              
              <p className="text-xl text-muted-foreground mb-8 max-w-3xl mx-auto leading-relaxed animate-fade-in">
                Connect with industry experts from top Indian companies. Get personalized guidance 
                to accelerate your career in technology.
              </p>
              
              {/* Action Buttons */}
              <motion.div 
                className="flex flex-col sm:flex-row gap-4 justify-center mb-8"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.1, ease: "easeOut" }}
              >
                <Button 
                  size="lg" 
                  className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-3"
                >
                  Find Your Mentor
                </Button>
                <Button 
                  variant="outline" 
                  size="lg" 
                  className="border-2 border-primary text-primary hover:bg-primary hover:text-white px-8 py-3"
                  onClick={() => window.location.href = '/become-mentor'}
                >
                  Become a Mentor
                </Button>
              </motion.div>
              
              {/* Search Bar */}
              <motion.div 
                className="max-w-2xl mx-auto mb-8"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
              >
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-5 w-5" />
                  <Input
                    placeholder="Search mentors by name, skills, or company..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10 pr-4 py-6 text-lg bg-card/60 border-primary/20 focus:border-primary/40"
                  />
                </div>
              </motion.div>
            </motion.div>
          </div>
        </section>

        {/* Top Performers Slideshow */}
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div 
              className="flex items-center justify-between mb-8"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl font-bold text-foreground flex items-center gap-3">
                <Trophy className="h-8 w-8 text-yellow-500" />
                Top Performers & Award Winners
              </h2>
              <div className="flex gap-2">
                <Button variant="outline" size="icon" className="rounded-full hover-scale">
                  <ChevronLeft className="h-4 w-4" />
                </Button>
                <Button variant="outline" size="icon" className="rounded-full hover-scale">
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
            </motion.div>
            
                         <motion.div 
               className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6"
               variants={containerVariants}
               initial="hidden"
               whileInView="visible"
               viewport={{ once: true }}
             >
               {topPerformers.map((performer) => (
                 <motion.div key={performer.id} variants={itemVariants} className="h-full">
                   <Card className="group hover:scale-105 transition-all duration-300 cursor-pointer bg-gradient-card border-primary/10 hover:border-primary/30 hover:shadow-glow-accent h-full flex flex-col">
                                         <CardHeader className="text-center p-4 flex-shrink-0">
                       <div className="relative mx-auto mb-4">
                         <div className="w-20 h-20 rounded-full overflow-hidden bg-muted mx-auto">
                           <img 
                             src={performer.image} 
                             alt={performer.name}
                             className="w-full h-full object-cover"
                           />
                         </div>
                         <div className="absolute -top-2 -right-2 text-3xl">
                           {performer.badge}
                         </div>
                       </div>
                       <CardTitle className="text-lg">{performer.name}</CardTitle>
                       <CardDescription className="text-sm">
                         {performer.role} at {performer.company}
                       </CardDescription>
                       <Badge variant="secondary" className="mt-2">
                         {performer.achievement}
                       </Badge>
                     </CardHeader>
                     <CardContent className="text-center p-4 pt-0 flex-1 flex flex-col justify-end">
                       <div className="flex items-center justify-center gap-2 mb-2">
                         <Star className="h-4 w-4 text-yellow-500 fill-current" />
                         <span className="text-sm font-medium">{performer.rating}</span>
                         <span className="text-sm text-muted-foreground">({performer.sessions} sessions)</span>
                       </div>
                       <Button className="w-full hover-scale mt-auto">View Profile</Button>
                     </CardContent>
                  </Card>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </section>

        {/* Filters Section */}
        <section className="py-8 bg-muted/30">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div 
              className="flex flex-col lg:flex-row gap-6 items-start lg:items-center"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              viewport={{ once: true }}
            >
              <div className="flex items-center gap-2">
                <Filter className="h-5 w-5 text-muted-foreground" />
                <span className="font-medium">Filter by:</span>
              </div>
              
              <div className="flex flex-wrap gap-4">
                <Select value={selectedCategory} onValueChange={handleCategoryChange}>
                  <SelectTrigger className="w-48 bg-card/60 border-primary/20">
                    <SelectValue placeholder="Select Category" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Categories</SelectItem>
                    {Object.keys(techCategories).map((category) => (
                      <SelectItem key={category} value={category}>
                        {category}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>

                <Select value={selectedSubcategory} onValueChange={setSelectedSubcategory}>
                  <SelectTrigger className="w-64 bg-card/60 border-primary/20">
                    <SelectValue placeholder="Select Subcategory" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Subcategories</SelectItem>
                    {selectedCategory !== "all" && techCategories[selectedCategory as keyof typeof techCategories]?.map((subcategory) => (
                      <SelectItem key={subcategory} value={subcategory}>
                        {subcategory}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Mentors List */}
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div 
              className="flex items-center justify-between mb-8"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl font-bold text-foreground">
                Available Mentors ({filteredMentors.length})
              </h2>
            </motion.div>
            
                         <motion.div 
               className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
               variants={containerVariants}
               initial="hidden"
               whileInView="visible"
               viewport={{ once: true }}
             >
               {filteredMentors.map((mentor) => (
                 <motion.div key={mentor.id} variants={itemVariants} className="h-full">
                   <Card className="hover:shadow-xl transition-all duration-300 hover:-translate-y-2 bg-gradient-card border-primary/10 hover:border-primary/30 hover:shadow-glow-accent h-full flex flex-col">
                                         <CardHeader className="p-6 flex-shrink-0">
                       <div className="flex items-start gap-4">
                         <div className="w-16 h-16 rounded-full overflow-hidden bg-muted flex-shrink-0">
                           <img 
                             src={mentor.image} 
                             alt={mentor.name}
                             className="w-full h-full object-cover"
                           />
                         </div>
                         <div className="flex-1 min-w-0">
                           <div className="flex items-center gap-2 mb-1">
                             <CardTitle className="text-xl">{mentor.name}</CardTitle>
                             {mentor.isVerified && <AIspireVerifiedBadge size="sm" />}
                           </div>
                           <CardDescription className="text-base mb-2">
                             {mentor.role} at {mentor.company}
                           </CardDescription>
                           <div className="flex items-center gap-4 text-sm text-muted-foreground">
                             <span className="flex items-center gap-1">
                               <MapPin className="h-4 w-4" />
                               {mentor.location}
                             </span>
                             <span className="flex items-center gap-1">
                               <Clock className="h-4 w-4" />
                               {mentor.experience}
                             </span>
                           </div>
                         </div>
                       </div>
                     </CardHeader>
                    
                                         <CardContent className="p-6 pt-0 flex-1 flex flex-col">
                       <div className="flex items-center justify-between mb-4">
                         <div className="flex items-center gap-2">
                           <Star className="h-4 w-4 text-yellow-500 fill-current" />
                           <span className="font-medium">{mentor.rating}</span>
                           <span className="text-sm text-muted-foreground">({mentor.sessions} sessions)</span>
                         </div>
                         <Badge variant="secondary" className="text-sm">
                           {mentor.category}
                         </Badge>
                       </div>

                       {/* Additional Stats */}
                       <div className="grid grid-cols-3 gap-2 mb-4 text-xs">
                         <div className="flex items-center gap-1 text-muted-foreground">
                           <Zap className="h-3 w-3" />
                           <span>{mentor.responseTime}</span>
                         </div>
                         <div className="flex items-center gap-1 text-muted-foreground">
                           <TrendingUp className="h-3 w-3" />
                           <span>{mentor.successRate}</span>
                         </div>
                         {mentor.isVerified && (
                           <div className="flex items-center gap-1 text-blue-600">
                             <CheckCircle className="h-3 w-3" />
                             <span>Verified</span>
                           </div>
                         )}
                       </div>
                       
                       <div className="mb-4">
                         <p className="text-sm text-muted-foreground mb-2">Expertise:</p>
                         <div className="flex flex-wrap gap-2">
                           {mentor.expertise.slice(0, 3).map((skill, index) => (
                             <Badge key={index} variant="outline" className="text-xs">
                               {skill}
                             </Badge>
                           ))}
                           {mentor.expertise.length > 3 && (
                             <Badge variant="outline" className="text-xs">
                               +{mentor.expertise.length - 3} more
                             </Badge>
                           )}
                         </div>
                       </div>
                       
                       <div className="flex items-center justify-between mb-4">
                         <div className="text-lg font-bold text-primary">
                           {mentor.hourlyRate}/hr
                         </div>
                         <div className="text-sm text-muted-foreground">
                           {mentor.availability}
                         </div>
                       </div>
                       
                       <div className="flex gap-2 mt-auto">
                         <Button className="flex-1 hover-scale">Book Session</Button>
                         <Button variant="outline" size="icon" className="hover-scale">
                           <MessageCircle className="h-4 w-4" />
                         </Button>
                       </div>
                     </CardContent>
                  </Card>
                </motion.div>
              ))}
            </motion.div>
            
            {filteredMentors.length === 0 && (
              <motion.div 
                className="text-center py-16"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, ease: "easeOut" }}
              >
                <Users className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-xl font-medium text-muted-foreground mb-2">
                  No mentors found
                </h3>
                <p className="text-muted-foreground">
                  Try adjusting your filters or search terms to find available mentors.
                </p>
              </motion.div>
            )}
          </div>
        </section>
      </div>
    </div>
  );
};

export default FindMentor;
