import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from "recharts";
import {
  TrendingUp,
  Download,
  Calendar,
  Trophy,
  Target,
  Brain,
  Clock,
  Eye,
  Mic,
  MessageSquare
} from "lucide-react";

const Analytics = () => {
  const [selectedTimeRange, setSelectedTimeRange] = useState("1M");

  // Mock data for charts
  const skillData = [
    { name: "Logical Reasoning", score: 85, maxScore: 100 },
    { name: "Coding", score: 78, maxScore: 100 },
    { name: "Communication", score: 92, maxScore: 100 },
    { name: "Problem Solving", score: 88, maxScore: 100 },
    { name: "Leadership", score: 75, maxScore: 100 },
    { name: "Technical Knowledge", score: 82, maxScore: 100 },
  ];

  const progressData = [
    { date: "Week 1", score: 65 },
    { date: "Week 2", score: 72 },
    { date: "Week 3", score: 78 },
    { date: "Week 4", score: 85 },
  ];

  const assessmentBreakdown = [
    { name: "Aptitude", value: 85, color: "#00D2FF" },
    { name: "Coding", value: 78, color: "#0099CC" },
    { name: "Behavioral", value: 92, color: "#007399" },
    { name: "Technical", value: 82, color: "#004D66" },
  ];

  const aiAnalysis = {
    confidence: 78,
    eyeContact: 85,
    speechClarity: 88,
    fillerWords: 12,
    overallRating: "B+"
  };

  const radarData = [
    { skill: "Technical", current: 82, target: 90 },
    { skill: "Communication", current: 92, target: 95 },
    { skill: "Problem Solving", current: 88, target: 90 },
    { skill: "Leadership", current: 75, target: 85 },
    { skill: "Adaptability", current: 80, target: 88 },
    { skill: "Creativity", current: 85, target: 90 },
  ];

  return (
    <div className="min-h-screen bg-gradient-bg">
      
      <div className="pt-24 pb-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
            <div>
              <h1 className="text-4xl font-bold mb-2">
                Performance 
                <span className="bg-gradient-primary bg-clip-text text-transparent"> Analytics</span>
              </h1>
              <p className="text-muted-foreground">
                Track your progress and get insights to improve your interview skills
              </p>
            </div>
            <div className="flex gap-4 mt-4 md:mt-0">
              <div className="flex gap-2">
                {["1W", "1M", "3M", "6M"].map((range) => (
                  <Button
                    key={range}
                    variant={selectedTimeRange === range ? "default" : "outline"}
                    size="sm"
                    onClick={() => setSelectedTimeRange(range)}
                  >
                    {range}
                  </Button>
                ))}
              </div>
              <Button variant="hero" size="sm">
                <Download className="w-4 h-4 mr-2" />
                Download Report
              </Button>
            </div>
          </div>

          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <Card className="p-6 bg-gradient-card border-primary/10">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Overall Score</p>
                  <p className="text-3xl font-bold text-primary">84%</p>
                  <p className="text-xs text-green-400 flex items-center mt-1">
                    <TrendingUp className="w-3 h-3 mr-1" />
                    +12% from last month
                  </p>
                </div>
                <Trophy className="w-8 h-8 text-primary" />
              </div>
            </Card>

            <Card className="p-6 bg-gradient-card border-primary/10">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Assessments</p>
                  <p className="text-3xl font-bold">12</p>
                  <p className="text-xs text-blue-400 flex items-center mt-1">
                    <Calendar className="w-3 h-3 mr-1" />
                    This month
                  </p>
                </div>
                <Target className="w-8 h-8 text-primary" />
              </div>
            </Card>

            <Card className="p-6 bg-gradient-card border-primary/10">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Study Time</p>
                  <p className="text-3xl font-bold">24h</p>
                  <p className="text-xs text-cyan-400 flex items-center mt-1">
                    <Clock className="w-3 h-3 mr-1" />
                    Weekly average
                  </p>
                </div>
                <Brain className="w-8 h-8 text-primary" />
              </div>
            </Card>

            <Card className="p-6 bg-gradient-card border-primary/10">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">AI Rating</p>
                  <p className="text-3xl font-bold">{aiAnalysis.overallRating}</p>
                  <Badge variant="secondary" className="mt-1">
                    Above Average
                  </Badge>
                </div>
                <MessageSquare className="w-8 h-8 text-primary" />
              </div>
            </Card>
          </div>

          {/* Charts Section */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            {/* Skill Breakdown */}
            <Card className="p-6 bg-gradient-card border-primary/10">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <BarChart className="w-5 h-5 mr-2 text-primary" />
                Skill Breakdown
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={skillData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis 
                    dataKey="name" 
                    stroke="#9CA3AF"
                    fontSize={12}
                    angle={-45}
                    textAnchor="end"
                    height={60}
                  />
                  <YAxis stroke="#9CA3AF" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: "#1F2937", 
                      border: "1px solid #374151",
                      borderRadius: "8px"
                    }}
                  />
                  <Bar dataKey="score" fill="#00D2FF" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </Card>

            {/* Progress Over Time */}
            <Card className="p-6 bg-gradient-card border-primary/10">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <TrendingUp className="w-5 h-5 mr-2 text-primary" />
                Progress Over Time
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={progressData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="date" stroke="#9CA3AF" />
                  <YAxis stroke="#9CA3AF" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: "#1F2937", 
                      border: "1px solid #374151",
                      borderRadius: "8px"
                    }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="score" 
                    stroke="#00D2FF" 
                    strokeWidth={3}
                    dot={{ fill: "#00D2FF", strokeWidth: 2, r: 6 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </Card>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Assessment Breakdown Pie Chart */}
            <Card className="p-6 bg-gradient-card border-primary/10">
              <h3 className="text-xl font-semibold mb-4">Assessment Breakdown</h3>
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie
                    data={assessmentBreakdown}
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    dataKey="value"
                    label={({ name, value }) => `${name}: ${value}%`}
                  >
                    {assessmentBreakdown.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </Card>

            {/* AI Interview Feedback */}
            <Card className="p-6 bg-gradient-card border-primary/10">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <Brain className="w-5 h-5 mr-2 text-primary" />
                AI Interview Analysis
              </h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <Eye className="w-4 h-4 mr-2 text-primary" />
                    <span className="text-sm">Eye Contact</span>
                  </div>
                  <Badge variant={aiAnalysis.eyeContact > 80 ? "default" : "secondary"}>
                    {aiAnalysis.eyeContact}%
                  </Badge>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <MessageSquare className="w-4 h-4 mr-2 text-primary" />
                    <span className="text-sm">Confidence</span>
                  </div>
                  <Badge variant={aiAnalysis.confidence > 75 ? "default" : "secondary"}>
                    {aiAnalysis.confidence}%
                  </Badge>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <Mic className="w-4 h-4 mr-2 text-primary" />
                    <span className="text-sm">Speech Clarity</span>
                  </div>
                  <Badge variant={aiAnalysis.speechClarity > 80 ? "default" : "secondary"}>
                    {aiAnalysis.speechClarity}%
                  </Badge>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <Clock className="w-4 h-4 mr-2 text-primary" />
                    <span className="text-sm">Filler Words</span>
                  </div>
                  <Badge variant={aiAnalysis.fillerWords < 15 ? "default" : "destructive"}>
                    {aiAnalysis.fillerWords}
                  </Badge>
                </div>
              </div>
            </Card>

            {/* Skills Radar */}
            <Card className="p-6 bg-gradient-card border-primary/10">
              <h3 className="text-xl font-semibold mb-4">Skills vs Target</h3>
              <ResponsiveContainer width="100%" height={250}>
                <RadarChart data={radarData}>
                  <PolarGrid stroke="#374151" />
                  <PolarAngleAxis dataKey="skill" tick={{ fill: "#9CA3AF", fontSize: 12 }} />
                  <PolarRadiusAxis 
                    angle={90} 
                    domain={[0, 100]} 
                    tick={{ fill: "#9CA3AF", fontSize: 10 }}
                  />
                  <Radar
                    name="Current"
                    dataKey="current"
                    stroke="#00D2FF"
                    fill="#00D2FF"
                    fillOpacity={0.3}
                    strokeWidth={2}
                  />
                  <Radar
                    name="Target"
                    dataKey="target"
                    stroke="#0099CC"
                    fill="transparent"
                    strokeWidth={2}
                    strokeDasharray="5 5"
                  />
                  <Legend />
                </RadarChart>
              </ResponsiveContainer>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;