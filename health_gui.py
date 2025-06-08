# health_gui.py
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QComboBox, QTextEdit
)
from health import save_health_record, get_latest_health_record

class HealthWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Health Record")
        self.setFixedSize(350, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("Weight (kg)")

        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Height (cm)")

        self.blood_group_input = QComboBox()
        self.blood_group_input.addItems(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])

        self.mental_health_input = QTextEdit()
        self.mental_health_input.setPlaceholderText("Mental Health Status (e.g., stressed, happy)")
        self.mental_health_input.setFixedHeight(60)

        self.save_button = QPushButton("Save Health Record")
        self.save_button.clicked.connect(self.save_record)

        self.view_button = QPushButton("View Latest Record")
        self.view_button.clicked.connect(self.view_record)

        layout.addWidget(QLabel("Weight (kg):"))
        layout.addWidget(self.weight_input)
        layout.addWidget(QLabel("Height (cm):"))
        layout.addWidget(self.height_input)
        layout.addWidget(QLabel("Blood Group:"))
        layout.addWidget(self.blood_group_input)
        layout.addWidget(QLabel("Mental Health Status:"))
        layout.addWidget(self.mental_health_input)

        layout.addWidget(self.save_button)
        layout.addWidget(self.view_button)

        self.setLayout(layout)

    def save_record(self):
        try:
            weight = float(self.weight_input.text())
            height = float(self.height_input.text())
            blood_group = self.blood_group_input.currentText()
            mental_health_status = self.mental_health_input.toPlainText().strip()

            success, msg = save_health_record(
                self.user_id, weight, height, blood_group, mental_health_status
            )

            if success:
                QMessageBox.information(self, "Success", msg)
                self.clear_inputs()
            else:
                QMessageBox.critical(self, "Error", msg)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Weight and height must be valid numbers.")

    def view_record(self):
        record = get_latest_health_record(self.user_id)
        if record:
            msg = (
                f"Weight: {record[0]} kg\n"
                f"Height: {record[1]} cm\n"
                f"Blood Group: {record[2]}\n"
                f"Mental Health: {record[3]}\n"
                f"BMI: {record[4]}\n"
                f"Date: {record[5]}"
            )
            QMessageBox.information(self, "Latest Health Record", msg)
        else:
            QMessageBox.information(self, "No Records", "No health record found.")

    def clear_inputs(self):
        self.weight_input.clear()
        self.height_input.clear()
        self.mental_health_input.clear()
        self.blood_group_input.setCurrentIndex(0)
