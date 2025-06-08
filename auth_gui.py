# auth_gui.py
import sys
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import pyqtSignal
from auth import login_user, register_user

class LoginWindow(QWidget):
    login_successful = pyqtSignal(str)  # Sends email when login is successful

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login or Register")
        self.setFixedSize(400, 400)

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Buttons shown first
        self.initial_login_btn = QPushButton("Login")
        self.initial_register_btn = QPushButton("Register")
        self.initial_login_btn.clicked.connect(self.show_login_fields)
        self.initial_register_btn.clicked.connect(self.show_register_fields)

        self.layout.addWidget(self.initial_login_btn)
        self.layout.addWidget(self.initial_register_btn)

        self.setLayout(self.layout)

    def clear_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_login_fields(self):
        self.clear_layout()

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)

        self.layout.addWidget(QLabel("Email:"))
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(QLabel("Password:"))
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(login_btn)

    def show_register_fields(self):
        self.clear_layout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        register_btn = QPushButton("Register")
        register_btn.clicked.connect(self.handle_register)



        self.layout.addWidget(QLabel("Full Name:"))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(QLabel("Email:"))
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(QLabel("Password:"))
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(register_btn)

    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Input Error", "Please enter email and password.")
            return

        if login_user(email, password):
            QMessageBox.information(self, "Success", "Login successful!")
            self.login_successful.emit(email)
        else:
            QMessageBox.critical(self, "Failed", "Invalid credentials.")

    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Input Error", "Please enter email and password.")
            return

        if login_user(email, password):
            QMessageBox.information(self, "Success", "Login successful!")
            self.login_successful.emit(email)
        else:
            QMessageBox.critical(self, "Failed", "Invalid credentials.")

    def handle_register(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not name or not email or not password:
            QMessageBox.warning(self, "Input Error", "Please fill all fields.")
            return

        success, msg = register_user(name, email, password)
        if success:
            QMessageBox.information(self, "Success", msg)
            self.login_successful.emit(email)
        else:
            QMessageBox.critical(self, "Error", msg)