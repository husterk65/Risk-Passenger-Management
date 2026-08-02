from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QListWidget,
    QListWidgetItem,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QStatusBar,
    QStackedWidget
)

from models.current_user import CurrentUser
from ui.pages.dashboard_page import DashboardPage


class MainWindow(QMainWindow):

    def __init__(self, current_user):

        super().__init__()
        self.current_user = current_user
        self.setWindowTitle("Passenger Risk Management")
        self.resize(1200, 700)

        self.init_ui()

    def init_ui(self):

        central = QWidget()

        self.setCentralWidget(central)

        root_layout = QHBoxLayout()

        central.setLayout(root_layout)

        # ==========================
        # Sidebar
        # ==========================

        self.sidebar = QListWidget()

        menus = [
            "Dashboard",
            "Risk Profiles",
            "Flights",
            "Risk Alerts",
            "Inspection",
            "History",
            "Users"
        ]

        for menu in menus:
            self.sidebar.addItem(QListWidgetItem(menu))

        self.sidebar.setFixedWidth(250)
        self.sidebar.setStyleSheet("""
        QListWidget{
            font-size:14px;
            border-right:1px solid #DADADA;
        }

        QListWidget::item{
            padding:12px;
            margin:2px;
        }

        QListWidget::item:selected{
            background:#1976D2;
            color:white;
        }
        """)
        # ==========================
        # Pages
        # ==========================

        self.pages = QStackedWidget()

        self.dashboard_page = DashboardPage()

        self.pages.addWidget(self.dashboard_page)

        # Temporary pages

        for text in [
            "Risk Profiles",
            "Flights",
            "Risk Alerts",
            "Inspection",
            "History",
            "Users"
        ]:

            page = QWidget()

            layout = QVBoxLayout()

            label = QLabel(text)

            label.setStyleSheet("""
                font-size:24px;
                font-weight:bold;
            """)

            layout.addWidget(label)

            layout.addStretch()

            page.setLayout(layout)

            self.pages.addWidget(page)

        root_layout.addWidget(self.sidebar)
        root_layout.addWidget(self.pages)

        self.sidebar.currentRowChanged.connect(
            self.pages.setCurrentIndex
        )

        self.sidebar.setCurrentRow(0)

        status = QStatusBar()

        status.showMessage(
            f"Logged in as {self.current_user.role}"
        )

        self.setStatusBar(status)