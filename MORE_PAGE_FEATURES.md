# MORE Page Features - Implementation Guide

## Overview
This document describes all the functionality implemented for the MORE page, including the 5 main buttons and validation improvements.

---

## Features Implemented

### 1. **Calculate Grade Button** (`calcgradeButton`)
**Function:** `calculate_grade_tool()`

**Purpose:** Standalone grade calculator tool that doesn't require student data.

**How to Use:**
1. Click "Calculate Grade" button on MORE page
2. Enter the following grades (0-100):
   - Seatwork
   - Assignment
   - Quizzes
   - Exam
3. View the calculated result showing:
   - Class Standing (40%)
   - Final Grade
   - Remarks (PASSED/FAILED)

**Validation:**
- All grades must be between 0 and 100
- All fields must be numeric

**Example Output:**
```
=== GRADE CALCULATION ===

Seatwork: 85
Assignment: 90
Quizzes: 88
Class Standing (40%): 87.75

Exam (60%): 92

FINAL GRADE: 90.3
REMARKS: PASSED
```

---

### 2. **Add Student Grade Button** (`addgradeButton`)
**Function:** `add_student_grade()`

**Purpose:** Add or update grades for a specific student in a specific course.

**How to Use:**
1. Click "Add Student Grade" button on MORE page
2. Enter Student ID
3. Enter Course Code (must be enrolled)
4. Enter all grades:
   - Seatwork (0-100)
   - Assignment (0-100)
   - Quizzes (0-100)
   - Exam (0-100)
5. System automatically calculates and saves final grade and remarks

**Validation:**
- Student ID must exist
- Student must be enrolled in the specified course
- All grades must be between 0 and 100

**What Gets Updated:**
- Seatwork grade
- Assignment grade
- Quizzes grade
- Exam grade
- Remarks (PASSED/FAILED)

---

### 3. **Get Class Ranking Button** (`rankButton`)
**Function:** `get_class_ranking()`

**Purpose:** Display all students ranked by their average grades across all courses.

**How to Use:**
1. Click "Get Class Ranking" button on MORE page
2. View ranked list in the failing student list area

**Display Format:**
```
#1 - John Doe (ID: 12345) | Avg: 92.5% | Courses: 3
#2 - Jane Smith (ID: 67890) | Avg: 88.3% | Courses: 2
#3 - Bob Johnson (ID: 11111) | Avg: 76.0% | Courses: 4
```

**Features:**
- Ranks students from highest to lowest average
- Shows student name, ID, average grade, and number of courses
- Only includes students with at least one course
- Calculates average across all enrolled courses

---

### 4. **Find Failing Students Button** (`failinfstudentButton`)
**Function:** `find_failing_students()`

**Purpose:** Identify all students with grades below 75% (failing) in any course.

**How to Use:**
1. Click "Find Failing Student" button on MORE page
2. View list of failing grades in the failing student list area

**Display Format:**
```
John Doe (ID: 12345) | MATH101: Mathematics | Grade: 68.5% - FAILED
Jane Smith (ID: 67890) | ENG201: English | Grade: 72.0% - FAILED
```

**Features:**
- Shows all failing grades across all students
- Includes student name, ID, course code, subject, and grade
- If no failing students: displays "No failing students - Great job! 🎉"
- Helps identify students who need assistance

---

### 5. **Log Out Button** (`logoutButton`)
**Function:** `logout()`

**Purpose:** Safely log out and return to login screen.

**How to Use:**
1. Click "Log out" button on MORE page
2. Confirm logout in dialog
3. Returns to login page with cleared fields

**Features:**
- Confirmation dialog to prevent accidental logout
- Clears username and password fields
- Maintains all student/course data in memory
- Secure logout process

---

## Additional Improvement: Course Code Validation

### **Add Course Validation**
**Modified Function:** `add_course()`

**Purpose:** Prevent duplicate course codes from being added to the system.

**How It Works:**
1. When adding a new course, system checks if course code already exists
2. If duplicate detected:
   - Shows warning message
   - Prevents course from being added
   - Allows user to try again with different code
