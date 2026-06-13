"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import EmailStr

app = FastAPI(
    title="Mergington High School API",
    description="API for viewing and signing up for extracurricular activities",
)

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=current_dir / "static"), name="static")


# In-memory activity database keyed by slug identifier
activities = {
    "chess-club": {
        "name": "Chess Club",
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
    },
    "programming-class": {
        "name": "Programming Class",
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
    },
    "gym-class": {
        "name": "Gym Class",
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
    },
    "soccer-club": {
        "name": "Soccer Club",
        "description": "Join our competitive soccer team and participate in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["alex@mergington.edu"],
    },
    "basketball-team": {
        "name": "Basketball Team",
        "description": "Train and compete in basketball tournaments",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["chris@mergington.edu", "jordan@mergington.edu"],
    },
    "debate-club": {
        "name": "Debate Club",
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 16,
        "participants": ["rachel@mergington.edu"],
    },
    "art-class": {
        "name": "Art Class",
        "description": "Explore various artistic mediums and techniques",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["maya@mergington.edu", "lucas@mergington.edu"],
    },
    "music-band": {
        "name": "Music Band",
        "description": "Learn instruments and perform in school concerts",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 25,
        "participants": ["david@mergington.edu"],
    },
    "robotics-club": {
        "name": "Robotics Club",
        "description": "Build and program robots for competitions",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["sarah@mergington.edu", "tyler@mergington.edu"],
    },
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_id}/signup")
def signup_for_activity(activity_id: str, email: EmailStr):
    """Sign up a student for an activity."""
    if activity_id not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_id]

    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up")

    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")

    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity['name']}"}
