from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit, QCalendarWidget, QDialogButtonBox
from PyQt5.QtCore import QDate

class EditTaskDialog(QDialog):
    def __init__(self, task_name, due_date):
        super().__init__()

        self.setWindowTitle('Edit Task')
        self.setGeometry(200, 200, 400, 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.task_label = QLabel('New Task Name:')
        self.layout.addWidget(self.task_label)

        self.task_entry = QLineEdit()
        self.task_entry.setText(task_name)
        self.layout.addWidget(self.task_entry)

        self.due_date_label = QLabel('New Due Date (YYYY-MM-DD):')
        self.layout.addWidget(self.due_date_label)

        self.due_date_calendar = QCalendarWidget()
        self.due_date_calendar.setSelectedDate(QDate.fromString(due_date, "yyyy-MM-dd"))
        self.layout.addWidget(self.due_date_calendar)

        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.layout.addWidget(button_box)

        self.result_value = 0

    def accept(self):
        self.result_value = 1
        super().accept()
