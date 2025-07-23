from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(title="Creator-Brand Marketplace API")

# --- Data Models ---

class Creator(BaseModel):
    id: str
    name: str
    bio: Optional[str] = ""
    location: Optional[str] = ""
    categories: List[str] = []
    followers: int = 0
    verified: bool = False

class Brand(BaseModel):
    id: str
    name: str
    description: Optional[str] = ""
    location: Optional[str] = ""
    categories: List[str] = []
    verified: bool = False

class Collaboration(BaseModel):
    id: str
    creator_id: str
    brand_id: str
    status: str  # "pending", "accepted", "completed"
    details: Optional[str] = ""
    payment_verified: bool = False

# --- In-memory storage (replace with DB in production) ---

creators = {}
brands = {}
collaborations = {}

# --- Creator Endpoints ---

@app.post("/creators/", response_model=Creator)
def register_creator(creator: Creator):
    creator.id = str(uuid.uuid4())
    creators[creator.id] = creator
    return creator

@app.get("/creators/", response_model=List[Creator])
def list_creators(category: Optional[str] = None, location: Optional[str] = None):
    result = list(creators.values())
    if category:
        result = [c for c in result if category in c.categories]
    if location:
        result = [c for c in result if c.location == location]
    return result

# --- Brand Endpoints ---

@app.post("/brands/", response_model=Brand)
def register_brand(brand: Brand):
    brand.id = str(uuid.uuid4())
    brands[brand.id] = brand
    return brand

@app.get("/brands/", response_model=List[Brand])
def list_brands(category: Optional[str] = None, location: Optional[str] = None):
    result = list(brands.values())
    if category:
        result = [b for b in result if category in b.categories]
    if location:
        result = [b for b in result if b.location == location]
    return result

# --- Collaboration Endpoints ---

@app.post("/collaborations/", response_model=Collaboration)
def propose_collaboration(collab: Collaboration):
    collab.id = str(uuid.uuid4())
    collab.status = "pending"
    collaborations[collab.id] = collab
    return collab

@app.get("/collaborations/", response_model=List[Collaboration])
def list_collaborations(creator_id: Optional[str] = None, brand_id: Optional[str] = None):
    result = list(collaborations.values())
    if creator_id:
        result = [c for c in result if c.creator_id == creator_id]
    if brand_id:
        result = [c for c in result if c.brand_id == brand_id]
    return result

@app.put("/collaborations/{collab_id}/status", response_model=Collaboration)
def update_collaboration_status(collab_id: str, status: str):
    if collab_id not in collaborations:
        raise HTTPException(status_code=404, detail="Collaboration not found")
    collaborations[collab_id].status = status
    return collaborations[collab_id]

# --- Health Check ---

@app.get("/health/")
def health():
    return {"status": "ok"}

# --- Run with: uvicorn influencer_brand_backend:app --reload ---