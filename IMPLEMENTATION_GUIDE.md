# Student Management System - Complete Features Implementation

## Summary of All Functions

### 1. **Edit Student** (`editStudent()`)
- **Purpose**: Modify existing student information
- **How it works**:
  - Prompts user to enter Student ID
  - Validates the ID exists in the system
  - Shows current student name in a pre-filled dialog
  - Updates the student record with new name
  - Logs action to recent activity
  - Refreshes both list and table displays

### 2. **Delete Student** (`deleteStudent()`)
- **Purpose**: Remove a student from the system
- **How it works**:
  - Prompts user to enter Student ID
  - Validates the ID exists
  - Shows confirmation dialog with student details
  - Deletes the student upon confirmation
  - Logs action to recent activity
  - Refreshes both list and table displays

### 3. **Edit Course** (`editCourse()`)
- **Purpose**: Modify existing course information
- **How it works**:
  - Prompts user to enter Course Code
  - Validates the course exists
  - Shows current course subject in a pre-filled dialog
  - Updates the course record
  - Logs action to recent activity
  - Refreshes both list and table displays

### 4. **Delete Course** (`deleteCourse()`)
- **Purpose**: Remove a course from the system
- **How it works**:
  - Prompts user to enter Course Code
  - Validates the course exists
  - Shows confirmation dialog with course details
  - Deletes the course upon confirmation
  - Logs action to recent activity
  - Refreshes both list and table displays

### 5. **Display Course List** (`displayCourseList()`)
- **Purpose**: Show all courses on the dashboard
- **Widget**: `courseList` (QListView on dashboard)
- **Format**: Displays as "COURSE_CODE: Subject Name"
- **Updates**: Automatically called after adding/editing/deleting courses

### 6. **Display Recent List** (`displayRecentList()`)
- **Purpose**: Track and show recent actions on the dashboard
- **Widget**: `recentList` (QListView on dashboard)
- **Features**:
  - Tracks last 10 actions
  - Shows newest actions first
  - Automatically updates when actions are performed

### 7. **Display Student Table** (`displayStudentTable()`) ✨ NEW
- **Purpose**: Show all students in a tabular format
- **Widget**: `studentTable_2` (QTableView on Students page)
- **Columns**: Student ID, Name, Course Code, Subject
- **Features**: Auto-resizes columns, updates automatically

### 8. **Display Course Table** (`displayCourseTable()`) ✨ NEW
- **Purpose**: Show all courses in a tabular format
- **Widget**: `courseTable` (QTableView on Courses page)
- **Columns**: Course Code, Subject
- **Features**: Auto-resizes columns, updates automatically

### 9. **Enroll Student** (`enrollStudent()`) ✨ NEW
- **Purpose**: Assign a course to a student
- **How it works**:
  - Prompts for Student ID
  - Validates student exists
  - Prompts for Course Code
  - Validates course exists
  - Enrolls student in the selected course
  - Updates student's course information
  - Logs action and refreshes displays

### 10. **Get Student Report** (`getStudentReport()`) ✨ NEW
- **Purpose**: Generate detailed student report with grade calculation
- **Widget**: `studentreportList` (QListView on Students page, Tab 2)
- **Shows**:
  - Student ID and Name
  - Enrolled course
  - Individual grades (seatwork, assignment, quizzes, exam)
  - Calculated class standing
  - Final grade
  - Pass/Fail status
- **Grade Calculation**:
  - Class Standing (40% of final): 25% seatwork + 25% assignment + 50% quizzes
  - Exam (60% of final): Direct score (0-100)
  - Passing Grade: 75%

### 11. **Get Course Report** (`getCourseReport()`) ✨ NEW
- **Purpose**: Generate course report showing all enrolled students
- **Widget**: `coursereportList` (QListView on Courses page, Tab 2)
- **Shows**:
  - Course Code and Subject
  - Total number of enrolled students
  - List of all enrolled students with IDs

### 12. **Calculate Grade** (`calculateGrade()`) ✨ NEW
- **Purpose**: Calculate final grade based on grading scheme
- **Formula**:
  ```
  Class Standing = (seatwork × 0.25) + (assignment × 0.25) + (quizzes × 0.50)
  Final Grade = (Class Standing × 0.40) + (exam × 0.60)
  Remarks = "PASSED" if Final Grade ≥ 75 else "FAILED"
  ```

## Grade Calculation System

### Grading Components:
1. **Class Standing (40% of final grade)**
   - Seatwork: 25% of class standing
   - Assignment: 25% of class standing
   - Quizzes: 50% of class standing

2. **Exam (60% of final grade)**
   - Score range: 0-100
   - Directly contributes 60% to final grade

