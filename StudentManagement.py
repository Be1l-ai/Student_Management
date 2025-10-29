from Student_Management import Ui_MainWindow
from PyQt6.QtWidgets import QWidget, QDialog, QMainWindow, QApplication, QMessageBox, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton
import sys

auth = {"username":"admin", "password":"admin123"}

class DialogPop(QDialog):
    def __init__(self, title="Input Information", fields=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedWidth(300)

        layout = QVBoxLayout(self)
        self.inputs = {}
        for field in fields:
            label = QLabel(field)
            line = QLineEdit()
            layout.addWidget(label)
            layout.addWidget(line)
            self.inputs[field] = line

        buttonLayout = QHBoxLayout()
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")
        okButton.clicked.connect(self.accept)
        cancelButton.clicked.connect(self.accept)
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)

        layout.addLayout(buttonLayout)

    def getInput(self):
            return {key: value.text() for key, value in self.inputs.items()}
    pass

class StudentManagement(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.guisetup()

        self.show()

    def guisetup(self):
        self.ui.loginButton.clicked.connect(self.login)
        self.ui.dashboardButton.clicked.connect(self.dashboardMain)
        self.ui.studentsButton.clicked.connect(self.students)
        self.ui.coursesButton.clicked.connect(self.courses)
        self.ui.moreButoon.clicked.connect(self.more)

    def login(self):
        username = self.ui.usernameInput.text()
        password = self.ui.passwordInput.text()

        if username == auth["username"]:
            if password == auth["password"]:
                self.ui.stackedWidget.setCurrentWidget(self.ui.pageMain)
                self.dashboardMain()
            else: 
                QMessageBox.warning(self, "error", "Wrong Password")
        else:
            QMessageBox.warning(self, "error", "Wrong Username")

    def dashboardMain(self):
        self.ui.Main.setCurrentWidget(self.ui.pageDashboard)

    def students(self):
        self.ui.Main.setCurrentWidget(self.ui.pageStudents)
        self.ui.addstudentButton.clicked.connect(self.addStudent)

    def courses(self):
        self.ui.Main.setCurrentWidget(self.ui.pageCourses)

    def more(self):
        self.ui.Main.setCurrentWidget(self.ui.pageMore)

    def addStudent(self):
        dialogStudent = DialogPop("Add New Student", ["Name:", "Course:"])
        if dialogStudent.exec() == QDialog.accepted:
            newStudent = dialogStudent.getInput()
            QMessageBox.warning(self, "Success", f"Got: {newStudent}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentManagement()
    sys.exit(app.exec())