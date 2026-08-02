from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QCheckBox,
    QPushButton,
    QHBoxLayout
)

from models.risk_profile import RiskProfile


class RiskProfileDialog(QDialog):

    def __init__(self, profile: RiskProfile | None = None, parent=None):

        super().__init__(parent)

        self.profile = profile

        self.setWindowTitle("Risk Profile")

        self.resize(500, 550)

        self.init_ui()

        if self.profile:
            self.load_data()

    def init_ui(self):

        layout = QVBoxLayout()

        form = QFormLayout()

        self.txt_name = QLineEdit()

        self.txt_passport = QLineEdit()

        self.txt_nationality = QLineEdit()

        self.txt_dob = QLineEdit()
        self.txt_dob.setPlaceholderText("YYYY-MM-DD")

        self.cbo_gender = QComboBox()
        self.cbo_gender.addItems(
            [
                "",
                "Male",
                "Female"
            ]
        )

        self.cbo_risk = QComboBox()
        self.cbo_risk.addItems(
            [
                "Low",
                "Medium",
                "High"
            ]
        )

        self.txt_reason = QTextEdit()

        self.txt_reason.setFixedHeight(70)

        self.txt_remark = QTextEdit()

        self.txt_remark.setFixedHeight(70)

        self.chk_active = QCheckBox()

        self.chk_active.setChecked(True)

        form.addRow("Full Name", self.txt_name)

        form.addRow("Passport", self.txt_passport)

        form.addRow("Nationality", self.txt_nationality)

        form.addRow("Date Of Birth", self.txt_dob)

        form.addRow("Gender", self.cbo_gender)

        form.addRow("Risk Level", self.cbo_risk)

        form.addRow("Risk Reason", self.txt_reason)

        form.addRow("Remarks", self.txt_remark)

        form.addRow("Active", self.chk_active)

        layout.addLayout(form)

        buttons = QHBoxLayout()

        buttons.addStretch()

        self.btn_save = QPushButton("Save")

        self.btn_cancel = QPushButton("Cancel")

        buttons.addWidget(self.btn_save)

        buttons.addWidget(self.btn_cancel)

        layout.addLayout(buttons)

        self.setLayout(layout)

        self.btn_cancel.clicked.connect(self.reject)

        self.btn_save.clicked.connect(self.accept)

    def load_data(self):

        self.txt_name.setText(self.profile.full_name)

        self.txt_passport.setText(self.profile.passport_number)

        self.txt_nationality.setText(self.profile.nationality)

        self.txt_dob.setText(self.profile.date_of_birth)

        self.cbo_gender.setCurrentText(self.profile.gender)

        self.cbo_risk.setCurrentText(self.profile.risk_level)

        self.txt_reason.setPlainText(self.profile.risk_reason)

        self.txt_remark.setPlainText(self.profile.remarks)

        self.chk_active.setChecked(self.profile.active)

    def get_profile(self):

        if self.profile is None:

            self.profile = RiskProfile()

        self.profile.full_name = self.txt_name.text().strip()

        self.profile.passport_number = self.txt_passport.text().strip()

        self.profile.nationality = self.txt_nationality.text().strip()

        self.profile.date_of_birth = self.txt_dob.text().strip()

        self.profile.gender = self.cbo_gender.currentText()

        self.profile.risk_level = self.cbo_risk.currentText()

        self.profile.risk_reason = self.txt_reason.toPlainText().strip()

        self.profile.remarks = self.txt_remark.toPlainText().strip()

        self.profile.active = self.chk_active.isChecked()

        return self.profile