3. If unique:
   - Course is added successfully
   - Displays in course list and tables

**Error Message:**
```
Course code 'MATH101' already exists. Please use a different code.
```

**Benefits:**
- Prevents data conflicts
- Maintains data integrity
- Protects existing course information
- Clear error messaging

---

## Technical Details

### Widget Used for Rankings/Failing Students
- **Widget:** `failingstudentList` (QListWidget)
- **Location:** RIGHT side of MORE page
- **Purpose:** Display both class rankings and failing student lists

### Grade Calculation Formula
All functions use the same grading formula:

```python
Class Standing = (Seatwork × 0.25) + (Assignment × 0.25) + (Quizzes × 0.50)
Final Grade = (Class Standing × 0.40) + (Exam × 0.60)
Passing Grade = 75% or higher
```

### Button Connections
All buttons are connected in the `gui_setup()` method:

```python
self.ui.calcgradeButton.clicked.connect(self.calculate_grade_tool)
self.ui.addgradeButton.clicked.connect(self.add_student_grade)
self.ui.rankButton.clicked.connect(self.get_class_ranking)
self.ui.failinfstudentButton.clicked.connect(self.find_failing_students)
self.ui.logoutButton.clicked.connect(self.logout)
```

---

## Usage Workflow Examples

### Example 1: Adding Grades for a Student
1. Navigate to MORE page
2. Click "Add Student Grade"
3. Enter Student ID: `12345`
4. Enter Course Code: `MATH101`
5. Enter Seatwork: `85`
6. Enter Assignment: `90`
7. Enter Quizzes: `88`
8. Enter Exam: `92`
9. System calculates: Final Grade = 90.3% - PASSED

### Example 2: Finding Failing Students
1. Navigate to MORE page
2. Click "Find Failing Student"
3. System scans all students and courses
4. Displays list of all grades below 75%
5. Use information to provide targeted support

### Example 3: Viewing Class Rankings
1. Navigate to MORE page
2. Click "Get Class Ranking"
3. View students ranked by average grade
4. Identify top performers and those needing help

---

## Error Handling

All functions include comprehensive error handling:

- ✅ Empty data checks (no students/courses)
- ✅ Invalid ID format validation
- ✅ Non-existent ID/course code detection
- ✅ Numeric value validation
- ✅ Grade range validation (0-100)
- ✅ Enrollment status verification
- ✅ Clear error messages for users

---

## Recent Actions Tracking

The following actions are tracked in the dashboard's recent actions list:
- "Calculated grade using tool"
- "Updated grades: [Student Name] - [Course Code]"
- "Generated class ranking"
- "Found failing students"
- "Added course: [Course Subject]" (with duplicate prevention)

---

## Testing Checklist

### Calculate Grade Tool
- [ ] Opens dialog with 4 input fields
- [ ] Validates numeric input
- [ ] Validates range (0-100)
- [ ] Calculates correct final grade
- [ ] Shows PASSED for grades ≥ 75
- [ ] Shows FAILED for grades < 75

### Add Student Grade
- [ ] Checks if students exist
- [ ] Validates student ID
- [ ] Checks course enrollment
- [ ] Updates all grade fields
- [ ] Calculates and saves remarks
- [ ] Shows confirmation message

### Get Class Ranking
- [ ] Handles no students case
- [ ] Skips students without courses
- [ ] Calculates correct averages
- [ ] Sorts in descending order
- [ ] Displays in correct format

### Find Failing Students
- [ ] Identifies all grades < 75%
- [ ] Shows course details
- [ ] Displays congratulations if none failing
- [ ] Shows count of failing grades

### Logout
- [ ] Shows confirmation dialog
- [ ] Clears login fields
- [ ] Returns to login page
- [ ] Preserves data in memory

### Course Code Validation
- [ ] Detects duplicate codes
- [ ] Shows warning message
- [ ] Prevents duplicate addition
- [ ] Allows unique codes

---

## Summary

All 5 MORE page buttons are now fully functional with proper validation and error handling. The course code duplication check has been added to prevent data conflicts. The system maintains data integrity while providing helpful feedback to users.
