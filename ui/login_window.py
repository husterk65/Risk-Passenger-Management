from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QMessageBox,
)
import traceback
from services.auth_service import AuthService


class LoginWindow(QWidget):

    login_success = pyqtSignal(object)

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Login")
        self.setFixedSize(350, 220)

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        title = QLabel("Passenger Risk Management")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)

        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def login(self):

        username = self.username.text().strip()
        password = self.password.text()

        current_user = AuthService.login(
            username,
            password
        )

        if current_user:

            self.login_success.emit(current_user)
            self.close()

        else:
            traceback.print_exc()
            QMessageBox.warning(
                self,
                "Login",
                "Username or Password is incorrect."
            )