# GigHub API
# Admission Number: C027-01-2727/2024
# Categories: Marketing, Data, Consulting | Currency: USD | Gigs: 12

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

app = FastAPI(
    title="GigHub API",
    description="API for managing freelance gig listings on GigHub (Nairobi). "
                 "Admission Number: C027-01-2727/2024",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Constants (derived from admission number C027-01-2727/2024)
# ---------------------------------------------------------------------------

ALLOWED_CATEGORIES = ["Marketing", "Data", "Consulting"]
CURRENCY = "USD"
ALLOWED_STATUSES = ["Open", "In Progress", "Closed"]


class StatusEnum(str, Enum):
    open = "Open"
    in_progress = "In Progress"
    closed = "Closed"


class CategoryEnum(str, Enum):
    marketing = "Marketing"
    data = "Data"
    consulting = "Consulting"


# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------

class GigCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=20, max_length=500)
    category: CategoryEnum
    budget: float = Field(..., gt=0)
    client_name: str = Field(..., min_length=2, max_length=50)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Social Media Campaign for Startup",
                "description": "Run a 30-day social media marketing campaign targeting Gen Z audiences in Nairobi.",
                "category": "Marketing",
                "budget": 800.0,
                "client_name": "Amina Hassan"
            }
        }


class GigUpdate(BaseModel):
    budget: Optional[float] = Field(None, gt=0)
    status: Optional[StatusEnum] = None

    class Config:
        json_schema_extra = {
            "example": {
                "budget": 950.0,
                "status": "In Progress"
            }
        }


class Gig(BaseModel):
    id: int
    title: str
    description: str
    category: str
    budget: float
    currency: str
    status: str
    client_name: str


# ---------------------------------------------------------------------------
# Dataset (12 gigs, based on admission number C027-01-2727/2024)
# ---------------------------------------------------------------------------

gigs_db: List[dict] = [
    {"id": 1, "title": "Social Media Campaign for Startup", "description": "Run a 30-day social media marketing campaign targeting Gen Z audiences in Nairobi.", "category": "Marketing", "budget": 800.0, "currency": "USD", "status": "Open", "client_name": "Amina Hassan"},
    {"id": 2, "title": "SEO Audit and Strategy Report", "description": "Conduct a full SEO audit of an e-commerce website and produce a strategy report.", "category": "Marketing", "budget": 450.0, "currency": "USD", "status": "Open", "client_name": "Brian Otieno"},
    {"id": 3, "title": "Email Marketing Funnel Setup", "description": "Design and implement an automated email marketing funnel for a SaaS product.", "category": "Marketing", "budget": 600.0, "currency": "USD", "status": "In Progress", "client_name": "Cynthia Wanjiru"},
    {"id": 4, "title": "Brand Positioning Strategy", "description": "Develop a brand positioning strategy for a new beverage company entering the market.", "category": "Marketing", "budget": 1200.0, "currency": "USD", "status": "Open", "client_name": "David Kimani"},
    {"id": 5, "title": "Customer Data Pipeline Build", "description": "Build an ETL pipeline to consolidate customer data from multiple sources into a warehouse.", "category": "Data", "budget": 1500.0, "currency": "USD", "status": "Open", "client_name": "Esther Nyambura"},
    {"id": 6, "title": "Sales Data Dashboard Creation", "description": "Create an interactive dashboard visualizing monthly sales data across all branches.", "category": "Data", "budget": 700.0, "currency": "USD", "status": "In Progress", "client_name": "Felix Mwangi"},
    {"id": 7, "title": "Churn Prediction Model", "description": "Build a machine learning model to predict customer churn using historical usage data.", "category": "Data", "budget": 1800.0, "currency": "USD", "status": "Open", "client_name": "Grace Achieng"},
    {"id": 8, "title": "Data Cleaning and Deduplication", "description": "Clean and deduplicate a large customer records database exported from legacy systems.", "category": "Data", "budget": 350.0, "currency": "USD", "status": "Closed", "client_name": "Hassan Ali"},
    {"id": 9, "title": "Business Process Optimization Review", "description": "Review internal business processes and recommend optimizations to cut operational costs.", "category": "Consulting", "budget": 2000.0, "currency": "USD", "status": "Open", "client_name": "Irene Njeri"},
    {"id": 10, "title": "Startup Fundraising Strategy Session", "description": "Provide consulting sessions to help a startup prepare its fundraising strategy and pitch.", "category": "Consulting", "budget": 900.0, "currency": "USD", "status": "In Progress", "client_name": "James Odhiambo"},
    {"id": 11, "title": "Market Entry Feasibility Study", "description": "Conduct a feasibility study for a company planning to enter the East African market.", "category": "Consulting", "budget": 1600.0, "currency": "USD", "status": "Open", "client_name": "Karen Wambui"},
    {"id": 12, "title": "HR Policy Framework Consulting", "description": "Advise on building an HR policy framework for a fast-growing 50-person company.", "category": "Consulting", "budget": 550.0, "currency": "USD", "status": "Closed", "client_name": "Leon Kariuki"},
]

