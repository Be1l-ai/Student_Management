from utils.student_management import Ui_MainWindow
from utils.dialog_helper import DialogHelper
from utils.displaymanager import DisplayManager
from utils.validators import Validator
from utils.reports import ReportGenerator
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
import sys

class StudentManagement(QMainWindow):
    """Main window for Student Management System."""

    def __init__(self):
        """Initialize the app with default values and UI."""
        super().__init__()

        self.auth = {'username':'admin', 'password':'admin123'}
        self.students = {}
        self.courses = {}
        self.recent_actions = []
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.gui_setup()

        self.show()

    def gui_setup(self):
        """Connect UI buttons to their handlers."""
        # Navigation
        self.ui.loginButton.clicked.connect(self.login)
        self.ui.dashboardButton.clicked.connect(self.dashboard_main)
        self.ui.studentsButton.clicked.connect(self.page_students)
        
        # Student operations
        self.ui.addstudentButton.clicked.connect(self.add_student)
        self.ui.editstudentButton.clicked.connect(self.edit_student)
        self.ui.enrollstudentButton.clicked.connect(self.enroll_student)
        self.ui.deletestudentButton.clicked.connect(self.delete_student)
        self.ui.searchstudentButton.clicked.connect(self.search_student)
        self.ui.getstudentreportButton.clicked.connect(self.get_student_report)

        # Course operations
        self.ui.coursesButton.clicked.connect(self.page_courses)
        self.ui.addcourseButton.clicked.connect(self.add_course)
        self.ui.editcourseButton.clicked.connect(self.edit_course)
        self.ui.deletecourseButton.clicked.connect(self.delete_course)
        self.ui.searchcourseButton.clicked.connect(self.search_course)
        self.ui.getcoursereportButton.clicked.connect(self.get_course_report)

        # Tools
        self.ui.moreButoon.clicked.connect(self.more)
        self.ui.calcgradeButton.clicked.connect(self.calculate_grade_tool)
        self.ui.addgradeButton.clicked.connect(self.add_student_grade)
        self.ui.rankButton.clicked.connect(self.get_class_ranking)
        self.ui.failinfstudentButton.clicked.connect(self.find_failing_students)
        self.ui.logoutButton.clicked.connect(self.logout)

    def login(self):
        """Handle login with basic authentication."""
        username = self.ui.usernameInput.text()
        password = self.ui.passwordInput.text()

        if username == self.auth['username']:
            if password == self.auth['password']:
                self.ui.stackedWidget.setCurrentWidget(self.ui.pageMain)
                self.dashboard_main()
            else: 
                QMessageBox.warning(self, "error", 'Wrong Password')
        else:
            QMessageBox.warning(self, 'error', "Wrong Username")

    def dashboard_main(self):
        """Go to dashboard page."""
        self.ui.Main.setCurrentWidget(self.ui.pageDashboard)

    def page_students(self):
        """Go to students page and refresh table."""
        self.ui.Main.setCurrentWidget(self.ui.pageStudents)
        self.display_student_table()

    def page_courses(self):
        """Go to courses page and refresh table."""
        self.ui.Main.setCurrentWidget(self.ui.pageCourses)
        self.display_course_table()

    def more(self):
        """Go to tools page."""
        self.ui.Main.setCurrentWidget(self.ui.pageMore)


    def add_student(self):
        """Add new student with auto-generated ID."""
        new_student = DialogHelper.get_user_input(self, ['Name'], title="Add Student")
        if new_student:
            self.students[Validator.generate_id()] = {
                'name': new_student['Name'],
                'courses': []
            }
            QMessageBox.information(self, "Success", f"Added: {new_student['Name']}")
            self.add_recent_action(f"Added student: {new_student['Name']}")
            self.display_student_list()
            self.display_student_table()

    def display_student_list(self):
        """Update student list widget."""
        DisplayManager.display_list(self.students, self.ui.studentList, action=1)

    def add_course(self):
        """Add new course, checks for duplicates."""
        new_course = DialogHelper.get_user_input(self, ['Course Code', "Subject"], title="Add Course")
        if new_course:
            course_code = new_course['Course Code'].strip()
            if course_code in self.courses:
                QMessageBox.warning(
                   self, 'Duplicate Course',
                   f"Course code '{course_code}' already exists. Please use a different code."
                )
                return
            
            self.courses[course_code] = {
                'course': course_code, 
                'subject': new_course["Subject"]
            }
            QMessageBox.information(self, 'Success', f'New course: {course_code}')
            self.add_recent_action(f"Added course: {new_course['Subject']}")
            self.display_course_list()
            self.display_course_table()

    def edit_student(self):
        """Edit student name by ID."""
        if not Validator.check_has_students(self, self.students):
            return
        
        input_data = DialogHelper.get_required_input(self, ['Student ID'], title="Edit Student")
        if not input_data:
            return
        
        student_id = Validator.validate_student_id(self, input_data['Student ID'].strip(), self.students)
        if student_id is None:
            return
        
        current_name = self.students[student_id]['name']
        dialog_edit = DialogHelper.get_user_input_fill(self, ['Name'], title="Edit Student", chosen_name='Name', set_name=current_name)
        if not dialog_edit:
            return
        
        self.students[student_id]['name'] = dialog_edit['Name']
        QMessageBox.information(self, 'Success', f"Updated student {student_id}")
        self.add_recent_action(f"Edited student: {dialog_edit['Name']}")
        self.display_student_list()
        self.display_student_table()

    def delete_student(self):
        """Delete student after confirmation."""
        if not Validator.check_has_students(self, self.students):
            return
        
        input_data = DialogHelper.get_required_input(self, ['Student ID'], title="Delete Student")
        if not input_data:
            return
        
        student_id = Validator.validate_student_id(self, input_data['Student ID'].strip(), self.students)
        if student_id is None:
            return
        
        student_name = self.students[student_id]['name']
        reply = QMessageBox.question(
            self, 
            'Confirm Deletion', 
            f"Delete student {student_name} (ID: {student_id})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            del self.students[student_id]
            QMessageBox.information(self, "Success", f'Deleted student {student_name}')
            self.add_recent_action(f"Deleted student: {student_name}")
            self.display_student_list()
            self.display_student_table()

    def edit_course(self):
        """Edit course subject by code."""
        if not Validator.check_has_courses(self, self.courses):
            return
        
        input_data = DialogHelper.get_required_input(self, ['Course Code'], title="Edit Course")
        if not input_data:
            return
        
        course_code = input_data['Course Code'].strip()

        if not Validator.validate_course_code(self, course_code, self.courses):
            return
        
        current_subject = self.courses[course_code]['subject']
        dialog_edit = DialogHelper.get_user_input_fill(self, ['Subject'], title="Edit Course", chosen_name='Subject', set_name=current_subject)
        if not dialog_edit:
            return
        
        self.courses[course_code]['subject'] = dialog_edit['Subject']
        QMessageBox.information(self, 'Success', f"Updated course {course_code}")
        self.add_recent_action(f"Edited course: {course_code}")
        self.display_course_list()
        self.display_course_table()

    def delete_course(self):
        """Delete course after confirmation."""
        if not Validator.check_has_courses(self, self.courses):
            return
        
        input_data = DialogHelper.get_required_input(self, ['Course Code'], title="Delete Course")
        if not input_data:
            return
        
        course_code = input_data['Course Code'].strip()
        if not Validator.validate_course_code(self, course_code, self.courses):
            return
        
        course_subject = self.courses[course_code]['subject']
        reply = QMessageBox.question(
            self, 
            'Confirm Deletion', 
            f"Delete course {course_subject} ({course_code})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            del self.courses[course_code]
            QMessageBox.information(self, 'Success', f'Deleted course {course_code}')
            self.add_recent_action(f"Deleted course: {course_code}")
            self.display_course_list()
            self.display_course_table()

    def display_course_list(self):
        """Update course list widget."""
        DisplayManager.display_list(self.courses, self.ui.courseList, action=2)

    def add_recent_action(self, action):
        """Add action to recent list, keep last 10."""
        self.recent_actions.insert(0, action)
        if len(self.recent_actions) > 10:
            self.recent_actions = self.recent_actions[:10]
        self.display_recent_list()

    def display_recent_list(self):
        """Update recent actions list."""
        DisplayManager.display_list(self.recent_actions, self.ui.recentList, action=0)

    def display_student_table(self):
        """Update student table."""
        DisplayManager.display_table(self.students, self.ui.studentTable_2, action=1)

    def display_course_table(self):
        """Update course table."""
        DisplayManager.display_table(self.courses, self.ui.courseTable, action=2)
                        
    def enroll_student(self):
        """Enroll student in a course with empty grades."""
        if not Validator.check_has_students(self, self.students):
            return
        if not Validator.check_has_courses(self, self.courses):
            return
        
        input_data = DialogHelper.get_user_input(self, ['Student ID'], title="Enroll Student")
        if not input_data:
            return
        
        student_id = Validator.validate_student_id(self, input_data['Student ID'].strip(), self.students)
        if student_id is None:
            return
        
        course_data = DialogHelper.get_user_input(self, ['Course Code'], title="Enroll in Course")
        if not course_data:
            return
        
        course_code = course_data['Course Code'].strip()
        if not Validator.validate_course_code(self, course_code, self.courses):
            return
        
        student_courses = self.students[student_id].get('courses', [])
        if any(c['code'] == course_code for c in student_courses):
            QMessageBox.warning(self, "Error", f'Student already enrolled in {course_code}')
            return
        
        new_course = {
            'code': course_code,
            'subject': self.courses[course_code]['subject'],
            'grades': {'seatwork': 0, 'assignment': 0, 'quizzes': 0, 'exam': 0},
            'remarks': ''
        }
        self.students[student_id]['courses'].append(new_course)
        
        student_name = self.students[student_id]['name']
        QMessageBox.information(
           self, 'Success', 
           f"Enrolled {student_name} in {self.courses[course_code]['subject']}"
        )
        self.add_recent_action(f"Enrolled {student_name} in {course_code}")
        self.display_student_list()
        self.display_student_table()

    def search_student(self):
        """Search students by ID or name."""
        search_text = self.ui.searchstudentInput.text().strip()
        
        if not search_text:
            QMessageBox.warning(self, 'Error', "Please enter search text")
            return
        
        if not self.students:
            QMessageBox.warning(self, "Error", 'No students to search')
            return
        
        results = []
        
        try:
            search_id = int(search_text)
            if search_id in self.students:
                results.append((search_id, self.students[search_id]))
        except ValueError:
            search_lower = search_text.lower()
            for student_id, info in self.students.items():
                if search_lower in info['name'].lower():
                    results.append((student_id, info))
        
        if results:
            results_dict = {sid: info for sid, info in results}
            DisplayManager.display_table(results_dict, self.ui.studentTable_2, action=1)
            QMessageBox.information(self, 'Search Results', f"Found {len(results)} student(s)")
        else:
            QMessageBox.information(self, "Search Results", 'No students found')
            self.display_student_table() 

    def search_course(self):
        """Search courses by code or subject."""
        search_text = self.ui.searchcourseInput.text().strip()
        
        if not search_text:
            QMessageBox.warning(self, 'Error', "Please enter search text")
            return
        if not self.courses:
            QMessageBox.warning(self, "Error", 'No courses to search')
            return
        
        results = []
        search_lower = search_text.lower()

        for course_code, info in self.courses.items():
            if (search_lower in course_code.lower() or
                search_lower in info['subject'].lower()):
                results.append((course_code, info))
        
        if results:
            results_dict = {code: info for code, info in results}
            DisplayManager.display_table(results_dict, self.ui.courseTable, action=2)
            QMessageBox.information(self, 'Search Results', f"Found {len(results)} course(s)")
        else:
            QMessageBox.information(self, "Search Results", 'No courses found')
            self.display_course_table()

    def get_student_report(self):
        """Generate full report for a student with all courses and grades."""
        if not Validator.check_has_students(self, self.students):
            return
        
        input_data = DialogHelper.get_user_input(self, ['Student ID'], title="Student Report")
        if not input_data:
            return
        
        student_id = Validator.validate_student_id(self, input_data["Student ID"].strip(), self.students)
        if student_id is None:
            return
        
        student = self.students[student_id]
        report = ReportGenerator.build_student_report(student_id, student, self.students)
        
        DisplayManager.display_list(report, self.ui.studentreportList, action=0)
        self.add_recent_action(f"Generated report for {student['name']}")

    def get_course_report(self):
        """Generate report for a course showing all enrolled students."""
        if not Validator.check_has_courses(self, self.courses):
            return
        
        input_data = DialogHelper.get_user_input(self, ["Course Code"], title="Course Report")
        if not input_data:
            return
        
        course_code = input_data["Course Code"].strip()
        if not Validator.validate_course_code(self, course_code, self.courses):
            return
        
        course = self.courses[course_code]
        report = ReportGenerator.build_course_report(course_code, course, self.students)
        
        DisplayManager.display_list(report, self.ui.coursereportList, action=0)
        self.add_recent_action(f"Generated report for {course_code}")

    def calculate_grade_tool(self):
        """Grade calculator tool without affecting student records."""
        grades_input = DialogHelper.get_user_input(
            self, 
            ['Seatwork (0-100)', "Assignment (0-100)", 'Quizzes (0-100)', "Exam (0-100)"], 
            title="Calculate Grade Tool"
        )
        if not grades_input:
            return
        
        grades = Validator.validate_grades(self, grades_input)
        if grades is None:
            return
        
        result_message, final_grade, remarks = ReportGenerator.format_grade_calculation(
            grades['Seatwork (0-100)'],
            grades["Assignment (0-100)"],
            grades['Quizzes (0-100)'],
            grades["Exam (0-100)"]
        )
        
        QMessageBox.information(self, 'Grade Calculation Result', result_message)
        self.add_recent_action("Calculated grade using tool")

    def add_student_grade(self):
        """Add or update grades for a student in a course."""
        if not Validator.check_has_students(self, self.students):
            return
        
        input_data = DialogHelper.get_user_input(self, ['Student ID'], title="Add Student Grade")
        if not input_data:
            return
        
        student_id = Validator.validate_student_id(self, input_data["Student ID"].strip(), self.students)
        if student_id is None:
            return

        student = self.students[student_id]
        student_courses = student.get("courses", [])
        
        if not student_courses:
            QMessageBox.warning(self, "Error", "Student has no enrolled courses")
            return
        
        course_data = DialogHelper.get_user_input(self, ['Course Code'], title="Add Student Grade")
        if not course_data:
            return
        
        course_code = course_data["Course Code"].strip()
        target_course = Validator.find_student_course(self.students, student_id, course_code)
        
        if not target_course:
            QMessageBox.warning(self, "Error", f"Student not enrolled in {course_code}")
            return
        
        grades_input = DialogHelper.get_user_input(
            self,
            ["Seatwork (0-100)", "Assignment (0-100)", "Quizzes (0-100)", "Exam (0-100)"], 
            title="Add Student Grade"
        )
        if not grades_input:
            return
        
        grades = Validator.validate_grades(self, grades_input)
        if grades is None:
            return
        
        target_course["grades"]["seatwork"] = grades["Seatwork (0-100)"]
        target_course["grades"]["assignment"] = grades["Assignment (0-100)"]
        target_course["grades"]["quizzes"] = grades["Quizzes (0-100)"]
        target_course["grades"]["exam"] = grades["Exam (0-100)"]
        
        final_grade, remarks = Validator.calculate_grade(
            grades["Seatwork (0-100)"], 
            grades["Assignment (0-100)"], 
            grades["Quizzes (0-100)"], 
            grades["Exam (0-100)"]
        )
        target_course["remarks"] = remarks
        
        QMessageBox.information(
            self, 
            "Success", 
            f"Grades updated for {student['name']} in {course_code}\n"
            f"Final Grade: {final_grade} - {remarks}"
        )
        self.add_recent_action(f"Updated grades: {student['name']} - {course_code}")

    def get_class_ranking(self):
        """Generate ranking of all students by average grade."""
        if not Validator.check_has_students(self, self.students):
            return
        
        student_averages = ReportGenerator.calculate_class_ranking(self.students)
        
        if not student_averages:
            QMessageBox.information(self, "Class Ranking", "No students with grades to rank")
            return
        
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
        """Find all students with grades below 75%."""
        if not Validator.check_has_students(self, self.students):
            return
        
        failing_students = ReportGenerator.find_failing_grades(self.students)
        
        if not failing_students:
            QMessageBox.information(self, "Failing Students", "No failing students found!")
            self.ui.failingstudentList.clear()
            self.ui.failingstudentList.addItem("No failing students")
            return
        
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
        """Log out and return to login screen."""
        reply = QMessageBox.question(
            self,
            'Logout',
            "Are you sure you want to log out?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.ui.usernameInput.clear()
            self.ui.passwordInput.clear()
            self.ui.stackedWidget.setCurrentWidget(self.ui.pageLogin)
            QMessageBox.information(self, 'Logged Out', "Successfully logged out")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentManagement()
    sys.exit(app.exec())