import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
  Search,
  Building2,
  Users,
  Clock,
  Star,
  ArrowRight,
  Filter,
  MapPin,
  Briefcase
} from "lucide-react";

const Companies = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");

  const categories = ["All", "Tech Giants", "Startups", "Finance", "Consulting", "Healthcare"];

  const companies = [
    {
      id: 1,
      name: "Google",
      logo: "🌟",
      category: "Tech Giants",
      location: "Mountain View, CA",
      employees: "100K+",
      rating: 4.8,
      difficulty: "Hard",
      rounds: [
        { name: "Phone Screen", duration: "45 min" },
        { name: "Technical Rounds", duration: "2x 60 min" },
        { name: "System Design", duration: "60 min" },
        { name: "Behavioral", duration: "45 min" }
      ],
      description: "Leading technology company known for search, cloud computing, and AI innovations."
    },
    {
      id: 2,
      name: "Amazon",
      logo: "📦",
      category: "Tech Giants",
      location: "Seattle, WA",
      employees: "1M+",
      rating: 4.6,
      difficulty: "Hard",
      rounds: [
        { name: "Online Assessment", duration: "90 min" },
        { name: "Technical Rounds", duration: "3x 60 min" },
        { name: "Bar Raiser", duration: "60 min" }
      ],
      description: "E-commerce and cloud computing giant with leadership principles focus."
    },
    {
      id: 3,
      name: "Microsoft",
      logo: "🪟",
      category: "Tech Giants",
      location: "Redmond, WA", 
      employees: "200K+",
      rating: 4.7,
      difficulty: "Medium",
      rounds: [
        { name: "Phone Screen", duration: "45 min" },
        { name: "Technical Rounds", duration: "4x 60 min" },
        { name: "As Appropriate", duration: "60 min" }
      ],
      description: "Technology corporation known for software, cloud services, and productivity tools."
    },
    {
      id: 4,
      name: "Meta",
      logo: "👤",
      category: "Tech Giants",
      location: "Menlo Park, CA",
      employees: "80K+",
      rating: 4.5,
      difficulty: "Hard",
      rounds: [
        { name: "Phone Screen", duration: "45 min" },
        { name: "Technical Rounds", duration: "2x 60 min" },
        { name: "System Design", duration: "60 min" },
        { name: "Behavioral", duration: "45 min" }
      ],
      description: "Social media and virtual reality company building the metaverse."
    },
    {
      id: 5,
      name: "Apple",
      logo: "🍎",
      category: "Tech Giants",
      location: "Cupertino, CA",
      employees: "150K+",
      rating: 4.6,
      difficulty: "Medium",
      rounds: [
        { name: "Phone Interview", duration: "30 min" },
        { name: "Technical Rounds", duration: "3x 60 min" },
        { name: "Presentation", duration: "30 min" }
      ],
      description: "Consumer electronics and software company known for innovative design."
    },
    {
      id: 6,
      name: "Netflix",
      logo: "🎬",
      category: "Tech Giants",
      location: "Los Gatos, CA",
      employees: "15K+",
      rating: 4.4,
      difficulty: "Hard",
      rounds: [
        { name: "Phone Screen", duration: "45 min" },
        { name: "Technical Interview", duration: "90 min" },
        { name: "Culture Fit", duration: "60 min" }
      ],
      description: "Streaming entertainment service with a focus on high-performance culture."
    }
  ];

  const filteredCompanies = companies.filter(company => {
    const matchesSearch = company.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === "All" || company.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case "Easy": return "text-green-500 border-green-500";
      case "Medium": return "text-yellow-500 border-yellow-500";
      case "Hard": return "text-red-500 border-red-500";
      default: return "text-primary border-primary";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-bg">
      
      <div className="pt-24 pb-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Company-Specific
              <span className="bg-gradient-primary bg-clip-text text-transparent block">
                Interview Prep
              </span>
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Practice with real interview questions and processes from top companies. 
              Get insights into what each company looks for in candidates.
            </p>
          </div>

          {/* Search and Filters */}
          <div className="flex flex-col md:flex-row gap-4 mb-8">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
              <Input
                type="text"
                placeholder="Search companies..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 bg-card border-border"
              />
            </div>
            
            <div className="flex flex-wrap gap-2">
              {categories.map((category) => (
                <Button
                  key={category}
                  variant={selectedCategory === category ? "default" : "outline"}
                  size="sm"
                  onClick={() => setSelectedCategory(category)}
                >
                  {category}
                </Button>
              ))}
            </div>
          </div>

          {/* Companies Grid */}
          <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-6">
            {filteredCompanies.map((company) => (
              <Card key={company.id} className="p-6 bg-gradient-card border-primary/10 hover:border-primary/30 transition-all duration-300 hover:shadow-glow-accent group">
                {/* Company Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <div className="text-3xl">{company.logo}</div>
                    <div>
                      <h3 className="text-xl font-bold group-hover:text-primary transition-colors">
                        {company.name}
                      </h3>
                      <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                        <MapPin className="w-3 h-3" />
                        <span>{company.location}</span>
                      </div>
                    </div>
                  </div>
                  <Badge variant="outline" className={getDifficultyColor(company.difficulty)}>
                    {company.difficulty}
                  </Badge>
                </div>

                {/* Company Stats */}
                <div className="grid grid-cols-3 gap-4 mb-4">
                  <div className="text-center">
                    <div className="flex items-center justify-center space-x-1 text-sm">
                      <Star className="w-3 h-3 text-yellow-500" />
                      <span className="font-medium">{company.rating}</span>
                    </div>
                    <div className="text-xs text-muted-foreground">Rating</div>
                  </div>
                  <div className="text-center">
                    <div className="flex items-center justify-center space-x-1 text-sm">
                      <Users className="w-3 h-3 text-primary" />
                      <span className="font-medium">{company.employees}</span>
                    </div>
                    <div className="text-xs text-muted-foreground">Employees</div>
                  </div>
                  <div className="text-center">
                    <div className="flex items-center justify-center space-x-1 text-sm">
                      <Briefcase className="w-3 h-3 text-primary" />
                      <span className="font-medium">{company.rounds.length}</span>
                    </div>
                    <div className="text-xs text-muted-foreground">Rounds</div>
                  </div>
                </div>

                {/* Description */}
                <p className="text-sm text-muted-foreground mb-4 leading-relaxed">
                  {company.description}
                </p>

                {/* Interview Rounds */}
                <div className="mb-6">
                  <h4 className="text-sm font-semibold mb-2 flex items-center">
                    <Clock className="w-3 h-3 mr-1 text-primary" />
                    Interview Process
                  </h4>
                  <div className="space-y-1">
                    {company.rounds.map((round, index) => (
                      <div key={index} className="flex justify-between items-center text-xs">
                        <span className="text-muted-foreground">{round.name}</span>
                        <span className="font-medium">{round.duration}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Action Button */}
                <Button 
                  variant="hero" 
                  className="w-full group-hover:shadow-glow-primary"
                >
                  Start {company.name} Prep
                  <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Card>
            ))}
          </div>

          {/* No Results */}
          {filteredCompanies.length === 0 && (
            <div className="text-center py-12">
              <Building2 className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">No companies found</h3>
              <p className="text-muted-foreground">
                Try adjusting your search or filter criteria
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Companies;