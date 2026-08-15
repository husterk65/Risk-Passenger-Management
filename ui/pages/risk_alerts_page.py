from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFrame,
)


class RiskAlertsPage(QWidget):

    def __init__(
        self,
        alert_store
    ):

        super().__init__()

        self.alert_store = alert_store

        self.init_ui()

        self.refresh()

    # =========================================================
    # UI
    # =========================================================

    def init_ui(self):

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        layout.setSpacing(
            16
        )

        # =====================================================
        # HEADER
        # =====================================================

        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()

        title_layout.setSpacing(
            2
        )

        # -----------------------------------------------------
        # Title
        # -----------------------------------------------------

        title = QLabel(
            "Risk Alerts"
        )

        title.setObjectName(
            "PageTitle"
        )

        # -----------------------------------------------------
        # Subtitle
        # -----------------------------------------------------

        subtitle = QLabel(
            "Review passengers identified during risk checks."
        )

        subtitle.setObjectName(
            "PageSubtitle"
        )

        title_layout.addWidget(
            title
        )

        title_layout.addWidget(
            subtitle
        )

        header_layout.addLayout(
            title_layout
        )

        header_layout.addStretch()

        layout.addLayout(
            header_layout
        )

        # =====================================================
        # FILTER CARD
        # =====================================================

        filter_card = QFrame()

        filter_card.setObjectName(
            "Card"
        )

        filter_layout = QHBoxLayout(
            filter_card
        )

        filter_layout.setContentsMargins(
            16,
            14,
            16,
            14
        )

        filter_layout.setSpacing(
            10
        )

        # -----------------------------------------------------
        # Flight
        # -----------------------------------------------------

        flight_label = QLabel(
            "Flight"
        )

        flight_label.setObjectName(
            "FilterLabel"
        )

        filter_layout.addWidget(
            flight_label
        )

        self.flight_filter = QComboBox()

        self.flight_filter.setObjectName(
            "FilterCombo"
        )

        self.flight_filter.setMinimumWidth(
            220
        )

        self.flight_filter.setMinimumHeight(
            38
        )

        self.flight_filter.currentIndexChanged.connect(
            self.refresh_table
        )

        filter_layout.addWidget(
            self.flight_filter
        )

        filter_layout.addSpacing(
            14
        )

        # -----------------------------------------------------
        # Search
        # -----------------------------------------------------

        search_label = QLabel(
            "Search"
        )

        search_label.setObjectName(
            "FilterLabel"
        )

        filter_layout.addWidget(
            search_label
        )

        self.search_box = QLineEdit()

        self.search_box.setObjectName(
            "SearchBox"
        )

        self.search_box.setPlaceholderText(
            "Passenger, passport, nationality..."
        )

        self.search_box.setMinimumWidth(
            320
        )

        self.search_box.setMinimumHeight(
            38
        )

        self.search_box.textChanged.connect(
            self.refresh_table
        )

        filter_layout.addWidget(
            self.search_box
        )

        filter_layout.addStretch()

        layout.addWidget(
            filter_card
        )

        # =====================================================
        # SUMMARY
        # =====================================================

        summary_card = QFrame()

        summary_card.setObjectName(
            "SummaryCard"
        )

        summary_layout = QHBoxLayout(
            summary_card
        )

        summary_layout.setContentsMargins(
            16,
            12,
            16,
            12
        )

        # -----------------------------------------------------
        # Alert icon / indicator
        # -----------------------------------------------------

        indicator = QFrame()

        indicator.setObjectName(
            "AlertIndicator"
        )

        indicator.setFixedSize(
            8,
            32
        )

        summary_layout.addWidget(
            indicator
        )

        summary_text_layout = QVBoxLayout()

        summary_text_layout.setSpacing(
            0
        )

        summary_title = QLabel(
            "Risk Alerts"
        )

        summary_title.setObjectName(
            "SummaryTitle"
        )

        self.summary_label = QLabel(
            "0 alert(s)"
        )

        self.summary_label.setObjectName(
            "SummaryValue"
        )

        summary_text_layout.addWidget(
            summary_title
        )

        summary_text_layout.addWidget(
            self.summary_label
        )

        summary_layout.addLayout(
            summary_text_layout
        )

        summary_layout.addStretch()

        layout.addWidget(
            summary_card
        )

        # =====================================================
        # TABLE CARD
        # =====================================================

        table_card = QFrame()

        table_card.setObjectName(
            "Card"
        )

        table_layout = QVBoxLayout(
            table_card
        )

        table_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        table_layout.setSpacing(
            0
        )

        # -----------------------------------------------------
        # Table
        # -----------------------------------------------------

        self.table = QTableWidget()

        self.table.setObjectName(
            "RiskAlertTable"
        )

        self.table.setColumnCount(
            9
        )

        self.table.setHorizontalHeaderLabels([
            "Flight",
            "Full Name",
            "Passport",
            "Nationality",
            "Date of Birth",
            "Gender",
            "Risk Level",
            "Risk Reason",
            "Checked At",
        ])

        self.table.setAlternatingRowColors(
            True
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.table.verticalHeader().setVisible(
            False
        )

        self.table.verticalHeader().setDefaultSectionSize(
            42
        )

        self.table.setShowGrid(
            False
        )

        header = (
            self.table.horizontalHeader()
        )

        header.setMinimumHeight(
            42
        )

        header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft
            |
            Qt.AlignmentFlag.AlignVCenter
        )

        # Các cột cố định theo nội dung

        for column in range(
            self.table.columnCount()
        ):

            header.setSectionResizeMode(
                column,
                QHeaderView.ResizeMode.ResizeToContents
            )

        # Risk reason chiếm phần còn lại

        header.setSectionResizeMode(
            7,
            QHeaderView.ResizeMode.Stretch
        )

        table_layout.addWidget(
            self.table
        )

        layout.addWidget(
            table_card
        )

        # =====================================================
        # EMPTY STATE
        # =====================================================

        self.empty_state = QFrame()

        self.empty_state.setObjectName(
            "EmptyState"
        )

        empty_layout = QVBoxLayout(
            self.empty_state
        )

        empty_layout.setContentsMargins(
            20,
            45,
            20,
            45
        )

        empty_layout.setSpacing(
            8
        )

        empty_icon = QLabel(
            "✓"
        )

        empty_icon.setObjectName(
            "EmptyIcon"
        )

        empty_icon.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        empty_title = QLabel(
            "No Risk Alerts"
        )

        empty_title.setObjectName(
            "EmptyTitle"
        )

        empty_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        empty_subtitle = QLabel(
            "No passengers have been flagged "
            "for the selected flight."
        )

        empty_subtitle.setObjectName(
            "EmptySubtitle"
        )

        empty_subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        empty_layout.addWidget(
            empty_icon
        )

        empty_layout.addWidget(
            empty_title
        )

        empty_layout.addWidget(
            empty_subtitle
        )

        layout.addWidget(
            self.empty_state
        )

        # Ban đầu table / empty state được điều khiển
        self.empty_state.hide()

        # =====================================================
        # STYLE
        # =====================================================

        self.setStyleSheet("""

        /* =================================================
           PAGE HEADER
           ================================================= */

        QLabel#PageTitle {
            font-size: 30px;
            font-weight: 700;
            color: #0f172a;
        }

        QLabel#PageSubtitle {
            font-size: 13px;
            color: #64748b;
        }


        /* =================================================
           CARD
           ================================================= */

        QFrame#Card {
            background: #ffffff;
            border: 1px solid #dbe3ef;
            border-radius: 12px;
        }


        /* =================================================
           FILTER
           ================================================= */

        QLabel#FilterLabel {
            font-size: 13px;
            font-weight: 600;
            color: #334155;
        }

        QComboBox#FilterCombo {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 7px;
            padding: 0 10px;
            color: #0f172a;
        }

        QComboBox#FilterCombo:hover {
            border: 1px solid #94a3b8;
        }

        QComboBox#FilterCombo:focus {
            border: 1px solid #2563eb;
        }

        QComboBox#FilterCombo::drop-down {
            border: none;
            width: 28px;
        }

        QLineEdit#SearchBox {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 7px;
            padding: 0 12px;
            color: #0f172a;
        }

        QLineEdit#SearchBox:hover {
            border: 1px solid #94a3b8;
        }

        QLineEdit#SearchBox:focus {
            border: 1px solid #2563eb;
        }


        /* =================================================
           SUMMARY
           ================================================= */

        QFrame#SummaryCard {
            background: #ffffff;
            border: 1px solid #dbe3ef;
            border-radius: 10px;
        }

        QFrame#AlertIndicator {
            background: #dc2626;
            border-radius: 4px;
        }

        QLabel#SummaryTitle {
            font-size: 11px;
            font-weight: 600;
            color: #64748b;
        }

        QLabel#SummaryValue {
            font-size: 16px;
            font-weight: 700;
            color: #0f172a;
        }


        /* =================================================
           TABLE
           ================================================= */

        QTableWidget#RiskAlertTable {
            background: #ffffff;
            border: none;
            color: #0f172a;
            font-size: 12px;
            selection-background-color: #e0ecff;
            selection-color: #0f172a;
            alternate-background-color: #f8fafc;
        }

        QHeaderView::section {
            background: #f8fafc;
            color: #475569;
            border: none;
            border-bottom: 1px solid #e2e8f0;
            padding: 11px 10px;
            font-size: 11px;
            font-weight: 700;
        }

        QTableWidget::item {
            border-bottom: 1px solid #f1f5f9;
            padding: 8px;
        }

        QTableWidget::item:selected {
            background: #e0ecff;
            color: #0f172a;
        }


        /* =================================================
           EMPTY STATE
           ================================================= */

        QFrame#EmptyState {
            background: #ffffff;
            border: 1px solid #dbe3ef;
            border-radius: 12px;
        }

        QLabel#EmptyIcon {
            font-size: 34px;
            font-weight: 700;
            color: #16a34a;
        }

        QLabel#EmptyTitle {
            font-size: 18px;
            font-weight: 700;
            color: #0f172a;
        }

        QLabel#EmptySubtitle {
            font-size: 13px;
            color: #64748b;
        }

        """)

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):

        self.refresh_flight_filter()

        self.refresh_table()

    # =========================================================
    # FLIGHT FILTER
    # =========================================================

    def refresh_flight_filter(self):

        current_value = (
            self.flight_filter.currentData()
        )

        self.flight_filter.blockSignals(
            True
        )

        self.flight_filter.clear()

        # -----------------------------------------------------
        # All flights
        # -----------------------------------------------------

        self.flight_filter.addItem(
            "All Flights",
            None
        )

        # -----------------------------------------------------
        # Get flights from runtime alerts
        # -----------------------------------------------------

        flights = {}

        for alert in (
            self.alert_store.get_all()
        ):

            flights[
                alert.flight_id
            ] = alert.flight_number

        # -----------------------------------------------------
        # Add flights
        # -----------------------------------------------------

        for flight_id, flight_number in sorted(
            flights.items(),
            key=lambda x: x[1]
        ):

            self.flight_filter.addItem(
                flight_number,
                flight_id
            )

        # -----------------------------------------------------
        # Restore previous selection
        # -----------------------------------------------------

        if current_value is not None:

            index = (
                self.flight_filter.findData(
                    current_value
                )
            )

            if index >= 0:

                self.flight_filter.setCurrentIndex(
                    index
                )

        self.flight_filter.blockSignals(
            False
        )

    # =========================================================
    # TABLE
    # =========================================================

    def refresh_table(self):

        alerts = (
            self.alert_store.get_all()
        )

        # =====================================================
        # FLIGHT FILTER
        # =====================================================

        selected_flight_id = (
            self.flight_filter.currentData()
        )

        if selected_flight_id is not None:

            alerts = [
                alert
                for alert in alerts
                if alert.flight_id
                == selected_flight_id
            ]

        # =====================================================
        # SEARCH
        # =====================================================

        keyword = (
            self.search_box
            .text()
            .strip()
            .upper()
        )

        if keyword:

            alerts = [

                alert

                for alert in alerts

                if (
                    keyword
                    in (
                        alert.full_name
                        or ""
                    ).upper()

                    or

                    keyword
                    in (
                        alert.passport_number
                        or ""
                    ).upper()

                    or

                    keyword
                    in (
                        alert.nationality
                        or ""
                    ).upper()
                )
            ]

        # =====================================================
        # SUMMARY
        # =====================================================

        self.summary_label.setText(
            f"{len(alerts)} alert(s)"
        )

        # =====================================================
        # EMPTY STATE
        # =====================================================

        if not alerts:

            self.table.hide()

            self.empty_state.show()

            return

        self.empty_state.hide()

        self.table.show()

        # =====================================================
        # TABLE DATA
        # =====================================================

        self.table.setRowCount(
            len(alerts)
        )

        for row_index, alert in enumerate(
            alerts
        ):

            values = [

                alert.flight_number,

                alert.full_name,

                alert.passport_number,

                alert.nationality,

                alert.date_of_birth,

                alert.gender,

                alert.risk_level,

                alert.risk_reason,

                alert.created_at,
            ]

            for column_index, value in enumerate(
                values
            ):

                item = QTableWidgetItem(
                    str(
                        value
                        or ""
                    )
                )

                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignVCenter
                    |
                    Qt.AlignmentFlag.AlignLeft
                )

                self.table.setItem(
                    row_index,
                    column_index,
                    item
                )

            # =================================================
            # RISK LEVEL
            # =================================================

            risk_level = (
                str(
                    alert.risk_level
                    or ""
                )
                .strip()
                .upper()
            )

            risk_item = (
                self.table.item(
                    row_index,
                    6
                )
            )

            if risk_item:

                if risk_level == "HIGH":

                    risk_item.setText(
                        "●  High"
                    )

                    risk_item.setForeground(
                        Qt.GlobalColor.darkRed
                    )

                elif risk_level == "MEDIUM":

                    risk_item.setText(
                        "●  Medium"
                    )

                    risk_item.setForeground(
                        Qt.GlobalColor.darkYellow
                    )

                elif risk_level == "LOW":

                    risk_item.setText(
                        "●  Low"
                    )

                    risk_item.setForeground(
                        Qt.GlobalColor.darkGreen
                    )

        # =====================================================
        # ROW HEIGHT
        # =====================================================

        for row in range(
            self.table.rowCount()
        ):

            self.table.setRowHeight(
                row,
                42
            )