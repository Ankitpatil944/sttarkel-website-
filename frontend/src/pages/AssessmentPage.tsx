import { useState, useEffect, useRef } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { 
  Clock, 
  CheckCircle, 
  XCircle, 
  ArrowLeft, 
  ArrowRight,
  Flag,
  Brain,
  Target,
  BarChart,
  Timer,
  AlertCircle
} from "lucide-react";
import { useNavigate } from "react-router-dom";

interface Question {
  id: number;
  question: string;
  type: 'multiple-choice' | 'true-false' | 'coding' | 'essay';
  options?: string[];
  correctAnswer?: string | number;
  explanation?: string;
  timeLimit?: number;
  points: number;
}

interface AssessmentState {
  currentQuestion: number;
  answers: Record<number, any>;
  timeRemaining: number;
  isCompleted: boolean;
  score: number;
  totalQuestions: number;
}

const AssessmentPage = () => {
  const navigate = useNavigate();
  const [assessmentState, setAssessmentState] = useState<AssessmentState>({
    currentQuestion: 0,
    answers: {},
    timeRemaining: 3600, // 1 hour in seconds
    isCompleted: false,
    score: 0,
    totalQuestions: 0
  });
  
  const [questions, setQuestions] = useState<Question[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showExplanation, setShowExplanation] = useState(false);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  // Sample questions - in a real app, these would come from an API
  const sampleQuestions: Question[] = [
    {
      id: 1,
      question: "What is the time complexity of binary search?",
      type: 'multiple-choice',
      options: ["O(1)", "O(log n)", "O(n)", "O(n²)"],
      correctAnswer: 1,
      explanation: "Binary search has O(log n) time complexity because it divides the search space in half with each iteration.",
      timeLimit: 60,
      points: 10
    },
    {
      id: 2,
      question: "Which data structure follows LIFO principle?",
      type: 'multiple-choice',
      options: ["Queue", "Stack", "Tree", "Graph"],
      correctAnswer: 1,
      explanation: "Stack follows LIFO (Last In, First Out) principle where the last element added is the first one to be removed.",
      timeLimit: 45,
      points: 8
    },
    {
      id: 3,
      question: "In React, what hook is used to manage component state?",
      type: 'multiple-choice',
      options: ["useEffect", "useState", "useContext", "useReducer"],
      correctAnswer: 1,
      explanation: "useState is the hook used to manage local component state in React functional components.",
      timeLimit: 45,
      points: 8
    },
    {
      id: 4,
      question: "What is the primary purpose of a REST API?",
      type: 'multiple-choice',
      options: ["To provide real-time updates", "To create web applications", "To enable communication between systems", "To store data"],
      correctAnswer: 2,
      explanation: "REST APIs are designed to enable communication between different systems over HTTP using standard methods.",
      timeLimit: 60,
      points: 10
    },
    {
      id: 5,
      question: "Which sorting algorithm has the best average-case time complexity?",
      type: 'multiple-choice',
      options: ["Bubble Sort", "Quick Sort", "Selection Sort", "Insertion Sort"],
      correctAnswer: 1,
      explanation: "Quick Sort has an average-case time complexity of O(n log n), making it one of the most efficient sorting algorithms.",
      timeLimit: 60,
      points: 10
    }
  ];

  useEffect(() => {
    // Simulate loading questions from API
    setTimeout(() => {
      setQuestions(sampleQuestions);
      setAssessmentState(prev => ({ ...prev, totalQuestions: sampleQuestions.length }));
      setIsLoading(false);
    }, 1000);

    // Start timer
    timerRef.current = setInterval(() => {
      setAssessmentState(prev => {
        if (prev.timeRemaining <= 1) {
          // Time's up - auto-submit
          clearInterval(timerRef.current!);
          return { ...prev, timeRemaining: 0, isCompleted: true };
        }
        return { ...prev, timeRemaining: prev.timeRemaining - 1 };
      });
    }, 1000);

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleAnswer = (answer: any) => {
    setAssessmentState(prev => ({
      ...prev,
      answers: { ...prev.answers, [questions[prev.currentQuestion].id]: answer }
    }));
  };

  const handleNext = () => {
    if (assessmentState.currentQuestion < questions.length - 1) {
      setAssessmentState(prev => ({ ...prev, currentQuestion: prev.currentQuestion + 1 }));
      setShowExplanation(false);
    }
  };

  const handlePrevious = () => {
    if (assessmentState.currentQuestion > 0) {
      setAssessmentState(prev => ({ ...prev, currentQuestion: prev.currentQuestion - 1 }));
      setShowExplanation(false);
    }
  };

  const handleSubmit = () => {
    // Calculate score
    let score = 0;
    questions.forEach(question => {
      const userAnswer = assessmentState.answers[question.id];
      if (userAnswer === question.correctAnswer) {
        score += question.points;
      }
    });

    setAssessmentState(prev => ({ 
      ...prev, 
      isCompleted: true, 
      score 
    }));
  };

  const handleFlagQuestion = () => {
    // In a real app, this would mark the question for review
    console.log('Question flagged for review');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-bg flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary mx-auto mb-4"></div>
          <h2 className="text-2xl font-semibold">Loading Assessment...</h2>
          <p className="text-muted-foreground">Preparing your questions</p>
        </div>
      </div>
    );
  }

  if (assessmentState.isCompleted) {
    return (
      <div className="min-h-screen bg-gradient-bg">
        <div className="pt-24 pb-20">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <Card className="p-8 text-center">
              <div className="mb-6">
                <CheckCircle className="w-20 h-20 text-green-500 mx-auto mb-4" />
                <h1 className="text-3xl font-bold mb-2">Assessment Complete!</h1>
                <p className="text-muted-foreground">Great job completing your assessment</p>
              </div>

              <div className="grid md:grid-cols-2 gap-6 mb-8">
                <div className="bg-primary/10 p-6 rounded-lg">
                  <h3 className="text-xl font-semibold mb-2">Your Score</h3>
                  <div className="text-4xl font-bold text-primary">
                    {assessmentState.score}/{questions.reduce((sum, q) => sum + q.points, 0)}
                  </div>
                  <div className="text-muted-foreground">
                    {Math.round((assessmentState.score / questions.reduce((sum, q) => sum + q.points, 0)) * 100)}%
                  </div>
                </div>
                <div className="bg-secondary/10 p-6 rounded-lg">
                  <h3 className="text-xl font-semibold mb-2">Questions Answered</h3>
                  <div className="text-4xl font-bold text-secondary">
                    {Object.keys(assessmentState.answers).length}/{questions.length}
                  </div>
                  <div className="text-muted-foreground">
                    {Math.round((Object.keys(assessmentState.answers).length / questions.length) * 100)}% completion
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <Button 
                  onClick={() => navigate('/ai-assessment')}
                  className="w-full md:w-auto"
                >
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Back to Assessment Center
                </Button>
                <Button 
                  variant="outline"
                  onClick={() => window.location.reload()}
                  className="w-full md:w-auto"
                >
                  <Target className="w-4 h-4 mr-2" />
                  Retake Assessment
                </Button>
              </div>
            </Card>
          </div>
        </div>
      </div>
    );
  }

  const currentQuestion = questions[assessmentState.currentQuestion];
  const userAnswer = assessmentState.answers[currentQuestion.id];
  const progress = ((assessmentState.currentQuestion + 1) / questions.length) * 100;

  return (
    <div className="min-h-screen bg-gradient-bg">
      <div className="pt-24 pb-20">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <Button 
                variant="ghost" 
                onClick={() => navigate('/ai-assessment')}
                className="text-muted-foreground hover:text-foreground"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Assessment Center
              </Button>
              <div className="text-right">
                <div className="text-sm text-muted-foreground">Time Remaining</div>
                <div className={`text-2xl font-mono font-bold ${
                  assessmentState.timeRemaining < 300 ? 'text-red-500' : 'text-foreground'
                }`}>
                  {formatTime(assessmentState.timeRemaining)}
                </div>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="mb-4">
              <div className="flex justify-between text-sm mb-2">
                <span>Question {assessmentState.currentQuestion + 1} of {questions.length}</span>
                <span>{Math.round(progress)}% Complete</span>
              </div>
              <Progress value={progress} className="h-2" />
            </div>
          </div>

          <div className="grid lg:grid-cols-4 gap-6">
            {/* Question Panel */}
            <div className="lg:col-span-3">
              <Card className="p-6">
                {/* Question Header */}
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center space-x-3">
                    <Badge variant="outline" className="text-primary border-primary">
                      {currentQuestion.type.replace('-', ' ').toUpperCase()}
                    </Badge>
                    <Badge variant="secondary">
                      {currentQuestion.points} points
                    </Badge>
                    {currentQuestion.timeLimit && (
                      <Badge variant="outline">
                        <Clock className="w-3 h-3 mr-1" />
                        {currentQuestion.timeLimit}s
                      </Badge>
                    )}
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleFlagQuestion}
                    className="text-muted-foreground hover:text-amber-500"
                  >
                    <Flag className="w-4 h-4" />
                  </Button>
                </div>

                {/* Question */}
                <div className="mb-8">
                  <h2 className="text-xl font-semibold mb-4">{currentQuestion.question}</h2>
                  
                  {/* Answer Options */}
                  {currentQuestion.type === 'multiple-choice' && currentQuestion.options && (
                    <div className="space-y-3">
                      {currentQuestion.options.map((option, index) => (
                        <label
                          key={index}
                          className={`flex items-center p-4 border rounded-lg cursor-pointer transition-colors ${
                            userAnswer === index
                              ? 'border-primary bg-primary/10'
                              : 'border-border hover:border-primary/50'
                          }`}
                        >
                          <input
                            type="radio"
                            name={`question-${currentQuestion.id}`}
                            value={index}
                            checked={userAnswer === index}
                            onChange={() => handleAnswer(index)}
                            className="sr-only"
                          />
                          <div className={`w-4 h-4 rounded-full border-2 mr-3 ${
                            userAnswer === index
                              ? 'border-primary bg-primary'
                              : 'border-muted-foreground'
                          }`}>
                            {userAnswer === index && (
                              <div className="w-2 h-2 bg-white rounded-full m-0.5"></div>
                            )}
                          </div>
                          <span className="flex-1">{option}</span>
                        </label>
                      ))}
                    </div>
                  )}

                  {currentQuestion.type === 'true-false' && (
                    <div className="space-y-3">
                      {['True', 'False'].map((option, index) => (
                        <label
                          key={index}
                          className={`flex items-center p-4 border rounded-lg cursor-pointer transition-colors ${
                            userAnswer === index
                              ? 'border-primary bg-primary/10'
                              : 'border-border hover:border-primary/50'
                          }`}
                        >
                          <input
                            type="radio"
                            name={`question-${currentQuestion.id}`}
                            value={index}
                            checked={userAnswer === index}
                            onChange={() => handleAnswer(index)}
                            className="sr-only"
                          />
                          <div className={`w-4 h-4 rounded-full border-2 mr-3 ${
                            userAnswer === index
                              ? 'border-primary bg-primary'
                              : 'border-border hover:border-primary/50'
                          }`}>
                            {userAnswer === index && (
                              <div className="w-2 h-2 bg-white rounded-full m-0.5"></div>
                            )}
                          </div>
                          <span className="flex-1">{option}</span>
                        </label>
                      ))}
                    </div>
                  )}

                  {currentQuestion.type === 'coding' && (
                    <div className="space-y-4">
                      <div className="bg-secondary/20 p-4 rounded-lg">
                        <p className="text-sm text-muted-foreground mb-2">
                          Write your code solution below:
                        </p>
                        <textarea
                          className="w-full h-32 p-3 bg-background border rounded-lg font-mono text-sm"
                          placeholder="// Write your code here..."
                          value={userAnswer || ''}
                          onChange={(e) => handleAnswer(e.target.value)}
                        />
                      </div>
                    </div>
                  )}

                  {currentQuestion.type === 'essay' && (
                    <div className="space-y-4">
                      <div className="bg-secondary/20 p-4 rounded-lg">
                        <p className="text-sm text-muted-foreground mb-2">
                          Write your detailed answer below:
                        </p>
                        <textarea
                          className="w-full h-32 p-3 bg-background border rounded-lg"
                          placeholder="Type your answer here..."
                          value={userAnswer || ''}
                          onChange={(e) => handleAnswer(e.target.value)}
                        />
                      </div>
                    </div>
                  )}
                </div>

                {/* Navigation */}
                <div className="flex justify-between">
                  <Button
                    variant="outline"
                    onClick={handlePrevious}
                    disabled={assessmentState.currentQuestion === 0}
                  >
                    <ArrowLeft className="w-4 h-4 mr-2" />
                    Previous
                  </Button>

                  <div className="flex space-x-3">
                    {assessmentState.currentQuestion < questions.length - 1 ? (
                      <Button onClick={handleNext}>
                        Next
                        <ArrowRight className="w-4 h-4 ml-2" />
                      </Button>
                    ) : (
                      <Button onClick={handleSubmit} className="bg-green-600 hover:bg-green-700">
                        <CheckCircle className="w-4 h-4 mr-2" />
                        Submit Assessment
                      </Button>
                    )}
                  </div>
                </div>
              </Card>
            </div>

            {/* Sidebar */}
            <div className="lg:col-span-1">
              <Card className="p-4">
                <h3 className="font-semibold mb-4 flex items-center">
                  <BarChart className="w-4 h-4 mr-2" />
                  Question Navigator
                </h3>
                
                <div className="grid grid-cols-5 gap-2 mb-4">
                  {questions.map((_, index) => (
                    <button
                      key={index}
                      onClick={() => {
                        setAssessmentState(prev => ({ ...prev, currentQuestion: index }));
                        setShowExplanation(false);
                      }}
                      className={`w-8 h-8 rounded text-xs font-medium transition-colors ${
                        index === assessmentState.currentQuestion
                          ? 'bg-primary text-white'
                          : assessmentState.answers[questions[index].id] !== undefined
                          ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                          : 'bg-secondary text-muted-foreground hover:bg-secondary/80'
                      }`}
                    >
                      {index + 1}
                    </button>
                  ))}
                </div>

                <div className="space-y-2 text-sm">
                  <div className="flex items-center justify-between">
                    <span className="flex items-center">
                      <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                      Answered
                    </span>
                    <span className="font-medium">
                      {Object.keys(assessmentState.answers).length}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="flex items-center">
                      <div className="w-3 h-3 bg-secondary rounded-full mr-2" />
                      Unanswered
                    </span>
                    <span className="font-medium">
                      {questions.length - Object.keys(assessmentState.answers).length}
                    </span>
                  </div>
                </div>

                {assessmentState.timeRemaining < 300 && (
                  <div className="mt-4 p-3 bg-red-100 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                    <div className="flex items-center text-red-600 dark:text-red-400">
                      <AlertCircle className="w-4 h-4 mr-2" />
                      <span className="text-sm font-medium">Time is running out!</span>
                    </div>
                  </div>
                )}
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AssessmentPage;
