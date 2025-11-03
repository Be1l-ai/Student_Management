from utils.dialog_pop import DialogPop
from PyQt6.QtWidgets import QDialog

class DialogHelper:
    @staticmethod
    def get_user_input(parent, fields, title="Input"):
        dialog = DialogPop(fields, parent=parent)
        dialog.setWindowTitle(title)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.get_input()
        return None

    @staticmethod
    def get_user_input_fill(parent, fields, title="Input", set_name="", chosen_name=""):
        dialog = DialogPop(fields, parent=parent)
        dialog.setWindowTitle(title)
        dialog.inputs[chosen_name].setText(set_name)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.get_input()
        return None
    
    @staticmethod
    def get_required_input(parent, fields, title="Input"):
        return DialogHelper.get_user_input(parent, fields, title)