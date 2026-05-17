from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

app = FastAPI(
    title="Benjamin Ntifo's  Application Management System",
    description="A mock API for managing student internship applications",
    version="1.0.0"
)

# =============================================
# 📦 SCHEMA (What an application looks like)
# =============================================


class Application(BaseModel):
    id: int
    fullName: str
    email: str
    phone: str
    whatsappNumber: str
    university: str
    course: str
    level: str
    track: str
    motivation: str
    portfolioLink: str
    resumeLink: str
    joinInnovationClub: bool
    status: str  # "pending", "accepted", "rejected"
    submittedAt: str


class CreateApplication(BaseModel):
    fullName: str
    email: str
    phone: str
    whatsappNumber: str
    university: str
    course: str
    level: str
    track: str
    motivation: str
    portfolioLink: str
    resumeLink: str
    joinInnovationClub: bool


class UpdateStatus(BaseModel):
    status: str  # "pending", "accepted", "rejected"


# =============================================
# 🗄️ MOCK DATABASE (Sample Data)
# =============================================

applications = [
    {
        "id": 1,
        "fullName": "Ntifo Benjamin",
        "email": "ntifobenjamin7@gmail.com",
        "phone": "0201234567",
        "whatsappNumber": "0201234567",
        "university": "KNUST",
        "course": "Computer Engineering",
        "level": "2nd Year",
        "track": "Backend Engineering",
        "motivation": "I want to build real-world APIs and backend systems.",
        "portfolioLink": "https://github.com/benjamin-ntifo",
        "resumeLink": "https://linkedin.com/in/benjamin-ntifo",
        "joinInnovationClub": True,
        "status": "pending",
        "submittedAt": "2026-05-01T09:00:00Z"
    },
    {
        "id": 2,
        "fullName": "Ama Serwaa Owusu",
        "email": "amaserwaa@gmail.com",
        "phone": "0245567812",
        "whatsappNumber": "0245567812",
        "university": "University of Ghana",
        "course": "Computer Engineering",
        "level": "2nd Year",
        "track": "Embedded Systems",
        "motivation": "I want to gain hands-on experience in embedded systems and IoT development.",
        "portfolioLink": "https://github.com/amase",
        "resumeLink": "https://linkedin.com/in/amase",
        "joinInnovationClub": True,
        "status": "accepted",
        "submittedAt": "2026-05-04T10:12:45Z"
    },
    {
        "id": 3,
        "fullName": "Yaw Mensah",
        "email": "yawmensah@gmail.com",
        "phone": "0558876123",
        "whatsappNumber": "0558876123",
        "university": "KNUST",
        "course": "Electrical Engineering",
        "level": "4th Year",
        "track": "Radar & RF Systems",
        "motivation": "To improve my knowledge in RF systems, radar engineering, and wireless communications.",
        "portfolioLink": "https://github.com/yawmensah",
        "resumeLink": "https://linkedin.com/in/yawmensah",
        "joinInnovationClub": True,
        "status": "pending",
        "submittedAt": "2026-05-05T08:45:30Z"
    },
    {
        "id": 4,
        "fullName": "Priscilla Adjei",
        "email": "priscilla.adjei@gmail.com",
        "phone": "0203344556",
        "whatsappNumber": "0203344556",
        "university": "Ashesi University",
        "course": "Software Engineering",
        "level": "3rd Year",
        "track": "Backend Engineering",
        "motivation": "I want to strengthen my backend engineering skills using FastAPI and modern software architecture.",
        "portfolioLink": "https://github.com/priscillaadjei",
        "resumeLink": "https://linkedin.com/in/priscillaadjei",
        "joinInnovationClub": True,
        "status": "accepted",
        "submittedAt": "2026-05-06T14:18:22Z"
    },
    {
        "id": 5,
        "fullName": "Daniel Kofi Asante",
        "email": "danielasante@gmail.com",
        "phone": "0277788990",
        "whatsappNumber": "0277788990",
        "university": "UENR",
        "course": "Biomedical Engineering",
        "level": "2nd Year",
        "track": "Biomedical Systems",
        "motivation": "To explore biomedical monitoring systems and healthcare technology innovations.",
        "portfolioLink": "https://github.com/danielasante",
        "resumeLink": "https://linkedin.com/in/danielasante",
        "joinInnovationClub": False,
        "status": "rejected",
        "submittedAt": "2026-05-07T11:05:10Z"
    }
]


