from utils.dialog import Ui_Dialog
from PyQt6.QtWidgets import QWidget, QDialog, QMainWindow, QApplication, QMessageBox, QLabel, QLineEdit, QPushButton

class DialogPop(QDialog):
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
        if all(field.text().strip() for field in self.inputs.values()):
            self.accept()
        else:
            QMessageBox.warning(self, 'Failed', 'Missing Information')
    def get_input(self):
        return {key: value.text() for key, value in self.inputs.items()}