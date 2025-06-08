from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from health_gui import HealthWindow
from medi_gui import MedicationWindow
from appointment_gui import AppointmentWindow
from auth import get_user_id_by_email

class DashboardWindow(QWidget):
    logout_successful = pyqtSignal()

    def __init__(self, user_email):
        super().__init__()
        self.user_email = user_email
        self.user_id = get_user_id_by_email(user_email)
        self.setWindowTitle("Health Dashboard")
        self.setFixedSize(500, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        welcome_label = QLabel(f"Welcome, {self.user_email}")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        health_btn = QPushButton("🩺 Health Records")
        health_btn.clicked.connect(self.open_health_window)

        medication_btn = QPushButton("💊 Medications")
        medication_btn.clicked.connect(self.open_medication_window)

        appointment_btn = QPushButton("📅 Appointments")
        appointment_btn.clicked.connect(self.open_appointment_window)

        logout_btn = QPushButton("🚪 Logout")
        logout_btn.clicked.connect(self.handle_logout)

        layout.addWidget(welcome_label)
        layout.addSpacing(20)
        layout.addWidget(health_btn)
        layout.addWidget(medication_btn)
        layout.addWidget(appointment_btn)
        layout.addSpacing(20)
        layout.addWidget(logout_btn)

        self.setLayout(layout)

    def open_health_window(self):
        self.health_window = HealthWindow(self.user_id)
        self.health_window.show()

    def open_medication_window(self):
        self.med_window = MedicationWindow(self.user_id)
        self.med_window.show()

    def open_appointment_window(self):
        self.app_window = AppointmentWindow(self.user_id)
        self.app_window.show()

    def handle_logout(self):
        QMessageBox.information(self, "Logout", "You have been logged out.")
        self.logout_successful.emit()
        self.close()
