"""
Validation utilities for the Student Management System.

This module provides the Validator class with static methods for:
- ID generation for new students
- Data validation (students, courses, grades)
- Grade calculation with weighted components
- Student course lookup

All validation methods display appropriate error messages
using PyQt6 message boxes when validation fails.
"""

import random
from PyQt6.QtWidgets import QMessageBox


class Validator:
    """Handles all validation logic for students, courses, and grades."""
    
    @staticmethod
    def generate_id():
        """Generate random 5-digit student ID."""
        return random.randint(10**4, (10**5) - 1)

    @staticmethod
    def check_has_students(parent, students):
        """Check if students exist, show warning if empty."""
        if not students:
            QMessageBox.warning(parent, 'Error', "No students available")
            return False
        return True

    @staticmethod
    def check_has_courses(parent, courses):
        """Check if courses exist, show warning if empty."""
        if not courses:
            QMessageBox.warning(parent, 'Error', "No courses available")
            return False
        return True

    @staticmethod
    def validate_student_id(parent, student_id_str, students):
        """Validate student ID format and existence."""
        try:
            student_id = int(student_id_str)
            if student_id not in students:
                QMessageBox.warning(parent, "Error", f'Student ID {student_id} not found')
                return None
            return student_id
        except ValueError:
            QMessageBox.warning(parent, 'Error', "Invalid Student ID format")
            return None

    @staticmethod
    def validate_course_code(parent, course_code, courses):
        """Validate that course code exists."""
        if course_code not in courses:
            QMessageBox.warning(parent, "Error", f'Course {course_code} not found')
            return False
        return True

    @staticmethod
    def validate_grades(parent, grades_dict):
        """Validate grades are numeric and within 0-100 range."""
        try:
            grade_values = {field: float(value) for field, value in grades_dict.items()}
            if not all(0 <= grade <= 100 for grade in grade_values.values()):
                QMessageBox.warning(parent, 'Error', "All grades must be between 0 and 100")
                return None
            return grade_values
        except ValueError:
            QMessageBox.warning(parent, "Error", 'Please enter valid numeric values')
            return None

    @staticmethod
    def find_student_course(students, student_id, course_code):
        """Find specific course in student's enrolled courses."""
        student_courses = students[student_id].get("courses", [])
        for course in student_courses:
            if course["code"] == course_code:
                return course
        return None

    @staticmethod
    def calculate_grade(seatwork, assignment, quizzes, exam):
        """
        Calculate final grade using weighted components.
        Class Standing (40%): Seatwork 25% + Assignment 25% + Quizzes 50%
        Exam: 60%. Passing: 75%
        """
        class_standing = (seatwork * 0.25) + (assignment * 0.25) + (quizzes * 0.50)
        final_grade = (class_standing * 0.40) + (exam * 0.60)
        remarks = 'PASSED' if final_grade >= 75 else 'FAILED'
        return round(final_grade, 2), remarks
