import { useState } from "react";
import { Link } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { 
  CheckCircle, 
  ArrowRight, 
  BookOpen, 
  Brain, 
  Zap,
  Clock,
  Target
} from "lucide-react";

const DifficultySelection = () => {
  const [selectedDifficulty, setSelectedDifficulty] = useState<string | null>(null);

  const difficulties = [
    {
      id: "beginner",
      title: "Beginner",
      subtitle: "Perfect for freshers",
      description: "Basic aptitude, fundamental coding problems, and entry-level behavioral questions",
      icon: BookOpen,
      duration: "45 mins",
      questions: "25 questions",
      features: [
        "Basic logical reasoning",
        "Simple coding challenges",
        "Fundamental behavioral questions",
        "Detailed explanations"
      ],
      color: "from-green-500 to-emerald-600",
      bgGlow: "shadow-green-500/20"
    },
    {
      id: "intermediate",
      title: "Intermediate",
      subtitle: "For experienced candidates",
      description: "Moderate difficulty with real-world scenarios and technical depth",
      icon: Brain,
      duration: "60 mins",
      questions: "35 questions",
      features: [
        "Advanced problem solving",
        "Medium coding challenges",
        "Situational interviews",
        "Performance analytics"
      ],
      color: "from-blue-500 to-cyan-600",
      bgGlow: "shadow-blue-500/20"
    },
    {
      id: "advanced",
      title: "Advanced",
      subtitle: "For senior positions",
      description: "Complex scenarios, system design, and leadership-focused assessments",
      icon: Zap,
      duration: "75 mins",
      questions: "45 questions",
      features: [
        "Complex algorithms",
        "System design questions",
        "Leadership scenarios",
        "Advanced AI feedback"
      ],
      color: "from-purple-500 to-pink-600",
      bgGlow: "shadow-purple-500/20"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-bg">
      
      <div className="pt-24 pb-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="text-center mb-16">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Choose Your
              <span className="bg-gradient-primary bg-clip-text text-transparent block">
                Challenge Level
              </span>
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Select the difficulty level that matches your experience and career goals. 
              Each level is designed to prepare you for specific interview scenarios.
            </p>
          </div>

          {/* Difficulty Cards */}
          <div className="grid md:grid-cols-3 gap-8 mb-12">
            {difficulties.map((difficulty) => (
              <Card 
                key={difficulty.id}
                className={`relative p-8 cursor-pointer transition-all duration-300 border-2 hover:scale-105 ${
                  selectedDifficulty === difficulty.id
                    ? "border-primary shadow-glow-primary"
                    : "border-border hover:border-primary/50"
                } bg-gradient-card hover:shadow-glow-accent`}
                onClick={() => setSelectedDifficulty(difficulty.id)}
              >
                {/* Selection indicator */}
                {selectedDifficulty === difficulty.id && (
                  <div className="absolute top-4 right-4">
                    <CheckCircle className="h-6 w-6 text-primary" />
                  </div>
                )}

                {/* Icon */}
                <div className={`w-16 h-16 rounded-xl bg-gradient-to-r ${difficulty.color} flex items-center justify-center mb-6 mx-auto`}>
                  <difficulty.icon className="h-8 w-8 text-white" />
                </div>

                {/* Content */}
                <div className="text-center mb-6">
                  <h3 className="text-2xl font-bold mb-2">{difficulty.title}</h3>
                  <p className="text-primary font-medium mb-3">{difficulty.subtitle}</p>
                  <p className="text-muted-foreground text-sm leading-relaxed">
                    {difficulty.description}
                  </p>
                </div>

                {/* Stats */}
                <div className="flex justify-center space-x-6 mb-6 text-sm">
                  <div className="flex items-center space-x-1">
                    <Clock className="h-4 w-4 text-muted-foreground" />
                    <span>{difficulty.duration}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Target className="h-4 w-4 text-muted-foreground" />
                    <span>{difficulty.questions}</span>
                  </div>
                </div>

                {/* Features */}
                <div className="space-y-2">
                  {difficulty.features.map((feature, index) => (
                    <div key={index} className="flex items-center space-x-2 text-sm">
                      <CheckCircle className="h-4 w-4 text-primary flex-shrink-0" />
                      <span className="text-muted-foreground">{feature}</span>
                    </div>
                  ))}
                </div>
              </Card>
            ))}
          </div>

          {/* Continue Button */}
          {selectedDifficulty && (
            <div className="text-center animate-in slide-in-from-bottom-4 duration-500">
              <Link to="/assessment/aptitude">
                <Button variant="hero" size="xl" className="group">
                  Start {difficulties.find(d => d.id === selectedDifficulty)?.title} Assessment
                  <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DifficultySelection;