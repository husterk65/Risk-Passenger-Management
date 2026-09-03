from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFrame,
    QPushButton,
    QCheckBox,
    QFileDialog,
    QMessageBox,
)

from utils.excel_service import ExcelService


# =============================================================
# FLIGHT FILTER POPUP
# =============================================================

class FlightFilterPopup(QFrame):

    def __init__(self, parent=None):
        super().__init__(
            parent,
            Qt.WindowType.Popup
        )

        self.setObjectName("FlightFilterPopup")

        self.setMinimumWidth(220)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(
            12,
            12,
            12,
            12
        )
        self.layout.setSpacing(6)

        # -----------------------------------------------------
        # Title
        # -----------------------------------------------------

        title = QLabel("Flight")
        title.setObjectName("PopupTitle")

        self.layout.addWidget(title)

        # -----------------------------------------------------
        # All flights
        # -----------------------------------------------------

        self.all_checkbox = QCheckBox("All Flights")
        self.all_checkbox.setChecked(True)

        self.layout.addWidget(
            self.all_checkbox
        )

        self.layout.addSpacing(4)

        # -----------------------------------------------------
        # Flight checkboxes
        # -----------------------------------------------------

        self.flight_checkboxes = []

        self.all_checkbox.stateChanged.connect(
            self._on_all_changed
        )

    # =========================================================
    # SET FLIGHTS
    # =========================================================

    def set_flights(self, flights):

        # Remove old checkboxes

        for checkbox in self.flight_checkboxes:
            self.layout.removeWidget(
                checkbox
            )
            checkbox.deleteLater()

        self.flight_checkboxes.clear()

        # Add new flights

        for flight_id, flight_number in flights:

            checkbox = QCheckBox(
                str(flight_number)
            )

            checkbox.setProperty(
                "flight_id",
                flight_id
            )

            checkbox.stateChanged.connect(
                self._on_flight_changed
            )

            self.flight_checkboxes.append(
                checkbox
            )

            self.layout.addWidget(
                checkbox
            )

    # =========================================================
    # ALL CHANGED
    # =========================================================

    def _on_all_changed(self, state):

        if state == Qt.CheckState.Checked.value:

            for checkbox in self.flight_checkboxes:

                checkbox.blockSignals(True)
                checkbox.setChecked(False)
                checkbox.blockSignals(False)

        self._emit_changed()

    # =========================================================
    # FLIGHT CHANGED
    # =========================================================

    def _on_flight_changed(self, state):

        checked = [
            checkbox
            for checkbox in self.flight_checkboxes
            if checkbox.isChecked()
        ]

        self.all_checkbox.blockSignals(True)

        if checked:
            self.all_checkbox.setChecked(False)
        else:
            self.all_checkbox.setChecked(True)

        self.all_checkbox.blockSignals(False)

        self._emit_changed()

    # =========================================================
    # SELECTED FLIGHTS
    # =========================================================

    def selected_flight_ids(self):

        if self.all_checkbox.isChecked():
            return None

        return [
            checkbox.property("flight_id")
            for checkbox in self.flight_checkboxes
            if checkbox.isChecked()
        ]

    # =========================================================
    # CHANGE CALLBACK
    # =========================================================

    def _emit_changed(self):

        parent = self.parent()

        if parent is not None:
            parent.refresh_table()


# =============================================================
# RISK ALERTS PAGE
# =============================================================

