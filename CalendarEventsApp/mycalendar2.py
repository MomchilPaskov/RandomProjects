import sys
import threading
import time
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QListWidget, QCalendarWidget)
from PyQt5.QtCore import Qt
from plyer import notification

# --- Списък със събития ---
events = []

# --- Функции ---
def add_event():
    name = name_input.text()
    time_str = time_input.text()
    date_str = calendar.selectedDate().toString("yyyy-MM-dd")
    if not name or not time_str:
        return
    events.append({"name": name, "time": time_str, "date": date_str})
    refresh_list()
    name_input.clear()
    time_input.clear()

def refresh_list():
    list_widget.clear()
    selected_date = calendar.selectedDate().toString("yyyy-MM-dd")
    for event in events:
        if event["date"] == selected_date:
            list_widget.addItem(f"{event['time']} - {event['name']}")

def check_events():
    while True:
        now_date = datetime.now().strftime("%Y-%m-%d")
        now_time = datetime.now().strftime("%H:%M")
        for event in events[:]:
            if event["date"] == now_date and event["time"] == now_time:
                notification.notify(
                    title="Предстоящо събитие",
                    message=f"{event['name']} започва сега!",
                    timeout=10
                )
                events.remove(event)
                refresh_list()
        time.sleep(30)

# --- GUI ---
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Моят Календар")
window.setGeometry(400, 200, 500, 500)
window.setStyleSheet("background-color: #2e2e2e; color: white; font-family: Arial; font-size: 12pt;")

main_layout = QVBoxLayout()

# --- Календар ---
calendar = QCalendarWidget()
calendar.setStyleSheet("""
    QCalendarWidget QWidget { alternate-background-color: #333; }
    QCalendarWidget QAbstractItemView:enabled { background-color: #1e1e1e; color: white; }
    QCalendarWidget QToolButton { background-color: #4caf50; color: white; border-radius: 5px; }
""")
calendar.selectionChanged.connect(lambda: refresh_list())
main_layout.addWidget(calendar)

# --- Добавяне на събитие ---
input_layout = QHBoxLayout()
name_input = QLineEdit()
name_input.setPlaceholderText("Име на събитието")
time_input = QLineEdit()
time_input.setPlaceholderText("Час (ЧЧ:ММ)")
add_btn = QPushButton("Добави")
add_btn.clicked.connect(add_event)
add_btn.setStyleSheet("background-color: #4caf50; color: white; border-radius: 5px; height: 30px;")
input_layout.addWidget(name_input)
input_layout.addWidget(time_input)
input_layout.addWidget(add_btn)
main_layout.addLayout(input_layout)

# --- Списък със събития ---
list_widget = QListWidget()
list_widget.setStyleSheet("background-color: #1e1e1e; color: white; border-radius: 5px;")
main_layout.addWidget(list_widget)

window.setLayout(main_layout)

# --- Стартираме проверката на събития в отделен thread ---
thread = threading.Thread(target=check_events, daemon=True)
thread.start()

window.show()
sys.exit(app.exec_())
