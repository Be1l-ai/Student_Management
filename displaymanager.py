from PyQt6.QtGui import QStandardItemModel, QStandardItem

class DisplayManager:
    @staticmethod
    def display_list(data, list_object, action=0):
        model = QStandardItemModel()
        if action == 1:
            for student_id, info in data.items():
                course_count = len(info.get("courses", []))
                courses_text = f'{course_count} course(s)' if course_count > 0 else "No courses"
                text_student = f"{student_id}: {info['name']} | {courses_text}"
                item = QStandardItem(text_student)
                model.appendRow(item)
        elif action == 2:
            for course_code, info in data.items():
                text_course = f'{course_code}: {info["subject"]}'
                item = QStandardItem(text_course)
                model.appendRow(item)
        else:
            for history in data:
                item = QStandardItem(str(history))
                model.appendRow(item)
        
        list_object.setModel(model)
    
    @staticmethod
    def display_table(data, table_object, action=0):
        model = QStandardItemModel()
        if action == 1:
            model.setHorizontalHeaderLabels(['Student ID', 'Name', 'Enrolled Courses'])
            for student_id, info in data.items():
                id_item = QStandardItem(str(student_id))
                name_item = QStandardItem(info['name'])
                courses_list= info.get('courses', [])
                if courses_list:
                    courses_string= ', '.join([f"{course['code']}: {course['subject']}" for course in courses_list])
                else:
                    courses_string = "No courses"
                courses_item = QStandardItem(courses_string)
                model.appendRow([id_item, name_item, courses_item])

        elif action== 2:
            model.setHorizontalHeaderLabels(['Course Code', 'Subject'])
            for course_code, info in data.items():
                code_item = QStandardItem(course_code)
                subject_item = QStandardItem(info['subject'])
                model.appendRow([code_item, subject_item])

        table_object.setModel(model)
        table_object.resizeColumnsToContents()