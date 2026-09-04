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
from ui.pages.history_page import HistoryPage


class MainWindow(QMainWindow):

    # =========================================================
    # INIT
    # =========================================================

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
    # ROLE / PERMISSION
    # =========================================================

    def is_admin(self):
        """
        Return True when the current user is an administrator.
        """

        return self.current_user.role.lower() == "admin"

    # =========================================================
    # UI
    # =========================================================

    def init_ui(self):

        # =====================================================
        # CENTRAL WIDGET
        # =====================================================

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

        # -----------------------------------------------------
        # All available menus
        # -----------------------------------------------------

        menus = [
            "Dashboard",
            "Risk Profiles",
            "Flights",
            "Risk Alerts",
        ]

        # -----------------------------------------------------
        # Admin-only menus
        # -----------------------------------------------------

        if self.is_admin():
            menus.extend([
                "History",
                "Users",
            ])

        # -----------------------------------------------------
        # Add menus to sidebar
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Username
        # -----------------------------------------------------

        user_name_label = QLabel(
            f"{self.current_user.full_name}"
        )

        user_name_label.setObjectName(
            "UserNameLabel"
        )

        sidebar_layout.addWidget(
            user_name_label
        )

        # -----------------------------------------------------
        # Role
        # -----------------------------------------------------

        role_label = QLabel(
            f"Role: {self.current_user.role}"
        )

        role_label.setObjectName(
            "UserLabel"
        )

        sidebar_layout.addWidget(
            role_label
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
        # Multiple flights can add results
        # to the same store.

        self.risk_alert_store = (
            RiskAlertStore()
        )

        # =====================================================
        # PAGE MAP
        # =====================================================

        # Instead of depending on hard-coded page indexes,
        # keep a mapping between menu names and page widgets.

        self.page_map = {}

        # =====================================================
        # DASHBOARD
        # =====================================================

        self.dashboard_page = (
            DashboardPage()
        )

        self.add_page(
            "Dashboard",
            self.dashboard_page
        )

        # =====================================================
        # RISK PROFILES
        # =====================================================

        self.risk_profile_page = RiskProfilePage(
            self.current_user
        )

        self.add_page(
            "Risk Profiles",
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
                self.risk_alert_store,
                self.current_user
            )
        )

        self.add_page(
            "Flights",
            self.flights_page
        )

        # =====================================================
        # RISK ALERTS
        # =====================================================

        # IMPORTANT:
        # RiskAlertsPage receives the SAME store.
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

        self.add_page(
            "Risk Alerts",
            self.risk_alerts_page
        )

        # =====================================================
        # ADMIN-ONLY PAGES
        # =====================================================

        if self.is_admin():

            # -------------------------------------------------
            # HISTORY
            # -------------------------------------------------

            self.history_page = HistoryPage()

            self.add_page(
                "History",
                self.history_page
            )

            # -------------------------------------------------
            # USERS
            # -------------------------------------------------

            self.users_page = (
                self.create_placeholder_page(
                    "Users"
                )
            )

            self.add_page(
                "Users",
                self.users_page
            )

        # =====================================================
        # CONTENT
        # =====================================================

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

        # =====================================================
        # START WITH DASHBOARD
        # =====================================================

        if self.sidebar.count() > 0:

            self.sidebar.setCurrentRow(
                0
            )

        # =====================================================
        # STATUS BAR
        # =====================================================

        status = QStatusBar()

        status.showMessage(
            f"Logged in as "
            f"{self.current_user.full_name} "
            f"({self.current_user.role})"
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


        /* =================================================
           Application title
           ================================================= */

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

        QLabel#UserNameLabel {
            color: #e2e8f0;
            font-size: 12px;
            font-weight: 600;
            padding: 4px 4px 0 4px;
        }

        QLabel#UserLabel {
            color: #94a3b8;
            font-size: 11px;
            padding: 4px;
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
    # ADD PAGE
    # =========================================================

    def add_page(
        self,
        name,
        page
    ):
        """
        Add a page to the stacked widget
        and register it in page_map.
        """

        self.page_map[name] = page

        self.pages.addWidget(
            page
        )

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

    # =========================================================
    # PAGE CHANGED
    # =========================================================

    def on_page_changed(
        self,
        index
    ):
        if index < 0:
            return

        # -----------------------------------------------------
        # Get selected menu
        # -----------------------------------------------------

        item = self.sidebar.item(index)

        if item is None:
            return

        page_name = item.text()

        # -----------------------------------------------------
        # Permission protection
        # -----------------------------------------------------

        # User accounts should never be able to access
        # History or Users.
        if (
            page_name in ("History", "Users")
            and not self.is_admin()
        ):
            return

        # -----------------------------------------------------
        # Find page
        # -----------------------------------------------------

        page = self.page_map.get(page_name)

        if page is None:
            return

        # -----------------------------------------------------
        # Show page
        # -----------------------------------------------------

        self.pages.setCurrentWidget(page)

        # -----------------------------------------------------
        # History refresh
        # -----------------------------------------------------

        if page_name == "History":
            self.history_page.load_data()

        # -----------------------------------------------------
        # Risk Alerts refresh
        # -----------------------------------------------------

        if page_name == "Risk Alerts":
            self.risk_alerts_page.refresh()