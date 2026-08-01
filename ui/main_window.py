from PyQt6.QtWidgets import (
    QLabel,
    QListWidget,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStatusBar,
)


class MainWindow(QMainWindow):

    def __init__(self, current_user):

        super().__init__()

        self.current_user = current_user

        self.setWindowTitle("Passenger Risk Management")
        self.resize(1400, 800)

        self.init_ui()

    def init_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout()

        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(220)

        self.sidebar.addItems([
            "Dashboard",
            "Risk Profiles",
            "Flights",
            "Risk Alerts",
            "Inspection",
            "History",
            "Users"
        ])

        content = QWidget()

        content_layout = QVBoxLayout()

        title = QLabel(
            f"Welcome {self.current_user.full_name}"
        )

        content_layout.addWidget(title)
        content_layout.addStretch()

        content.setLayout(content_layout)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(content)

        central.setLayout(main_layout)

        status = QStatusBar()
        status.showMessage(
            f"Logged in as {self.current_user.role}"
        )

        self.setStatusBar(status)