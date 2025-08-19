import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Badge } from "@/components/ui/badge";
import { motion, AnimatePresence } from 'framer-motion';
import { 
  User, 
  Briefcase, 
  Shield, 
  CheckCircle, 
  ArrowRight, 
  ArrowLeft,
  Star,
  Award,
  GraduationCap,
  MapPin,
  Mail,
  Phone,
  Linkedin,
  Github,
  Globe,
  Upload,
  Eye,
  EyeOff
} from "lucide-react";

interface MentorFormData {
  // Personal Info
  firstName: string;
  lastName: string;
  displayName: string;
  email: string;
  phone: string;
  location: string;
  bio: string;
  
  // Professional Info
  currentRole: string;
  company: string;
  experience: string;
  expertise: string[];
  education: string;
  certifications: string[];
  linkedinUrl: string;
  githubUrl: string;
  portfolioUrl: string;
  resumeFile: File | null;
  
  // Account Security
  password: string;
  confirmPassword: string;
  agreeToTerms: boolean;
  agreeToPrivacy: boolean;
  agreeToMentorGuidelines: boolean;
}

const BecomeMentor = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [completionRate, setCompletionRate] = useState(0);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  
  const [formData, setFormData] = useState<MentorFormData>({
    firstName: '',
    lastName: '',
    displayName: '',
    email: '',
    phone: '',
    location: '',
    bio: '',
    currentRole: '',
    company: '',
    experience: '',
    expertise: [],
    education: '',
    certifications: [],
    linkedinUrl: '',
    githubUrl: '',
    portfolioUrl: '',
    resumeFile: null,
    password: '',
    confirmPassword: '',
    agreeToTerms: false,
    agreeToPrivacy: false,
    agreeToMentorGuidelines: false,
  });

  const steps = [
    { id: 1, title: "Personal Info", icon: User, description: "Tell us about yourself" },
    { id: 2, title: "Professional Info", icon: Briefcase, description: "Share your expertise" },
    { id: 3, title: "Account Security", icon: Shield, description: "Secure your account" }
  ];

  const techCategories = [
    "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "PHP", "Ruby", "Swift",
    "React", "Vue", "Angular", "Node.js", "Django", "Flask", "Spring Boot", "Laravel",
    "Machine Learning", "Data Science", "DevOps", "Cloud Computing", "Mobile Development",
    "Web Development", "Database Design", "Cybersecurity", "Blockchain", "IoT"
  ];

  const experienceLevels = [
    "1-2 years", "3-5 years", "6-8 years", "9-12 years", "13+ years"
  ];

  const educationLevels = [
    "High School", "Bachelor's Degree", "Master's Degree", "PhD", "Self-taught", "Bootcamp"
  ];

  const calculateCompletionRate = () => {
    let completed = 0;
    let total = 0;

    // Personal Info (7 fields)
    total += 7;
    if (formData.firstName) completed++;
    if (formData.lastName) completed++;
    if (formData.displayName) completed++;
    if (formData.email) completed++;
    if (formData.phone) completed++;
    if (formData.location) completed++;
    if (formData.bio) completed++;

    // Professional Info (10 fields)
    total += 10;
    if (formData.currentRole) completed++;
    if (formData.company) completed++;
    if (formData.experience) completed++;
    if (formData.expertise.length > 0) completed++;
    if (formData.education) completed++;
    if (formData.certifications.length > 0) completed++;
    if (formData.linkedinUrl) completed++;
    if (formData.githubUrl) completed++;
    if (formData.portfolioUrl) completed++;
    if (formData.resumeFile) completed++;

    // Account Security (5 fields)
    total += 5;
    if (formData.password) completed++;
    if (formData.confirmPassword) completed++;
    if (formData.agreeToTerms) completed++;
    if (formData.agreeToPrivacy) completed++;
    if (formData.agreeToMentorGuidelines) completed++;

    return Math.round((completed / total) * 100);
  };

  const updateFormData = (field: keyof MentorFormData, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleNext = () => {
    if (currentStep < 3) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = async () => {
    // Here you would submit the form data to your backend
    console.log('Submitting mentor application:', formData);
    // Add API call here
  };

  // Update completion rate whenever form data changes
  useEffect(() => {
    setCompletionRate(calculateCompletionRate());
  }, [formData]);

  const renderPersonalInfo = () => (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      className="space-y-6"
    >
      <div className="space-y-4">
        <div>
          <Label htmlFor="firstName" className="text-base font-medium">
            Full Name <span className="text-muted-foreground">(Private)</span>
          </Label>
          <div className="grid grid-cols-2 gap-4 mt-2">
            <Input
              id="firstName"
              placeholder="First Name"
              value={formData.firstName}
              onChange={(e) => updateFormData('firstName', e.target.value)}
              className="bg-card/60 border-primary/20"
            />
            <Input
              id="lastName"
              placeholder="Last Name"
              value={formData.lastName}
              onChange={(e) => updateFormData('lastName', e.target.value)}
              className="bg-card/60 border-primary/20"
            />
          </div>
        </div>

        <div>
          <Label htmlFor="displayName" className="text-base font-medium">
            Display Name <span className="text-red-500">*</span>
          </Label>
          <Input
            id="displayName"
            placeholder="Type your display name"
            value={formData.displayName}
            onChange={(e) => updateFormData('displayName', e.target.value)}
            className="mt-2 bg-card/60 border-primary/20"
          />
          <p className="text-sm text-muted-foreground mt-1">
            This is how you'll appear to potential mentees
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Label htmlFor="email" className="text-base font-medium">
              Email Address <span className="text-red-500">*</span>
            </Label>
            <Input
              id="email"
              type="email"
              placeholder="your.email@example.com"
              value={formData.email}
              onChange={(e) => updateFormData('email', e.target.value)}
              className="mt-2 bg-card/60 border-primary/20"
            />
          </div>

          <div>
            <Label htmlFor="phone" className="text-base font-medium">
              Phone Number
            </Label>
            <Input
              id="phone"
              type="tel"
              placeholder="+91 98765 43210"
              value={formData.phone}
              onChange={(e) => updateFormData('phone', e.target.value)}
              className="mt-2 bg-card/60 border-primary/20"
            />
          </div>
        </div>

        <div>
          <Label htmlFor="location" className="text-base font-medium">
            Location
          </Label>
          <Input
            id="location"
            placeholder="City, State"
            value={formData.location}
            onChange={(e) => updateFormData('location', e.target.value)}
            className="mt-2 bg-card/60 border-primary/20"
          />
        </div>

        <div>
          <Label htmlFor="bio" className="text-base font-medium">
            Bio <span className="text-red-500">*</span>
          </Label>
          <Textarea
            id="bio"
            placeholder="Tell us about yourself, your passion for mentoring, and what makes you unique..."
            value={formData.bio}
            onChange={(e) => updateFormData('bio', e.target.value)}
            className="mt-2 bg-card/60 border-primary/20 min-h-[120px]"
          />
          <p className="text-sm text-muted-foreground mt-1">
            This will appear on your public profile
          </p>
        </div>
      </div>
    </motion.div>
  );

  const renderProfessionalInfo = () => (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      className="space-y-6"
    >
      <div className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Label htmlFor="currentRole" className="text-base font-medium">
              Current Role <span className="text-red-500">*</span>
            </Label>
            <Input
              id="currentRole"
              placeholder="e.g., Senior Software Engineer"
              value={formData.currentRole}
              onChange={(e) => updateFormData('currentRole', e.target.value)}
              className="mt-2 bg-card/60 border-primary/20"
            />
          </div>

          <div>
            <Label htmlFor="company" className="text-base font-medium">
              Company <span className="text-red-500">*</span>
            </Label>
            <Input
              id="company"
              placeholder="e.g., Google, Microsoft, TCS"
              value={formData.company}
              onChange={(e) => updateFormData('company', e.target.value)}
              className="mt-2 bg-card/60 border-primary/20"
            />
          </div>
        </div>

        <div>
          <Label htmlFor="experience" className="text-base font-medium">
            Years of Experience <span className="text-red-500">*</span>
          </Label>
          <Select value={formData.experience} onValueChange={(value) => updateFormData('experience', value)}>
            <SelectTrigger className="mt-2 bg-card/60 border-primary/20">
              <SelectValue placeholder="Select experience level" />
            </SelectTrigger>
            <SelectContent>
              {experienceLevels.map((level) => (
                <SelectItem key={level} value={level}>
                  {level}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div>
          <Label className="text-base font-medium">
            Areas of Expertise <span className="text-red-500">*</span>
          </Label>
          <div className="mt-2 grid grid-cols-2 md:grid-cols-3 gap-2">
            {techCategories.map((category) => (
              <div key={category} className="flex items-center space-x-2">
                <Checkbox
                  id={category}
                  checked={formData.expertise.includes(category)}
                  onCheckedChange={(checked) => {
                    if (checked) {
                      updateFormData('expertise', [...formData.expertise, category]);
                    } else {
                      updateFormData('expertise', formData.expertise.filter(e => e !== category));
                    }
                  }}
                />
                <Label htmlFor={category} className="text-sm cursor-pointer">
                  {category}
                </Label>
              </div>
            ))}
          </div>
        </div>

        <div>
          <Label htmlFor="education" className="text-base font-medium">
            Education
          </Label>
          <Select value={formData.education} onValueChange={(value) => updateFormData('education', value)}>
            <SelectTrigger className="mt-2 bg-card/60 border-primary/20">
              <SelectValue placeholder="Select education level" />
            </SelectTrigger>
            <SelectContent>
              {educationLevels.map((level) => (
                <SelectItem key={level} value={level}>
                  {level}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div>
          <Label className="text-base font-medium">
            Certifications
          </Label>
          <div className="mt-2 space-y-2">
            {formData.certifications.map((cert, index) => (
              <div key={index} className="flex gap-2">
                <Input
                  placeholder="e.g., AWS Certified Solutions Architect"
                  value={cert}
                  onChange={(e) => {
                    const newCerts = [...formData.certifications];
                    newCerts[index] = e.target.value;
                    updateFormData('certifications', newCerts);
                  }}
                  className="bg-card/60 border-primary/20"
                />
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    updateFormData('certifications', formData.certifications.filter((_, i) => i !== index));
                  }}
                >
                  Remove
                </Button>
              </div>
            ))}
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                updateFormData('certifications', [...formData.certifications, '']);
              }}
            >
              Add Certification
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <Label htmlFor="linkedinUrl" className="text-base font-medium">
              LinkedIn Profile
            </Label>
            <Input
              id="linkedinUrl"
              type="url"
              placeholder="https://linkedin.com/in/yourprofile"
              value={formData.linkedinUrl}
              onChange={(e) => updateFormData('linkedinUrl', e.target.value)}
              className="mt-2 bg-card/60 border-primary/20"
            />
          </div>

          <div>
            <Label htmlFor="githubUrl" className="text-base font-medium">
              GitHub Profile
            </Label>
            <Input
              id="githubUrl"
              type="url"
              placeholder="https://github.com/yourusername"
              value={formData.githubUrl}
              onChange={(e) => updateFormData('githubUrl', e.target.value)}
              className="mt-2 bg-card/60 border-primary/20"
            />
          </div>

          <div>
            <Label htmlFor="portfolioUrl" className="text-base font-medium">
              Portfolio Website
            </Label>
            <Input
              id="portfolioUrl"
              type="url"
              placeholder="https://yourportfolio.com"
              value={formData.portfolioUrl}
              onChange={(e) => updateFormData('portfolioUrl', e.target.value)}
              className="mt-2 bg-card/60 border-primary/20"
            />
          </div>
        </div>

        <div>
          <Label htmlFor="resume" className="text-base font-medium">
            Resume/CV
          </Label>
          <div className="mt-2">
            <Input
              id="resume"
              type="file"
              accept=".pdf,.doc,.docx"
              onChange={(e) => updateFormData('resumeFile', e.target.files?.[0] || null)}
              className="bg-card/60 border-primary/20"
            />
            <p className="text-sm text-muted-foreground mt-1">
              Upload your resume (PDF, DOC, DOCX) - Max 5MB
            </p>
          </div>
        </div>
      </div>
    </motion.div>
  );

  const renderAccountSecurity = () => (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      className="space-y-6"
    >
      <div className="space-y-4">
        <div>
          <Label htmlFor="password" className="text-base font-medium">
            Password <span className="text-red-500">*</span>
          </Label>
          <div className="relative mt-2">
            <Input
              id="password"
              type={showPassword ? "text" : "password"}
              placeholder="Create a strong password"
              value={formData.password}
              onChange={(e) => updateFormData('password', e.target.value)}
              className="bg-card/60 border-primary/20 pr-10"
            />
            <Button
              type="button"
              variant="ghost"
              size="sm"
              className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
            </Button>
          </div>
          <p className="text-sm text-muted-foreground mt-1">
            Must be at least 8 characters with uppercase, lowercase, number, and special character
          </p>
        </div>

        <div>
          <Label htmlFor="confirmPassword" className="text-base font-medium">
            Confirm Password <span className="text-red-500">*</span>
          </Label>
          <div className="relative mt-2">
            <Input
              id="confirmPassword"
              type={showConfirmPassword ? "text" : "password"}
              placeholder="Confirm your password"
              value={formData.confirmPassword}
              onChange={(e) => updateFormData('confirmPassword', e.target.value)}
              className="bg-card/60 border-primary/20 pr-10"
            />
            <Button
              type="button"
              variant="ghost"
              size="sm"
              className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            >
              {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
            </Button>
          </div>
        </div>

        <div className="space-y-4 pt-4">
          <div className="flex items-start space-x-3">
            <Checkbox
              id="terms"
              checked={formData.agreeToTerms}
              onCheckedChange={(checked) => updateFormData('agreeToTerms', checked)}
            />
            <Label htmlFor="terms" className="text-sm leading-relaxed cursor-pointer">
              I agree to the <a href="#" className="text-primary hover:underline">Terms of Service</a> and 
              <a href="#" className="text-primary hover:underline"> Community Guidelines</a>
            </Label>
          </div>

          <div className="flex items-start space-x-3">
            <Checkbox
              id="privacy"
              checked={formData.agreeToPrivacy}
              onCheckedChange={(checked) => updateFormData('agreeToPrivacy', checked)}
            />
            <Label htmlFor="privacy" className="text-sm leading-relaxed cursor-pointer">
              I agree to the <a href="#" className="text-primary hover:underline">Privacy Policy</a> and 
              consent to the processing of my personal data
            </Label>
          </div>

          <div className="flex items-start space-x-3">
            <Checkbox
              id="guidelines"
              checked={formData.agreeToMentorGuidelines}
              onCheckedChange={(checked) => updateFormData('agreeToMentorGuidelines', checked)}
            />
            <Label htmlFor="guidelines" className="text-sm leading-relaxed cursor-pointer">
              I agree to follow the <a href="#" className="text-primary hover:underline">Mentor Guidelines</a> 
              and commit to providing quality mentorship
            </Label>
          </div>
        </div>
      </div>
    </motion.div>
  );

  return (
    <div className="min-h-screen bg-gradient-bg">
      <div className="min-h-screen max-w-screen-2xl mx-auto px-4 sm:px-6 lg:px-8 
                    m-4 sm:m-6 lg:m-10 bg-gradient-bg border border-blue-300 rounded-3xl overflow-hidden bg-gradient-to-b from-slate-100 to-cyan-50
                    animate-fade-in mt-20" style={{ marginTop: '5rem' }}>
        
        {/* Header */}
        <div className="bg-white/80 backdrop-blur-sm border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                <Award className="w-4 h-4 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-semibold text-gray-900">Become a Mentor</h1>
                <p className="text-sm text-gray-600">Join our community of tech experts</p>
              </div>
            </div>
            <div className="text-right">
              <div className="text-sm font-medium text-gray-900">Completion Rate: {completionRate}%</div>
              <div className="w-32 h-2 bg-gray-200 rounded-full mt-1">
                <div 
                  className="h-2 bg-primary rounded-full transition-all duration-300"
                  style={{ width: `${completionRate}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>

        {/* Progress Steps */}
        <div className="bg-white/60 backdrop-blur-sm border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-center space-x-8">
            {steps.map((step, index) => (
              <div key={step.id} className="flex items-center space-x-4">
                <div className={`flex items-center justify-center w-10 h-10 rounded-full border-2 transition-all duration-300 ${
                  currentStep >= step.id 
                    ? 'bg-primary border-primary text-white' 
                    : 'bg-white border-gray-300 text-gray-500'
                }`}>
                  {currentStep > step.id ? (
                    <CheckCircle className="w-5 h-5" />
                  ) : (
                    <step.icon className="w-5 h-5" />
                  )}
                </div>
                <div className="hidden md:block">
                  <div className={`text-sm font-medium ${
                    currentStep >= step.id ? 'text-gray-900' : 'text-gray-500'
                  }`}>
                    {step.title}
                  </div>
                  <div className="text-xs text-gray-500">{step.description}</div>
                </div>
                {index < steps.length - 1 && (
                  <div className={`w-8 h-0.5 ${
                    currentStep > step.id ? 'bg-primary' : 'bg-gray-300'
                  }`}></div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 p-6">
          <div className="max-w-4xl mx-auto">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                {steps[currentStep - 1].title}
              </h2>
              <p className="text-gray-600">
                {steps[currentStep - 1].description}
              </p>
            </div>

            <Card className="bg-white/80 backdrop-blur-sm border-gray-200">
              <CardContent className="p-6">
                <AnimatePresence mode="wait">
                  {currentStep === 1 && renderPersonalInfo()}
                  {currentStep === 2 && renderProfessionalInfo()}
                  {currentStep === 3 && renderAccountSecurity()}
                </AnimatePresence>
              </CardContent>
            </Card>

            {/* Navigation Buttons */}
            <div className="flex justify-between mt-6">
              <Button
                variant="outline"
                onClick={handlePrevious}
                disabled={currentStep === 1}
                className="flex items-center space-x-2"
              >
                <ArrowLeft className="w-4 h-4" />
                Previous
              </Button>

              {currentStep < 3 ? (
                <Button
                  onClick={handleNext}
                  className="flex items-center space-x-2"
                >
                  Next
                  <ArrowRight className="w-4 h-4" />
                </Button>
              ) : (
                <Button
                  onClick={handleSubmit}
                  className="flex items-center space-x-2"
                  disabled={completionRate < 100}
                >
                  Submit Application
                  <CheckCircle className="w-4 h-4" />
                </Button>
              )}
            </div>

            {/* Mandatory Fields Note */}
            <div className="text-right mt-4">
              <span className="text-sm text-gray-500">* Mandatory fields</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BecomeMentor;
