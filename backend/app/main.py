from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import engine, Base, get_db
from models import User, AcademicRecord, Grade, ClassSchedule
from schemas import (
    UserCreate, UserOut, Token, AcademicRecordOut, AcademicRecordCreate,
    GradeOut, GradeCreate, ClassScheduleOut, ClassScheduleCreate,
    AcademicSummary, GradeSummary
)
from auth import get_password_hash, verify_password, create_access_token, get_current_user
from datetime import datetime
from pydantic import BaseModel
from typing import List

# ✅ Create all DB tables
Base.metadata.create_all(bind=engine)

# ✅ FastAPI app instance
app = FastAPI(title="College Management API")

# ✅ Allow frontend (React) to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://10.127.129.61:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# 🔹 AUTHENTICATION
# -------------------------------

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=Token)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    """Login and get JWT token"""
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current logged-in user"""
    return current_user

# -------------------------------
# 🔹 ACADEMIC RECORDS
# -------------------------------

@app.get("/academic-records", response_model=List[AcademicRecordOut])
def get_academic_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(AcademicRecord).filter(
        AcademicRecord.student_id == current_user.id
    ).order_by(
        AcademicRecord.academic_year.desc(),
        AcademicRecord.semester.desc()
    ).all()

@app.post("/academic-records", response_model=AcademicRecordOut)
def create_academic_record(
    record: AcademicRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = db.query(AcademicRecord).filter(
        AcademicRecord.student_id == current_user.id,
        AcademicRecord.semester == record.semester,
        AcademicRecord.academic_year == record.academic_year
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Record for this semester already exists")
    db_record = AcademicRecord(student_id=current_user.id, **record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

# -------------------------------
# 🔹 GRADES
# -------------------------------

@app.get("/grades", response_model=List[GradeOut])
def get_grades(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Grade).filter(
        Grade.student_id == current_user.id
    ).order_by(
        Grade.academic_year.desc(),
        Grade.semester.desc(),
        Grade.course_code
    ).all()

@app.post("/grades", response_model=GradeOut)
def create_grade(
    grade: GradeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_grade = Grade(student_id=current_user.id, **grade.dict())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

# -------------------------------
# 🔹 CLASS SCHEDULE
# -------------------------------

@app.get("/class-schedules", response_model=List[ClassScheduleOut])
def get_class_schedules(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(ClassSchedule).filter(
        ClassSchedule.student_id == current_user.id
    ).order_by(
        ClassSchedule.day_of_week,
        ClassSchedule.start_time
    ).all()

@app.post("/class-schedules", response_model=ClassScheduleOut)
def create_class_schedule(
    schedule: ClassScheduleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_schedule = ClassSchedule(student_id=current_user.id, **schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

# -------------------------------
# 🔹 DASHBOARD SUMMARY
# -------------------------------

@app.get("/academic-summary", response_model=AcademicSummary)
def get_academic_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    latest_record = db.query(AcademicRecord).filter(
        AcademicRecord.student_id == current_user.id
    ).order_by(
        AcademicRecord.academic_year.desc(),
        AcademicRecord.semester.desc()
    ).first()

    current_gpa = latest_record.gpa if latest_record else 0.0
    total_credits = latest_record.total_credits if latest_record else 0

    active_courses = db.query(ClassSchedule).filter(
        ClassSchedule.student_id == current_user.id,
        ClassSchedule.academic_year == "2024-2025"  # Example: current year
    ).count()

    completed_courses = db.query(Grade).filter(
        Grade.student_id == current_user.id
    ).distinct(Grade.course_code).count()

    return AcademicSummary(
        current_gpa=current_gpa,
        total_credits=total_credits,
        active_courses=active_courses,
        completed_courses=completed_courses
    )

@app.get("/grade-summary", response_model=List[GradeSummary])
def get_grade_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    subquery = db.query(
        Grade.course_code,
        func.max(Grade.created_at).label("latest_date")
    ).filter(
        Grade.student_id == current_user.id
    ).group_by(Grade.course_code).subquery()

    latest_grades = db.query(Grade).join(
        subquery,
        (Grade.course_code == subquery.c.course_code) &
        (Grade.created_at == subquery.c.latest_date)
    ).filter(
        Grade.student_id == current_user.id
    ).all()

    return [
        GradeSummary(
            course_code=grade.course_code,
            course_name=grade.course_name,
            latest_grade=grade.grade_letter,
            grade_points=grade.grade_points,
            credits=grade.credits,
            semester=grade.semester
        )
        for grade in latest_grades
    ]