3. **Passing Grade**: 75%

### Example Calculation:
```
Given:
- Seatwork: 80
- Assignment: 85
- Quizzes: 90
- Exam: 88

Class Standing = (80 × 0.25) + (85 × 0.25) + (90 × 0.50)
               = 20 + 21.25 + 45
               = 86.25

Final Grade = (86.25 × 0.40) + (88 × 0.60)
            = 34.5 + 52.8
            = 87.3

Remarks: PASSED (≥ 75)
```

## GUI Connections

All buttons have been connected in the `guisetup()` method:

```python
# Student buttons
self.ui.addstudentButton.clicked.connect(self.addStudent)
self.ui.editstudentButton.clicked.connect(self.editStudent)
self.ui.enrollstudentButton.clicked.connect(self.enrollStudent)  # NEW
self.ui.deletestudentButton.clicked.connect(self.deleteStudent)
self.ui.getstudentreportButton.clicked.connect(self.getStudentReport)  # NEW

# Course buttons
self.ui.addcourseButton.clicked.connect(self.addCourse)
self.ui.editcourseButton.clicked.connect(self.editCourse)
self.ui.deletecourseButton.clicked.connect(self.deleteCourse)
self.ui.getcoursereportButton.clicked.connect(self.getCourseReport)  # NEW
```

## Global Variables Added

- `recent_actions = []` - List to store recent activity

## Usage Instructions

### To Enroll a Student in a Course: ✨ NEW
1. Navigate to Students page
2. Click "Enroll Student" button
3. Enter the Student ID (5-digit number)
4. Enter the Course Code (e.g., MATH101)
5. Click OK to confirm enrollment
6. Student's course information will be updated

### To Generate a Student Report: ✨ NEW
1. Navigate to Students page
2. Click on "Tab 2" (Student Report)
3. Click "Get Student Report" button
4. Enter the Student ID
5. View the detailed report showing:
   - Personal information
   - Course enrollment
   - All grades
   - Calculated final grade
   - Pass/Fail status

### To Generate a Course Report: ✨ NEW
1. Navigate to Courses page
2. Click on "Tab 2" (Course Report)
3. Click "Get Course Report" button
4. Enter the Course Code
5. View the report showing:
   - Course details
   - Number of enrolled students
   - List of all students in the course

### To View Student Table: ✨ NEW
1. Navigate to Students page
2. View "Tab 1" (Student List)
3. See all students in tabular format with:
   - Student ID
   - Name
   - Course Code
   - Subject

### To View Course Table: ✨ NEW
1. Navigate to Courses page
2. View "Tab 1" (Course List)
3. See all courses in tabular format with:
   - Course Code
   - Subject

### To Edit a Student:
1. Navigate to Students page
2. Click "Edit Student" button
3. Enter the Student ID (5-digit number)
4. Modify the name in the dialog
5. Click OK to confirm

### To Delete a Student:
1. Navigate to Students page
2. Click "Delete Student" button
3. Enter the Student ID
4. Confirm deletion in the popup dialog

### To Edit a Course:
1. Navigate to Courses page
2. Click "Edit Course" button
3. Enter the Course Code
4. Modify the subject name
5. Click OK to confirm

### To Delete a Course:
1. Navigate to Courses page
2. Click "Delete Course" button
3. Enter the Course Code
4. Confirm deletion in the popup dialog

### To View Dashboard Lists:
1. Go to Dashboard
2. **Student List** (left side) - Shows all students with IDs
3. **Course List** (right side) - Shows all courses with codes
4. **Recent List** (bottom) - Shows last 10 actions performed

## Error Handling

All functions include:
- Empty list validation (checks if students/courses exist)
- ID/Code validation (checks if the entered ID exists)
- Input format validation
- User confirmation for deletions
- Success/error message boxes
- Proper exception handling for invalid inputs

## Data Structure

### Student Object:
```python
{
    student_id: {
        "name": "Student Name",
        "course": {
            "Course code": "MATH101",
            "subject": "Mathematics",
            "grade": {
                "class standing": {
                    "seatwok": 0,
                    "assignment": 0,
                    "quizzes": 0
                },
                "exam": 0
            }
        },
        "remarks": "PASSED/FAILED"
    }
}
```

### Course Object:
```python
{
    "COURSE_CODE": {
        "course": "COURSE_CODE",
        "subject": "Subject Name"
    }
}
```

## Notes

- All display functions automatically update when data changes
- Recent actions are limited to 10 most recent items
- Delete operations require confirmation to prevent accidents
- All actions are logged to the recent activity list
- Tables automatically resize columns for better readability
- Grade calculations follow the specified formula
- Student remarks are automatically updated when reports are generated
