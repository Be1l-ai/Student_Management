# Student Management System - Version 2.0 Updates

## Major Changes

### 1. ✅ PEP 8 Naming Conventions
All functions and variables have been refactored to follow Python's PEP 8 style guide:

**Class Methods (before → after):**
- `guisetup()` → `gui_setup()`
- `dashboardMain()` → `dashboard_main()`
- `generateID()` → `generate_id()`
- `addStudent()` → `add_student()`
- `editStudent()` → `edit_student()`
- `deleteStudent()` → `delete_student()`
- `enrollStudent()` → `enroll_student()`
- `addCourse()` → `add_course()`
- `editCourse()` → `edit_course()`
- `deleteCourse()` → `delete_course()`
- `displaystudentList()` → `display_student_list()`
- `displayStudentTable()` → `display_student_table()`
- `displayCourseList()` → `display_course_list()`
- `displayCourseTable()` → `display_course_table()`
- `displayRecentList()` → `display_recent_list()`
- `addRecentAction()` → `add_recent_action()`
- `calculateGrade()` → `calculate_grade()`
- `getStudentReport()` → `get_student_report()`
- `getCourseReport()` → `get_course_report()`

**DialogPop Class:**
- `uiDialog` → `ui_dialog`
- `getInput()` → `get_input()`

**Variables:**
- `dialogStudent` → `dialog_student`
- `newStudent` → `new_student`
- `dialogCourse` → `dialog_course`
- `newCourse` → `new_course`
- All other camelCase variables converted to snake_case

### 2. ✅ Multiple Course Support

**OLD Data Structure (Single Course):**
```python
students[id] = {
    "name": "Student Name",
    "course": {
        "Course code": "MATH101",
        "subject": "Mathematics",
        "grade": {...}
    },
    "remarks": ""
}
```

**NEW Data Structure (Multiple Courses):**
```python
students[id] = {
    "name": "Student Name",
    "courses": [
        {
            "code": "MATH101",
            "subject": "Mathematics",
            "grades": {
                "seatwork": 0,
                "assignment": 0,
                "quizzes": 0,
                "exam": 0
            },
            "remarks": ""
        },
        {
            "code": "ENG101",
            "subject": "English",
            "grades": {...},
            "remarks": ""
        }
    ]
}
```

**Benefits:**
- Students can now enroll in multiple courses
- Each course has independent grades
- Each course has its own pass/fail status
- Better reflects real-world academic systems

### 3. ✅ Search Functionality

#### Student Search (`search_student()`)
- **Search by ID**: Enter numeric student ID for exact match
- **Search by Name**: Enter any part of the student's name (case-insensitive)
- **Features**:
  - Partial name matching
  - Case-insensitive search
  - Displays results in student table
  - Shows number of results found
  - Resets to full list if no results

**Usage:**
1. Navigate to Students page
2. Enter search term in search box
3. Click "Search" button
4. View filtered results in table

**Examples:**
- Search "12345" → Finds student with ID 12345
- Search "john" → Finds all students with "john" in their name
- Search "smith" → Finds John Smith, Jane Smith, etc.

#### Course Search (`search_course()`)
- **Search by Code**: Search by course code (e.g., "MATH101")
- **Search by Subject**: Search by subject name (e.g., "Mathematics")
- **Features**:
  - Partial matching for both code and subject
  - Case-insensitive search
  - Displays results in course table
  - Shows number of results found
  - Resets to full list if no results

**Usage:**
1. Navigate to Courses page
2. Enter search term in search box
3. Click "Search" button
4. View filtered results in table

**Examples:**
- Search "MATH" → Finds MATH101, MATH102, etc.
- Search "101" → Finds all courses ending with 101
- Search "english" → Finds all English courses

### 4. ✅ Enhanced Enrollment System

**New Features:**
- Students can enroll in multiple courses
- Duplicate enrollment prevention
- Each course maintains independent grade records
- Enrollment history preserved

**Enrollment Process:**
1. Click "Enroll Student" button
2. Enter Student ID
3. Enter Course Code
4. System checks:
   - Student exists
   - Course exists
   - Student not already enrolled in that course
5. Course added to student's course list
6. Grade structure initialized for that course

### 5. ✅ Updated Display Functions

#### Student Table
**Columns:**
- Student ID
- Name
- Enrolled Courses (shows all enrolled courses with codes and subjects)

