# Enhanced Backend Architecture Design

## Database Schema

### 1. Users Table (Base for both Influencers and Brands)
```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    user_type TEXT NOT NULL CHECK (user_type IN ('influencer', 'brand')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Influencers Table
```sql
CREATE TABLE influencers (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    name TEXT NOT NULL,
    bio TEXT,
    location TEXT,
    profile_image_url TEXT,
    verified BOOLEAN DEFAULT FALSE,
    overall_rating REAL DEFAULT 0.0,
    total_reviews INTEGER DEFAULT 0,
    workload_preference TEXT CHECK (workload_preference IN ('light', 'moderate', 'heavy')),
    income_goals TEXT,
    growth_aspirations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Social Media Accounts Table
```sql
CREATE TABLE social_media_accounts (
    id TEXT PRIMARY KEY,
    influencer_id TEXT NOT NULL REFERENCES influencers(id),
    platform TEXT NOT NULL CHECK (platform IN ('instagram', 'telegram', 'youtube', 'twitter', 'facebook')),
    username TEXT NOT NULL,
    follower_count INTEGER DEFAULT 0,
    engagement_rate REAL DEFAULT 0.0,
    verified BOOLEAN DEFAULT FALSE,
    url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Audience Demographics Table
```sql
CREATE TABLE audience_demographics (
    id TEXT PRIMARY KEY,
    influencer_id TEXT NOT NULL REFERENCES influencers(id),
    age_group TEXT NOT NULL,
    gender TEXT NOT NULL,
    location TEXT NOT NULL,
    percentage REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. Content Types Table
```sql
CREATE TABLE content_types (
    id TEXT PRIMARY KEY,
    influencer_id TEXT NOT NULL REFERENCES influencers(id),
    content_type TEXT NOT NULL CHECK (content_type IN ('stories', 'posts', 'reels', 'videos', 'live_streams')),
    avg_views INTEGER DEFAULT 0,
    avg_engagement REAL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6. Niches Table
```sql
CREATE TABLE niches (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);
```

### 7. Influencer Niches Table (Many-to-Many)
```sql
CREATE TABLE influencer_niches (
    influencer_id TEXT NOT NULL REFERENCES influencers(id),
    niche_id TEXT NOT NULL REFERENCES niches(id),
    PRIMARY KEY (influencer_id, niche_id)
);
```

### 8. Brands Table
```sql
CREATE TABLE brands (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    name TEXT NOT NULL,
    description TEXT,
    location TEXT,
    website_url TEXT,
    logo_url TEXT,
    company_size TEXT CHECK (company_size IN ('startup', 'small', 'medium', 'large', 'enterprise')),
    verified BOOLEAN DEFAULT FALSE,
    overall_rating REAL DEFAULT 0.0,
    total_reviews INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 9. Brand Niches Table (Many-to-Many)
```sql
CREATE TABLE brand_niches (
    brand_id TEXT NOT NULL REFERENCES brands(id),
    niche_id TEXT NOT NULL REFERENCES niches(id),
    PRIMARY KEY (brand_id, niche_id)
);
```

### 10. Campaigns Table
```sql
CREATE TABLE campaigns (
    id TEXT PRIMARY KEY,
    brand_id TEXT NOT NULL REFERENCES brands(id),
    title TEXT NOT NULL,
    description TEXT,
    budget_min REAL,
    budget_max REAL,
    campaign_type TEXT CHECK (campaign_type IN ('generic', 'custom', 'collaboration')),
    target_platforms TEXT, -- JSON array of platforms
    target_demographics TEXT, -- JSON object with demographics
    deliverables TEXT, -- JSON array of deliverables
    deadline DATE,
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'paused', 'completed', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 11. Collaborations Table (Enhanced)
```sql
CREATE TABLE collaborations (
    id TEXT PRIMARY KEY,
    influencer_id TEXT NOT NULL REFERENCES influencers(id),
    brand_id TEXT NOT NULL REFERENCES brands(id),
    campaign_id TEXT REFERENCES campaigns(id),
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'in_progress', 'completed', 'cancelled')),
    details TEXT,
    contract_terms TEXT,
    agreed_budget REAL,
    payment_status TEXT DEFAULT 'pending' CHECK (payment_status IN ('pending', 'partial', 'completed')),
    deliverables_submitted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 12. Reviews Table
```sql
CREATE TABLE reviews (
    id TEXT PRIMARY KEY,
    reviewer_id TEXT NOT NULL REFERENCES users(id),
    reviewee_id TEXT NOT NULL REFERENCES users(id),
    collaboration_id TEXT REFERENCES collaborations(id),
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 13. Analytics Table
```sql
CREATE TABLE analytics (
    id TEXT PRIMARY KEY,
    influencer_id TEXT NOT NULL REFERENCES influencers(id),
    fake_follower_percentage REAL DEFAULT 0.0,
    engagement_quality_score REAL DEFAULT 0.0,
    audience_language TEXT, -- JSON array of languages
    growth_rate REAL DEFAULT 0.0,
    estimated_reach INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 14. Generic Campaigns Table
```sql
CREATE TABLE generic_campaigns (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT NOT NULL, -- e.g., 'betting', 'crypto'
    payout_per_engagement REAL,
    min_followers INTEGER DEFAULT 1000,
    target_platforms TEXT, -- JSON array
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'paused', 'completed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 15. Influencer Generic Campaign Participations Table
```sql
CREATE TABLE influencer_generic_campaigns (
    id TEXT PRIMARY KEY,
    influencer_id TEXT NOT NULL REFERENCES influencers(id),
    generic_campaign_id TEXT NOT NULL REFERENCES generic_campaigns(id),
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'completed', 'cancelled')),
    earnings REAL DEFAULT 0.0,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Endpoints Design

### Authentication Endpoints
- `POST /auth/register` - Register new user (influencer or brand)
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user info

### Influencer Endpoints
- `GET /influencers` - List influencers with advanced filtering
- `GET /influencers/{id}` - Get specific influencer details
- `PUT /influencers/{id}` - Update influencer profile
- `POST /influencers/{id}/social-accounts` - Add social media account
- `PUT /influencers/{id}/social-accounts/{account_id}` - Update social media account
- `DELETE /influencers/{id}/social-accounts/{account_id}` - Remove social media account
- `POST /influencers/{id}/demographics` - Add audience demographic data
- `GET /influencers/{id}/analytics` - Get influencer analytics
- `POST /influencers/{id}/content-types` - Add content type data

### Brand Endpoints
- `GET /brands` - List brands with filtering
- `GET /brands/{id}` - Get specific brand details
- `PUT /brands/{id}` - Update brand profile

### Campaign Endpoints
- `GET /campaigns` - List campaigns with filtering
- `POST /campaigns` - Create new campaign
- `GET /campaigns/{id}` - Get campaign details
- `PUT /campaigns/{id}` - Update campaign
- `DELETE /campaigns/{id}` - Delete campaign

### Generic Campaign Endpoints
- `GET /generic-campaigns` - List available generic campaigns
- `POST /generic-campaigns/{id}/join` - Join a generic campaign
- `GET /influencers/{id}/generic-campaigns` - Get influencer's generic campaigns

### Collaboration Endpoints
- `GET /collaborations` - List collaborations with filtering
- `POST /collaborations` - Propose new collaboration
- `GET /collaborations/{id}` - Get collaboration details
- `PUT /collaborations/{id}/status` - Update collaboration status
- `PUT /collaborations/{id}/payment` - Update payment status

### Discovery & Matching Endpoints
- `POST /discovery/match-influencers` - Smart matching for brands
- `POST /discovery/match-brands` - Smart matching for influencers
- `GET /discovery/suggestions` - Get personalized suggestions

### Reviews Endpoints
- `GET /reviews` - List reviews with filtering
- `POST /reviews` - Submit new review
- `GET /users/{id}/reviews` - Get reviews for specific user

### Analytics Endpoints
- `GET /analytics/influencer/{id}` - Get detailed influencer analytics
- `POST /analytics/influencer/{id}/update` - Update analytics data
- `GET /analytics/fake-followers/{id}` - Get fake follower analysis
- `GET /analytics/engagement/{id}` - Get engagement analysis

### AI Chatbot Endpoints
- `POST /chatbot/analyze` - Get AI analysis and recommendations
- `POST /chatbot/chat` - Chat with AI assistant

### Utility Endpoints
- `GET /niches` - List all available niches
- `POST /niches` - Create new niche (admin only)
- `GET /health` - Health check endpoint

## Technology Stack

- **Framework**: FastAPI (for better async support and automatic API documentation)
- **Database**: SQLite for development, PostgreSQL for production
- **ORM**: SQLAlchemy
- **Authentication**: JWT tokens
- **Password Hashing**: bcrypt
- **Data Validation**: Pydantic models
- **CORS**: FastAPI CORS middleware
- **Documentation**: Automatic OpenAPI/Swagger documentation

## Key Features Implementation

### 1. Smart Matching Algorithm
- Implement scoring algorithm based on:
  - Niche overlap
  - Audience demographic match
  - Platform compatibility
  - Budget alignment
  - Historical collaboration success

### 2. Analytics Engine
- Fake follower detection (placeholder algorithm)
- Engagement quality scoring
- Growth rate calculation
- Reach estimation

### 3. Monetization System
- Generic campaign auto-matching
- Tailored campaign recommendations
- Earnings tracking

### 4. Rating System
- Bidirectional rating (influencers rate brands, brands rate influencers)
- Weighted average calculations
- Review moderation system

### 5. AI Chatbot Integration
- Account audit functionality
- Growth tip generation
- Monetization opportunity identification
- Integration with OpenAI API for natural language processing

