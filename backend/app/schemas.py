from pydantic import BaseModel
from typing import Optional, List

# ----------------------
# AUTH / USER
# ----------------------
class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

# ----------------------
# ACADEMIC RECORDS
# ----------------------
class AcademicRecordBase(BaseModel):
    academic_year: str
    semester: str
    gpa: float
    total_credits: int

class AcademicRecordCreate(AcademicRecordBase):
    pass

class AcademicRecordOut(AcademicRecordBase):
    id: int
    class Config:
        orm_mode = True

# ----------------------
# GRADES
# ----------------------
class GradeBase(BaseModel):
    course_code: str
    course_name: str
    grade_letter: str
    grade_points: float
    credits: int
    semester: str
    academic_year: str

class GradeCreate(GradeBase):
    pass

class GradeOut(GradeBase):
    id: int
    class Config:
        orm_mode = True

class GradeSummary(BaseModel):
    course_code: str
    course_name: str
    latest_grade: str
    grade_points: float
    credits: int
    semester: str

# ----------------------
# CLASS SCHEDULE
# ----------------------
class ClassScheduleBase(BaseModel):
    course_code: str
    course_name: str
    day_of_week: str
    start_time: str
    end_time: str
    academic_year: str
    semester: str

class ClassScheduleCreate(ClassScheduleBase):
    pass

class ClassScheduleOut(ClassScheduleBase):
    id: int
    class Config:
        orm_mode = True

# ----------------------
# DASHBOARD SUMMARY
# ----------------------
class AcademicSummary(BaseModel):
    current_gpa: float
    total_credits: int
    active_courses: int
    completed_courses: int
