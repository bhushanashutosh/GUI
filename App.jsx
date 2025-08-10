import { useState, useEffect, createContext, useContext } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Separator } from '@/components/ui/separator.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { 
  Users, 
  TrendingUp, 
  DollarSign, 
  Star, 
  Search, 
  Filter, 
  Plus, 
  Settings, 
  LogOut,
  BarChart3,
  MessageSquare,
  Bell,
  Eye,
  Heart,
  Share2,
  Calendar,
  MapPin,
  Globe,
  Instagram,
  Youtube,
  Twitter,
  Facebook,
  Send,
  CheckCircle,
  Clock,
  AlertCircle,
  Target,
  Zap,
  Briefcase,
  Award,
  TrendingDown,
  Activity
} from 'lucide-react'
import { LineChart, Line, AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import './App.css'

// Context for authentication and user state
const AuthContext = createContext()

// Mock data for demonstration
const mockInfluencers = [
  {
    id: '1',
    name: 'Sarah Johnson',
    bio: 'Fashion & Lifestyle Influencer',
    location: 'New York, USA',
    verified: true,
    overall_rating: 4.8,
    total_reviews: 127,
    max_followers: 250000,
    niches: ['fashion', 'beauty', 'lifestyle'],
    social_accounts: [
      { platform: 'instagram', username: '@sarahjohnson', follower_count: 250000, engagement_rate: 0.045 },
      { platform: 'youtube', username: 'SarahJohnsonVlogs', follower_count: 85000, engagement_rate: 0.032 }
    ]
  },
  {
    id: '2',
    name: 'Mike Chen',
    bio: 'Tech Reviewer & Gaming Content Creator',
    location: 'San Francisco, USA',
    verified: true,
    overall_rating: 4.6,
    total_reviews: 89,
    max_followers: 180000,
    niches: ['tech', 'gaming'],
    social_accounts: [
      { platform: 'youtube', username: 'TechWithMike', follower_count: 180000, engagement_rate: 0.038 },
      { platform: 'twitter', username: '@mikechentech', follower_count: 45000, engagement_rate: 0.025 }
    ]
  }
]

const mockCampaigns = [
  {
    id: '1',
    title: 'Summer Fashion Collection Launch',
    description: 'Promote our new summer collection with authentic styling content',
    budget_min: 1000,
    budget_max: 5000,
    campaign_type: 'custom',
    target_platforms: ['instagram', 'youtube'],
    deadline: '2024-03-15',
    brand_name: 'StyleCo Fashion'
  },
  {
    id: '2',
    title: 'Gaming Headset Review',
    description: 'Create honest review content for our new gaming headset',
    budget_min: 500,
    budget_max: 2000,
    campaign_type: 'custom',
    target_platforms: ['youtube', 'twitter'],
    deadline: '2024-03-20',
    brand_name: 'AudioTech Gaming'
  }
]

const mockAnalyticsData = [
  { month: 'Jan', followers: 45000, engagement: 3.2, earnings: 1200 },
  { month: 'Feb', followers: 52000, engagement: 3.8, earnings: 1800 },
  { month: 'Mar', followers: 58000, engagement: 4.2, earnings: 2400 },
  { month: 'Apr', followers: 65000, engagement: 4.5, earnings: 3200 },
  { month: 'May', followers: 72000, engagement: 4.1, earnings: 2800 },
  { month: 'Jun', followers: 78000, engagement: 4.7, earnings: 3600 }
]

// Authentication component
function AuthPage() {
  const [isLogin, setIsLogin] = useState(true)
  const [userType, setUserType] = useState('influencer')
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: ''
  })
  const { login } = useContext(AuthContext)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    // Mock authentication
    const mockUser = {
      id: '1',
      email: formData.email,
      user_type: userType,
      name: formData.name || 'Demo User'
    }
    login(mockUser)
    navigate('/dashboard')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-bold text-gray-900">
            {isLogin ? 'Welcome Back' : 'Join the Platform'}
          </CardTitle>
          <CardDescription>
            {isLogin ? 'Sign in to your account' : 'Create your account to get started'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && (
              <div className="space-y-2">
                <Label htmlFor="name">Full Name</Label>
                <Input
                  id="name"
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  required={!isLogin}
                />
              </div>
            )}
            
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                required
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                required
              />
            </div>

            {!isLogin && (
              <div className="space-y-2">
                <Label>Account Type</Label>
                <Select value={userType} onValueChange={setUserType}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="influencer">Influencer</SelectItem>
                    <SelectItem value="brand">Brand</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            )}

            <Button type="submit" className="w-full">
              {isLogin ? 'Sign In' : 'Create Account'}
            </Button>
          </form>

          <div className="mt-4 text-center">
            <button
              type="button"
              onClick={() => setIsLogin(!isLogin)}
              className="text-sm text-blue-600 hover:underline"
            >
              {isLogin ? "Don't have an account? Sign up" : "Already have an account? Sign in"}
            </button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

