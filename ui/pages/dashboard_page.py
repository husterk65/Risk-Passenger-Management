from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout


class DashboardPage(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("Dashboard")
        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        layout.addStretch()

        self.setLayout(layout)