**Display Format:**
- If enrolled: "MATH101: Mathematics, ENG101: English"
- If not enrolled: "No courses"

#### Student List (Dashboard)
**Format:**
- Shows student ID, name, and course count
- Example: "12345: John Smith | 3 course(s)"
- Example: "67890: Jane Doe | No courses"

### 6. ✅ Enhanced Report Functions

#### Student Report (`get_student_report()`)
**Shows:**
- Student ID and Name
- List of all enrolled courses
- For each course:
  - Course code and subject
  - Individual grade components (seatwork, assignment, quizzes, exam)
  - Calculated class standing
  - Final grade
  - Pass/Fail status

**Sample Report:**
```
=== STUDENT REPORT ===
Student ID: 12345
Name: John Smith

=== ENROLLED COURSES (2) ===

--- COURSE 1: MATH101 - Mathematics ---
Seatwork: 85
Assignment: 90
Quizzes: 88
Class Standing: 87.75
Exam: 92
FINAL GRADE: 90.3
REMARKS: PASSED

--- COURSE 2: ENG101 - English ---
Seatwork: 78
Assignment: 82
Quizzes: 80
Class Standing: 80.0
Exam: 75
FINAL GRADE: 77.0
REMARKS: PASSED
```

#### Course Report (`get_course_report()`)
**Shows:**
- Course code and subject
- Total number of enrolled students
- List of all enrolled students with IDs

**Sample Report:**
```
=== COURSE REPORT ===
Course Code: MATH101
Subject: Mathematics

=== ENROLLED STUDENTS (3) ===
ID: 12345 - John Smith
ID: 67890 - Jane Doe
ID: 11111 - Bob Johnson
```

## Updated GUI Connections

All new functions are connected to their respective buttons:

```python
# Student page
self.ui.searchstudentButton.clicked.connect(self.search_student)

# Course page
self.ui.searchcourseButton.clicked.connect(self.search_course)
```

## Breaking Changes

⚠️ **Important**: The data structure for students has changed significantly.

**Migration Notes:**
- Old student data with single `course` object won't work
- Need to migrate existing data to new `courses` list format
- All grades moved from `course.grade.class standing` to `course.grades`
- Fixed typo: `seatwok` → `seatwork`

## Code Quality Improvements

1. **PEP 8 Compliance**: All code now follows Python style guidelines
2. **Better Documentation**: All functions have docstrings
3. **Consistent Naming**: snake_case for all Python code
4. **Cleaner Structure**: More logical organization of data

## New Features Summary

| Feature | Status | Description |
|---------|--------|-------------|
| PEP 8 Naming | ✅ Complete | All functions use snake_case |
| Multiple Courses | ✅ Complete | Students can enroll in multiple courses |
| Student Search | ✅ Complete | Search by ID or name |
| Course Search | ✅ Complete | Search by code or subject |
| Enhanced Enrollment | ✅ Complete | Add multiple courses per student |
| Updated Reports | ✅ Complete | Show all courses in reports |
| Duplicate Prevention | ✅ Complete | Can't enroll twice in same course |

## Usage Examples

### Example 1: Enrolling Student in Multiple Courses
```
1. Add student "John Smith" (ID: 12345)
2. Enroll John in MATH101
3. Enroll John in ENG101
4. Enroll John in SCI101
5. View student table → Shows all 3 courses
6. Generate student report → Shows grades for all 3 courses
```

### Example 2: Searching for Students
```
1. Add multiple students
2. Enter "john" in search box
3. Click Search → Shows all Johns
4. Clear search to see all students again
```

### Example 3: Searching for Courses
```
1. Add MATH101, MATH102, ENG101
2. Enter "MATH" in search box
3. Click Search → Shows MATH101 and MATH102
4. Enter "101" → Shows MATH101 and ENG101
```

## Performance Improvements

- Search operations use efficient filtering
- Table updates only when necessary
- No redundant data processing

## Future Enhancements (Potential)

- Bulk enrollment (enroll student in multiple courses at once)
- Course prerequisites
- GPA calculation across all courses
- Export reports to PDF/CSV
- Student transcript generation
- Course capacity limits
- Waitlist functionality

## Testing Recommendations

1. Test enrolling one student in multiple courses
2. Test search with partial names
3. Test search with course codes
4. Verify duplicate enrollment prevention
5. Generate reports for students with multiple courses
6. Test all CRUD operations with new data structure
