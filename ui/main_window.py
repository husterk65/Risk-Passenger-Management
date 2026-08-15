from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QListWidget,
    QListWidgetItem,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QStatusBar,
    QStackedWidget,
    QFrame,
)

from ui.pages.dashboard_page import DashboardPage
from ui.pages.risk_profile_page import RiskProfilePage
from ui.pages.flights_page import FlightsPage
from ui.pages.risk_alerts_page import RiskAlertsPage

from utils.risk_alert_store import RiskAlertStore


class MainWindow(QMainWindow):

    def __init__(self, current_user):

        super().__init__()

        self.current_user = current_user

        self.setWindowTitle(
            "Passenger Risk Management"
        )

        self.resize(
            1280,
            750
        )

        self.init_ui()

    # =========================================================
    # UI
    # =========================================================

    def init_ui(self):

        central = QWidget()

        self.setCentralWidget(
            central
        )

        root_layout = QHBoxLayout(
            central
        )

        root_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        root_layout.setSpacing(
            0
        )

        # =====================================================
        # SIDEBAR
        # =====================================================

        sidebar_frame = QFrame()

        sidebar_frame.setObjectName(
            "Sidebar"
        )

        sidebar_frame.setFixedWidth(
            240
        )

        sidebar_layout = QVBoxLayout(
            sidebar_frame
        )

        sidebar_layout.setContentsMargins(
            16,
            20,
            16,
            16
        )

        sidebar_layout.setSpacing(
            10
        )

        # -----------------------------------------------------
        # Application title
        # -----------------------------------------------------

        app_title = QLabel(
            "PASSENGER"
        )

        app_title.setObjectName(
            "AppTitle"
        )

        app_subtitle = QLabel(
            "RISK MANAGEMENT"
        )

        app_subtitle.setObjectName(
            "AppSubtitle"
        )

        sidebar_layout.addWidget(
            app_title
        )

        sidebar_layout.addWidget(
            app_subtitle
        )

        sidebar_layout.addSpacing(
            25
        )

        # =====================================================
        # NAVIGATION
        # =====================================================

        self.sidebar = QListWidget()

        self.sidebar.setObjectName(
            "SidebarList"
        )

        menus = [
            "Dashboard",
            "Risk Profiles",
            "Flights",
            "Risk Alerts",
            "Inspection",
            "History",
            "Users",
        ]

        for menu in menus:

            item = QListWidgetItem(
                menu
            )

            self.sidebar.addItem(
                item
            )

        sidebar_layout.addWidget(
            self.sidebar
        )

        # =====================================================
        # USER INFORMATION
        # =====================================================

        sidebar_layout.addSpacing(
            10
        )

        user_line = QFrame()

        user_line.setFrameShape(
            QFrame.Shape.HLine
        )

        user_line.setObjectName(
            "UserLine"
        )

        sidebar_layout.addWidget(
            user_line
        )

        user_label = QLabel(
            f"Logged in as\n"
            f"{self.current_user.role}"
        )

        user_label.setObjectName(
            "UserLabel"
        )

        sidebar_layout.addWidget(
            user_label
        )

        root_layout.addWidget(
            sidebar_frame
        )

        # =====================================================
        # MAIN CONTENT
        # =====================================================

        content_frame = QFrame()

        content_frame.setObjectName(
            "Content"
        )

        content_layout = QVBoxLayout(
            content_frame
        )

        content_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        content_layout.setSpacing(
            0
        )

        # =====================================================
        # STACKED PAGES
        # =====================================================

        self.pages = QStackedWidget()

        # =====================================================
        # RUNTIME RISK ALERT STORE
        # =====================================================

        # One store for the whole application session.
        #
        # Risk Check results are kept in memory.
        #
        # They are NOT saved to database.
        #
        # Multiple flights can add results to the same store.

        self.risk_alert_store = (
            RiskAlertStore()
        )

        # =====================================================
        # DASHBOARD
        # =====================================================

        self.dashboard_page = (
            DashboardPage()
        )

        self.pages.addWidget(
            self.dashboard_page
        )

        # =====================================================
        # RISK PROFILES
        # =====================================================

        self.risk_profile_page = (
            RiskProfilePage()
        )

        self.pages.addWidget(
            self.risk_profile_page
        )

        # =====================================================
        # FLIGHTS
        # =====================================================

        # IMPORTANT:
        # Pass the SAME RiskAlertStore instance
        # to FlightsPage.

        self.flights_page = (
            FlightsPage(
                self.risk_alert_store
            )
        )

        self.pages.addWidget(
            self.flights_page
        )

        # =====================================================
        # RISK ALERTS
        # =====================================================

        # IMPORTANT:
        # RiskAlertsPage receives the SAME store.
        #
        # Therefore:
        #
        # FlightsPage
        #       ↓
        # RiskAlertStore
        #       ↓
        # RiskAlertsPage

        self.risk_alerts_page = (
            RiskAlertsPage(
                self.risk_alert_store
            )
        )

        self.pages.addWidget(
            self.risk_alerts_page
        )

        # =====================================================
        # TEMPORARY PAGES
        # =====================================================

        for text in [
            "Inspection",
            "History",
            "Users",
        ]:

            page = (
                self.create_placeholder_page(
                    text
                )
            )

            self.pages.addWidget(
                page
            )

        content_layout.addWidget(
            self.pages
        )

        root_layout.addWidget(
            content_frame
        )

        # =====================================================
        # NAVIGATION SIGNAL
        # =====================================================

        self.sidebar.currentRowChanged.connect(
            self.on_page_changed
        )

        # Start with Dashboard

        self.sidebar.setCurrentRow(
            0
        )

        # =====================================================
        # STATUS BAR
        # =====================================================

        status = QStatusBar()

        status.showMessage(
            f"Logged in as "
            f"{self.current_user.role}"
        )

        self.setStatusBar(
            status
        )

        # =====================================================
        # STYLE
        # =====================================================

        self.setStyleSheet("""

        /* =================================================
           Main Window
           ================================================= */

        QMainWindow {
            background: #f8fafc;
        }

        QFrame#Content {
            background: #f8fafc;
        }


        /* =================================================
           Sidebar
           ================================================= */

        QFrame#Sidebar {

            background: #0f172a;

            border: none;
        }


        QLabel#AppTitle {

            color: #ffffff;

            font-size: 18px;

            font-weight: 700;

            letter-spacing: 1px;
        }


        QLabel#AppSubtitle {

            color: #64748b;

            font-size: 10px;

            font-weight: 600;

            letter-spacing: 2px;
        }


        /* =================================================
           Navigation
           ================================================= */

        QListWidget#SidebarList {

            background: transparent;

            border: none;

            outline: none;

            color: #cbd5e1;

            font-size: 13px;
        }


        QListWidget#SidebarList::item {

            padding: 13px 14px;

            margin: 3px 0;

            border-radius: 8px;
        }


        QListWidget#SidebarList::item:hover {

            background: #1e293b;

            color: #ffffff;
        }


        QListWidget#SidebarList::item:selected {

            background: #2563eb;

            color: #ffffff;

            font-weight: 600;
        }


        /* =================================================
           User
           ================================================= */

        QFrame#UserLine {

            color: #1e293b;

            background: #1e293b;

            max-height: 1px;
        }


        QLabel#UserLabel {

            color: #94a3b8;

            font-size: 11px;

            padding: 8px 4px;
        }


        /* =================================================
           Status Bar
           ================================================= */

        QStatusBar {

            background: #ffffff;

            color: #64748b;

            border-top: 1px solid #e2e8f0;

            font-size: 11px;
        }

        """)

    # =========================================================
    # PLACEHOLDER PAGE
    # =========================================================

    def create_placeholder_page(
        self,
        title
    ):

        page = QWidget()

        layout = QVBoxLayout(
            page
        )

        layout.setContentsMargins(
            35,
            30,
            35,
            30
        )

        title_label = QLabel(
            title
        )

        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #0f172a;
        """)

        layout.addWidget(
            title_label
        )

        layout.addStretch()

        return page

    def on_page_changed(self, index):

        self.pages.setCurrentIndex(index)

        # Risk Alerts page
        if index == 3:
            self.risk_alerts_page.refresh()