from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QFrame,
    QFileDialog,
    QMessageBox,
    QTableView,
    QAbstractItemView,
    QHeaderView,
)

from PyQt6.QtGui import (
    QStandardItemModel,
    QStandardItem,
)

from services.flight_service import FlightService
from services.flight_passenger_service import FlightPassengerService
from services.risk_check_service import RiskCheckService

from utils.excel_service import ExcelService


class FlightsPage(QWidget):

    def __init__(
        self,
        risk_alert_store
    ):

        super().__init__()

        # =====================================================
        # RUNTIME RISK ALERT STORE
        # =====================================================

        self.risk_alert_store = (
            risk_alert_store
        )

        # Risk check service dùng chung runtime store
        self.risk_check_service = (
            RiskCheckService(
                self.risk_alert_store
            )
        )

        # =====================================================
        # DATA
        # =====================================================

        self.flights = []

        self.current_flight = None

        self.passengers = []

        self.passengers_by_flight = {}

        # =====================================================
        # UI
        # =====================================================

        self.init_ui()

        self.load_flights()

    # =========================================================
    # UI
    # =========================================================

    def init_ui(self):

        main_layout = QVBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        main_layout.setSpacing(
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
            "Flights"
        )

        title.setObjectName(
            "PageTitle"
        )

        # -----------------------------------------------------
        # Subtitle
        # -----------------------------------------------------

        subtitle = QLabel(
            "Manage imported flights and passenger lists."
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

        # =====================================================
        # IMPORT EXCEL
        # =====================================================

        self.import_button = QPushButton(
            "Import Excel"
        )

        self.import_button.setObjectName(
            "PrimaryButton"
        )

        self.import_button.clicked.connect(
            self.import_excel
        )

        header_layout.addWidget(
            self.import_button
        )

        # =====================================================
        # RISK CHECK
        # =====================================================

        self.risk_check_button = QPushButton(
            "Risk Check"
        )

        self.risk_check_button.setObjectName(
            "RiskCheckButton"
        )

        # Chưa chọn flight -> disable
        self.risk_check_button.setEnabled(
            False
        )

        self.risk_check_button.clicked.connect(
            self.run_risk_check
        )

        header_layout.addWidget(
            self.risk_check_button
        )

        main_layout.addLayout(
            header_layout
        )

        # =====================================================
        # CONTENT
        # =====================================================

        content_layout = QHBoxLayout()

        content_layout.setSpacing(
            16
        )

        # =====================================================
        # LEFT PANEL
        # FLIGHT LIST
        # =====================================================

        left_frame = QFrame()

        left_frame.setObjectName(
            "Card"
        )

        left_frame.setFixedWidth(
            300
        )

        left_layout = QVBoxLayout(
            left_frame
        )

        left_layout.setContentsMargins(
            16,
            16,
            16,
            16
        )

        left_layout.setSpacing(
            12
        )

        # -----------------------------------------------------
        # Flight List title
        # -----------------------------------------------------

        flight_title = QLabel(
            "Flight List"
        )

        flight_title.setObjectName(
            "SectionTitle"
        )

        left_layout.addWidget(
            flight_title
        )

        # -----------------------------------------------------
        # Search
        # -----------------------------------------------------

        self.search_box = QLineEdit()

        self.search_box.setPlaceholderText(
            "Search flights..."
        )

        self.search_box.setMinimumHeight(
            40
        )

        self.search_box.textChanged.connect(
            self.filter_flights
        )

        left_layout.addWidget(
            self.search_box
        )

        # -----------------------------------------------------
        # Flight list
        # -----------------------------------------------------

        self.flight_list = QListWidget()

        self.flight_list.setObjectName(
            "FlightList"
        )

        self.flight_list.setSelectionMode(
            QListWidget.SelectionMode.SingleSelection
        )

        self.flight_list.currentItemChanged.connect(
            self.on_flight_selected
        )

        left_layout.addWidget(
            self.flight_list
        )

        # -----------------------------------------------------
        # Flight count
        # -----------------------------------------------------

        self.flight_count_label = QLabel(
            "0 flight(s)"
        )

        self.flight_count_label.setObjectName(
            "CountLabel"
        )

        left_layout.addWidget(
            self.flight_count_label
        )

        content_layout.addWidget(
            left_frame
        )

        # =====================================================
        # RIGHT PANEL
        # PASSENGERS
        # =====================================================

        right_frame = QFrame()

        right_frame.setObjectName(
            "Card"
        )

        right_layout = QVBoxLayout(
            right_frame
        )

        right_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        right_layout.setSpacing(
            10
        )

        # -----------------------------------------------------
        # Flight number
        # -----------------------------------------------------

        self.flight_header = QLabel(
            "Select a flight"
        )

        self.flight_header.setObjectName(
            "FlightHeader"
        )

        right_layout.addWidget(
            self.flight_header
        )

        # -----------------------------------------------------
        # Flight information
        # -----------------------------------------------------

        self.flight_info = QLabel(
            "Choose a flight from the list "
            "to view its passengers."
        )

        self.flight_info.setObjectName(
            "FlightInfo"
        )

        right_layout.addWidget(
            self.flight_info
        )

        # -----------------------------------------------------
        # Passenger count
        # -----------------------------------------------------

        self.passenger_count = QLabel(
            ""
        )

        self.passenger_count.setObjectName(
            "PassengerCount"
        )

        right_layout.addWidget(
            self.passenger_count
        )

        # -----------------------------------------------------
        # Passenger table
        # -----------------------------------------------------

        self.passenger_table = QTableView()

        self.passenger_table.setObjectName(
            "PassengerTable"
        )

        self.passenger_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.passenger_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.passenger_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.passenger_table.setAlternatingRowColors(
            True
        )

        self.passenger_table.verticalHeader().setVisible(
            False
        )

        self.passenger_table.horizontalHeader().setStretchLastSection(
            False
        )

        self.passenger_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        right_layout.addWidget(
            self.passenger_table
        )

        content_layout.addWidget(
            right_frame
        )

        main_layout.addLayout(
            content_layout
        )

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

        QLabel#SectionTitle {
            font-size: 18px;
            font-weight: 700;
            color: #0f172a;
        }

        QLabel#FlightHeader {
            font-size: 24px;
            font-weight: 700;
            color: #0f172a;
        }

        QLabel#FlightInfo {
            font-size: 13px;
            color: #64748b;
        }

        QLabel#PassengerCount {
            font-size: 16px;
            font-weight: 600;
            color: #0f172a;
        }

        QLabel#CountLabel {
            color: #64748b;
            font-size: 12px;
        }

        QLineEdit {
            border: 1px solid #cbd5e1;
            border-radius: 7px;
            padding: 9px;
            background: #ffffff;
            color: #0f172a;
            selection-color: #0f172a;
            selection-background-color: #dbeafe;
        }

        QLineEdit:focus {
            border: 1px solid #2563eb;
        }

        QPushButton#PrimaryButton {
            background: #2563eb;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 11px 18px;
            font-weight: 600;
        }

        QPushButton#PrimaryButton:hover {
            background: #1d4ed8;
        }

        QPushButton#RiskCheckButton {
            background: #0f766e;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 11px 18px;
            font-weight: 600;
        }

        QPushButton#RiskCheckButton:hover {
            background: #115e59;
        }

        QPushButton#RiskCheckButton:disabled {
            background: #cbd5e1;
            color: #64748b;
        }

        QListWidget#FlightList {
            border: none;
            background: transparent;
            color: #0f172a;
        }

        QListWidget#FlightList::item {
            color: #0f172a;
            padding: 12px;
            margin-bottom: 6px;
            border-radius: 8px;
        }

        QListWidget#FlightList::item:hover {
            background: #f1f5f9;
        }

        QListWidget#FlightList::item:selected {
            background: #e0ecff;
            color: #1d4ed8;
        }

        QTableView#PassengerTable {
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            gridline-color: #f1f5f9;
            background: #ffffff;
            color: #0f172a;
        }

        QTableView#PassengerTable::item {
            background: #ffffff;
            color: #0f172a;
        }

        QTableView#PassengerTable::item:alternate {
            background: #f8fafc;
        }

        QTableView#PassengerTable QHeaderView::section {
            background: #f8fafc;
            color: #334155;
            border: none;
            border-bottom: 1px solid #e5e7eb;
            padding: 8px;
            font-weight: 600;
        }

        """)

    # =========================================================
    # LOAD FLIGHTS
    # =========================================================

    def load_flights(self):

        try:

            self.flights = (
                FlightService.get_all()
            )

            self.display_flights(
                self.flights
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"Failed to load flights:\n{e}"
            )

    # =========================================================
    # DISPLAY FLIGHTS
    # =========================================================

    def display_flights(
        self,
        flights
    ):

        self.flight_list.blockSignals(
            True
        )

        self.flight_list.clear()

        for flight in flights:

            item = QListWidgetItem()

            item.setData(
                Qt.ItemDataRole.UserRole,
                flight
            )

            text = (
                f"{flight.flight_number}\n"
                f"{flight.airline}\n"
                f"{flight.flight_date}\n"
                f"{flight.origin} → "
                f"{flight.destination}"
            )

            item.setText(
                text
            )

            self.flight_list.addItem(
                item
            )

        self.flight_list.blockSignals(
            False
        )

        self.flight_count_label.setText(
            f"{len(flights)} flight(s)"
        )

    # =========================================================
    # SEARCH
    # =========================================================

    def filter_flights(
        self,
        text
    ):

        text = (
            text
            .strip()
            .lower()
        )

        filtered = []

        for flight in self.flights:

            searchable = " ".join([
                str(
                    getattr(
                        flight,
                        "flight_number",
                        ""
                    )
                ),

                str(
                    getattr(
                        flight,
                        "airline",
                        ""
                    )
                ),

                str(
                    getattr(
                        flight,
                        "origin",
                        ""
                    )
                ),

                str(
                    getattr(
                        flight,
                        "destination",
                        ""
                    )
                ),

                str(
                    getattr(
                        flight,
                        "flight_date",
                        ""
                    )
                ),
            ]).lower()

            if text in searchable:

                filtered.append(
                    flight
                )

        self.display_flights(
            filtered
        )

    # =========================================================
    # FLIGHT SELECTED
    # =========================================================

    def on_flight_selected(
        self,
        current,
        previous
    ):

        if current is None:

            self.current_flight = None

            self.risk_check_button.setEnabled(
                False
            )

            self.flight_header.setText(
                "Select a flight"
            )

            self.flight_info.setText(
                "Choose a flight from the list "
                "to view its passengers."
            )

            self.passenger_count.setText(
                ""
            )

            self.passenger_table.setModel(
                None
            )

            return

        flight = current.data(
            Qt.ItemDataRole.UserRole
        )

        self.current_flight = flight

        # Có flight -> enable Risk Check
        self.risk_check_button.setEnabled(
            True
        )

        self.show_flight(
            flight
        )

    # =========================================================
    # SHOW FLIGHT
    # =========================================================

    def show_flight(
        self,
        flight
    ):

        self.flight_header.setText(
            flight.flight_number
        )

        self.flight_info.setText(
            f"{flight.airline}  •  "
            f"{flight.flight_date}  •  "
            f"{flight.origin} → "
            f"{flight.destination}"
        )

        try:

            if flight.id not in self.passengers_by_flight:
                self.passengers_by_flight[flight.id] = (
                    FlightPassengerService
                    .get_by_flight(
                        flight.id
                    )
                )

            self.passengers = self.passengers_by_flight[flight.id]

            self.passenger_count.setText(
                f"{len(self.passengers)} passenger(s)"
            )

            self.display_passengers(
                self.passengers
            )

        except Exception as e:

            self.passenger_count.setText(
                "Unable to load passengers"
            )

            QMessageBox.critical(
                self,
                "Error",
                f"Failed to load passengers:\n{e}"
            )

    # =========================================================
    # DISPLAY PASSENGERS
    # =========================================================

    def display_passengers(
        self,
        passengers
    ):

        model = QStandardItemModel()

        columns = [
            ("STT", None),
            ("Seat", "seat_number"),
            ("Full Name", "full_name"),
            ("Gender", "gender"),
            ("Nationality", "nationality"),
            ("Date of Birth", "date_of_birth"),
            ("Document Type", "document_type"),
            ("Document Number", "document_number"),
            ("Issuing Country", "issuing_country"),
            ("Residence Country", "residence_country"),
            ("Origin", "origin"),
            ("Destination", "destination"),
            ("First Airport", "first_airport"),
            ("Baggage", "baggage_count"),
            ("Document Expiry", "document_expiry_date"),
        ]

        model.setColumnCount(
            len(columns)
        )

        model.setHorizontalHeaderLabels(
            [
                title
                for title, _ in columns
            ]
        )

        for index, passenger in enumerate(
            passengers,
            start=1
        ):

            row = []

            for title, field in columns:

                if field is None:

                    value = index

                else:

                    value = getattr(
                        passenger,
                        field,
                        ""
                    )

                item = QStandardItem(
                    str(value)
                )

                item.setEditable(
                    False
                )

                row.append(
                    item
                )

            model.appendRow(
                row
            )

        self.passenger_table.setModel(
            model
        )

    # =========================================================
    # IMPORT EXCEL
    # =========================================================

    def import_excel(self):

        file_path, _ = (
            QFileDialog.getOpenFileName(
                self,
                "Select Excel File",
                "",
                "Excel Files (*.xlsx *.xls)"
            )
        )

        if not file_path:
            return

        try:

            result = (
                ExcelService
                .import_flight_excel(
                    file_path
                )
            )

            # Reload danh sách flight
            self.load_flights()

            QMessageBox.information(
                self,
                "Import Successful",
                (
                    "Flight imported successfully.\n\n"
                    f"Flight: "
                    f"{result.flight.flight_number}\n"
                    f"Passengers: "
                    f"{result.passenger_count}"
                )
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Import Failed",
                str(e)
            )

    # =========================================================
    # RISK CHECK
    # =========================================================

    def run_risk_check(self):

        # -----------------------------------------------------
        # Check flight selected
        # -----------------------------------------------------

        if self.current_flight is None:

            QMessageBox.warning(
                self,
                "No Flight Selected",
                "Please select a flight first."
            )

            return

        flight = (
            self.current_flight
        )

        try:

            # -------------------------------------------------
            # IMPORTANT
            #
            # RiskAlertStore chỉ lưu runtime.
            #
            # Nếu flight này đã được check trước đó,
            # xóa kết quả cũ của flight này trước khi check lại.
            #
            # Các flight khác vẫn được giữ nguyên.
            # -------------------------------------------------

            self.risk_alert_store.replace_flight_alerts(
                flight.id,
                []
            )

            # -------------------------------------------------
            # Run risk check
            # -------------------------------------------------
            #
            # KHÔNG gọi:
            #
            # RiskCheckService.check(...)
            #
            # Vì RiskCheckService của bạn dùng:
            #
            # service = RiskCheckService(alert_store)
            # service.check_flight(flight)
            #
            # -------------------------------------------------

            alerts = (
                self.risk_check_service
                .check_flight(
                    flight
                )
            )

            # -------------------------------------------------
            # Count alerts của flight hiện tại
            # -------------------------------------------------

            flight_alert_count = (
                self.risk_alert_store
                .count_by_flight(
                    flight.id
                )
            )

            # -------------------------------------------------
            # Count tất cả alerts trong session
            # -------------------------------------------------

            total_alert_count = (
                self.risk_alert_store
                .count()
            )

            # -------------------------------------------------
            # Result
            # -----------------------------------------------------

            QMessageBox.information(
                self,
                "Risk Check Complete",
                (
                    f"Flight: "
                    f"{flight.flight_number}\n\n"

                    f"Risk alerts found: "
                    f"{flight_alert_count}\n\n"

                    f"Total alerts in this session: "
                    f"{total_alert_count}"
                )
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Risk Check Failed",
                str(e)
            )