next_id = 13  # next available id for new gigs


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def find_gig(gig_id: int) -> Optional[dict]:
    return next((g for g in gigs_db if g["id"] == gig_id), None)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/gigs", response_model=List[Gig], tags=["Gigs"])
def list_gigs(
    category: Optional[CategoryEnum] = Query(None, description="Filter by category"),
    min_budget: Optional[float] = Query(None, ge=0, description="Minimum budget filter"),
    max_budget: Optional[float] = Query(None, ge=0, description="Maximum budget filter"),
):
    """Return all gigs, optionally filtered by category and/or min_budget/max_budget."""
    results = gigs_db

    if category is not None:
        results = [g for g in results if g["category"] == category.value]

    if min_budget is not None:
        results = [g for g in results if g["budget"] >= min_budget]

    if max_budget is not None:
        results = [g for g in results if g["budget"] <= max_budget]

    return results


@app.get("/gigs/search", response_model=List[Gig], tags=["Gigs"])
def search_gigs(q: str = Query(..., min_length=1, description="Search term for gig title")):
    """Search for gigs whose title contains the query string (case-insensitive)."""
    q_lower = q.lower()
    results = [g for g in gigs_db if q_lower in g["title"].lower()]
    return results


@app.get("/gigs/{gig_id}", response_model=Gig, tags=["Gigs"])
def get_gig(gig_id: int):
    """Return a single gig by its ID."""
    gig = find_gig(gig_id)
    if gig is None:
        raise HTTPException(status_code=404, detail=f"Gig with id {gig_id} not found")
    return gig


@app.post("/gigs", response_model=Gig, status_code=201, tags=["Gigs"])
def create_gig(gig: GigCreate):
    """Create a new gig. Currency is fixed by the platform's assigned currency (USD)."""
    global next_id

    new_gig = {
        "id": next_id,
        "title": gig.title,
        "description": gig.description,
        "category": gig.category.value,
        "budget": gig.budget,
        "currency": CURRENCY,
        "status": "Open",
        "client_name": gig.client_name,
    }
    gigs_db.append(new_gig)
    next_id += 1
    return new_gig


@app.put("/gigs/{gig_id}", response_model=Gig, tags=["Gigs"])
def update_gig(gig_id: int, update: GigUpdate):
    """Update a gig's budget and/or status."""
    gig = find_gig(gig_id)
    if gig is None:
        raise HTTPException(status_code=404, detail=f"Gig with id {gig_id} not found")

    if update.budget is not None:
        gig["budget"] = update.budget

    if update.status is not None:
        gig["status"] = update.status.value

    return gig


@app.delete("/gigs/{gig_id}", tags=["Gigs"])
def delete_gig(gig_id: int):
    """Delete a gig by its ID."""
    gig = find_gig(gig_id)
    if gig is None:
        raise HTTPException(status_code=404, detail=f"Gig with id {gig_id} not found")

    gigs_db.remove(gig)
    return {"detail": f"Gig with id {gig_id} has been deleted"}


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to the GigHub API",
        "admission_number": "C027-01-2727/2024",
        "docs": "/docs",
    }