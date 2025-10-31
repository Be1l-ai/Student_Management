# Quick Reference Guide - Version 2.0

## PEP 8 Function Name Changes

| Old Name (v1.0) | New Name (v2.0) |
|----------------|-----------------|
| `guisetup()` | `gui_setup()` |
| `dashboardMain()` | `dashboard_main()` |
| `generateID()` | `generate_id()` |
| `addStudent()` | `add_student()` |
| `editStudent()` | `edit_student()` |
| `deleteStudent()` | `delete_student()` |
| `enrollStudent()` | `enroll_student()` |
| `addCourse()` | `add_course()` |
| `editCourse()` | `edit_course()` |
| `deleteCourse()` | `delete_course()` |
| `displaystudentList()` | `display_student_list()` |
| `displayStudentTable()` | `display_student_table()` |
| `displayCourseList()` | `display_course_list()` |
| `displayCourseTable()` | `display_course_table()` |
| `displayRecentList()` | `display_recent_list()` |
| `addRecentAction()` | `add_recent_action()` |
| `calculateGrade()` | `calculate_grade()` |
| `getStudentReport()` | `get_student_report()` |
| `getCourseReport()` | `get_course_report()` |
| N/A | `search_student()` ⭐ NEW |
| N/A | `search_course()` ⭐ NEW |

## New Features Quick Start

### 1. Multiple Course Enrollment

**How to enroll a student in multiple courses:**
```
1. Students page → "Enroll Student"
2. Enter Student ID: 12345
3. Enter Course Code: MATH101
4. Click OK → Student enrolled in MATH101

5. Click "Enroll Student" again
6. Enter Student ID: 12345 (same student)
7. Enter Course Code: ENG101
8. Click OK → Student enrolled in ENG101 too!
```

**Result:**
- Student table shows: "12345: John Smith | MATH101: Mathematics, ENG101: English"
- Dashboard shows: "12345: John Smith | 2 course(s)"

### 2. Student Search

**Search by ID:**
```
1. Students page → Search box
2. Enter: 12345
3. Click "Search"
4. Result: Shows student with ID 12345
```

**Search by Name:**
```
1. Students page → Search box
2. Enter: john
3. Click "Search"
4. Result: Shows all students with "john" in their name
```

**Clear Search:**
- Just search for empty or navigate away and back

### 3. Course Search

**Search by Code:**
```
1. Courses page → Search box
2. Enter: MATH
3. Click "Search"
4. Result: Shows MATH101, MATH102, etc.
```

**Search by Subject:**
```
1. Courses page → Search box
2. Enter: mathematics
3. Click "Search"
4. Result: Shows all Mathematics courses
```

## Data Structure Changes

### OLD (v1.0) - Single Course:
```python
{
    12345: {
        "name": "John Smith",
        "course": {
            "Course code": "MATH101",
            "subject": "Mathematics",
            "grade": {
                "class standing": {
                    "seatwok": 85,      # Typo!
                    "assignment": 90,
                    "quizzes": 88
                },
                "exam": 92
            }
        },
        "remarks": "PASSED"
    }
}
```

### NEW (v2.0) - Multiple Courses:
```python
{
    12345: {
        "name": "John Smith",
        "courses": [
            {
                "code": "MATH101",
                "subject": "Mathematics",
                "grades": {
                    "seatwork": 85,     # Fixed typo!
                    "assignment": 90,
                    "quizzes": 88,
                    "exam": 92
                },
                "remarks": "PASSED"
            },
            {
                "code": "ENG101",
                "subject": "English",
                "grades": {
                    "seatwork": 78,
                    "assignment": 82,
                    "quizzes": 80,
                    "exam": 75
                },
                "remarks": "PASSED"
            }
        ]
    }
}
```

## Common Tasks

### Task: Add a student and enroll in 3 courses
```
1. Add Student → Name: "John Smith" → Got ID: 12345
2. Enroll Student → ID: 12345, Course: MATH101 ✓
3. Enroll Student → ID: 12345, Course: ENG101 ✓
4. Enroll Student → ID: 12345, Course: SCI101 ✓
5. View in table → Shows all 3 courses
```

### Task: Find all students in a specific course
```
1. Courses page → Tab 2
2. Click "Get Course Report"
3. Enter Course Code: MATH101
4. View list of all enrolled students
```

### Task: Generate transcript for a student
```
1. Students page → Tab 2
2. Click "Get Student Report"
3. Enter Student ID: 12345
4. View complete report with all courses and grades
```

### Task: Search for students by partial name
```
1. Students page → Search box
2. Enter partial name: "smi"
3. Click "Search"
4. See: John Smith, Jane Smith, etc.
```

## Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Student already enrolled in MATH101" | Trying to enroll twice | Student already in that course |
| "No students available" | Empty database | Add students first |
| "Invalid Student ID format" | Non-numeric ID | Enter numbers only |
| "Please enter search text" | Empty search box | Type something to search |

## Tips & Tricks

1. **Quick View**: Dashboard shows course count at a glance
2. **Search Reset**: Navigate away and back to reset search
3. **Multiple Enrollment**: Enroll in any number of courses
4. **Comprehensive Reports**: Student report shows ALL courses
5. **No Duplicates**: System prevents enrolling twice in same course

## Keyboard Shortcuts

- Enter key in search box = Click Search button (if connected)
- Tab key = Move between form fields
- Escape = Close dialogs

## Common Workflows

### Workflow 1: New Student Complete Setup
```
1. Add Student (get ID)
2. Enroll in Course 1
3. Enroll in Course 2
4. Enroll in Course 3
5. Verify in table
```

### Workflow 2: Find and Edit Student
```
1. Search for student by name
2. Note the Student ID
3. Click "Edit Student"
4. Enter ID and modify
```

### Workflow 3: Course Management
```
1. Add multiple courses
2. Search to verify they exist
3. Enroll students
4. Generate course report to see enrollment
```

## Troubleshooting

**Q: Why can't I enroll a student twice?**
A: Duplicate prevention - it's a feature, not a bug!

**Q: Where did the single course structure go?**
A: Updated to support multiple courses per student.

**Q: How do I see all students again after searching?**
A: Navigate away and back, or search for empty string.

**Q: Can I enroll a student before adding them?**
A: No, add student first, then enroll.

**Q: Do I need to re-enter grades when enrolling?**
A: No, grades start at 0 and can be updated later (future feature).

## What's Coming Next?

Planned features (not yet implemented):
- Grade entry interface
- Bulk enrollment
- CSV export
- Student transcripts
- GPA calculation
- Course prerequisites
- Semester/term support
