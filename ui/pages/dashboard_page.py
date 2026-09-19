from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)

from services.risk_profile_service import RiskProfileService


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.flights_page = None
        self.risk_alert_store = None

        self.total_profiles_value = None
        self.total_flights_value = None
        self.risk_alerts_value = None

        self.init_ui()
        self.load_data()

    # ============================================================
    # UI
    # ============================================================

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f7fb;
                color: #1f2937;
                font-family: "Segoe UI";
            }

            QLabel {
                color: #1f2937;
                background-color: transparent;
            }

            /* ====================================================
               STAT CARDS
               ==================================================== */

            QFrame#StatCard {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }

            QLabel#CardTitle {
                color: #6b7280;
                font-size: 13px;
                font-weight: 500;
                background-color: transparent;
            }

            QLabel#CardValue {
                font-size: 28px;
                font-weight: 700;
                background-color: transparent;
            }

            /* ====================================================
               SYSTEM OVERVIEW
               ==================================================== */

            QFrame#OverviewCard {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }

            QLabel#OverviewTitle {
                color: #111827;
                font-size: 16px;
                font-weight: 600;
                background-color: transparent;
            }

            QLabel#OverviewText {
                color: #6b7280;
                font-size: 13px;
                background-color: transparent;
            }

            QLabel#OverviewStatus {
                color: #16a34a;
                font-size: 13px;
                font-weight: 600;
                background-color: transparent;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 24, 28, 28)
        main_layout.setSpacing(22)

        # ========================================================
        # Header
        # ========================================================

        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)

        title = QLabel("Dashboard")
        title.setStyleSheet("""
            font-size: 26px;
            font-weight: 700;
            color: #111827;
        """)

        subtitle = QLabel(
            "Overview of passenger risk management"
        )
        subtitle.setStyleSheet("""
            font-size: 13px;
            color: #6b7280;
        """)

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        main_layout.addLayout(header_layout)

        # ========================================================
        # Statistics Cards
        # ========================================================

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(18)

        # Total Risk Profiles - Blue
        total_card, self.total_profiles_value = self.create_stat_card(
            title="Total Risk Profiles",
            value="0",
            color="#2563EB",
            light_color="#EFF6FF",
        )

        # Total Flights - Purple
        flights_card, self.total_flights_value = self.create_stat_card(
            title="Total Flights",
            value="0",
            color="#7C3AED",
            light_color="#F5F3FF",
        )

        # Risk Alerts - Red
        alerts_card, self.risk_alerts_value = self.create_stat_card(
            title="Risk Alerts",
            value="0",
            color="#DC2626",
            light_color="#FEF2F2",
        )

        cards_layout.addWidget(total_card)
        cards_layout.addWidget(flights_card)
        cards_layout.addWidget(alerts_card)

        main_layout.addLayout(cards_layout)

        # ========================================================
        # System Overview
        # ========================================================

        overview_card = QFrame()
        overview_card.setObjectName("OverviewCard")
        overview_card.setMinimumHeight(120)

        overview_layout = QVBoxLayout(overview_card)
        overview_layout.setContentsMargins(22, 18, 22, 18)
        overview_layout.setSpacing(7)

        overview_title = QLabel("System Overview")
        overview_title.setObjectName("OverviewTitle")

        overview_text = QLabel(
            "The passenger risk management system is ready "
            "for daily operations."
        )
        overview_text.setObjectName("OverviewText")
        overview_text.setWordWrap(True)

        status_layout = QHBoxLayout()
        status_layout.setSpacing(7)

        status_dot = QLabel("●")
        status_dot.setStyleSheet("""
            color: #22C55E;
            font-size: 11px;
        """)

        status_label = QLabel("System Ready")
        status_label.setObjectName("OverviewStatus")

        status_layout.addWidget(status_dot)
        status_layout.addWidget(status_label)
        status_layout.addStretch()

        overview_layout.addWidget(overview_title)
        overview_layout.addWidget(overview_text)
        overview_layout.addLayout(status_layout)
        overview_layout.addStretch()

        main_layout.addWidget(overview_card)

        main_layout.addStretch(1)

    # ============================================================
    # Statistic Card
    # ============================================================

    def create_stat_card(
        self,
        title,
        value,
        color,
        light_color,
    ):
        card = QFrame()
        card.setObjectName("StatCard")
        card.setMinimumHeight(128)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)

        # --------------------------------------------------------
        # Top row
        # --------------------------------------------------------

        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)

        # Colored indicator
        indicator = QLabel("●")
        indicator.setStyleSheet(f"""
            color: {color};
            font-size: 13px;
        """)

        title_label = QLabel(title)
        title_label.setObjectName("CardTitle")

        top_layout.addWidget(indicator)
        top_layout.addWidget(title_label)
        top_layout.addStretch()

        # --------------------------------------------------------
        # Value
        # --------------------------------------------------------

        value_label = QLabel(value)
        value_label.setObjectName("CardValue")

        value_label.setStyleSheet(f"""
            color: {color};
            font-size: 28px;
            font-weight: 700;
        """)

        value_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft |
            Qt.AlignmentFlag.AlignVCenter
        )

        # --------------------------------------------------------
        # Bottom accent
        # --------------------------------------------------------

        accent = QFrame()
        accent.setFixedHeight(4)

        accent.setStyleSheet(f"""
            background-color: {light_color};
            border-radius: 2px;
        """)

        layout.addLayout(top_layout)
        layout.addWidget(value_label)
        layout.addStretch()
        layout.addWidget(accent)

        return card, value_label

    # ============================================================
    # Load Data
    # ============================================================

    def set_runtime_sources(
        self,
        flights_page,
        risk_alert_store
    ):
        self.flights_page = flights_page
        self.risk_alert_store = risk_alert_store
        self.refresh_runtime_counts()

    def load_data(self):
        self.load_risk_profiles()
        self.refresh_runtime_counts()

    def refresh_runtime_counts(self):
        self.load_flights()
        self.load_alerts()

    # ============================================================
    # Risk Profiles
    # ============================================================

    def load_risk_profiles(self):
        try:
            profiles = RiskProfileService.get_all()

            if profiles is None:
                profiles = []

            self.total_profiles_value.setText(str(len(profiles)))

        except Exception as e:
            print(
                f"[Dashboard] Failed to load risk profiles: {e}"
            )

            self.total_profiles_value.setText("0")

    # ============================================================
    # Flights
    # ============================================================

    def load_flights(self):
        flights = []

        if self.flights_page is not None:
            flights = self.flights_page.flights or []

        self.total_flights_value.setText(str(len(flights)))

    # ============================================================
    # Risk Alerts
    # ============================================================

    def load_alerts(self):
        total_alerts = 0

        if self.risk_alert_store is not None:
            total_alerts = self.risk_alert_store.count()

        self.risk_alerts_value.setText(str(total_alerts))

    # ============================================================
    # Refresh
    # ============================================================

    def refresh(self):
        """
        Refresh Dashboard data.

        Can be called from MainWindow later if needed.
        """

        self.load_data()