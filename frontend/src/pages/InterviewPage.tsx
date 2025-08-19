import { useState, useRef, useEffect } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { 
  Video, 
  Mic, 
  MicOff, 
  VideoOff, 
  Phone, 
  MessageSquare, 
  Brain, 
  Eye, 
  Volume2, 
  Settings,
  Play,
  Pause,
  RotateCcw,
  CheckCircle,
  XCircle,
  ArrowLeft,
  ArrowRight,
  Clock,
  Star,
  TrendingUp,
  AlertCircle,
  Sparkles,
  Zap,
  Target,
  Lightbulb,
  FileText,
  BarChart3,
  Users,
  Timer
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import { motion } from 'framer-motion';
import './OutlinedText.css';

interface InterviewQuestion {
  id: number;
  question: string;
  category: 'behavioral' | 'technical' | 'situational' | 'strengths-weaknesses';
  timeLimit: number;
  tips: string[];
}

interface InterviewState {
  currentQuestion: number;
  isRecording: boolean;
  isPaused: boolean;
  timeRemaining: number;
  isCompleted: boolean;
  responses: Record<number, {
    answer: string;
    duration: number;
    confidence: number;
    eyeContact: number;
    speechClarity: number;
    emotionalState: string;
  }>;
}

const InterviewPage = () => {
  const navigate = useNavigate();
  const videoRef = useRef<HTMLVideoElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const [interviewState, setInterviewState] = useState<InterviewState>({
    currentQuestion: 0,
    isRecording: false,
    isPaused: false,
    timeRemaining: 0,
    isCompleted: false,
    responses: {}
  });

  const [isVideoOn, setIsVideoOn] = useState(true);
  const [isMicOn, setIsMicOn] = useState(true);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [showTips, setShowTips] = useState(false);
  const [liveTranscript, setLiveTranscript] = useState<string[]>([]);
  const [realTimeMetrics, setRealTimeMetrics] = useState({
    confidence: 78,
    eyeContact: 85,
    speechClarity: 82,
    emotionalState: "Confident",
    overallSentiment: "Positive"
  });

  // Sample interview questions
  const interviewQuestions: InterviewQuestion[] = [
    {
      id: 1,
      question: "Tell me about yourself and your background.",
      category: 'behavioral',
      timeLimit: 120,
      tips: [
        "Start with a brief personal introduction",
        "Focus on relevant professional experience",
        "Connect your background to the role",
        "Keep it concise and engaging"
      ]
    },
    {
      id: 2,
      question: "Why are you interested in this position?",
      category: 'behavioral',
      timeLimit: 90,
      tips: [
        "Show enthusiasm for the company",
        "Connect your skills to the role",
        "Mention specific aspects that excite you",
        "Demonstrate research about the company"
      ]
    },
    {
      id: 3,
      question: "Describe a challenging project you've worked on.",
      category: 'situational',
      timeLimit: 150,
      tips: [
        "Use the STAR method (Situation, Task, Action, Result)",
        "Focus on your problem-solving approach",
        "Highlight what you learned",
        "Show resilience and adaptability"
      ]
    },
    {
      id: 4,
      question: "How do you handle working under pressure?",
      category: 'behavioral',
      timeLimit: 90,
      tips: [
        "Provide specific examples",
        "Show your prioritization skills",
        "Demonstrate stress management techniques",
        "Highlight positive outcomes"
      ]
    },
    {
      id: 5,
      question: "Where do you see yourself in 5 years?",
      category: 'strengths-weaknesses',
      timeLimit: 90,
      tips: [
        "Show ambition and realistic goals",
        "Connect to the company's growth",
        "Demonstrate career planning",
        "Show commitment to continuous learning"
      ]
    }
  ];

  useEffect(() => {
    // Initialize video stream
    const initializeStream = async () => {
      try {
        const mediaStream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: true
        });
        setStream(mediaStream);
        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream;
        }
      } catch (error) {
        console.error('Error accessing media devices:', error);
      }
    };

    initializeStream();

    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  const startRecording = async () => {
    if (!stream) return;

    try {
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'video/webm' });
        const url = URL.createObjectURL(blob);
        console.log('Recording saved:', url);
      };

      mediaRecorder.start();
      setInterviewState(prev => ({ 
        ...prev, 
        isRecording: true, 
        timeRemaining: interviewQuestions[prev.currentQuestion].timeLimit 
      }));

      // Start timer
      timerRef.current = setInterval(() => {
        setInterviewState(prev => {
          if (prev.timeRemaining <= 1) {
            // Time's up - stop recording
            if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
              mediaRecorderRef.current.stop();
            }
            clearInterval(timerRef.current!);
            return { ...prev, isRecording: false, timeRemaining: 0 };
          }
          return { ...prev, timeRemaining: prev.timeRemaining - 1 };
        });
      }, 1000);

      // Simulate live transcript
      const transcriptInterval = setInterval(() => {
        if (interviewState.isRecording) {
          setLiveTranscript(prev => [...prev, "This is a simulated live transcript..."]);
        } else {
          clearInterval(transcriptInterval);
        }
      }, 3000);

    } catch (error) {
      console.error('Error starting recording:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
    }
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }
    setInterviewState(prev => ({ ...prev, isRecording: false }));
  };

  const pauseRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.pause();
    }
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }
    setInterviewState(prev => ({ ...prev, isPaused: true }));
  };

  const resumeRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'paused') {
      mediaRecorderRef.current.resume();
    }
    timerRef.current = setInterval(() => {
      setInterviewState(prev => {
        if (prev.timeRemaining <= 1) {
          if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
            mediaRecorderRef.current.stop();
          }
          clearInterval(timerRef.current!);
          return { ...prev, isRecording: false, timeRemaining: 0 };
        }
        return { ...prev, timeRemaining: prev.timeRemaining - 1 };
      });
    }, 1000);
    setInterviewState(prev => ({ ...prev, isPaused: false }));
  };

  const toggleVideo = () => {
    if (stream) {
      const videoTrack = stream.getVideoTracks()[0];
      if (videoTrack) {
        videoTrack.enabled = !isVideoOn;
        setIsVideoOn(!isVideoOn);
      }
    }
  };

  const toggleMic = () => {
    if (stream) {
      const audioTrack = stream.getAudioTracks()[0];
      if (audioTrack) {
        audioTrack.enabled = !isMicOn;
        setIsMicOn(!isMicOn);
      }
    }
  };

  const handleNext = () => {
    if (interviewState.currentQuestion < interviewQuestions.length - 1) {
      setInterviewState(prev => ({ 
        ...prev, 
        currentQuestion: prev.currentQuestion + 1,
        timeRemaining: interviewQuestions[prev.currentQuestion + 1].timeLimit
      }));
      setShowTips(false);
    }
  };

  const handlePrevious = () => {
    if (interviewState.currentQuestion > 0) {
      setInterviewState(prev => ({ 
        ...prev, 
        currentQuestion: prev.currentQuestion - 1,
        timeRemaining: interviewQuestions[prev.currentQuestion - 1].timeLimit
      }));
      setShowTips(false);
    }
  };

  const handleComplete = () => {
    setInterviewState(prev => ({ ...prev, isCompleted: true }));
    navigate('/analytics');
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const currentQuestion = interviewQuestions[interviewState.currentQuestion];
  const currentResponse = interviewState.responses[currentQuestion.id];
  const progress = ((interviewState.currentQuestion + 1) / interviewQuestions.length) * 100;

  return (
    <div className="min-h-screen bg-gradient-bg">
      <div
        className="min-h-screen max-w-screen-2xl mx-auto px-4 sm:px-6 lg:px-8 
                    m-4 sm:m-6 lg:m-10 bg-gradient-bg border border-blue-300 rounded-3xl overflow-hidden bg-gradient-to-b from-slate-100 to-cyan-50
                    animate-fade-in mt-20"
        style={{ marginTop: '5rem' }}
      >
        {/* Header */}
        <div className="pt-20 mt-10 pb-8">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-8">
              <div className="inline-flex items-center space-x-2 bg-card/50 backdrop-blur-sm rounded-full px-4 py-2 mb-6 border border-primary/20 animate-fade-in">
                <Sparkles className="h-4 w-4 text-primary animate-pulse" />
                <span className="text-sm font-medium">AI-Powered Interview Practice</span>
              </div>
              <h1 className="text-3xl sm:text-4xl md:text-6xl lg:text-7xl font-normal mb-6 leading-tight animate-fade-in text-[#2D3253]">
                AI Interview <span className="bg-gradient-primary bg-clip-text text-transparent">Simulator</span>
              </h1>
              <p className="text-xl text-muted-foreground mb-10 max-w-3xl mx-auto leading-relaxed animate-fade-in">
                Practice with our AI interviewer and get real-time feedback on your performance.
              </p>
            </div>

            {/* Progress and Timer */}
            <div className="flex justify-between items-center mb-6">
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <Clock className="w-5 h-5 text-primary" />
                  <span className="text-sm font-medium">Question</span>
                  <div className="text-2xl font-bold">
                    {interviewState.currentQuestion + 1} / {interviewQuestions.length}
                  </div>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="flex-1 max-w-md mx-4">
                <div className="flex justify-between text-sm mb-2">
                  <span>Interview Progress</span>
                  <span>{Math.round(progress)}% Complete</span>
                </div>
                <Progress value={progress} className="h-2" />
              </div>

              {/* Timer */}
              {interviewState.isRecording && (
                <div className="text-center">
                  <div className="text-sm text-muted-foreground mb-1">Time Remaining</div>
                  <div className={`text-2xl font-mono font-bold ${
                    interviewState.timeRemaining < 30 ? 'text-red-500' : 'text-foreground'
                  }`}>
                    {formatTime(interviewState.timeRemaining)}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Main Interview Interface */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-8">
          <div className="grid lg:grid-cols-2 gap-8 mb-8">
            {/* AI Interviewer Panel */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
            >
              <Card className="p-6 bg-gradient-card border-primary/10 hover:border-primary/30 transition-all duration-300 hover:shadow-glow-accent h-full">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-xl font-semibold flex items-center">
                    <Brain className="w-5 h-5 mr-2 text-primary" />
                    AI Interviewer
                  </h3>
                  <Badge variant="outline" className="text-primary border-primary">
                    Question {interviewState.currentQuestion + 1} of {interviewQuestions.length}
                  </Badge>
                </div>
                
                {/* AI Avatar */}
                <div className="aspect-video bg-gradient-to-br from-primary/10 to-accent/10 rounded-lg mb-4 flex items-center justify-center relative overflow-hidden">
                  {/* Animated background */}
                  <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-accent/20 animate-pulse"></div>
                  
                  {/* 3D Avatar */}
                  <div className="relative z-10 w-32 h-32 bg-gradient-primary rounded-full flex items-center justify-center shadow-glow-primary">
                    <Brain className="w-16 h-16 text-white" />
                  </div>
                  
                  {/* Speaking indicator */}
                  {interviewState.isRecording && (
                    <div className="absolute bottom-4 left-4 flex items-center space-x-2 bg-black/50 rounded-full px-3 py-1">
                      <Volume2 className="w-4 h-4 text-primary animate-pulse" />
                      <span className="text-sm text-white">Speaking...</span>
                    </div>
                  )}
                </div>

                {/* Question */}
                <div className="mb-6">
                  <h2 className="text-xl font-semibold mb-4">{currentQuestion.question}</h2>
                  
                  {/* Tips Toggle */}
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setShowTips(!showTips)}
                    className="mb-4"
                  >
                    <Lightbulb className="w-4 h-4 mr-2" />
                    {showTips ? 'Hide' : 'Show'} Tips
                  </Button>

                  {showTips && (
                    <motion.div 
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      className="bg-primary/10 p-4 rounded-lg"
                    >
                      <h4 className="font-semibold mb-2 text-primary">Tips for this question:</h4>
                      <ul className="space-y-1 text-sm">
                        {currentQuestion.tips.map((tip, index) => (
                          <li key={index} className="flex items-start">
                            <Star className="w-3 h-3 text-primary mr-2 mt-0.5 flex-shrink-0" />
                            {tip}
                          </li>
                        ))}
                      </ul>
                    </motion.div>
                  )}
                </div>

                {/* Recording Controls */}
                <div className="flex justify-center space-x-4">
                  {!interviewState.isRecording ? (
                    <Button 
                      onClick={startRecording}
                      size="lg"
                      className="bg-red-600 hover:bg-red-700 hover-scale"
                    >
                      <Play className="w-5 h-5 mr-2" />
                      Start AI Interview
                    </Button>
                  ) : (
                    <>
                      {interviewState.isPaused ? (
                        <Button 
                          onClick={resumeRecording}
                          size="lg"
                          variant="outline"
                          className="hover-scale"
                        >
                          <Play className="w-5 h-5 mr-2" />
                          Resume
                        </Button>
                      ) : (
                        <Button 
                          onClick={pauseRecording}
                          size="lg"
                          variant="outline"
                          className="hover-scale"
                        >
                          <Pause className="w-5 h-5 mr-2" />
                          Pause
                        </Button>
                      )}
                      <Button 
                        onClick={stopRecording}
                        size="lg"
                        variant="outline"
                        className="hover-scale"
                      >
                        <CheckCircle className="w-5 h-5 mr-2" />
                        Stop & Analyze
                      </Button>
                    </>
                  )}
                </div>
              </Card>
            </motion.div>

            {/* User Video Panel */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <Card className="p-6 bg-gradient-card border-primary/10 hover:border-primary/30 transition-all duration-300 hover:shadow-glow-accent h-full">
                <h3 className="text-lg font-semibold mb-4 flex items-center">
                  <Video className="w-5 h-5 mr-2" />
                  Your Video
                </h3>
                
                <div className="aspect-video bg-secondary rounded-lg overflow-hidden relative mb-4">
                  <video
                    ref={videoRef}
                    autoPlay
                    muted
                    playsInline
                    className="w-full h-full object-cover"
                  />
                  
                  {!isVideoOn && (
                    <div className="absolute inset-0 bg-black flex items-center justify-center">
                      <VideoOff className="w-16 h-16 text-white" />
                    </div>
                  )}

                  {/* Recording indicator */}
                  {interviewState.isRecording && (
                    <div className="absolute top-4 right-4 flex items-center space-x-2 bg-red-600 rounded-full px-3 py-1">
                      <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                      <span className="text-sm text-white">Recording</span>
                    </div>
                  )}
                </div>

                {/* Video Controls */}
                <div className="flex justify-center space-x-4">
                  <Button
                    variant={isVideoOn ? "default" : "outline"}
                    onClick={toggleVideo}
                    size="sm"
                    className="hover-scale"
                  >
                    {isVideoOn ? <Video className="w-4 h-4 mr-2" /> : <VideoOff className="w-4 h-4 mr-2" />}
                    {isVideoOn ? 'Video On' : 'Video Off'}
                  </Button>
                  <Button
                    variant={isMicOn ? "default" : "outline"}
                    onClick={toggleMic}
                    size="sm"
                    className="hover-scale"
                  >
                    {isMicOn ? <Mic className="w-4 h-4 mr-2" /> : <MicOff className="w-4 h-4 mr-2" />}
                    {isMicOn ? 'Mic On' : 'Mic Off'}
                  </Button>
                </div>
              </Card>
            </motion.div>
          </div>

          {/* Real-time Analysis and Live Transcript */}
          <div className="grid lg:grid-cols-2 gap-8">
            {/* Real-time Analysis */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
            >
              <Card className="p-6 bg-gradient-card border-primary/10 hover:border-primary/30 transition-all duration-300 hover:shadow-glow-accent">
                <h3 className="text-lg font-semibold mb-4 flex items-center">
                  <BarChart3 className="w-5 h-5 mr-2 text-primary" />
                  Real-time Analysis
                </h3>
                
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Confidence Level</span>
                    <span className="font-bold text-primary">{realTimeMetrics.confidence}%</span>
                  </div>
                  <Progress value={realTimeMetrics.confidence} className="h-2" />
                  
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Eye Contact</span>
                    <span className="font-bold text-green-600">{realTimeMetrics.eyeContact}%</span>
                  </div>
                  <Progress value={realTimeMetrics.eyeContact} className="h-2 bg-green-100" />
                  
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Speech Clarity</span>
                    <span className="font-bold text-blue-600">{realTimeMetrics.speechClarity}%</span>
                  </div>
                  <Progress value={realTimeMetrics.speechClarity} className="h-2 bg-blue-100" />
                  
                  <div className="flex justify-between items-center pt-2 border-t">
                    <span className="text-sm font-medium">Emotional State</span>
                    <Badge variant="outline" className="text-blue-600 border-blue-600">
                      {realTimeMetrics.emotionalState}
                    </Badge>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Overall Sentiment</span>
                    <Badge variant="outline" className="text-green-600 border-green-600">
                      {realTimeMetrics.overallSentiment}
                    </Badge>
                  </div>
                </div>
              </Card>
            </motion.div>

            {/* Live Transcript */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.6 }}
            >
              <Card className="p-6 bg-gradient-card border-primary/10 hover:border-primary/30 transition-all duration-300 hover:shadow-glow-accent">
                <h3 className="text-lg font-semibold mb-4 flex items-center">
                  <FileText className="w-5 h-5 mr-2 text-primary" />
                  Live Transcript
                </h3>
                
                <div className="h-48 overflow-y-auto bg-secondary/20 rounded-lg p-4">
                  {liveTranscript.length > 0 ? (
                    <div className="space-y-2">
                      {liveTranscript.map((transcript, index) => (
                        <div key={index} className="text-sm text-muted-foreground">
                          <span className="text-primary font-medium">You:</span> {transcript}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center text-muted-foreground py-8">
                      <MessageSquare className="w-8 h-8 mx-auto mb-2 opacity-50" />
                      <p>Start the interview to see live transcription</p>
                    </div>
                  )}
                </div>
              </Card>
            </motion.div>
          </div>

          {/* Navigation and Question Navigator */}
          <div className="mt-8 grid lg:grid-cols-3 gap-6">
            {/* Question Navigator */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.8 }}
              className="lg:col-span-2"
            >
              <Card className="p-6 bg-gradient-card border-primary/10 hover:border-primary/30 transition-all duration-300 hover:shadow-glow-accent">
                <h3 className="font-semibold mb-4 flex items-center">
                  <Target className="w-4 h-4 mr-2" />
                  Question Navigator
                </h3>
                
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
                  {interviewQuestions.map((question, index) => (
                    <button
                      key={question.id}
                      onClick={() => {
                        setInterviewState(prev => ({ 
                          ...prev, 
                          currentQuestion: index,
                          timeRemaining: question.timeLimit
                        }));
                        setShowTips(false);
                      }}
                      className={`p-3 rounded-lg text-left transition-all duration-300 hover-scale ${
                        index === interviewState.currentQuestion
                          ? 'bg-primary text-white shadow-lg'
                          : interviewState.responses[question.id]
                          ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 border-2 border-green-300'
                          : 'bg-secondary text-muted-foreground hover:bg-secondary/80 border-2 border-transparent'
                      }`}
                    >
                      <div className="font-medium text-sm">Q{index + 1}</div>
                      <div className="text-xs opacity-80 mt-1">
                        {question.category.replace('-', ' ')}
                      </div>
                    </button>
                  ))}
                </div>
              </Card>
            </motion.div>

            {/* Navigation Controls */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 1 }}
            >
              <Card className="p-6 bg-gradient-card border-primary/10 hover:border-primary/30 transition-all duration-300 hover:shadow-glow-accent">
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <Button
                      variant="outline"
                      onClick={handlePrevious}
                      disabled={interviewState.currentQuestion === 0}
                      size="sm"
                      className="hover-scale"
                    >
                      <ArrowLeft className="w-4 h-4 mr-2" />
                      Previous
                    </Button>

                    <div className="flex space-x-2">
                      {interviewState.currentQuestion < interviewQuestions.length - 1 ? (
                        <Button onClick={handleNext} size="sm" className="hover-scale">
                          Next
                          <ArrowRight className="w-4 h-4 ml-2" />
                        </Button>
                      ) : (
                        <Button 
                          onClick={handleComplete} 
                          size="sm"
                          className="bg-green-600 hover:bg-green-700 hover-scale"
                        >
                          <CheckCircle className="w-4 h-4 mr-2" />
                          Complete
                        </Button>
                      )}
                    </div>
                  </div>

                  {/* Quick Stats */}
                  <div className="pt-4 border-t">
                    <div className="text-sm text-muted-foreground mb-2">Interview Stats</div>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Questions Answered</span>
                        <span className="font-medium">{Object.keys(interviewState.responses).length}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span>Total Time</span>
                        <span className="font-medium">12:34</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span>Average Score</span>
                        <span className="font-medium text-primary">85%</span>
                      </div>
                    </div>
                  </div>
                </div>
              </Card>
            </motion.div>
          </div>
        </div>
      </div>

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

export default InterviewPage;
