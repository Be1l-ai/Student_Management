# Grading System Documentation

## Overview
The Student Management System uses a weighted grading system to calculate final grades.

## Grade Components

### 1. Class Standing (40% of Final Grade)
Class standing is composed of three components:
- **Seatwork**: 25% of class standing
- **Assignment**: 25% of class standing  
- **Quizzes**: 50% of class standing

**Formula:**
```
Class Standing = (Seatwork × 0.25) + (Assignment × 0.25) + (Quizzes × 0.50)
```

### 2. Exam (60% of Final Grade)
- Direct score from 0-100
- Contributes 60% to the final grade

## Final Grade Calculation

**Formula:**
```
Final Grade = (Class Standing × 0.40) + (Exam × 0.60)
```

## Passing Criteria
- **Passing Grade**: 75%
- **Remarks**: 
  - PASSED if Final Grade ≥ 75
  - FAILED if Final Grade < 75

## Examples

### Example 1: Passing Student
```
Given Scores:
- Seatwork: 85
- Assignment: 90
- Quizzes: 92
- Exam: 88

Step 1: Calculate Class Standing
Class Standing = (85 × 0.25) + (90 × 0.25) + (92 × 0.50)
               = 21.25 + 22.5 + 46
               = 89.75

Step 2: Calculate Final Grade
Final Grade = (89.75 × 0.40) + (88 × 0.60)
            = 35.9 + 52.8
            = 88.7

Result: PASSED (88.7 ≥ 75)
```

### Example 2: Failing Student
```
Given Scores:
- Seatwork: 60
- Assignment: 65
- Quizzes: 70
- Exam: 68

Step 1: Calculate Class Standing
Class Standing = (60 × 0.25) + (65 × 0.25) + (70 × 0.50)
               = 15 + 16.25 + 35
               = 66.25

Step 2: Calculate Final Grade
Final Grade = (66.25 × 0.40) + (68 × 0.60)
            = 26.5 + 40.8
            = 67.3

Result: FAILED (67.3 < 75)
```

### Example 3: Borderline Case
```
Given Scores:
- Seatwork: 75
- Assignment: 78
- Quizzes: 80
- Exam: 74

Step 1: Calculate Class Standing
Class Standing = (75 × 0.25) + (78 × 0.25) + (80 × 0.50)
               = 18.75 + 19.5 + 40
               = 78.25

Step 2: Calculate Final Grade
Final Grade = (78.25 × 0.40) + (74 × 0.60)
            = 31.3 + 44.4
            = 75.7

Result: PASSED (75.7 ≥ 75)
```

## Score Range
- All component scores should ideally be in the range 0-100
- Exam score is strictly limited to 0-100
- Class standing components can theoretically exceed 100 but typically stay within 0-100

## Implementation in Code

The `calculateGrade()` method in `StudentManagement.py` implements this formula:

```python
def calculateGrade(self, seatwork, assignment, quizzes, exam):
    # Calculate class standing (weighted average)
    class_standing = (seatwork * 0.25) + (assignment * 0.25) + (quizzes * 0.50)
    
    # Final grade: 40% class standing + 60% exam
    final_grade = (class_standing * 0.40) + (exam * 0.60)
    
    # Determine remarks
    remarks = "PASSED" if final_grade >= 75 else "FAILED"
    
    return round(final_grade, 2), remarks
```

## Usage in Student Reports

When you generate a student report using the "Get Student Report" button:
1. The system retrieves all grade components from the student record
2. Calculates the class standing using the weighted formula
3. Calculates the final grade
4. Determines pass/fail status
5. Updates the student's remarks field
6. Displays a comprehensive report with all calculations

## Tips for Inputting Grades

To maintain accurate grading:
1. Ensure all scores are entered on a 0-100 scale
2. Double-check exam scores (they have the highest weight)
3. Remember that quizzes count for 50% of class standing
4. Use the student report feature to verify calculations
5. Final grades are rounded to 2 decimal places

## Grade Weight Summary

| Component | % of Class Standing | % of Final Grade | Overall Impact |
|-----------|-------------------|------------------|----------------|
| Seatwork | 25% | - | 10% (0.25 × 0.40) |
| Assignment | 25% | - | 10% (0.25 × 0.40) |
| Quizzes | 50% | - | 20% (0.50 × 0.40) |
| **Class Standing Total** | **100%** | **40%** | **40%** |
| Exam | - | 60% | 60% |
| **TOTAL** | - | **100%** | **100%** |
