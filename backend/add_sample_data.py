#!/usr/bin/env python3
"""
Script to add sample academic data for testing
Run this after starting the backend server to populate with test data
"""

import requests
import json
from datetime import datetime, timedelta

# Backend URL
BASE_URL = "http://127.0.0.1:8000"

def get_auth_token():
    """Get authentication token by logging in"""
    login_data = {
        "email": "test@student.com",  # Use an existing user email
        "password": "password123"     # Use the correct password
    }
    
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Login failed: {response.text}")
        return None

def add_sample_data(token):
    """Add sample academic data"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Sample Academic Records
    academic_records = [
        {
            "semester": "Fall 2024",
            "academic_year": "2024-2025",
            "total_credits": 15,
            "gpa": 3.8,
            "status": "Active"
        },
        {
            "semester": "Spring 2024",
            "academic_year": "2023-2024",
            "total_credits": 18,
            "gpa": 3.6,
            "status": "Completed"
        }
    ]
    
    print("Adding academic records...")
    for record in academic_records:
        response = requests.post(f"{BASE_URL}/academic-records", 
                               json=record, headers=headers)
        if response.status_code == 200:
            print(f"✓ Added academic record: {record['semester']}")
        else:
            print(f"✗ Failed to add academic record: {response.text}")
    
    # Sample Grades
    grades = [
        {
            "course_code": "CS101",
            "course_name": "Introduction to Computer Science",
            "semester": "Fall 2024",
            "academic_year": "2024-2025",
            "grade_letter": "A",
            "grade_points": 4.0,
            "credits": 3,
            "exam_type": "Final",
            "exam_date": datetime.now().isoformat(),
            "remarks": "Excellent performance"
        },
        {
            "course_code": "MATH201",
            "course_name": "Calculus II",
            "semester": "Fall 2024",
            "academic_year": "2024-2025",
            "grade_letter": "B+",
            "grade_points": 3.5,
            "credits": 4,
            "exam_type": "Final",
            "exam_date": datetime.now().isoformat(),
            "remarks": "Good understanding of concepts"
        },
        {
            "course_code": "ENG101",
            "course_name": "English Composition",
            "semester": "Fall 2024",
            "academic_year": "2024-2025",
            "grade_letter": "A-",
            "grade_points": 3.7,
            "credits": 3,
            "exam_type": "Final",
            "exam_date": datetime.now().isoformat(),
            "remarks": "Strong writing skills"
        },
        {
            "course_code": "PHYS101",
            "course_name": "General Physics I",
            "semester": "Fall 2024",
            "academic_year": "2024-2025",
            "grade_letter": "B",
            "grade_points": 3.0,
            "credits": 4,
            "exam_type": "Final",
            "exam_date": datetime.now().isoformat(),
            "remarks": "Room for improvement in problem solving"
        },
        {
            "course_code": "CS101",
            "course_name": "Introduction to Computer Science",
            "semester": "Fall 2024",
            "academic_year": "2024-2025",
            "grade_letter": "A",
            "grade_points": 4.0,
            "credits": 3,
            "exam_type": "Midterm",
            "exam_date": (datetime.now() - timedelta(days=30)).isoformat(),
            "remarks": "Outstanding midterm performance"
        }
    ]
    
    print("\nAdding grades...")
    for grade in grades:
        response = requests.post(f"{BASE_URL}/grades", 
                               json=grade, headers=headers)
        if response.status_code == 200:
            print(f"✓ Added grade: {grade['course_code']} - {grade['grade_letter']}")
        else:
            print(f"✗ Failed to add grade: {response.text}")
    
    # Sample Class Schedules
    class_schedules = [
        {
            "course_code": "CS101",
            "course_name": "Introduction to Computer Science",
            "instructor": "Dr. Sarah Johnson",
            "room": "CS-201",
            "day_of_week": "Monday",
            "start_time": "09:00",
            "end_time": "10:30",
            "semester": "Fall 2024",
            "academic_year": "2024-2025"
        },
        {
            "course_code": "CS101",
            "course_name": "Introduction to Computer Science",
            "instructor": "Dr. Sarah Johnson",
            "room": "CS-201",
            "day_of_week": "Wednesday",
            "start_time": "09:00",
            "end_time": "10:30",
            "semester": "Fall 2024",
            "academic_year": "2024-2025"
        },
        {
            "course_code": "CS101",
            "course_name": "Introduction to Computer Science",
            "instructor": "Dr. Sarah Johnson",
            "room": "CS-201",
            "day_of_week": "Friday",
            "start_time": "09:00",
            "end_time": "10:30",
            "semester": "Fall 2024",
            "academic_year": "2024-2025"
        },
        {
            "course_code": "MATH201",
            "course_name": "Calculus II",
            "instructor": "Prof. Michael Chen",
            "room": "MATH-105",
            "day_of_week": "Tuesday",
            "start_time": "11:00",
            "end_time": "12:30",
            "semester": "Fall 2024",
            "academic_year": "2024-2025"
        },
        {
            "course_code": "MATH201",
            "course_name": "Calculus II",
            "instructor": "Prof. Michael Chen",
            "room": "MATH-105",
            "day_of_week": "Thursday",
            "start_time": "11:00",
            "end_time": "12:30",
            "semester": "Fall 2024",
            "academic_year": "2024-2025"
        },
        {
            "course_code": "ENG101",
            "course_name": "English Composition",
            "instructor": "Dr. Emily Rodriguez",
            "room": "ENG-302",
            "day_of_week": "Monday",
            "start_time": "14:00",
            "end_time": "15:30",
            "semester": "Fall 2024",
            "academic_year": "2024-2025"
        },
        {
            "course_code": "ENG101",
            "course_name": "English Composition",
            "instructor": "Dr. Emily Rodriguez",
            "room": "ENG-302",
            "day_of_week": "Wednesday",
            "start_time": "14:00",
            "end_time": "15:30",
            "semester": "Fall 2024",
            "academic_year": "2024-2025"
        },
        {
            "course_code": "PHYS101",
            "course_name": "General Physics I",
            "instructor": "Dr. Robert Wilson",
            "room": "PHYS-150",
            "day_of_week": "Tuesday",
            "start_time": "16:00",
            "end_time": "17:30",
            "semester": "Fall 2024",
            "academic_year": "2024-2025"
        },
        {
            "course_code": "PHYS101",
            "course_name": "General Physics I",
            "instructor": "Dr. Robert Wilson",
            "room": "PHYS-150",
            "day_of_week": "Thursday",
            "start_time": "16:00",
            "end_time": "17:30",
            "semester": "Fall 2024",
            "academic_year": "2024-2025"
        }
    ]
    
    print("\nAdding class schedules...")
    for schedule in class_schedules:
        response = requests.post(f"{BASE_URL}/class-schedules", 
                               json=schedule, headers=headers)
        if response.status_code == 200:
            print(f"✓ Added schedule: {schedule['course_code']} - {schedule['day_of_week']}")
        else:
            print(f"✗ Failed to add schedule: {response.text}")

def main():
    print("Adding sample academic data...")
    print("Make sure your backend server is running on http://127.0.0.1:8000")
    print("And you have a user account with email: test@student.com")
    print("-" * 50)
    
    # Get authentication token
    token = get_auth_token()
    if not token:
        print("Failed to authenticate. Please check your credentials.")
        return
    
    # Add sample data
    add_sample_data(token)
    
    print("\n" + "=" * 50)
    print("Sample data added successfully!")
    print("You can now test the academic features in your student portal.")
    print("Dashboard will show real data from the database.")

if __name__ == "__main__":
    main()