// Dashboard Layout Component
function DashboardLayout({ children, user }) {
  const { logout } = useContext(AuthContext)
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState('overview')

  const handleLogout = () => {
    logout()
    navigate('/auth')
  }

  const influencerTabs = [
    { id: 'overview', label: 'Overview', icon: BarChart3 },
    { id: 'campaigns', label: 'Campaigns', icon: Target },
    { id: 'analytics', label: 'Analytics', icon: TrendingUp },
    { id: 'profile', label: 'Profile', icon: Settings },
    { id: 'collaborations', label: 'Collaborations', icon: Briefcase }
  ]

  const brandTabs = [
    { id: 'overview', label: 'Overview', icon: BarChart3 },
    { id: 'discovery', label: 'Discovery', icon: Search },
    { id: 'campaigns', label: 'My Campaigns', icon: Target },
    { id: 'analytics', label: 'Analytics', icon: TrendingUp },
    { id: 'profile', label: 'Profile', icon: Settings }
  ]

  const tabs = user.user_type === 'influencer' ? influencerTabs : brandTabs

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h1 className="text-2xl font-bold text-gray-900">
              Influencer Platform
            </h1>
            <Badge variant="secondary" className="capitalize">
              {user.user_type}
            </Badge>
          </div>
          
          <div className="flex items-center space-x-4">
            <Button variant="ghost" size="sm">
              <Bell className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm">
              <MessageSquare className="h-4 w-4" />
            </Button>
            <div className="flex items-center space-x-2">
              <Avatar className="h-8 w-8">
                <AvatarFallback>{user.name?.charAt(0) || 'U'}</AvatarFallback>
              </Avatar>
              <span className="text-sm font-medium">{user.name}</span>
            </div>
            <Button variant="ghost" size="sm" onClick={handleLogout}>
              <LogOut className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200 px-6">
        <div className="flex space-x-8">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 py-4 px-2 border-b-2 text-sm font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Icon className="h-4 w-4" />
                <span>{tab.label}</span>
              </button>
            )
          })}
        </div>
      </nav>

      {/* Main Content */}
      <main className="p-6">
        {user.user_type === 'influencer' ? (
          <InfluencerDashboard activeTab={activeTab} user={user} />
        ) : (
          <BrandDashboard activeTab={activeTab} user={user} />
        )}
      </main>
    </div>
  )
}

