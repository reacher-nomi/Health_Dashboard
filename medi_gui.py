# medication_gui.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox,
    QComboBox, QCheckBox, QListWidget, QListWidgetItem, QDateEdit, QHBoxLayout
)
from PyQt6.QtCore import QDate
from medi import add_medication, get_medications, delete_medication

class MedicationWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Medication Tracker")
        self.setFixedSize(400, 500)
        self.init_ui()
        self.load_medications()

    def init_ui(self):
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Medicine Name")

        self.dosage_input = QLineEdit()
        self.dosage_input.setPlaceholderText("Dosage (e.g., 500mg)")

        self.frequency_input = QComboBox()
        self.frequency_input.addItems(["Once a day", "Twice a day", "Every 6 hours", "As needed"])

        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDate.currentDate())

        self.end_date_input = QDateEdit()
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDate(QDate.currentDate())

        self.reminder_checkbox = QCheckBox("Enable Reminder")

        self.add_button = QPushButton("Add Medication")
        self.add_button.clicked.connect(self.add_med)

        self.med_list = QListWidget()
        self.med_list.itemDoubleClicked.connect(self.delete_selected_med)

        layout.addWidget(QLabel("Medicine Name:"))
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Dosage:"))
        layout.addWidget(self.dosage_input)

        layout.addWidget(QLabel("Frequency:"))
        layout.addWidget(self.frequency_input)

        layout.addWidget(QLabel("Start Date:"))
        layout.addWidget(self.start_date_input)

        layout.addWidget(QLabel("End Date:"))
        layout.addWidget(self.end_date_input)

        layout.addWidget(self.reminder_checkbox)
        layout.addWidget(self.add_button)

        layout.addWidget(QLabel("Your Medications (double-click to delete):"))
        layout.addWidget(self.med_list)

        self.setLayout(layout)

    def add_med(self):
        name = self.name_input.text().strip()
        dosage = self.dosage_input.text().strip()
        frequency = self.frequency_input.currentText()
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")
        reminder = 1 if self.reminder_checkbox.isChecked() else 0

        if not name or not dosage:
            QMessageBox.warning(self, "Missing Info", "Please fill all required fields.")
            return

        success, msg = add_medication(
            self.user_id, name, dosage, frequency, start_date, end_date, reminder
        )
        if success:
            QMessageBox.information(self, "Success", msg)
            self.clear_inputs()
            self.load_medications()
        else:
            QMessageBox.critical(self, "Error", msg)

    def load_medications(self):
        self.med_list.clear()
        medications = get_medications(self.user_id)
        for med in medications:
            item = QListWidgetItem(
                f"{med[1]} | {med[2]} | {med[3]} | {med[4]} to {med[5]} | Reminder: {'Yes' if med[6] else 'No'}"
            )
            item.setData(1, med[0])  # medication ID
            self.med_list.addItem(item)

    def delete_selected_med(self, item):
        med_id = item.data(1)
        confirm = QMessageBox.question(
            self, "Confirm Delete", "Are you sure you want to delete this medication?"
        )
        if confirm == QMessageBox.StandardButton.Yes:
            if delete_medication(med_id):
                QMessageBox.information(self, "Deleted", "Medication deleted.")
                self.load_medications()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete.")
    
    def clear_inputs(self):
        self.name_input.clear()
        self.dosage_input.clear()
        self.frequency_input.setCurrentIndex(0)
        self.reminder_checkbox.setChecked(False)
        self.start_date_input.setDate(QDate.currentDate())
        self.end_date_input.setDate(QDate.currentDate())
