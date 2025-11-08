"""
Report generation and analytics for the Student Management System.

This module provides comprehensive reporting capabilities including:
- Student reports with all enrolled courses and grades
- Course reports with enrollment lists
- Class rankings by average grade
- Failing student identification
- Grade calculation tools

All report methods return formatted data ready for display.
"""

from utils.validators import Validator


class ReportGenerator:
    """Generate reports and analytics for students and courses."""
    
    @staticmethod
    def build_student_report(student_id, student, students):
        """
        Build comprehensive report for a student.
        Returns formatted report list with courses and grades.
        """
        report = [
            f"=== STUDENT REPORT ===",
            f"Student ID: {student_id}",
            f"Name: {student['name']}",
            f"",
        ]
        
        student_courses = student.get("courses", [])
        
        if not student_courses:
            report.append("No courses enrolled")
        else:
            report.append(f"=== ENROLLED COURSES ({len(student_courses)}) ===")
            report.append("")
            
            for idx, course in enumerate(student_courses, 1):
                seatwork = course["grades"]["seatwork"]
                assignment = course["grades"]["assignment"]
                quizzes = course["grades"]["quizzes"]
                exam = course["grades"]["exam"]
                
                final_grade, remarks = Validator.calculate_grade(seatwork, assignment, quizzes, exam)
                course["remarks"] = remarks
                class_standing = round((seatwork * 0.25 + assignment * 0.25 + quizzes * 0.50), 2)
                
                report.extend([
                    f"--- COURSE {idx}: {course['code']} - {course['subject']} ---",
                    f"Seatwork: {seatwork}",
                    f"Assignment: {assignment}",
                    f"Quizzes: {quizzes}",
                    f"Class Standing: {class_standing}",
                    f"Exam: {exam}",
                    f"FINAL GRADE: {final_grade}",
                    f"REMARKS: {remarks}",
                    f""
                ])
        
        return report
    
    @staticmethod
    def build_course_report(course_code, course, students):
        """
        Build report for a course showing all enrolled students.
        Returns formatted report list with student enrollment.
        """
        enrolled_students = []
        for student_id, student_info in students.items():
            for student_course in student_info.get("courses", []):
                if student_course["code"] == course_code:
                    enrolled_students.append({
                        "id": student_id,
                        "name": student_info["name"]
                    })
                    break
        
        report = [
            f"=== COURSE REPORT ===",
            f"Course Code: {course_code}",
            f"Subject: {course['subject']}",
            f"",
            f"=== ENROLLED STUDENTS ({len(enrolled_students)}) ===",
        ]
        
        if enrolled_students:
            for student in enrolled_students:
                report.append(f"ID: {student['id']} - {student['name']}")
        else:
            report.append("No students enrolled")
        
        return report
    
    @staticmethod
    def calculate_class_ranking(students):
        """
        Calculate ranking of all students by average grade.
        Returns sorted list of student data with averages.
        """
        student_averages = []
        
        for student_id, student_info in students.items():
            courses_list = student_info.get("courses", [])
            
            if not courses_list:
                continue
            
            total_grade = 0
            course_count = 0
            
            for course in courses_list:
                grades = course["grades"]
                final_grade, _ = Validator.calculate_grade(
                    grades["seatwork"],
                    grades["assignment"],
                    grades["quizzes"],
                    grades["exam"]
                )
                total_grade += final_grade
                course_count += 1
            
            if course_count > 0:
                average_grade = round(total_grade / course_count, 2)
                student_averages.append({
                    "id": student_id,
                    "name": student_info["name"],
                    "average": average_grade,
                    "courses": course_count
                })
        
        student_averages.sort(key=lambda x: x["average"], reverse=True)
        return student_averages
    
    @staticmethod
    def find_failing_grades(students):
        """
        Find all students with grades below 75%.
        Returns list of failing grade records.
        """
        failing_students = []
        
        for student_id, student_info in students.items():
            courses_list = student_info.get("courses", [])
            
            if not courses_list:
                continue
            
            for course in courses_list:
                grades = course["grades"]
                final_grade, remarks = Validator.calculate_grade(
                    grades["seatwork"],
                    grades["assignment"],
                    grades["quizzes"],
                    grades["exam"]
                )
                
                if final_grade < 75:
                    failing_students.append({
                        "id": student_id,
                        "name": student_info["name"],
                        "course": course["code"],
                        "subject": course["subject"],
                        "grade": final_grade
                    })
        
        return failing_students
    
    @staticmethod
    def format_grade_calculation(seatwork, assignment, quizzes, exam):
        """
        Format grade calculation result as display message.
        Returns formatted string with breakdown and final grade.
        """
        final_grade, remarks = Validator.calculate_grade(seatwork, assignment, quizzes, exam)
        class_standing = round((seatwork * 0.25 + assignment * 0.25 + quizzes * 0.50), 2)
        
        result_message = (
            f'=== GRADE CALCULATION ===\n\n'
            f"Seatwork: {seatwork}\n"
            f'Assignment: {assignment}\n'
            f"Quizzes: {quizzes}\n"
            f'Class Standing (40%): {class_standing}\n\n'
            f"Exam (60%): {exam}\n\n"
            f'FINAL GRADE: {final_grade}\n'
            f"REMARKS: {remarks}"
        )
        
        return result_message, final_grade, remarks
