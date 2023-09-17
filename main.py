import sys
import sqlite3
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTreeWidget, QTreeWidgetItem, QCalendarWidget
from PyQt5.QtCore import Qt
from dialogs import EditTaskDialog 

class DailyTasksApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Daily Tasks')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.init_ui()

        self.conn = sqlite3.connect('tasks.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS tasks (task_name TEXT, created_at TIMESTAMP, due_date TIMESTAMP)')
        self.conn.commit()

        self.load_tasks()

    def init_ui(self):

        self.task_list = QTreeWidget()
        self.task_list.setColumnCount(3)
        self.task_list.setHeaderLabels(['Task Name', 'Created Date', 'Due Date'])
        self.layout.addWidget(self.task_list)

        self.task_label = QLabel('Task name:')
        self.layout.addWidget(self.task_label)

        self.task_entry = QLineEdit()
        self.layout.addWidget(self.task_entry)

        self.due_date_label = QLabel('Due Date:')
        self.layout.addWidget(self.due_date_label)

        self.due_date_calendar = QCalendarWidget()
        self.layout.addWidget(self.due_date_calendar)

        self.add_button = QPushButton('Add')
        self.add_button.clicked.connect(self.add_task)
        self.layout.addWidget(self.add_button)

        self.task_entry.returnPressed.connect(self.add_task)

        self.delete_button = QPushButton('Delete')
        self.delete_button.clicked.connect(self.delete_task)
        self.layout.addWidget(self.delete_button)

        self.edit_button = QPushButton('Edit')
        self.edit_button.clicked.connect(self.edit_task)
        self.layout.addWidget(self.edit_button)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.delete_task()

    def add_task(self):
        task = self.task_entry.text()
        due_date = self.due_date_calendar.selectedDate().toString('yyyy-MM-dd')

        if task:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute('INSERT INTO tasks (task_name, created_at, due_date) VALUES (?, ?, ?)',
                                (task, current_time, due_date))
            self.conn.commit()
            self.load_tasks()
            self.task_entry.clear()

    def delete_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            selected_task_name = selected_item.text(0)
            self.cursor.execute('DELETE FROM tasks WHERE task_name = ?', (selected_task_name,))
            self.conn.commit()
            self.load_tasks()

    def edit_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            selected_task_name = selected_item.text(0)
            selected_due_date = selected_item.text(2)

            dialog = EditTaskDialog(selected_task_name, selected_due_date)
            dialog.exec_()

            if dialog.result() == 1:
                edited_task = dialog.task_entry.text()
                edited_due_date = dialog.due_date_calendar.selectedDate().toString('yyyy-MM-dd')

                if edited_task and edited_due_date:
                    self.cursor.execute('UPDATE tasks SET task_name = ?, due_date = ? WHERE task_name = ?',
                                        (edited_task, edited_due_date, selected_task_name))
                    self.conn.commit()
                    self.load_tasks()

    def load_tasks(self):
        self.task_list.clear()

        self.cursor.execute('SELECT task_name, created_at, due_date FROM tasks')
        tasks = self.cursor.fetchall()

        for task in tasks:
            item = QTreeWidgetItem([task[0], task[1], task[2]])
            self.task_list.addTopLevelItem(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DailyTasksApp()
    window.show()
    sys.exit(app.exec_())

