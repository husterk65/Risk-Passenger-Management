from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
)


class UserDialog(QDialog):
    def __init__(self, user=None, parent=None):
        super().__init__(parent)

        self.user = user
        self.is_edit = user is not None

        self.setWindowTitle(
            "Edit User" if self.is_edit else "Add User"
        )
        self.setFixedWidth(420)

        self.init_ui()

        if self.is_edit:
            self.load_user()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # =====================================================
        # Form
        # =====================================================

        form = QFormLayout()
        form.setSpacing(12)

        # Username
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText(
            "Enter username"
        )

        if self.is_edit:
            self.username_edit.setReadOnly(True)

        form.addRow(
            "Username:",
            self.username_edit
        )

        # Full name
        self.full_name_edit = QLineEdit()
        self.full_name_edit.setPlaceholderText(
            "Enter full name"
        )

        form.addRow(
            "Full Name:",
            self.full_name_edit
        )

        # Password
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        if self.is_edit:
            self.password_edit.setPlaceholderText(
                "Leave blank to keep current password"
            )
            password_label = "New Password:"
        else:
            self.password_edit.setPlaceholderText(
                "Enter password"
            )
            password_label = "Password:"

        form.addRow(
            password_label,
            self.password_edit
        )

        # Confirm password
        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setEchoMode(
            QLineEdit.EchoMode.Password
        )
        self.confirm_password_edit.setPlaceholderText(
            "Confirm password"
        )

        if self.is_edit:
            confirm_label = "Confirm New Password:"
        else:
            confirm_label = "Confirm Password:"

        form.addRow(
            confirm_label,
            self.confirm_password_edit
        )

        # Role
        self.role_combo = QComboBox()
        self.role_combo.addItems([
            "User",
            "Admin",
        ])

        form.addRow(
            "Role:",
            self.role_combo
        )

        # Active
        self.active_checkbox = QCheckBox(
            "Active"
        )
        self.active_checkbox.setChecked(True)

        form.addRow(
            "Status:",
            self.active_checkbox
        )

        layout.addLayout(form)

        # =====================================================
        # Buttons
        # =====================================================

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.cancel_button = QPushButton(
            "Cancel"
        )

        self.save_button = QPushButton(
            "Save"
        )
        self.save_button.setObjectName(
            "PrimaryButton"
        )

        self.cancel_button.clicked.connect(
            self.reject
        )

        self.save_button.clicked.connect(
            self.validate_and_accept
        )

        button_layout.addWidget(
            self.cancel_button
        )
        button_layout.addWidget(
            self.save_button
        )

        layout.addLayout(button_layout)

        # =====================================================
        # Style
        # =====================================================

        self.setStyleSheet("""
            QDialog {
                background-color: #f4f7fb;
                color: #0f172a;
            }

            QLabel {
                color: #0f172a;
            }

            QLineEdit {
                min-height: 34px;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 0 8px;
                background-color: white;
                color: #0f172a;
                selection-background-color: #bfdbfe;
                selection-color: #0f172a;
            }

            QLineEdit:focus {
                border: 1px solid #2563eb;
            }

            QLineEdit:read-only {
                background-color: #f1f5f9;
                color: #64748b;
            }

            QComboBox {
                min-height: 34px;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 0 8px;
                background-color: white;
                color: #0f172a;
            }

            QComboBox:focus {
                border: 1px solid #2563eb;
            }

            QComboBox QAbstractItemView {
                background-color: white;
                color: #0f172a;
                selection-background-color: #dbeafe;
                selection-color: #0f172a;
                border: 1px solid #d1d5db;
            }

            QCheckBox {
                color: #0f172a;
                spacing: 8px;
            }

            QPushButton {
                min-height: 34px;
                padding: 0 16px;
                border-radius: 6px;
                border: 1px solid #d1d5db;
                background-color: white;
                color: #0f172a;
            }

            QPushButton:hover {
                background-color: #f1f5f9;
            }

            QPushButton#PrimaryButton {
                background-color: #2563eb;
                color: white;
                border: none;
            }

            QPushButton#PrimaryButton:hover {
                background-color: #1d4ed8;
            }
        """)

    # =========================================================
    # Load existing user
    # =========================================================

    def load_user(self):
        self.username_edit.setText(
            self.user.get("username", "")
        )

        self.full_name_edit.setText(
            self.user.get("full_name", "")
        )

        role = self.user.get(
            "role",
            "User"
        )

        index = self.role_combo.findText(
            role,
            Qt.MatchFlag.MatchFixedString
        )

        if index >= 0:
            self.role_combo.setCurrentIndex(
                index
            )

        self.active_checkbox.setChecked(
            self.user.get("active", True)
        )

    # =========================================================
    # Validation
    # =========================================================

    def validate_and_accept(self):
        username = (
            self.username_edit
            .text()
            .strip()
        )

        full_name = (
            self.full_name_edit
            .text()
            .strip()
        )

        password = (
            self.password_edit.text()
        )

        confirm_password = (
            self.confirm_password_edit.text()
        )

        # Username
        if not username:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Username cannot be empty."
            )
            self.username_edit.setFocus()
            return

        # Full name
        if not full_name:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Full name cannot be empty."
            )
            self.full_name_edit.setFocus()
            return

        # -----------------------------------------------------
        # Add user
        # -----------------------------------------------------

        if not self.is_edit:

            if not password:
                QMessageBox.warning(
                    self,
                    "Validation Error",
                    "Password cannot be empty."
                )
                self.password_edit.setFocus()
                return

            if not confirm_password:
                QMessageBox.warning(
                    self,
                    "Validation Error",
                    "Please confirm the password."
                )
                self.confirm_password_edit.setFocus()
                return

        # -----------------------------------------------------
        # Edit user
        # -----------------------------------------------------

        else:

            # Blank password means:
            # keep current password
            if not password:

                if confirm_password:
                    QMessageBox.warning(
                        self,
                        "Validation Error",
                        "Please enter the new password."
                    )
                    self.password_edit.setFocus()
                    return

                # No password change
                self.accept()
                return

        # -----------------------------------------------------
        # Password confirmation
        # -----------------------------------------------------

        if password != confirm_password:

            QMessageBox.warning(
                self,
                "Validation Error",
                "Password and confirmation do not match."
            )

            self.confirm_password_edit.setFocus()
            return

        self.accept()

    # =========================================================
    # Get form data
    # =========================================================

    def get_data(self):
        return {
            "username": (
                self.username_edit
                .text()
                .strip()
            ),

            "full_name": (
                self.full_name_edit
                .text()
                .strip()
            ),

            "password": (
                self.password_edit
                .text()
            ),

            "confirm_password": (
                self.confirm_password_edit
                .text()
            ),

            "role": (
                self.role_combo
                .currentText()
            ),

            "active": (
                self.active_checkbox
                .isChecked()
            ),
        }