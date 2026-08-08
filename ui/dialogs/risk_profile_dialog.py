from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QDialogButtonBox,
    QSpinBox,
)

from PyQt6.QtCore import QDate

from models.risk_profile import RiskProfile


class RiskProfileDialog(QDialog):

    def __init__(
        self,
        profile=None,
        parent=None
    ):

        super().__init__(parent)

        self.profile = profile

        self.setWindowTitle(
            "Edit Risk Profile"
            if profile
            else "Add Risk Profile"
        )

        self.setMinimumWidth(500)

        self.init_ui()

        if self.profile:
            self.load_profile()

    # ==================================================
    # UI
    # ==================================================

    def init_ui(self):

        layout = QVBoxLayout()

        form = QFormLayout()

        # ----------------------------------------------
        # Full Name
        # ----------------------------------------------

        self.full_name_edit = QLineEdit()

        form.addRow(
            "Full Name:",
            self.full_name_edit
        )

        # ----------------------------------------------
        # Passport
        # ----------------------------------------------

        self.passport_edit = QLineEdit()

        form.addRow(
            "Passport Number:",
            self.passport_edit
        )

        # ----------------------------------------------
        # Nationality
        # ----------------------------------------------

        self.nationality_edit = QLineEdit()

        form.addRow(
            "Nationality:",
            self.nationality_edit
        )

        # ----------------------------------------------
        # Date of Birth
        # ----------------------------------------------

        self.dob_edit = QDateEdit()

        self.dob_edit.setCalendarPopup(True)

        self.dob_edit.setDisplayFormat(
            "yyyy-MM-dd"
        )

        self.dob_edit.setDate(
            QDate.currentDate()
        )

        form.addRow(
            "Date of Birth:",
            self.dob_edit
        )

        # ----------------------------------------------
        # Gender
        # ----------------------------------------------

        self.gender_combo = QComboBox()

        self.gender_combo.addItems([
            "",
            "Male",
            "Female",
            "Other"
        ])

        form.addRow(
            "Gender:",
            self.gender_combo
        )

        # ----------------------------------------------
        # Flight Count
        # ----------------------------------------------

        self.flight_count_spin = QSpinBox()

        self.flight_count_spin.setMinimum(0)

        self.flight_count_spin.setMaximum(
            999999
        )

        form.addRow(
            "Flight Count:",
            self.flight_count_spin
        )

        # ----------------------------------------------
        # Baggage Card Count
        # ----------------------------------------------

        self.baggage_card_count_spin = QSpinBox()

        self.baggage_card_count_spin.setMinimum(0)

        self.baggage_card_count_spin.setMaximum(
            999999
        )

        form.addRow(
            "Baggage Cards:",
            self.baggage_card_count_spin
        )

        # ----------------------------------------------
        # Destination Airport
        # ----------------------------------------------

        self.destination_airport_edit = QLineEdit()

        form.addRow(
            "Destination Airport:",
            self.destination_airport_edit
        )

        # ----------------------------------------------
        # Risk Level
        # ----------------------------------------------

        self.risk_level_combo = QComboBox()

        self.risk_level_combo.addItems([
            "Low",
            "Medium",
            "High",
            "Critical"
        ])

        form.addRow(
            "Risk Level:",
            self.risk_level_combo
        )

        # ----------------------------------------------
        # Risk Reason
        # ----------------------------------------------

        self.risk_reason_edit = QLineEdit()

        form.addRow(
            "Risk Reason:",
            self.risk_reason_edit
        )

        # ----------------------------------------------
        # Remarks
        # ----------------------------------------------

        self.remarks_edit = QLineEdit()

        form.addRow(
            "Remarks:",
            self.remarks_edit
        )

        # ----------------------------------------------
        # Active
        # ----------------------------------------------

        self.active_combo = QComboBox()

        self.active_combo.addItem(
            "Yes",
            True
        )

        self.active_combo.addItem(
            "No",
            False
        )

        form.addRow(
            "Active:",
            self.active_combo
        )

        layout.addLayout(form)

        # ----------------------------------------------
        # Buttons
        # ----------------------------------------------

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(
            self.accept
        )

        buttons.rejected.connect(
            self.reject
        )

        layout.addWidget(buttons)

        self.setLayout(layout)

    # ==================================================
    # LOAD PROFILE
    # ==================================================

    def load_profile(self):

        self.full_name_edit.setText(
            self.profile.full_name or ""
        )

        self.passport_edit.setText(
            self.profile.passport_number or ""
        )

        self.nationality_edit.setText(
            self.profile.nationality or ""
        )

        # Date
        dob = QDate.fromString(
            self.profile.date_of_birth or "",
            "yyyy-MM-dd"
        )

        if dob.isValid():
            self.dob_edit.setDate(dob)
        else:
            self.dob_edit.setDate(
                QDate.currentDate()
            )

        # Gender
        gender_index = self.gender_combo.findText(
            self.profile.gender or ""
        )

        if gender_index >= 0:
            self.gender_combo.setCurrentIndex(
                gender_index
            )

        # Flight count
        self.flight_count_spin.setValue(
            self.profile.flight_count or 0
        )

        # Baggage cards
        self.baggage_card_count_spin.setValue(
            self.profile.baggage_card_count or 0
        )

        # Destination
        self.destination_airport_edit.setText(
            self.profile.destination_airport or ""
        )

        # Risk level
        risk_index = self.risk_level_combo.findText(
            self.profile.risk_level or "Low"
        )

        if risk_index >= 0:
            self.risk_level_combo.setCurrentIndex(
                risk_index
            )

        # Risk reason
        self.risk_reason_edit.setText(
            self.profile.risk_reason or ""
        )

        # Remarks
        self.remarks_edit.setText(
            self.profile.remarks or ""
        )

        # Active
        active_index = self.active_combo.findData(
            self.profile.active
        )

        if active_index >= 0:
            self.active_combo.setCurrentIndex(
                active_index
            )

    # ==================================================
    # GET PROFILE
    # ==================================================

    def get_profile(self):

        return RiskProfile(

            id=(
                self.profile.id
                if self.profile
                else None
            ),

            full_name=(
                self.full_name_edit
                .text()
                .strip()
            ),

            passport_number=(
                self.passport_edit
                .text()
                .strip()
            ),

            nationality=(
                self.nationality_edit
                .text()
                .strip()
            ),

            date_of_birth=(
                self.dob_edit
                .date()
                .toString("yyyy-MM-dd")
            ),

            gender=(
                self.gender_combo
                .currentText()
            ),

            flight_count=(
                self.flight_count_spin
                .value()
            ),

            baggage_card_count=(
                self.baggage_card_count_spin
                .value()
            ),

            destination_airport=(
                self.destination_airport_edit
                .text()
                .strip()
            ),

            risk_level=(
                self.risk_level_combo
                .currentText()
            ),

            risk_reason=(
                self.risk_reason_edit
                .text()
                .strip()
            ),

            remarks=(
                self.remarks_edit
                .text()
                .strip()
            ),

            active=(
                self.active_combo
                .currentData()
            ),

            created_at=(
                self.profile.created_at
                if self.profile
                else ""
            )
        )