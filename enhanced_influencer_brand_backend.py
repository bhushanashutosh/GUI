from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import sqlite3
import hashlib
import jwt
import json
import random
import uuid
from datetime import datetime, timedelta
import os

# Initialize FastAPI app
app = FastAPI(
    title="Enhanced Influencer-Brand Platform API",
    description="Comprehensive platform for influencer-brand collaborations with advanced matching, analytics, and monetization",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"

# Database setup
DATABASE_PATH = "influencer_platform.db"

def init_database():
    """Initialize the SQLite database with all required tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            user_type TEXT NOT NULL CHECK (user_type IN ('influencer', 'brand')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Influencers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS influencers (
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
        )
    ''')
    
    # Social media accounts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS social_media_accounts (
            id TEXT PRIMARY KEY,
            influencer_id TEXT NOT NULL REFERENCES influencers(id),
            platform TEXT NOT NULL CHECK (platform IN ('instagram', 'telegram', 'youtube', 'twitter', 'facebook')),
            username TEXT NOT NULL,
            follower_count INTEGER DEFAULT 0,
            engagement_rate REAL DEFAULT 0.0,
            verified BOOLEAN DEFAULT FALSE,
            url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Audience demographics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audience_demographics (
            id TEXT PRIMARY KEY,
            influencer_id TEXT NOT NULL REFERENCES influencers(id),
            age_group TEXT NOT NULL,
            gender TEXT NOT NULL,
            location TEXT NOT NULL,
            percentage REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Content types table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS content_types (
            id TEXT PRIMARY KEY,
            influencer_id TEXT NOT NULL REFERENCES influencers(id),
            content_type TEXT NOT NULL CHECK (content_type IN ('stories', 'posts', 'reels', 'videos', 'live_streams')),
            avg_views INTEGER DEFAULT 0,
            avg_engagement REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Niches table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS niches (
            id TEXT PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        )
    ''')
    
    # Influencer niches table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS influencer_niches (
            influencer_id TEXT NOT NULL REFERENCES influencers(id),
            niche_id TEXT NOT NULL REFERENCES niches(id),
            PRIMARY KEY (influencer_id, niche_id)
        )
    ''')
    
    # Brands table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS brands (
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
        )
    ''')
    
    # Brand niches table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS brand_niches (
            brand_id TEXT NOT NULL REFERENCES brands(id),
            niche_id TEXT NOT NULL REFERENCES niches(id),
            PRIMARY KEY (brand_id, niche_id)
        )
    ''')
    
    # Campaigns table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id TEXT PRIMARY KEY,
            brand_id TEXT NOT NULL REFERENCES brands(id),
            title TEXT NOT NULL,
            description TEXT,
            budget_min REAL,
            budget_max REAL,
            campaign_type TEXT CHECK (campaign_type IN ('generic', 'custom', 'collaboration')),
            target_platforms TEXT,
            target_demographics TEXT,
            deliverables TEXT,
            deadline DATE,
            status TEXT DEFAULT 'active' CHECK (status IN ('active', 'paused', 'completed', 'cancelled')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Collaborations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS collaborations (
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
        )
    ''')
    
    # Reviews table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id TEXT PRIMARY KEY,
            reviewer_id TEXT NOT NULL REFERENCES users(id),
            reviewee_id TEXT NOT NULL REFERENCES users(id),
            collaboration_id TEXT REFERENCES collaborations(id),
            rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Analytics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analytics (
            id TEXT PRIMARY KEY,
            influencer_id TEXT NOT NULL REFERENCES influencers(id),
            fake_follower_percentage REAL DEFAULT 0.0,
            engagement_quality_score REAL DEFAULT 0.0,
            audience_language TEXT,
            growth_rate REAL DEFAULT 0.0,
            estimated_reach INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Generic campaigns table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generic_campaigns (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT NOT NULL,
            payout_per_engagement REAL,
            min_followers INTEGER DEFAULT 1000,
            target_platforms TEXT,
            status TEXT DEFAULT 'active' CHECK (status IN ('active', 'paused', 'completed')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Influencer generic campaign participations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS influencer_generic_campaigns (
            id TEXT PRIMARY KEY,
            influencer_id TEXT NOT NULL REFERENCES influencers(id),
            generic_campaign_id TEXT NOT NULL REFERENCES generic_campaigns(id),
            status TEXT DEFAULT 'active' CHECK (status IN ('active', 'completed', 'cancelled')),
            earnings REAL DEFAULT 0.0,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert some default niches
    default_niches = [
        ('fashion', 'Fashion and style content'),
        ('beauty', 'Beauty and cosmetics content'),
        ('fitness', 'Health and fitness content'),
        ('food', 'Food and cooking content'),
        ('travel', 'Travel and lifestyle content'),
        ('tech', 'Technology and gadgets content'),
        ('gaming', 'Gaming and esports content'),
        ('business', 'Business and entrepreneurship content'),
        ('education', 'Educational and learning content'),
        ('entertainment', 'Entertainment and comedy content')
    ]
    
    for niche_name, description in default_niches:
        cursor.execute('''
            INSERT OR IGNORE INTO niches (id, name, description) 
            VALUES (?, ?, ?)
        ''', (str(uuid.uuid4()), niche_name, description))
    
    # Insert some default generic campaigns
    default_campaigns = [
        ('Crypto Promotion', 'Promote cryptocurrency platforms', 'crypto', 0.05, 1000, '["instagram", "twitter", "youtube"]'),
        ('Betting Platform Ads', 'Advertise online betting platforms', 'betting', 0.03, 5000, '["instagram", "twitter"]'),
        ('E-commerce Deals', 'Promote e-commerce deals and discounts', 'ecommerce', 0.02, 1000, '["instagram", "facebook", "youtube"]')
    ]
    
    for title, desc, category, payout, min_followers, platforms in default_campaigns:
        cursor.execute('''
            INSERT OR IGNORE INTO generic_campaigns (id, title, description, category, payout_per_engagement, min_followers, target_platforms) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (str(uuid.uuid4()), title, desc, category, payout, min_followers, platforms))
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_database()

# Pydantic models
class UserCreate(BaseModel):
    email: str
    password: str
    user_type: str

class UserLogin(BaseModel):
    email: str
    password: str

class InfluencerCreate(BaseModel):
    name: str
    bio: Optional[str] = ""
    location: Optional[str] = ""
    workload_preference: Optional[str] = "moderate"
    income_goals: Optional[str] = ""
    growth_aspirations: Optional[str] = ""

class InfluencerUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    workload_preference: Optional[str] = None
    income_goals: Optional[str] = None
    growth_aspirations: Optional[str] = None

class SocialMediaAccount(BaseModel):
    platform: str
    username: str
    follower_count: int = 0
    engagement_rate: float = 0.0
    verified: bool = False
    url: Optional[str] = None

class AudienceDemographic(BaseModel):
    age_group: str
    gender: str
    location: str
    percentage: float

class ContentType(BaseModel):
    content_type: str
    avg_views: int = 0
    avg_engagement: float = 0.0

class BrandCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    location: Optional[str] = ""
    website_url: Optional[str] = ""
    company_size: Optional[str] = "small"

class CampaignCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    campaign_type: str = "custom"
    target_platforms: Optional[List[str]] = []
    target_demographics: Optional[Dict[str, Any]] = {}
    deliverables: Optional[List[str]] = []
    deadline: Optional[str] = None

class CollaborationCreate(BaseModel):
    influencer_id: str
    brand_id: str
    campaign_id: Optional[str] = None
    details: Optional[str] = ""
    contract_terms: Optional[str] = ""
    agreed_budget: Optional[float] = None

class ReviewCreate(BaseModel):
    reviewee_id: str
    collaboration_id: Optional[str] = None
    rating: int
    comment: Optional[str] = ""

# Utility functions
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

def get_db_connection():
    return sqlite3.connect(DATABASE_PATH)

# Authentication endpoints
@app.post("/auth/register")
def register_user(user: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user already exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (user.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user_id = str(uuid.uuid4())
    password_hash = hash_password(user.password)
    
    cursor.execute('''
        INSERT INTO users (id, email, password_hash, user_type) 
        VALUES (?, ?, ?, ?)
    ''', (user_id, user.email, password_hash, user.user_type))
    
    conn.commit()
    conn.close()
    
    # Create access token
    access_token = create_access_token(data={"sub": user_id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user_id,
        "user_type": user.user_type
    }

@app.post("/auth/login")
def login_user(user: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, password_hash, user_type FROM users WHERE email = ?", (user.email,))
    result = cursor.fetchone()
    conn.close()
    
    if not result or not verify_password(user.password, result[1]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(data={"sub": result[0]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": result[0],
        "user_type": result[2]
    }

@app.get("/auth/me")
def get_current_user_info(current_user: str = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, email, user_type FROM users WHERE id = ?", (current_user,))
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": result[0],
        "email": result[1],
        "user_type": result[2]
    }

# Influencer endpoints
@app.post("/influencers")
def create_influencer_profile(influencer: InfluencerCreate, current_user: str = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user is of type influencer
    cursor.execute("SELECT user_type FROM users WHERE id = ?", (current_user,))
    user_type = cursor.fetchone()[0]
    if user_type != 'influencer':
        conn.close()
        raise HTTPException(status_code=403, detail="Only influencers can create influencer profiles")
    
    # Check if profile already exists
    cursor.execute("SELECT id FROM influencers WHERE user_id = ?", (current_user,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Influencer profile already exists")
    
    influencer_id = str(uuid.uuid4())
    cursor.execute('''
        INSERT INTO influencers (id, user_id, name, bio, location, workload_preference, income_goals, growth_aspirations) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (influencer_id, current_user, influencer.name, influencer.bio, influencer.location, 
          influencer.workload_preference, influencer.income_goals, influencer.growth_aspirations))
    
    conn.commit()
    conn.close()
    
    return {"id": influencer_id, "message": "Influencer profile created successfully"}

@app.get("/influencers")
def list_influencers(
    niche: Optional[str] = None,
    location: Optional[str] = None,
    min_followers: Optional[int] = None,
    platform: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT DISTINCT i.id, i.name, i.bio, i.location, i.verified, i.overall_rating, i.total_reviews,
               GROUP_CONCAT(DISTINCT n.name) as niches,
               MAX(sma.follower_count) as max_followers
        FROM influencers i
        LEFT JOIN influencer_niches in_n ON i.id = in_n.influencer_id
        LEFT JOIN niches n ON in_n.niche_id = n.id
        LEFT JOIN social_media_accounts sma ON i.id = sma.influencer_id
        WHERE 1=1
    '''
    
    params = []
    
    if niche:
        query += " AND n.name = ?"
        params.append(niche)
    
    if location:
        query += " AND i.location = ?"
        params.append(location)
    
    if platform:
        query += " AND sma.platform = ?"
        params.append(platform)
    
    query += " GROUP BY i.id"
    
    if min_followers:
        query += " HAVING max_followers >= ?"
        params.append(min_followers)
    
    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    influencers = []
    for row in results:
        influencers.append({
            "id": row[0],
            "name": row[1],
            "bio": row[2],
            "location": row[3],
            "verified": bool(row[4]),
            "overall_rating": row[5],
            "total_reviews": row[6],
            "niches": row[7].split(',') if row[7] else [],
            "max_followers": row[8] or 0
        })
    
    return influencers

@app.get("/influencers/{influencer_id}")
def get_influencer_details(influencer_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get influencer basic info
    cursor.execute('''
        SELECT i.*, u.email FROM influencers i 
        JOIN users u ON i.user_id = u.id 
        WHERE i.id = ?
    ''', (influencer_id,))
    
    influencer = cursor.fetchone()
    if not influencer:
        conn.close()
        raise HTTPException(status_code=404, detail="Influencer not found")
    
    # Get social media accounts
    cursor.execute("SELECT * FROM social_media_accounts WHERE influencer_id = ?", (influencer_id,))
    social_accounts = cursor.fetchall()
    
    # Get niches
    cursor.execute('''
        SELECT n.name FROM niches n 
        JOIN influencer_niches in_n ON n.id = in_n.niche_id 
        WHERE in_n.influencer_id = ?
    ''', (influencer_id,))
    niches = [row[0] for row in cursor.fetchall()]
    
    # Get analytics
    cursor.execute("SELECT * FROM analytics WHERE influencer_id = ?", (influencer_id,))
    analytics = cursor.fetchone()
    
    conn.close()
    
    return {
        "id": influencer[0],
        "name": influencer[2],
        "bio": influencer[3],
        "location": influencer[4],
        "verified": bool(influencer[6]),
        "overall_rating": influencer[7],
        "total_reviews": influencer[8],
        "workload_preference": influencer[9],
        "income_goals": influencer[10],
        "growth_aspirations": influencer[11],
        "social_accounts": [
            {
                "platform": acc[2],
                "username": acc[3],
                "follower_count": acc[4],
                "engagement_rate": acc[5],
                "verified": bool(acc[6]),
                "url": acc[7]
            } for acc in social_accounts
        ],
        "niches": niches,
        "analytics": {
            "fake_follower_percentage": analytics[2] if analytics else 0.0,
            "engagement_quality_score": analytics[3] if analytics else 0.0,
            "growth_rate": analytics[5] if analytics else 0.0,
            "estimated_reach": analytics[6] if analytics else 0
        } if analytics else None
    }

@app.post("/influencers/{influencer_id}/social-accounts")
def add_social_account(influencer_id: str, account: SocialMediaAccount, current_user: str = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verify ownership
    cursor.execute("SELECT user_id FROM influencers WHERE id = ?", (influencer_id,))
    result = cursor.fetchone()
    if not result or result[0] != current_user:
        conn.close()
        raise HTTPException(status_code=403, detail="Not authorized to modify this profile")
    
    account_id = str(uuid.uuid4())
    cursor.execute('''
        INSERT INTO social_media_accounts (id, influencer_id, platform, username, follower_count, engagement_rate, verified, url) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (account_id, influencer_id, account.platform, account.username, account.follower_count, 
          account.engagement_rate, account.verified, account.url))
    
    conn.commit()
    conn.close()
    
    return {"id": account_id, "message": "Social media account added successfully"}

# Brand endpoints
@app.post("/brands")
def create_brand_profile(brand: BrandCreate, current_user: str = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user is of type brand
    cursor.execute("SELECT user_type FROM users WHERE id = ?", (current_user,))
    user_type = cursor.fetchone()[0]
    if user_type != 'brand':
        conn.close()
        raise HTTPException(status_code=403, detail="Only brands can create brand profiles")
    
    # Check if profile already exists
    cursor.execute("SELECT id FROM brands WHERE user_id = ?", (current_user,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Brand profile already exists")
    
    brand_id = str(uuid.uuid4())
    cursor.execute('''
        INSERT INTO brands (id, user_id, name, description, location, website_url, company_size) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (brand_id, current_user, brand.name, brand.description, brand.location, brand.website_url, brand.company_size))
    
    conn.commit()
    conn.close()
    
    return {"id": brand_id, "message": "Brand profile created successfully"}

@app.get("/brands")
def list_brands(
    niche: Optional[str] = None,
    location: Optional[str] = None,
    company_size: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT DISTINCT b.id, b.name, b.description, b.location, b.website_url, b.company_size, 
               b.verified, b.overall_rating, b.total_reviews,
               GROUP_CONCAT(DISTINCT n.name) as niches
        FROM brands b
        LEFT JOIN brand_niches bn ON b.id = bn.brand_id
        LEFT JOIN niches n ON bn.niche_id = n.id
        WHERE 1=1
    '''
    
    params = []
    
    if niche:
        query += " AND n.name = ?"
        params.append(niche)
    
    if location:
        query += " AND b.location = ?"
        params.append(location)
    
    if company_size:
        query += " AND b.company_size = ?"
        params.append(company_size)
    
    query += " GROUP BY b.id LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    brands = []
    for row in results:
        brands.append({
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "location": row[3],
            "website_url": row[4],
            "company_size": row[5],
            "verified": bool(row[6]),
            "overall_rating": row[7],
            "total_reviews": row[8],
            "niches": row[9].split(',') if row[9] else []
        })
    
    return brands

# Campaign endpoints
@app.post("/campaigns")
def create_campaign(campaign: CampaignCreate, current_user: str = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get brand_id for current user
    cursor.execute("SELECT id FROM brands WHERE user_id = ?", (current_user,))
    result = cursor.fetchone()
    if not result:
        conn.close()
        raise HTTPException(status_code=403, detail="Only brands can create campaigns")
    
    brand_id = result[0]
    campaign_id = str(uuid.uuid4())
    
    cursor.execute('''
        INSERT INTO campaigns (id, brand_id, title, description, budget_min, budget_max, campaign_type, 
                             target_platforms, target_demographics, deliverables, deadline) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (campaign_id, brand_id, campaign.title, campaign.description, campaign.budget_min, campaign.budget_max,
          campaign.campaign_type, json.dumps(campaign.target_platforms), json.dumps(campaign.target_demographics),
          json.dumps(campaign.deliverables), campaign.deadline))
    
    conn.commit()
    conn.close()
    
    return {"id": campaign_id, "message": "Campaign created successfully"}

@app.get("/campaigns")
def list_campaigns(
    brand_id: Optional[str] = None,
    campaign_type: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT c.*, b.name as brand_name FROM campaigns c
        JOIN brands b ON c.brand_id = b.id
        WHERE 1=1
    '''
    
    params = []
    
    if brand_id:
        query += " AND c.brand_id = ?"
        params.append(brand_id)
    
    if campaign_type:
        query += " AND c.campaign_type = ?"
        params.append(campaign_type)
    
    if status:
        query += " AND c.status = ?"
        params.append(status)
    
    query += " ORDER BY c.created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    campaigns = []
    for row in results:
        campaigns.append({
            "id": row[0],
            "brand_id": row[1],
            "brand_name": row[12],
            "title": row[2],
            "description": row[3],
            "budget_min": row[4],
            "budget_max": row[5],
            "campaign_type": row[6],
            "target_platforms": json.loads(row[7]) if row[7] else [],
            "target_demographics": json.loads(row[8]) if row[8] else {},
            "deliverables": json.loads(row[9]) if row[9] else [],
            "deadline": row[10],
            "status": row[11]
        })
    
    return campaigns

# Generic campaigns endpoints
@app.get("/generic-campaigns")
def list_generic_campaigns():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM generic_campaigns WHERE status = 'active'")
    results = cursor.fetchall()
    conn.close()
    
    campaigns = []
    for row in results:
        campaigns.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "category": row[3],
            "payout_per_engagement": row[4],
            "min_followers": row[5],
            "target_platforms": json.loads(row[6]) if row[6] else []
        })
    
    return campaigns

@app.post("/generic-campaigns/{campaign_id}/join")
def join_generic_campaign(campaign_id: str, current_user: str = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get influencer_id for current user
    cursor.execute("SELECT id FROM influencers WHERE user_id = ?", (current_user,))
    result = cursor.fetchone()
    if not result:
        conn.close()
        raise HTTPException(status_code=403, detail="Only influencers can join generic campaigns")
    
    influencer_id = result[0]
    
    # Check if already joined
    cursor.execute('''
        SELECT id FROM influencer_generic_campaigns 
        WHERE influencer_id = ? AND generic_campaign_id = ?
    ''', (influencer_id, campaign_id))
    
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Already joined this campaign")
    
    participation_id = str(uuid.uuid4())
    cursor.execute('''
        INSERT INTO influencer_generic_campaigns (id, influencer_id, generic_campaign_id) 
        VALUES (?, ?, ?)
    ''', (participation_id, influencer_id, campaign_id))
    
    conn.commit()
    conn.close()
    
    return {"message": "Successfully joined generic campaign"}

# Collaboration endpoints
@app.post("/collaborations")
def create_collaboration(collaboration: CollaborationCreate, current_user: str = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    collaboration_id = str(uuid.uuid4())
    cursor.execute('''
        INSERT INTO collaborations (id, influencer_id, brand_id, campaign_id, details, contract_terms, agreed_budget) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (collaboration_id, collaboration.influencer_id, collaboration.brand_id, collaboration.campaign_id,
          collaboration.details, collaboration.contract_terms, collaboration.agreed_budget))
    
    conn.commit()
    conn.close()
    
    return {"id": collaboration_id, "message": "Collaboration created successfully"}

@app.get("/collaborations")
def list_collaborations(
    influencer_id: Optional[str] = None,
    brand_id: Optional[str] = None,
    status: Optional[str] = None,
    current_user: str = Depends(get_current_user)
):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT c.*, i.name as influencer_name, b.name as brand_name 
        FROM collaborations c
        JOIN influencers i ON c.influencer_id = i.id
        JOIN brands b ON c.brand_id = b.id
        WHERE 1=1
    '''
    
    params = []
    
    if influencer_id:
        query += " AND c.influencer_id = ?"
        params.append(influencer_id)
    
    if brand_id:
        query += " AND c.brand_id = ?"
        params.append(brand_id)
    
    if status:
        query += " AND c.status = ?"
        params.append(status)
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    collaborations = []
    for row in results:
        collaborations.append({
            "id": row[0],
            "influencer_id": row[1],
            "influencer_name": row[13],
            "brand_id": row[2],
            "brand_name": row[14],
            "campaign_id": row[3],
            "status": row[4],
            "details": row[5],
            "contract_terms": row[6],
            "agreed_budget": row[7],
            "payment_status": row[8],
            "deliverables_submitted": bool(row[9])
        })
    
    return collaborations

@app.put("/collaborations/{collaboration_id}/status")
def update_collaboration_status(collaboration_id: str, status: str, current_user: str = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE collaborations SET status = ?, updated_at = CURRENT_TIMESTAMP 
        WHERE id = ?
    ''', (status, collaboration_id))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Collaboration not found")
    
    conn.commit()
    conn.close()
    
    return {"message": "Collaboration status updated successfully"}

# Reviews endpoints
@app.post("/reviews")
def create_review(review: ReviewCreate, current_user: str = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    review_id = str(uuid.uuid4())
    cursor.execute('''
        INSERT INTO reviews (id, reviewer_id, reviewee_id, collaboration_id, rating, comment) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (review_id, current_user, review.reviewee_id, review.collaboration_id, review.rating, review.comment))
    
    # Update overall rating for reviewee
    cursor.execute('''
        SELECT AVG(rating), COUNT(*) FROM reviews WHERE reviewee_id = ?
    ''', (review.reviewee_id,))
    
    avg_rating, total_reviews = cursor.fetchone()
    
    # Update influencer or brand rating
    cursor.execute("SELECT user_type FROM users WHERE id = ?", (review.reviewee_id,))
    user_type = cursor.fetchone()[0]
    
    if user_type == 'influencer':
        cursor.execute('''
            UPDATE influencers SET overall_rating = ?, total_reviews = ? 
            WHERE user_id = ?
        ''', (avg_rating, total_reviews, review.reviewee_id))
    else:
        cursor.execute('''
            UPDATE brands SET overall_rating = ?, total_reviews = ? 
            WHERE user_id = ?
        ''', (avg_rating, total_reviews, review.reviewee_id))
    
    conn.commit()
    conn.close()
    
    return {"id": review_id, "message": "Review submitted successfully"}

@app.get("/reviews")
def list_reviews(reviewee_id: Optional[str] = None, limit: int = 50, offset: int = 0):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM reviews WHERE 1=1"
    params = []
    
    if reviewee_id:
        query += " AND reviewee_id = ?"
        params.append(reviewee_id)
    
    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    reviews = []
    for row in results:
        reviews.append({
            "id": row[0],
            "reviewer_id": row[1],
            "reviewee_id": row[2],
            "collaboration_id": row[3],
            "rating": row[4],
            "comment": row[5],
            "created_at": row[6]
        })
    
    return reviews

# Discovery and matching endpoints
@app.post("/discovery/match-influencers")
def match_influencers_for_brand(
    niche: Optional[str] = None,
    min_followers: Optional[int] = None,
    max_budget: Optional[float] = None,
    platforms: Optional[List[str]] = None,
    current_user: str = Depends(get_current_user)
):
    """Smart matching algorithm for brands to find suitable influencers"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Complex query to match influencers based on multiple criteria
    query = '''
        SELECT DISTINCT i.id, i.name, i.bio, i.location, i.overall_rating,
               MAX(sma.follower_count) as max_followers,
               GROUP_CONCAT(DISTINCT n.name) as niches,
               AVG(sma.engagement_rate) as avg_engagement
        FROM influencers i
        LEFT JOIN influencer_niches in_n ON i.id = in_n.influencer_id
        LEFT JOIN niches n ON in_n.niche_id = n.id
        LEFT JOIN social_media_accounts sma ON i.id = sma.influencer_id
        WHERE 1=1
    '''
    
    params = []
    
    if niche:
        query += " AND n.name = ?"
        params.append(niche)
    
    if platforms:
        placeholders = ','.join(['?' for _ in platforms])
        query += f" AND sma.platform IN ({placeholders})"
        params.extend(platforms)
    
    query += " GROUP BY i.id"
    
    if min_followers:
        query += " HAVING max_followers >= ?"
        params.append(min_followers)
    
    # Order by a combination of rating and engagement
    query += " ORDER BY (i.overall_rating * 0.4 + avg_engagement * 0.6) DESC LIMIT 20"
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    matches = []
    for row in results:
        match_score = (row[4] * 0.4 + (row[7] or 0) * 0.6) * 100  # Convert to percentage
        matches.append({
            "influencer_id": row[0],
            "name": row[1],
            "bio": row[2],
            "location": row[3],
            "overall_rating": row[4],
            "max_followers": row[5] or 0,
            "niches": row[6].split(',') if row[6] else [],
            "avg_engagement": row[7] or 0,
            "match_score": round(match_score, 2)
        })
    
    return matches

# Analytics endpoints
@app.get("/analytics/influencer/{influencer_id}")
def get_influencer_analytics(influencer_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get basic analytics
    cursor.execute("SELECT * FROM analytics WHERE influencer_id = ?", (influencer_id,))
    analytics = cursor.fetchone()
    
    # Get social media metrics
    cursor.execute('''
        SELECT platform, follower_count, engagement_rate 
        FROM social_media_accounts 
        WHERE influencer_id = ?
    ''', (influencer_id,))
    social_metrics = cursor.fetchall()
    
    # Get collaboration history
    cursor.execute('''
        SELECT COUNT(*) as total_collabs, 
               COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_collabs,
               AVG(agreed_budget) as avg_budget
        FROM collaborations 
        WHERE influencer_id = ?
    ''', (influencer_id,))
    collab_stats = cursor.fetchone()
    
    conn.close()
    
    return {
        "influencer_id": influencer_id,
        "fake_follower_percentage": analytics[2] if analytics else 0.0,
        "engagement_quality_score": analytics[3] if analytics else 0.0,
        "growth_rate": analytics[5] if analytics else 0.0,
        "estimated_reach": analytics[6] if analytics else 0,
        "social_metrics": [
            {
                "platform": metric[0],
                "follower_count": metric[1],
                "engagement_rate": metric[2]
            } for metric in social_metrics
        ],
        "collaboration_stats": {
            "total_collaborations": collab_stats[0] or 0,
            "completed_collaborations": collab_stats[1] or 0,
            "average_budget": collab_stats[2] or 0.0,
            "completion_rate": (collab_stats[1] / collab_stats[0] * 100) if collab_stats[0] > 0 else 0
        }
    }

# AI Chatbot endpoints (placeholder implementation)
@app.post("/chatbot/analyze")
def ai_analyze_account(current_user: str = Depends(get_current_user)):
    """AI-powered account analysis and recommendations"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get influencer data
    cursor.execute("SELECT id FROM influencers WHERE user_id = ?", (current_user,))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Influencer profile not found")
    
    influencer_id = result[0]
    
    # Get analytics and social media data
    cursor.execute("SELECT * FROM analytics WHERE influencer_id = ?", (influencer_id,))
    analytics = cursor.fetchone()
    
    cursor.execute("SELECT * FROM social_media_accounts WHERE influencer_id = ?", (influencer_id,))
    social_accounts = cursor.fetchall()
    
    # Simple AI analysis (placeholder)
    recommendations = []
    
    total_followers = sum(acc[4] for acc in social_accounts)
    avg_engagement = sum(acc[5] for acc in social_accounts) / len(social_accounts) if social_accounts else 0
    
    if total_followers < 5000:
        recommendations.append("Focus on growing your follower base through consistent, high-quality content")
    
    if avg_engagement < 0.03:
        recommendations.append("Work on improving engagement rates by posting more interactive content")
    
    if len(social_accounts) < 3:
        recommendations.append("Consider expanding to more social media platforms to increase reach")
    
    # Monetization opportunities
    monetization_tips = [
        "Join generic campaigns for quick earnings",
        "Build a strong portfolio to attract premium brand collaborations",
        "Consider creating your own products or services"
    ]
    
    conn.close()
    
    return {
        "account_audit": {
            "total_followers": total_followers,
            "average_engagement": avg_engagement,
            "platforms_count": len(social_accounts),
            "growth_potential": "High" if total_followers < 10000 else "Moderate"
        },
        "growth_recommendations": recommendations,
        "monetization_opportunities": monetization_tips
    }

# Utility endpoints
@app.get("/niches")
def list_niches():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM niches ORDER BY name")
    results = cursor.fetchall()
    conn.close()
    
    return [{"id": row[0], "name": row[1], "description": row[2]} for row in results]

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# Run with: uvicorn enhanced_influencer_brand_backend:app --host 0.0.0.0 --port 8000 --reload

