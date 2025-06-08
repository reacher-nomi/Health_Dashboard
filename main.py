import sys
from PyQt6.QtWidgets import QApplication
from auth_gui import LoginWindow
from dashboard import DashboardWindow  

def main():
    app = QApplication(sys.argv)

    # Step 1: Launch Login/Register Window
    login_window = LoginWindow()

    def show_login_again():
        new_login_window = LoginWindow()
        new_login_window.login_successful.connect(on_login_success)
        new_login_window.show()
        app.login_window = new_login_window
    

    # Handle post-login navigation
    def on_login_success(user_email):
        dashboard = DashboardWindow(user_email)
        dashboard.show()

        login_window.close()

        app.dashboard = dashboard
        
        dashboard.logout_successful.connect(show_login_again)
        
    login_window.login_successful.connect(on_login_success)
    login_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