# =============================================
# 🏠 HOME ROUTE
# =============================================

@app.get("/")
def home():
    return {
        "message": "Welcome to Zaptek Application Management API 🚀",
        "version": "1.0.0",
        "endpoints": {
            "GET all applications": "/applications",
            "GET single application": "/applications/{id}",
            "GET by status": "/applications/status/{status}",
            "POST new application": "/applications",
            "PUT update status": "/applications/{id}/status",
            "DELETE application": "/applications/{id}"
        }
    }


# =============================================
# 📋 GET - Read all applications
# =============================================

@app.get("/applications")
def get_all_applications():
    return {
        "total": len(applications),
        "applications": applications
    }


# =============================================
# 🔍 GET - Read a single application by ID
# =============================================

@app.get("/applications/{id}")
def get_application(id: int):
    for app_item in applications:
        if app_item["id"] == id:
            return app_item
    raise HTTPException(
        status_code=404, detail=f"Application with id {id} not found")


# =============================================
# 🔍 GET - Filter applications by status
# =============================================

@app.get("/applications/status/{status}")
def get_by_status(status: str):
    valid_statuses = ["pending", "accepted", "rejected"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Choose from: {valid_statuses}"
        )
    filtered = [a for a in applications if a["status"] == status]
    return {
        "status": status,
        "total": len(filtered),
        "applications": filtered
    }


# =============================================
# ➕ POST - Create a new application
# =============================================

@app.post("/applications", status_code=201)
def create_application(new_app: CreateApplication):
    # Check if email already exists
    for app_item in applications:
        if app_item["email"] == new_app.email:
            raise HTTPException(
                status_code=400,
                detail="An application with this email already exists"
            )

    # Generate new ID
    new_id = max(a["id"] for a in applications) + 1

    # Create the new application
    application = {
        "id": new_id,
        "fullName": new_app.fullName,
        "email": new_app.email,
        "phone": new_app.phone,
        "whatsappNumber": new_app.whatsappNumber,
        "university": new_app.university,
        "course": new_app.course,
        "level": new_app.level,
        "track": new_app.track,
        "motivation": new_app.motivation,
        "portfolioLink": new_app.portfolioLink,
        "resumeLink": new_app.resumeLink,
        "joinInnovationClub": new_app.joinInnovationClub,
        "status": "pending",
        "submittedAt": datetime.utcnow().isoformat() + "Z"
    }

    applications.append(application)
    return {
        "message": "Application submitted successfully! ✅",
        "application": application
    }


# =============================================
# ✏️ PUT - Update application status
# =============================================

@app.put("/applications/{id}/status")
def update_status(id: int, update: UpdateStatus):
    valid_statuses = ["pending", "accepted", "rejected"]
    if update.status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Choose from: {valid_statuses}"
        )

    for app_item in applications:
        if app_item["id"] == id:
            app_item["status"] = update.status
            return {
                "message": f"Status updated to '{update.status}' ✅",
                "application": app_item
            }

    raise HTTPException(
        status_code=404, detail=f"Application with id {id} not found")


# =============================================
# 🗑️ DELETE - Remove an application
# =============================================

@app.delete("/applications/{id}")
def delete_application(id: int):
    for index, app_item in enumerate(applications):
        if app_item["id"] == id:
            deleted = applications.pop(index)
            return {
                "message": f"Application for '{deleted['fullName']}' deleted successfully ✅",
                "deleted_application": deleted
            }

    raise HTTPException(
        status_code=404, detail=f"Application with id {id} not found")