class RiskAlertsPage(QWidget):

    def __init__(self, alert_store):

        super().__init__()

        self.alert_store = alert_store

        self.flight_filter_popup = None

        self.init_ui()

        self.refresh()

    # =========================================================
    # UI
    # =========================================================

    def init_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        layout.setSpacing(16)

        # =====================================================
        # HEADER
        # =====================================================

        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()

        title_layout.setSpacing(2)

        title = QLabel(
            "Risk Alerts"
        )

        title.setObjectName(
            "PageTitle"
        )

        subtitle = QLabel(
            "Review passengers identified during risk checks."
        )

        subtitle.setObjectName(
            "PageSubtitle"
        )

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        header_layout.addLayout(
            title_layout
        )

        header_layout.addStretch()

        # -----------------------------------------------------
        # Export Excel
        # -----------------------------------------------------

        self.export_excel_button = QPushButton(
            "Export Excel"
        )

        self.export_excel_button.setObjectName(
            "ExportExcelButton"
        )

        self.export_excel_button.setMinimumHeight(
            38
        )

        self.export_excel_button.clicked.connect(
            self.export_excel
        )

        header_layout.addWidget(
            self.export_excel_button
        )

        # -----------------------------------------------------
        # Export PDF
        # -----------------------------------------------------

        self.export_pdf_button = QPushButton(
            "Export PDF"
        )

        self.export_pdf_button.setObjectName(
            "ExportPdfButton"
        )

        self.export_pdf_button.setMinimumHeight(
            38
        )

        self.export_pdf_button.clicked.connect(
            self.export_pdf
        )

        header_layout.addWidget(
            self.export_pdf_button
        )

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

        filter_layout.setSpacing(10)

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

        self.flight_filter_button = QPushButton(
            "All Flights"
        )

        self.flight_filter_button.setObjectName(
            "FilterButton"
        )

        self.flight_filter_button.setMinimumWidth(
            220
        )

        self.flight_filter_button.setMinimumHeight(
            38
        )

        self.flight_filter_button.clicked.connect(
            self.open_flight_filter
        )

        filter_layout.addWidget(
            self.flight_filter_button
        )

        filter_layout.addSpacing(14)

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

        summary_text_layout.setSpacing(0)

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

        table_layout.setSpacing(0)

        # -----------------------------------------------------
        # Table
        # -----------------------------------------------------

        self.table = QTableWidget()

        self.table.setObjectName(
            "RiskAlertTable"
        )

        self.table.setColumnCount(9)

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

        header = self.table.horizontalHeader()

        header.setMinimumHeight(
            42
        )

        header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft
            |
            Qt.AlignmentFlag.AlignVCenter
        )

        # -----------------------------------------------------
        # Column sizing
        # -----------------------------------------------------

        for column in range(
            self.table.columnCount()
        ):

            header.setSectionResizeMode(
                column,
                QHeaderView.ResizeMode.ResizeToContents
            )

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

        empty_layout.setSpacing(8)

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
            "for the selected filter."
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

        self.empty_state.hide()

        # =====================================================
        # STYLE
        # =====================================================

        self.setStyleSheet("""
        QLabel#PageTitle {
            font-size: 30px;
            font-weight: 700;
            color: #0f172a;
        }

        QLabel#PageSubtitle {
            font-size: 13px;
            color: #64748b;
        }

        QFrame#Card {
            background: #ffffff;
            border: 1px solid #dbe3ef;
            border-radius: 12px;
        }

        QLabel#FilterLabel {
            font-size: 13px;
            font-weight: 600;
            color: #334155;
        }

        QPushButton#FilterButton {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 7px;
            padding: 0 12px;
            color: #0f172a;
            text-align: left;
        }

        QPushButton#FilterButton:hover {
            border: 1px solid #94a3b8;
        }

        QPushButton#FilterButton:pressed {
            background: #f8fafc;
        }

        QPushButton#ExportExcelButton {
            background: #ecfdf3;
            border: 1px solid #bbf7d0;
            border-radius: 7px;
            padding: 0 14px;
            color: #15803d;
            font-weight: 600;
        }

        QPushButton#ExportExcelButton:hover {
            background: #dcfce7;
            border: 1px solid #86efac;
        }

        QPushButton#ExportPdfButton {
            background: #fff1f2;
            border: 1px solid #fecdd3;
            border-radius: 7px;
            padding: 0 14px;
            color: #be123c;
            font-weight: 600;
        }

        QPushButton#ExportPdfButton:hover {
            background: #ffe4e6;
            border: 1px solid #fda4af;
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

        QFrame#FlightFilterPopup {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
        }

        QLabel#PopupTitle {
            font-size: 13px;
            font-weight: 700;
            color: #0f172a;
        }

        QCheckBox {
            font-size: 13px;
            color: #334155;
            padding: 4px;
        }

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
            color: #0f172a;
            padding: 8px;
        }

        QTableWidget::item:selected {
            background: #e0ecff;
            color: #0f172a;
        }

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

        alerts = self.alert_store.get_all()

        flights = {}

        for alert in alerts:

            flights[
                alert.flight_id
            ] = alert.flight_number

        # Create popup

        self.flight_filter_popup = FlightFilterPopup(
            self
        )

        sorted_flights = sorted(
            flights.items(),
            key=lambda x: str(
                x[1]
            ).upper()
        )

        self.flight_filter_popup.set_flights(
            sorted_flights
        )

        self.flight_filter_popup.adjustSize()

    # =========================================================
    # OPEN FLIGHT FILTER
    # =========================================================

    def open_flight_filter(self):

        if self.flight_filter_popup is None:
            self.refresh_flight_filter()

        # Position popup below button

        position = (
            self.flight_filter_button
            .mapToGlobal(
                self.flight_filter_button.rect().bottomLeft()
            )
        )

        self.flight_filter_popup.move(
            position
        )

        # IMPORTANT:
        # This is a QWidget/QFrame popup,
        # NOT a QDialog.
        #
        # Therefore:
        # DO NOT use popup.exec()

        self.flight_filter_popup.show()

        self.flight_filter_popup.raise_()

        self.flight_filter_popup.activateWindow()

    # =========================================================
    # GET FILTERED ALERTS
    # =========================================================

    def get_filtered_alerts(self):

        alerts = list(
            self.alert_store.get_all()
        )

        # -----------------------------------------------------
        # Flight filter
        # -----------------------------------------------------

        if self.flight_filter_popup is not None:

            selected_ids = (
                self.flight_filter_popup
                .selected_flight_ids()
            )

            if selected_ids is not None:

                alerts = [
                    alert
                    for alert in alerts
                    if alert.flight_id
                    in selected_ids
                ]

        # -----------------------------------------------------
        # Search
        # -----------------------------------------------------

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

        return alerts

    # =========================================================
    # UPDATE FILTER BUTTON TEXT
    # =========================================================

    def update_filter_button(self):

        if self.flight_filter_popup is None:

            self.flight_filter_button.setText(
                "All Flights"
            )

            return

        selected_ids = (
            self.flight_filter_popup
            .selected_flight_ids()
        )

        if selected_ids is None:

            self.flight_filter_button.setText(
                "All Flights"
            )

            return

        if not selected_ids:

            self.flight_filter_button.setText(
                "All Flights"
            )

            return

        if len(selected_ids) == 1:

            for checkbox in (
                self.flight_filter_popup
                .flight_checkboxes
            ):

                if (
                    checkbox.property(
                        "flight_id"
                    )
                    ==
                    selected_ids[0]
                ):

                    self.flight_filter_button.setText(
                        checkbox.text()
                    )

                    return

        self.flight_filter_button.setText(
            f"{len(selected_ids)} Flights Selected"
        )

    # =========================================================
    # TABLE
    # =========================================================

    def refresh_table(self):

        if not hasattr(
            self,
            "table"
        ):
            return

        self.update_filter_button()

        alerts = self.get_filtered_alerts()

        # -----------------------------------------------------
        # Summary
        # -----------------------------------------------------

        self.summary_label.setText(
            f"{len(alerts)} alert(s)"
        )

        # -----------------------------------------------------
        # Empty state
        # -----------------------------------------------------

        if not alerts:

            self.table.hide()

            self.empty_state.show()

            return

        self.empty_state.hide()

        self.table.show()

        # -----------------------------------------------------
        # Table rows
        # -----------------------------------------------------

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

            # -------------------------------------------------
            # Risk level
            # -------------------------------------------------

            risk_level = (
                str(
                    alert.risk_level
                    or ""
                )
                .strip()
                .upper()
            )

            risk_item = self.table.item(
                row_index,
                6
            )

            if risk_item:

                if risk_level == "HIGH":

                    risk_item.setText(
                        "●  High"
                    )

                    risk_item.setForeground(
                        QColor("#dc2626")
                    )

                elif risk_level == "MEDIUM":

                    risk_item.setText(
                        "●  Medium"
                    )

                    risk_item.setForeground(
                        QColor("#d97706")
                    )

                elif risk_level == "LOW":

                    risk_item.setText(
                        "●  Low"
                    )

                    risk_item.setForeground(
                        QColor("#16a34a")
                    )

            # -------------------------------------------------
            # Row height
            # -------------------------------------------------

            self.table.setRowHeight(
                row_index,
                42
            )

    # =========================================================
    # EXPORT EXCEL
    # =========================================================

    def export_excel(self):

        alerts = self.get_filtered_alerts()

        if not alerts:

            QMessageBox.information(
                self,
                "Export Excel",
                "Không có dữ liệu để xuất."
            )

            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Risk Alerts",
            "risk_alerts.xlsx",
            "Excel Files (*.xlsx)"
        )

        if not file_path:
            return

        try:

            ExcelService.export_risk_alerts(
                alerts,
                file_path
            )

            QMessageBox.information(
                self,
                "Export Excel",
                "Xuất danh sách rủi ro thành công."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Export Excel",
                f"Không thể xuất Excel:\n\n{e}"
            )

    # =========================================================
    # EXPORT PDF
    # =========================================================

    def export_pdf(self):

        alerts = self.get_filtered_alerts()

        if not alerts:

            QMessageBox.information(
                self,
                "Export PDF",
                "Không có dữ liệu để xuất."
            )

            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Risk Alerts",
            "risk_alerts.pdf",
            "PDF Files (*.pdf)"
        )

        if not file_path:
            return

        try:

            ExcelService.export_risk_alerts_pdf(
                alerts,
                file_path
            )

            QMessageBox.information(
                self,
                "Export PDF",
                "Xuất danh sách rủi ro thành công."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Export PDF",
                f"Không thể xuất PDF:\n\n{e}"
            )