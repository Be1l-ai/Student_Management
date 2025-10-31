from Student_Management import Ui_MainWindow
from dialog import Ui_Dialog
from displaymanager import DisplayManager
from PyQt6.QtWidgets import QWidget, QDialog, QMainWindow, QApplication, QMessageBox, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt

import sys
import random

auth = {'username':'admin', 'password':'admin123'}
students = {}
courses = {}
recent_actions = []  # recent actions for dashboard

class DialogPop(QDialog):
    # custom dialog for getting input
    def __init__(self, fields, parent=None):
        super().__init__(parent)
       
        self.ui_dialog = Ui_Dialog()
        self.ui_dialog.setupUi(self)

        layout = self.ui_dialog.frame_dialog.layout()

        self.inputs = {}

        for field in fields:
            label = QLabel(f'{field}:')
            input_field = QLineEdit()
            layout.addWidget(label)
            layout.addWidget(input_field)
            self.inputs[field] = input_field

        self.ui_dialog.buttonBox.accepted.disconnect() 
        self.ui_dialog.buttonBox.accepted.connect(self.check)
        self.ui_dialog.buttonBox.rejected.connect(self.reject)

    def check(self):
        # make sure all fields filled
        if all(field.text().strip() for field in self.inputs.values()):
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Missing Input')

    def get_input(self):
        # get all the input values
        return {key: value.text() for key, value in self.inputs.items()}

