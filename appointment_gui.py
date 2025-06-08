# appointment_gui.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox,
    QListWidget, QListWidgetItem, QDateEdit
)
from PyQt6.QtCore import QDate
from appointment import add_appointment, get_appointments

class AppointmentWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Appointments")
        self.setFixedSize(400, 450)
        self.init_ui()
        self.load_appointments()

    def init_ui(self):
        layout = QVBoxLayout()

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())

        self.doctor_input = QLineEdit()
        self.doctor_input.setPlaceholderText("Doctor's Name")

        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Notes for Appointment")

        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Location / Hospital")

        self.add_button = QPushButton("Add Appointment")
        self.add_button.clicked.connect(self.add_appointment)

        self.appt_list = QListWidget()

        layout.addWidget(QLabel("Appointment Date:"))
        layout.addWidget(self.date_input)

        layout.addWidget(QLabel("Doctor:"))
        layout.addWidget(self.doctor_input)

        layout.addWidget(QLabel("Notes:"))
        layout.addWidget(self.notes_input)

        layout.addWidget(QLabel("Location:"))
        layout.addWidget(self.location_input)

        layout.addWidget(self.add_button)
        layout.addWidget(QLabel("Upcoming Appointments:"))
        layout.addWidget(self.appt_list)

        self.setLayout(layout)

    def add_appointment(self):
        date = self.date_input.date().toString("yyyy-MM-dd")
        doctor = self.doctor_input.text().strip()
        notes = self.notes_input.text().strip()
        location = self.location_input.text().strip()

        if not doctor or not notes or not location:
            QMessageBox.warning(self, "Missing Info", "Please fill in all fields.")
            return

        success, msg = add_appointment(self.user_id, date, doctor, notes, location)
        if success:
            QMessageBox.information(self, "Success", msg)
            self.clear_inputs()
            self.load_appointments()
        else:
            QMessageBox.critical(self, "Error", msg)

    def load_appointments(self):
        self.appt_list.clear()
        appointments = get_appointments(self.user_id)
        for appt in appointments:
            item = QListWidgetItem(
                f"{appt[0]} | Dr. {appt[1]} | {appt[2]} @ {appt[3]}"
            )
            self.appt_list.addItem(item)

    def clear_inputs(self):
        self.date_input.setDate(QDate.currentDate())
        self.doctor_input.clear()
        self.notes_input.clear()
        self.location_input.clear()
