from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    academic_records = relationship("AcademicRecord", back_populates="student")
    grades = relationship("Grade", back_populates="student")
    schedules = relationship("ClassSchedule", back_populates="student")


class AcademicRecord(Base):
    __tablename__ = "academic_records"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    academic_year = Column(String(20))
    semester = Column(String(20))
    gpa = Column(Float, default=0.0)
    total_credits = Column(Integer, default=0)

    student = relationship("User", back_populates="academic_records")


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    course_code = Column(String(20))
    course_name = Column(String(100))
    grade_letter = Column(String(5))
    grade_points = Column(Float)
    credits = Column(Integer)
    semester = Column(String(20))
    academic_year = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("User", back_populates="grades")


class ClassSchedule(Base):
    __tablename__ = "class_schedules"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    course_code = Column(String(20))
    course_name = Column(String(100))
    day_of_week = Column(String(20))  # e.g. Monday
    start_time = Column(String(10))   # e.g. 09:00
    end_time = Column(String(10))     # e.g. 10:30
    academic_year = Column(String(20))
    semester = Column(String(20))

    student = relationship("User", back_populates="schedules")