// Influencer Dashboard Component
function InfluencerDashboard({ activeTab, user }) {
  const [profile, setProfile] = useState({
    name: user.name,
    bio: 'Content creator passionate about lifestyle and fashion',
    location: 'New York, USA',
    workload_preference: 'moderate',
    income_goals: '$5000/month',
    growth_aspirations: 'Reach 100K followers'
  })

  const [socialAccounts, setSocialAccounts] = useState([
    { platform: 'instagram', username: '@demo_user', follower_count: 25000, engagement_rate: 0.045 },
    { platform: 'youtube', username: 'DemoChannel', follower_count: 8500, engagement_rate: 0.032 }
  ])

  const renderOverview = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Followers</p>
                <p className="text-2xl font-bold text-gray-900">33.5K</p>
              </div>
              <Users className="h-8 w-8 text-blue-500" />
            </div>
            <div className="mt-2 flex items-center text-sm">
              <TrendingUp className="h-4 w-4 text-green-500 mr-1" />
              <span className="text-green-600">+12% from last month</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Avg Engagement</p>
                <p className="text-2xl font-bold text-gray-900">4.2%</p>
              </div>
              <Heart className="h-8 w-8 text-red-500" />
            </div>
            <div className="mt-2 flex items-center text-sm">
              <TrendingUp className="h-4 w-4 text-green-500 mr-1" />
              <span className="text-green-600">+0.3% from last month</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Monthly Earnings</p>
                <p className="text-2xl font-bold text-gray-900">$3,600</p>
              </div>
              <DollarSign className="h-8 w-8 text-green-500" />
            </div>
            <div className="mt-2 flex items-center text-sm">
              <TrendingUp className="h-4 w-4 text-green-500 mr-1" />
              <span className="text-green-600">+28% from last month</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Rating</p>
                <p className="text-2xl font-bold text-gray-900">4.8</p>
              </div>
              <Star className="h-8 w-8 text-yellow-500" />
            </div>
            <div className="mt-2 flex items-center text-sm">
              <span className="text-gray-600">Based on 47 reviews</span>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Growth Analytics</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={mockAnalyticsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="followers" stroke="#3b82f6" strokeWidth={2} />
                <Line type="monotone" dataKey="engagement" stroke="#ef4444" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <div className="flex-1">
                  <p className="text-sm font-medium">Collaboration completed</p>
                  <p className="text-xs text-gray-500">StyleCo Fashion campaign - $2,500 earned</p>
                </div>
                <span className="text-xs text-gray-400">2h ago</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <div className="flex-1">
                  <p className="text-sm font-medium">New campaign invitation</p>
                  <p className="text-xs text-gray-500">TechGear wants to collaborate</p>
                </div>
                <span className="text-xs text-gray-400">5h ago</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                <div className="flex-1">
                  <p className="text-sm font-medium">Payment received</p>
                  <p className="text-xs text-gray-500">$1,200 from FashionBrand Inc.</p>
                </div>
                <span className="text-xs text-gray-400">1d ago</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )

  const renderCampaigns = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">Available Campaigns</h2>
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm">
            <Filter className="h-4 w-4 mr-2" />
            Filter
          </Button>
          <Button variant="outline" size="sm">
            <Search className="h-4 w-4 mr-2" />
            Search
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockCampaigns.map((campaign) => (
          <Card key={campaign.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-center justify-between">
                <Badge variant="secondary">{campaign.campaign_type}</Badge>
                <span className="text-sm text-gray-500">{campaign.brand_name}</span>
              </div>
              <CardTitle className="text-lg">{campaign.title}</CardTitle>
              <CardDescription>{campaign.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Budget:</span>
                  <span className="font-medium">${campaign.budget_min} - ${campaign.budget_max}</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Deadline:</span>
                  <span className="font-medium">{campaign.deadline}</span>
                </div>
                <div className="flex flex-wrap gap-1">
                  {campaign.target_platforms.map((platform) => (
                    <Badge key={platform} variant="outline" className="text-xs">
                      {platform}
                    </Badge>
                  ))}
                </div>
                <div className="flex space-x-2 pt-2">
                  <Button size="sm" className="flex-1">Apply Now</Button>
                  <Button variant="outline" size="sm">
                    <Eye className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Generic Campaigns - Quick Earnings</CardTitle>
          <CardDescription>Join these campaigns with one click for instant monetization</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 border rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-medium">Crypto Promotion</h4>
                <Badge>$0.05/engagement</Badge>
              </div>
              <p className="text-sm text-gray-600 mb-3">Promote cryptocurrency platforms</p>
              <Button size="sm" className="w-full">
                <Zap className="h-4 w-4 mr-2" />
                Join Campaign
              </Button>
            </div>
            <div className="p-4 border rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-medium">E-commerce Deals</h4>
                <Badge>$0.02/engagement</Badge>
              </div>
              <p className="text-sm text-gray-600 mb-3">Share shopping deals and discounts</p>
              <Button size="sm" className="w-full">
                <Zap className="h-4 w-4 mr-2" />
                Join Campaign
              </Button>
            </div>
            <div className="p-4 border rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-medium">App Downloads</h4>
                <Badge>$0.08/engagement</Badge>
              </div>
              <p className="text-sm text-gray-600 mb-3">Promote mobile app downloads</p>
              <Button size="sm" className="w-full">
                <Zap className="h-4 w-4 mr-2" />
                Join Campaign
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  const renderAnalytics = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Analytics Dashboard</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Follower Growth</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={mockAnalyticsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Area type="monotone" dataKey="followers" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.3} />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Earnings Trend</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={mockAnalyticsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="earnings" fill="#10b981" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Account Health</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Fake Followers</span>
                  <span>2.3%</span>
                </div>
                <Progress value={2.3} className="h-2" />
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Engagement Quality</span>
                  <span>87%</span>
                </div>
                <Progress value={87} className="h-2" />
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Growth Rate</span>
                  <span>12%</span>
                </div>
                <Progress value={12} className="h-2" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Platform Performance</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Instagram className="h-4 w-4 text-pink-500" />
                  <span className="text-sm">Instagram</span>
                </div>
                <span className="text-sm font-medium">4.5%</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Youtube className="h-4 w-4 text-red-500" />
                  <span className="text-sm">YouTube</span>
                </div>
                <span className="text-sm font-medium">3.2%</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Twitter className="h-4 w-4 text-blue-500" />
                  <span className="text-sm">Twitter</span>
                </div>
                <span className="text-sm font-medium">2.8%</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>AI Insights</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <Alert>
                <Activity className="h-4 w-4" />
                <AlertDescription className="text-sm">
                  Your engagement rate is 15% above average for your niche.
                </AlertDescription>
              </Alert>
              <Alert>
                <TrendingUp className="h-4 w-4" />
                <AlertDescription className="text-sm">
                  Consider posting more video content to boost growth.
                </AlertDescription>
              </Alert>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )

  const renderProfile = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Profile Settings</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Basic Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="name">Full Name</Label>
              <Input
                id="name"
                value={profile.name}
                onChange={(e) => setProfile({...profile, name: e.target.value})}
              />
            </div>
            <div>
              <Label htmlFor="bio">Bio</Label>
              <Textarea
                id="bio"
                value={profile.bio}
                onChange={(e) => setProfile({...profile, bio: e.target.value})}
                rows={3}
              />
            </div>
            <div>
              <Label htmlFor="location">Location</Label>
              <Input
                id="location"
                value={profile.location}
                onChange={(e) => setProfile({...profile, location: e.target.value})}
              />
            </div>
            <Button>Save Changes</Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Preferences</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label>Workload Preference</Label>
              <Select value={profile.workload_preference} onValueChange={(value) => setProfile({...profile, workload_preference: value})}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="light">Light (1-2 campaigns/month)</SelectItem>
                  <SelectItem value="moderate">Moderate (3-5 campaigns/month)</SelectItem>
                  <SelectItem value="heavy">Heavy (6+ campaigns/month)</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="income_goals">Income Goals</Label>
              <Input
                id="income_goals"
                value={profile.income_goals}
                onChange={(e) => setProfile({...profile, income_goals: e.target.value})}
              />
            </div>
            <div>
              <Label htmlFor="growth_aspirations">Growth Aspirations</Label>
              <Textarea
                id="growth_aspirations"
                value={profile.growth_aspirations}
                onChange={(e) => setProfile({...profile, growth_aspirations: e.target.value})}
                rows={2}
              />
            </div>
            <Button>Update Preferences</Button>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Social Media Accounts</CardTitle>
          <CardDescription>Manage your connected social media platforms</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {socialAccounts.map((account, index) => (
              <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center space-x-3">
                  {account.platform === 'instagram' && <Instagram className="h-5 w-5 text-pink-500" />}
                  {account.platform === 'youtube' && <Youtube className="h-5 w-5 text-red-500" />}
                  {account.platform === 'twitter' && <Twitter className="h-5 w-5 text-blue-500" />}
                  {account.platform === 'facebook' && <Facebook className="h-5 w-5 text-blue-600" />}
                  <div>
                    <p className="font-medium capitalize">{account.platform}</p>
                    <p className="text-sm text-gray-500">{account.username}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-medium">{account.follower_count.toLocaleString()}</p>
                  <p className="text-sm text-gray-500">{(account.engagement_rate * 100).toFixed(1)}% engagement</p>
                </div>
              </div>
            ))}
            <Button variant="outline" className="w-full">
              <Plus className="h-4 w-4 mr-2" />
              Add Social Account
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  const renderCollaborations = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">My Collaborations</h2>
      
      <Tabs defaultValue="active" className="w-full">
        <TabsList>
          <TabsTrigger value="active">Active</TabsTrigger>
          <TabsTrigger value="pending">Pending</TabsTrigger>
          <TabsTrigger value="completed">Completed</TabsTrigger>
        </TabsList>
        
        <TabsContent value="active" className="space-y-4">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="font-semibold">Summer Fashion Collection</h3>
                  <p className="text-sm text-gray-600">StyleCo Fashion</p>
                </div>
                <Badge>In Progress</Badge>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div>
                  <p className="text-sm text-gray-600">Budget</p>
                  <p className="font-medium">$2,500</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Deadline</p>
                  <p className="font-medium">March 15, 2024</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Deliverables</p>
                  <p className="font-medium">3 Instagram posts, 1 Story</p>
                </div>
              </div>
              <div className="flex space-x-2">
                <Button size="sm">Upload Content</Button>
                <Button variant="outline" size="sm">
                  <MessageSquare className="h-4 w-4 mr-2" />
                  Message Brand
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="pending" className="space-y-4">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="font-semibold">Gaming Headset Review</h3>
                  <p className="text-sm text-gray-600">AudioTech Gaming</p>
                </div>
                <Badge variant="secondary">Pending</Badge>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div>
                  <p className="text-sm text-gray-600">Proposed Budget</p>
                  <p className="font-medium">$1,200</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Deadline</p>
                  <p className="font-medium">March 20, 2024</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Platform</p>
                  <p className="font-medium">YouTube</p>
                </div>
              </div>
              <div className="flex space-x-2">
                <Button size="sm">Accept</Button>
                <Button variant="outline" size="sm">Negotiate</Button>
                <Button variant="destructive" size="sm">Decline</Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="completed" className="space-y-4">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="font-semibold">Tech Product Launch</h3>
                  <p className="text-sm text-gray-600">TechCorp Inc.</p>
                </div>
                <Badge variant="outline">Completed</Badge>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                <div>
                  <p className="text-sm text-gray-600">Earned</p>
                  <p className="font-medium">$1,800</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Completed</p>
                  <p className="font-medium">Feb 28, 2024</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Rating Given</p>
                  <div className="flex items-center">
                    <Star className="h-4 w-4 text-yellow-500 fill-current" />
                    <span className="ml-1 font-medium">4.8</span>
                  </div>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Payment</p>
                  <p className="font-medium text-green-600">Received</p>
                </div>
              </div>
              <Button variant="outline" size="sm">View Details</Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )

  switch (activeTab) {
    case 'overview':
      return renderOverview()
    case 'campaigns':
      return renderCampaigns()
    case 'analytics':
      return renderAnalytics()
    case 'profile':
      return renderProfile()
    case 'collaborations':
      return renderCollaborations()
    default:
      return renderOverview()
  }
}

// Brand Dashboard Component
function BrandDashboard({ activeTab, user }) {
  const renderOverview = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Active Campaigns</p>
                <p className="text-2xl font-bold text-gray-900">8</p>
              </div>
              <Target className="h-8 w-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Reach</p>
                <p className="text-2xl font-bold text-gray-900">2.4M</p>
              </div>
              <Users className="h-8 w-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Campaign ROI</p>
                <p className="text-2xl font-bold text-gray-900">340%</p>
              </div>
              <TrendingUp className="h-8 w-8 text-purple-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Monthly Spend</p>
                <p className="text-2xl font-bold text-gray-900">$24.5K</p>
              </div>
              <DollarSign className="h-8 w-8 text-orange-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Campaign Performance</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={mockAnalyticsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="earnings" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Top Performing Influencers</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {mockInfluencers.slice(0, 3).map((influencer) => (
                <div key={influencer.id} className="flex items-center space-x-3">
                  <Avatar>
                    <AvatarFallback>{influencer.name.charAt(0)}</AvatarFallback>
                  </Avatar>
                  <div className="flex-1">
                    <p className="font-medium">{influencer.name}</p>
                    <p className="text-sm text-gray-500">{influencer.max_followers.toLocaleString()} followers</p>
                  </div>
                  <div className="text-right">
                    <div className="flex items-center">
                      <Star className="h-4 w-4 text-yellow-500 fill-current" />
                      <span className="ml-1 text-sm font-medium">{influencer.overall_rating}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )

  const renderDiscovery = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">Discover Influencers</h2>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Create Campaign
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Advanced Filters</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <Label>Niche</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select niche" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="fashion">Fashion</SelectItem>
                  <SelectItem value="tech">Technology</SelectItem>
                  <SelectItem value="beauty">Beauty</SelectItem>
                  <SelectItem value="fitness">Fitness</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Platform</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select platform" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="instagram">Instagram</SelectItem>
                  <SelectItem value="youtube">YouTube</SelectItem>
                  <SelectItem value="twitter">Twitter</SelectItem>
                  <SelectItem value="facebook">Facebook</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Min Followers</Label>
              <Input type="number" placeholder="e.g., 10000" />
            </div>
            <div>
              <Label>Location</Label>
              <Input placeholder="e.g., New York" />
            </div>
          </div>
          <div className="flex space-x-2 mt-4">
            <Button>Apply Filters</Button>
            <Button variant="outline">Reset</Button>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockInfluencers.map((influencer) => (
          <Card key={influencer.id} className="hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center space-x-3 mb-4">
                <Avatar className="h-12 w-12">
                  <AvatarFallback>{influencer.name.charAt(0)}</AvatarFallback>
                </Avatar>
                <div className="flex-1">
                  <div className="flex items-center space-x-2">
                    <h3 className="font-semibold">{influencer.name}</h3>
                    {influencer.verified && <CheckCircle className="h-4 w-4 text-blue-500" />}
                  </div>
                  <p className="text-sm text-gray-600">{influencer.bio}</p>
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Followers:</span>
                  <span className="font-medium">{influencer.max_followers.toLocaleString()}</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Rating:</span>
                  <div className="flex items-center">
                    <Star className="h-4 w-4 text-yellow-500 fill-current" />
                    <span className="ml-1 font-medium">{influencer.overall_rating}</span>
                    <span className="text-gray-500 ml-1">({influencer.total_reviews})</span>
                  </div>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Location:</span>
                  <span className="font-medium">{influencer.location}</span>
                </div>

                <div className="flex flex-wrap gap-1">
                  {influencer.niches.map((niche) => (
                    <Badge key={niche} variant="secondary" className="text-xs">
                      {niche}
                    </Badge>
                  ))}
                </div>

                <div className="flex space-x-2 pt-2">
                  <Button size="sm" className="flex-1">Contact</Button>
                  <Button variant="outline" size="sm">
                    <Eye className="h-4 w-4" />
                  </Button>
                  <Button variant="outline" size="sm">
                    <Heart className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )

  const renderCampaigns = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">My Campaigns</h2>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Create New Campaign
        </Button>
      </div>

      <Tabs defaultValue="active" className="w-full">
        <TabsList>
          <TabsTrigger value="active">Active</TabsTrigger>
          <TabsTrigger value="draft">Draft</TabsTrigger>
          <TabsTrigger value="completed">Completed</TabsTrigger>
        </TabsList>
        
        <TabsContent value="active" className="space-y-4">
          {mockCampaigns.map((campaign) => (
            <Card key={campaign.id}>
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="font-semibold text-lg">{campaign.title}</h3>
                    <p className="text-gray-600">{campaign.description}</p>
                  </div>
                  <Badge>Active</Badge>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                  <div>
                    <p className="text-sm text-gray-600">Budget</p>
                    <p className="font-medium">${campaign.budget_min} - ${campaign.budget_max}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Applications</p>
                    <p className="font-medium">12 received</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Deadline</p>
                    <p className="font-medium">{campaign.deadline}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Status</p>
                    <p className="font-medium text-green-600">On Track</p>
                  </div>
                </div>

                <div className="flex space-x-2">
                  <Button size="sm">View Applications</Button>
                  <Button variant="outline" size="sm">Edit Campaign</Button>
                  <Button variant="outline" size="sm">Analytics</Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </TabsContent>
      </Tabs>
    </div>
  )

  const renderAnalytics = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Campaign Analytics</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>ROI Trends</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={mockAnalyticsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="earnings" stroke="#10b981" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Audience Demographics</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={[
                    { name: '18-24', value: 30, fill: '#3b82f6' },
                    { name: '25-34', value: 45, fill: '#10b981' },
                    { name: '35-44', value: 20, fill: '#f59e0b' },
                    { name: '45+', value: 5, fill: '#ef4444' }
                  ]}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="value"
                  label
                />
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  )

  const renderProfile = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Brand Profile</h2>
      
      <Card>
        <CardHeader>
          <CardTitle>Company Information</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="company_name">Company Name</Label>
              <Input id="company_name" defaultValue="Demo Brand Inc." />
            </div>
            <div>
              <Label htmlFor="website">Website</Label>
              <Input id="website" defaultValue="https://demobrand.com" />
            </div>
          </div>
          <div>
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              defaultValue="We are a leading fashion brand focused on sustainable and ethical clothing."
              rows={3}
            />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="location">Location</Label>
              <Input id="location" defaultValue="New York, USA" />
            </div>
            <div>
              <Label>Company Size</Label>
              <Select defaultValue="medium">
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="startup">Startup (1-10 employees)</SelectItem>
                  <SelectItem value="small">Small (11-50 employees)</SelectItem>
                  <SelectItem value="medium">Medium (51-200 employees)</SelectItem>
                  <SelectItem value="large">Large (201-1000 employees)</SelectItem>
                  <SelectItem value="enterprise">Enterprise (1000+ employees)</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <Button>Save Changes</Button>
        </CardContent>
      </Card>
    </div>
  )

  switch (activeTab) {
    case 'overview':
      return renderOverview()
    case 'discovery':
      return renderDiscovery()
    case 'campaigns':
      return renderCampaigns()
    case 'analytics':
      return renderAnalytics()
    case 'profile':
      return renderProfile()
    default:
      return renderOverview()
  }
}

// Main App Component
function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check for existing session
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      setUser(JSON.parse(savedUser))
    }
    setLoading(false)
  }, [])

  const login = (userData) => {
    setUser(userData)
    localStorage.setItem('user', JSON.stringify(userData))
  }

  const logout = () => {
    setUser(null)
    localStorage.removeItem('user')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      <Router>
        <div className="App">
          <Routes>
            <Route 
              path="/auth" 
              element={user ? <Navigate to="/dashboard" /> : <AuthPage />} 
            />
            <Route 
              path="/dashboard" 
              element={user ? <DashboardLayout user={user} /> : <Navigate to="/auth" />} 
            />
            <Route 
              path="/" 
              element={<Navigate to={user ? "/dashboard" : "/auth"} />} 
            />
          </Routes>
        </div>
      </Router>
    </AuthContext.Provider>
  )
}

export default App