class StudentManagement(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.gui_setup()

        self.show()

    def gui_setup(self):
        # connecting buttons
        self.ui.loginButton.clicked.connect(self.login)
        self.ui.dashboardButton.clicked.connect(self.dashboard_main)

        self.ui.studentsButton.clicked.connect(self.students)
        self.ui.addstudentButton.clicked.connect(self.add_student)
        self.ui.editstudentButton.clicked.connect(self.edit_student)
        self.ui.enrollstudentButton.clicked.connect(self.enroll_student)
        self.ui.deletestudentButton.clicked.connect(self.delete_student)
        self.ui.searchstudentButton.clicked.connect(self.search_student)
        self.ui.getstudentreportButton.clicked.connect(self.get_student_report)

        self.ui.coursesButton.clicked.connect(self.courses)
        self.ui.addcourseButton.clicked.connect(self.add_course)
        self.ui.editcourseButton.clicked.connect(self.edit_course)
        self.ui.deletecourseButton.clicked.connect(self.delete_course)
        self.ui.searchcourseButton.clicked.connect(self.search_course)
        self.ui.getcoursereportButton.clicked.connect(self.get_course_report)

        self.ui.moreButoon.clicked.connect(self.more)
        self.ui.calcgradeButton.clicked.connect(self.calculate_grade_tool)
        self.ui.addgradeButton.clicked.connect(self.add_student_grade)
        self.ui.rankButton.clicked.connect(self.get_class_ranking)
        self.ui.failinfstudentButton.clicked.connect(self.find_failing_students)
        self.ui.logoutButton.clicked.connect(self.logout)

    def login(self):
        username = self.ui.usernameInput.text()
        password = self.ui.passwordInput.text()

        if username == auth['username']:
            if password == auth['password']:
                self.ui.stackedWidget.setCurrentWidget(self.ui.pageMain)
                self.dashboard_main()
            else: 
                QMessageBox.warning(self, "error", 'Wrong Password')
        else:
            QMessageBox.warning(self, 'error', "Wrong Username")

    def dashboard_main(self):
        # go to dashboard
        self.ui.Main.setCurrentWidget(self.ui.pageDashboard)

    def students(self):
        # students page
        self.ui.Main.setCurrentWidget(self.ui.pageStudents)
        self.display_student_table()

    def courses(self):
        # courses page
        self.ui.Main.setCurrentWidget(self.ui.pageCourses)
        self.display_course_table()

    def more(self):
        # more page
        self.ui.Main.setCurrentWidget(self.ui.pageMore)

    def generate_id(self):
        # random 5 digit id
        return random.randint(10**4, (10**5)-1)

    def add_student(self):
        # add new student
        dialog_student = DialogPop(['Name'], parent=self)
        if dialog_student.exec() == QDialog.DialogCode.Accepted:
            new_student = dialog_student.get_input()
            if new_student:
                students[self.generate_id()] = {
                    'name': new_student['Name'],
                    'courses': []  # can enroll in multiple courses
                }
                QMessageBox.information(self, "Success", f"Added: {new_student['Name']}")
                self.add_recent_action(f"Added student: {new_student['Name']}")
                self.display_student_list()
                self.display_student_table()

    def display_student_list(self):
        # show students in dashboard
        DisplayManager.display_list(students, self.ui.studentList, action=1)


    def add_course(self):
        # add a new course
        dialog_course = DialogPop(['Course Code', "Subject"], parent=self)
        if dialog_course.exec() == QDialog.DialogCode.Accepted:
            new_course = dialog_course.get_input()
            if new_course:
                course_code = new_course['Course Code'].strip()
                
                # check if code exists already
                if course_code in courses:
                    QMessageBox.warning(
                        self, 
                        'Duplicate Course', 
                        f"Course code '{course_code}' already exists. Please use a different code."
                    )
                    return
                
                courses[course_code] = {
                    'course': course_code, 
                    'subject': new_course["Subject"]
                }
                QMessageBox.information(self, 'Success', f'New course: {course_code}')
                self.add_recent_action(f"Added course: {new_course['Subject']}")
                self.display_course_list()
                self.display_course_table()

    def edit_student(self):
        # edit student info
        if not students:
            QMessageBox.warning(self, 'Error', "No students available to edit")
            return
        
        dialog_select = DialogPop(['Student ID'], parent=self)
        
        if dialog_select.exec() == QDialog.DialogCode.Accepted:
            input_data = dialog_select.get_input()
            student_id = input_data.get('Student ID', '').strip()
            
            try:
                student_id = int(student_id)
                if student_id not in students:
                    QMessageBox.warning(self, "Error", f'Student ID {student_id} not found')
                    return
                
                # get current name first
                current_name = students[student_id]['name']
                dialog_edit = DialogPop(['Name'], parent=self)
                dialog_edit.inputs['Name'].setText(current_name)
                
                if dialog_edit.exec() == QDialog.DialogCode.Accepted:
                    new_data = dialog_edit.get_input()
                    students[student_id]['name'] = new_data['Name']
                    QMessageBox.information(self, 'Success', f"Updated student {student_id}")
                    self.add_recent_action(f"Edited student: {new_data['Name']}")
                    self.display_student_list()
                    self.display_student_table()
                    
            except ValueError:
                QMessageBox.warning(self, "Error", 'Invalid Student ID format')

    def delete_student(self):
        # delete a student
        if not students:
            QMessageBox.warning(self, 'Error', "No students to delete")
            return
        
        dialog_select = DialogPop(['Student ID'], parent=self)
        
        if dialog_select.exec() == QDialog.DialogCode.Accepted:
            input_data = dialog_select.get_input()
            student_id = input_data.get('Student ID', '').strip()
            
            try:
                student_id = int(student_id)
                if student_id not in students:
                    QMessageBox.warning(self, "Error", f'Student ID {student_id} not found')
                    return
                
                student_name = students[student_id]['name']
                reply = QMessageBox.question(
                    self, 
                    'Confirm Deletion', 
                    f"Delete student {student_name} (ID: {student_id})?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    del students[student_id]
                    QMessageBox.information(self, "Success", f'Deleted student {student_name}')
                    self.add_recent_action(f"Deleted student: {student_name}")
                    self.display_student_list()
                    self.display_student_table()
                    
            except ValueError:
                QMessageBox.warning(self, 'Error', "Invalid Student ID format")

    def edit_course(self):
        # edit course
        if not courses:
            QMessageBox.warning(self, 'Error', "No courses available to edit")
            return
        
        dialog_select = DialogPop(['Course Code'], parent=self)
        
        if dialog_select.exec() == QDialog.DialogCode.Accepted:
            input_data = dialog_select.get_input()
            course_code = input_data.get('Course Code', '').strip()
            
            if course_code not in courses:
                QMessageBox.warning(self, "Error", f'Course {course_code} not found')
                return
            
            # show what it is currently
            current_subject = courses[course_code]['subject']
            dialog_edit = DialogPop(['Subject'], parent=self)
            dialog_edit.inputs['Subject'].setText(current_subject)
            
            if dialog_edit.exec() == QDialog.DialogCode.Accepted:
                new_data = dialog_edit.get_input()
                courses[course_code]['subject'] = new_data['Subject']
                QMessageBox.information(self, 'Success', f"Updated course {course_code}")
                self.add_recent_action(f"Edited course: {course_code}")
                self.display_course_list()
                self.display_course_table()

    def delete_course(self):
        # delete course
        if not courses:
            QMessageBox.warning(self, 'Error', "No courses to delete")
            return
        
        dialog_select = DialogPop(['Course Code'], parent=self)
        
        if dialog_select.exec() == QDialog.DialogCode.Accepted:
            input_data = dialog_select.get_input()
            course_code = input_data.get('Course Code', '').strip()
            
            if course_code not in courses:
                QMessageBox.warning(self, "Error", f'Course {course_code} not found')
                return
            
            course_subject = courses[course_code]['subject']
            reply = QMessageBox.question(
                self, 
                'Confirm Deletion', 
                f"Delete course {course_subject} ({course_code})?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                del courses[course_code]
                QMessageBox.information(self, 'Success', f'Deleted course {course_code}')
                self.add_recent_action(f"Deleted course: {course_code}")
                self.display_course_list()
                self.display_course_table()

    def display_course_list(self):
        # show courses in dashboard
        DisplayManager.display_list(courses, self.ui.courseList, action=2)

    def add_recent_action(self, action):
        # add to recent actions list
        global recent_actions
        recent_actions.insert(0, action)  # add at beginning
        # only keep 10
        if len(recent_actions) > 10:
            recent_actions = recent_actions[:10]
        self.display_recent_list()

    def display_recent_list(self):
        # display recent actions
        DisplayManager.display_list(recent_actions, self.ui.recentList, action=0)

    def display_student_table(self):
        # display students in table
        DisplayManager.display_table(students, self.ui.studentTable_2, action=1)

    def display_course_table(self):
        # show courses in table
        DisplayManager.display_table(courses, self.ui.courseTable, action=2)
                        
    def enroll_student(self):
        # enroll student in course
        if not students:
            QMessageBox.warning(self, 'Error', "No students available")
            return
        
        if not courses:
            QMessageBox.warning(self, "Error", 'No courses available')
            return
        
        # get student id first
        dialog_student = DialogPop(['Student ID'], parent=self)
        if dialog_student.exec() == QDialog.DialogCode.Accepted:
            input_data = dialog_student.get_input()
            student_id = input_data.get('Student ID', '').strip()
            
            try:
                student_id = int(student_id)
                if student_id not in students:
                    QMessageBox.warning(self, "Error", f'Student ID {student_id} not found')
                    return
                
                # get course code
                dialog_course = DialogPop(['Course Code'], parent=self)
                if dialog_course.exec() == QDialog.DialogCode.Accepted:
                    course_data = dialog_course.get_input()
                    course_code = course_data.get('Course Code', '').strip()
                    
                    if course_code not in courses:
                        QMessageBox.warning(self, 'Error', f"Course {course_code} not found")
                        return
                    
                    # check if already enrolled
                    student_courses = students[student_id].get('courses', [])
                    if any(c['code'] == course_code for c in student_courses):
                        QMessageBox.warning(self, "Error", f'Student already enrolled in {course_code}')
                        return
                    
                    # add course to student
                    new_course = {
                        'code': course_code,
                        'subject': courses[course_code]['subject'],
                        'grades': {
                            'seatwork': 0,
                            'assignment': 0,
                            'quizzes': 0,
                            'exam': 0
                        },
                        'remarks': ''
                    }
                    students[student_id]['courses'].append(new_course)
                    
                    student_name = students[student_id]['name']
                    QMessageBox.information(
                        self, 
                        'Success', 
                        f"Enrolled {student_name} in {courses[course_code]['subject']}"
                    )
                    self.add_recent_action(f"Enrolled {student_name} in {course_code}")
                    self.display_student_list()
                    self.display_student_table()
                    
            except ValueError:
                QMessageBox.warning(self, 'Error', "Invalid Student ID format")

    def search_student(self):
        # search students
        search_text = self.ui.searchstudentInput.text().strip()
        
        if not search_text:
            QMessageBox.warning(self, 'Error', "Please enter search text")
            return
        
        if not students:
            QMessageBox.warning(self, "Error", 'No students to search')
            return
        
        # results list
        results = []
        
        # try searching by id
        try:
            search_id = int(search_text)
            if search_id in students:
                results.append((search_id, students[search_id]))
        except ValueError:
            # search by name instead
            search_lower = search_text.lower()
            for student_id, info in students.items():
                if search_lower in info['name'].lower():
                    results.append((student_id, info))
        
        # show results in table
        if results:
            # convert results list to dict for DisplayManager
            results_dict = {sid: info for sid, info in results}
            DisplayManager.display_table(results_dict, self.ui.studentTable_2, action=1)
            QMessageBox.information(self, 'Search Results', f"Found {len(results)} student(s)")
        else:
            QMessageBox.information(self, "Search Results", 'No students found')
            self.display_student_table()  # show all again

    def search_course(self):
        # search courses
        search_text = self.ui.searchcourseInput.text().strip()
        
        if not search_text:
            QMessageBox.warning(self, 'Error', "Please enter search text")
            return
        
        if not courses:
            QMessageBox.warning(self, "Error", 'No courses to search')
            return
        
        # search results
        results = []
        search_lower = search_text.lower()
        
        for course_code, info in courses.items():
            if (search_lower in course_code.lower() or 
                search_lower in info['subject'].lower()):
                results.append((course_code, info))
        
        # show results
        if results:
            # convert results list to dict for DisplayManager
            results_dict = {code: info for code, info in results}
            DisplayManager.display_table(results_dict, self.ui.courseTable, action=2)
            QMessageBox.information(self, 'Search Results', f"Found {len(results)} course(s)")
        else:
            QMessageBox.information(self, "Search Results", 'No courses found')
            self.display_course_table()  # reset to show all

    def calculate_grade(self, seatwork, assignment, quizzes, exam):
        # calculate grade
        # class standing 40%: seatwork 25%, assignment 25%, quizzes 50%
        # exam 60%
        # passing is 75%
        class_standing = (seatwork * 0.25) + (assignment * 0.25) + (quizzes * 0.50)
        
        # final grade
        final_grade = (class_standing * 0.40) + (exam * 0.60)
        
        # check if passed
        remarks = 'PASSED' if final_grade >= 75 else 'FAILED'
        
        return round(final_grade, 2), remarks

    def get_student_report(self):
        """Generate and display a detailed report for a student (all courses)"""
        if not students:
            QMessageBox.warning(self, "Error", "No students available")
            return
        
        dialog_select = DialogPop(["Student ID"], parent=self)
        if dialog_select.exec() == QDialog.DialogCode.Accepted:
            input_data = dialog_select.get_input()
            student_id = input_data.get("Student ID", "").strip()
            
            try:
                student_id = int(student_id)
                if student_id not in students:
                    QMessageBox.warning(self, "Error", f"Student ID {student_id} not found")
                    return
                
                student = students[student_id]
                
                # Build report
                report = [
                    f"=== STUDENT REPORT ===",
                    f"Student ID: {student_id}",
                    f"Name: {student['name']}",
                    f"",
                ]
                
                # Get all enrolled courses
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
                        
                        final_grade, remarks = self.calculate_grade(seatwork, assignment, quizzes, exam)
                        
                        # Update course remarks
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
                
                # Display in list view
                DisplayManager.display_list(report, self.ui.studentreportList, action=0)
                self.add_recent_action(f"Generated report for {student['name']}")
                
            except ValueError:
                QMessageBox.warning(self, "Error", "Invalid Student ID format")

    def get_course_report(self):
        """Generate and display a report for a course showing enrolled students"""
        if not courses:
            QMessageBox.warning(self, "Error", "No courses available")
            return
        
        dialog_select = DialogPop(["Course Code"], parent=self)
        if dialog_select.exec() == QDialog.DialogCode.Accepted:
            input_data = dialog_select.get_input()
            course_code = input_data.get("Course Code", "").strip()
            
            if course_code not in courses:
                QMessageBox.warning(self, "Error", f"Course {course_code} not found")
                return
            
            course = courses[course_code]
            
            # Find all students enrolled in this course
            enrolled_students = []
            for student_id, student_info in students.items():
                # Check if student has this course in their courses list
                for student_course in student_info.get("courses", []):
                    if student_course["code"] == course_code:
                        enrolled_students.append({
                            "id": student_id,
                            "name": student_info["name"]
                        })
                        break
            
            # Build report
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
            
            # Display in list view
            DisplayManager.display_list(report, self.ui.coursereportList, action=0)
            self.add_recent_action(f"Generated report for course {course_code}")

    def calculate_grade_tool(self):
        # calculate grade tool
        dialog_grades = DialogPop(['Seatwork (0-100)', "Assignment (0-100)", 'Quizzes (0-100)', "Exam (0-100)"], parent=self)
        
        if dialog_grades.exec() == QDialog.DialogCode.Accepted:
            grades_input = dialog_grades.get_input()
            
            try:
                seatwork = float(grades_input['Seatwork (0-100)'])
                assignment = float(grades_input["Assignment (0-100)"])
                quizzes = float(grades_input['Quizzes (0-100)'])
                exam = float(grades_input["Exam (0-100)"])
                
                # check if valid range
                if not all(0 <= grade <= 100 for grade in [seatwork, assignment, quizzes, exam]):
                    QMessageBox.warning(self, 'Error', "All grades must be between 0 and 100")
                    return
                
                final_grade, remarks = self.calculate_grade(seatwork, assignment, quizzes, exam)
                
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
                
                QMessageBox.information(self, 'Grade Calculation Result', result_message)
                self.add_recent_action("Calculated grade using tool")
                
            except ValueError:
                QMessageBox.warning(self, "Error", 'Please enter valid numeric values')

    def add_student_grade(self):
        """Add or update grades for a student in a specific course"""
        if not students:
            QMessageBox.warning(self, "Error", "No students available")
            return
        
        # Get student ID
        dialog_student = DialogPop(["Student ID"], parent=self)
        if dialog_student.exec() == QDialog.DialogCode.Accepted:
            input_data = dialog_student.get_input()
            student_id = input_data.get("Student ID", "").strip()
            
            try:
                student_id = int(student_id)
                if student_id not in students:
                    QMessageBox.warning(self, "Error", f"Student ID {student_id} not found")
                    return
                
                student = students[student_id]
                student_courses = student.get("courses", [])
                
                if not student_courses:
                    QMessageBox.warning(self, "Error", "Student has no enrolled courses")
                    return
                
                # Get course code
                dialog_course = DialogPop(["Course Code"], parent=self)
                if dialog_course.exec() == QDialog.DialogCode.Accepted:
                    course_data = dialog_course.get_input()
                    course_code = course_data.get("Course Code", "").strip()
                    
                    # Find the course in student's courses
                    target_course = None
                    for course in student_courses:
                        if course["code"] == course_code:
                            target_course = course
                            break
                    
                    if not target_course:
                        QMessageBox.warning(self, "Error", f"Student not enrolled in {course_code}")
                        return
                    
                    # Get grades
                    dialog_grades = DialogPop(
                        ["Seatwork (0-100)", "Assignment (0-100)", "Quizzes (0-100)", "Exam (0-100)"], 
                        parent=self
                    )
                    
                    if dialog_grades.exec() == QDialog.DialogCode.Accepted:
                        grades_input = dialog_grades.get_input()
                        
                        try:
                            seatwork = float(grades_input["Seatwork (0-100)"])
                            assignment = float(grades_input["Assignment (0-100)"])
                            quizzes = float(grades_input["Quizzes (0-100)"])
                            exam = float(grades_input["Exam (0-100)"])
                            
                            # Validate ranges
                            if not all(0 <= grade <= 100 for grade in [seatwork, assignment, quizzes, exam]):
                                QMessageBox.warning(self, "Error", "All grades must be between 0 and 100")
                                return
                            
                            # Update grades
                            target_course["grades"]["seatwork"] = seatwork
                            target_course["grades"]["assignment"] = assignment
                            target_course["grades"]["quizzes"] = quizzes
                            target_course["grades"]["exam"] = exam
                            
                            # Calculate and update remarks
                            final_grade, remarks = self.calculate_grade(seatwork, assignment, quizzes, exam)
                            target_course["remarks"] = remarks
                            
                            QMessageBox.information(
                                self, 
                                "Success", 
                                f"Grades updated for {student['name']} in {course_code}\n"
                                f"Final Grade: {final_grade} - {remarks}"
                            )
                            self.add_recent_action(f"Updated grades: {student['name']} - {course_code}")
                            
                        except ValueError:
                            QMessageBox.warning(self, "Error", "Please enter valid numeric values")
                    
            except ValueError:
                QMessageBox.warning(self, "Error", "Invalid Student ID format")

    def get_class_ranking(self):
        """Calculate and display class ranking based on average grades"""
        if not students:
            QMessageBox.warning(self, "Error", "No students available")
            return
        
        # Calculate average grade for each student
        student_averages = []
        
        for student_id, student_info in students.items():
            courses_list = student_info.get("courses", [])
            
            if not courses_list:
                continue  # Skip students with no courses
            
            # Calculate average final grade across all courses
            total_grade = 0
            course_count = 0
            
            for course in courses_list:
                grades = course["grades"]
                final_grade, _ = self.calculate_grade(
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
        
        if not student_averages:
            QMessageBox.information(self, "Class Ranking", "No students with grades to rank")
            return
        
        # Sort by average grade (descending)
        student_averages.sort(key=lambda x: x["average"], reverse=True)
        
        # Display in list widget
        self.ui.failingstudentList.clear()
        
        for rank, student in enumerate(student_averages, 1):
            rank_text = f"#{rank} - {student['name']} (ID: {student['id']}) | Avg: {student['average']}% | Courses: {student['courses']}"
            self.ui.failingstudentList.addItem(rank_text)
        
        QMessageBox.information(
            self, 
            "Class Ranking", 
            f"Displayed ranking for {len(student_averages)} student(s)"
        )
        self.add_recent_action("Generated class ranking")

    def find_failing_students(self):
        """Find and display all students with failing grades (below 75%)"""
        if not students:
            QMessageBox.warning(self, "Error", "No students available")
            return
        
        failing_students = []
        
        for student_id, student_info in students.items():
            courses_list = student_info.get("courses", [])
            
            if not courses_list:
                continue  # Skip students with no courses
            
            # Check each course for failing grades
            for course in courses_list:
                grades = course["grades"]
                final_grade, remarks = self.calculate_grade(
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
        
        if not failing_students:
            QMessageBox.information(self, "Failing Students", "No failing students found!")
            self.ui.failingstudentList.clear()
            self.ui.failingstudentList.addItem("No failing students - Great job! 🎉")
            return
        
        # Display in list widget
        self.ui.failingstudentList.clear()
        
        for student in failing_students:
            fail_text = (
                f"{student['name']} (ID: {student['id']}) | "
                f"{student['course']}: {student['subject']} | "
                f"Grade: {student['grade']}% - FAILED"
            )
            self.ui.failingstudentList.addItem(fail_text)
        
        QMessageBox.warning(
            self, 
            "Failing Students", 
            f"Found {len(failing_students)} failing grade(s)"
        )
        self.add_recent_action("Found failing students")

    def logout(self):
        # logout
        reply = QMessageBox.question(
            self,
            'Logout',
            "Are you sure you want to log out?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # clear login stuff
            self.ui.usernameInput.clear()
            self.ui.passwordInput.clear()
            
            # go back to login
            self.ui.stackedWidget.setCurrentWidget(self.ui.pageLogin)
            
            QMessageBox.information(self, 'Logged Out', "Successfully logged out")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentManagement()
    sys.exit(app.exec())