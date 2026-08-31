
from PyQt6.QtCore import pyqtSignal, Qt, QTimer

from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QFrame,
)

from services.auth_service import AuthService


class LoginWindow(QDialog):

    login_success = pyqtSignal(object)

    # =========================================================
    # INIT
    # =========================================================

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Passenger Risk Management"
        )

        # -----------------------------------------------------
        # Window flags
        # -----------------------------------------------------

        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.WindowCloseButtonHint
        )

        # -----------------------------------------------------
        # Default size
        # -----------------------------------------------------

        self.resize(
            920,
            560
        )

        # -----------------------------------------------------
        # Minimum size
        # -----------------------------------------------------

        self.setMinimumSize(
            760,
            480
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_StyledBackground,
            True
        )

        self.init_ui()

    # =========================================================
    # SHOW EVENT
    # =========================================================

    def showEvent(self, event):

        super().showEvent(event)

        # Đợi Qt/WSLg hoàn tất việc tạo window frame
        # rồi mới tính vị trí.
        QTimer.singleShot(
            100,
            self.center_on_screen
        )

    # =========================================================
    # CENTER WINDOW
    # =========================================================

    def center_on_screen(self):

        screen = QApplication.primaryScreen()

        if screen is None:
            return

        screen_geometry = (
            screen.availableGeometry()
        )

        frame_geometry = (
            self.frameGeometry()
        )

        frame_geometry.moveCenter(
            screen_geometry.center()
        )

        self.move(
            frame_geometry.topLeft()
        )

    # =========================================================
    # UI
    # =========================================================

    def init_ui(self):

        # =====================================================
        # ROOT LAYOUT
        # =====================================================

        root_layout = QHBoxLayout(
            self
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
        # BRAND PANEL
        # =====================================================

        brand_panel = QFrame()

        brand_panel.setObjectName(
            "BrandPanel"
        )

        brand_layout = QVBoxLayout(
            brand_panel
        )

        brand_layout.setContentsMargins(
            48,
            48,
            48,
            48
        )

        brand_layout.setSpacing(
            16
        )

        # =====================================================
        # BRAND TITLE
        # =====================================================

        brand_title = QLabel(
            "PASSENGER"
        )

        brand_title.setObjectName(
            "BrandTitle"
        )

        brand_layout.addWidget(
            brand_title
        )

        # =====================================================
        # BRAND SUBTITLE
        # =====================================================

        brand_subtitle = QLabel(
            "RISK MANAGEMENT"
        )

        brand_subtitle.setObjectName(
            "BrandSubtitle"
        )

        brand_layout.addWidget(
            brand_subtitle
        )

        brand_layout.addSpacing(
            20
        )

        # =====================================================
        # DESCRIPTION
        # =====================================================

        description = QLabel(
            "Monitor flights, identify suspicious "
            "passengers, and review risk alerts "
            "in one place."
        )

        description.setObjectName(
            "BrandDescription"
        )

        description.setWordWrap(
            True
        )

        description.setMaximumWidth(
            380
        )

        brand_layout.addWidget(
            description
        )

        brand_layout.addSpacing(
            14
        )

        # =====================================================
        # FEATURES
        # =====================================================

        feature_list = QVBoxLayout()

        feature_list.setSpacing(
            12
        )

        features = [
            "Real-time passenger screening",
            "Flight-based risk filtering",
            "Actionable alert review and export",
        ]

        for text in features:

            item = QLabel(
                "•  " + text
            )

            item.setObjectName(
                "FeatureItem"
            )

            feature_list.addWidget(
                item
            )

        brand_layout.addLayout(
            feature_list
        )

        brand_layout.addStretch()

        # =====================================================
        # FORM PANEL
        # =====================================================

        form_panel = QFrame()

        form_panel.setObjectName(
            "FormPanel"
        )

        form_layout = QVBoxLayout(
            form_panel
        )

        form_layout.setContentsMargins(
            56,
            56,
            56,
            48
        )

        form_layout.setSpacing(
            16
        )

        # =====================================================
        # WELCOME TITLE
        # =====================================================

        welcome = QLabel(
            "Welcome back"
        )

        welcome.setObjectName(
            "WelcomeTitle"
        )

        form_layout.addWidget(
            welcome
        )

        # =====================================================
        # WELCOME SUBTITLE
        # =====================================================

        subtitle = QLabel(
            "Sign in to continue"
        )

        subtitle.setObjectName(
            "WelcomeSubtitle"
        )

        form_layout.addWidget(
            subtitle
        )

        form_layout.addSpacing(
            16
        )

        # =====================================================
        # USERNAME
        # =====================================================

        self.username = QLineEdit()

        self.username.setObjectName(
            "LoginField"
        )

        self.username.setPlaceholderText(
            "Username"
        )

        self.username.setMinimumHeight(
            44
        )

        # =====================================================
        # PASSWORD
        # =====================================================

        self.password = QLineEdit()

        self.password.setObjectName(
            "LoginField"
        )

        self.password.setPlaceholderText(
            "Password"
        )

        self.password.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.password.setMinimumHeight(
            44
        )

        # =====================================================
        # SIGNALS
        # =====================================================

        self.username.returnPressed.connect(
            self.password.setFocus
        )

        self.password.returnPressed.connect(
            self.login
        )

        # =====================================================
        # ADD INPUTS
        # =====================================================

        form_layout.addWidget(
            self.username
        )

        form_layout.addWidget(
            self.password
        )

        form_layout.addSpacing(
            4
        )

        # =====================================================
        # LOGIN BUTTON
        # =====================================================

        self.login_button = QPushButton(
            "Login"
        )

        self.login_button.setObjectName(
            "PrimaryButton"
        )

        self.login_button.setMinimumHeight(
            44
        )

        self.login_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.login_button.clicked.connect(
            self.login
        )

        form_layout.addWidget(
            self.login_button
        )

        form_layout.addStretch()

        # =====================================================
        # ADD PANELS TO ROOT
        # =====================================================

        root_layout.addWidget(
            brand_panel,
            1
        )

        root_layout.addWidget(
            form_panel,
            1
        )

        # =====================================================
        # STYLE
        # =====================================================

        self.setStyleSheet("""

            /* =================================================
               MAIN WINDOW
               ================================================= */

            QDialog {
                background: #f8fafc;
            }

            /* =================================================
               BRAND PANEL
               ================================================= */

            QFrame#BrandPanel {
                background: qlineargradient(
                    x1: 0,
                    y1: 0,
                    x2: 1,
                    y2: 1,
                    stop: 0 #0b1220,
                    stop: 1 #172033
                );

                border: none;
            }

            /* =================================================
               BRAND TITLE
               ================================================= */

            QLabel#BrandTitle {
                background: transparent;
                color: #ffffff;
                font-size: 30px;
                font-weight: 800;
                letter-spacing: 2px;
            }

            /* =================================================
               BRAND SUBTITLE
               ================================================= */

            QLabel#BrandSubtitle {
                background: transparent;
                color: #93c5fd;
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 3px;
            }

            /* =================================================
               BRAND DESCRIPTION
               ================================================= */

            QLabel#BrandDescription {
                background: transparent;
                color: #f1f5f9;
                font-size: 14px;
                font-weight: 400;
            }

            /* =================================================
               FEATURE ITEMS
               ================================================= */

            QLabel#FeatureItem {
                background: transparent;
                color: #e2e8f0;
                font-size: 13px;
                font-weight: 500;
            }

            /* =================================================
               FORM PANEL
               ================================================= */

            QFrame#FormPanel {
                background: #ffffff;
                border: none;
            }

            /* =================================================
               WELCOME TITLE
               ================================================= */

            QLabel#WelcomeTitle {
                background: transparent;
                color: #0f172a;
                font-size: 30px;
                font-weight: 800;
            }

            /* =================================================
               WELCOME SUBTITLE
               ================================================= */

            QLabel#WelcomeSubtitle {
                background: transparent;
                color: #64748b;
                font-size: 13px;
                font-weight: 400;
            }

            /* =================================================
               LOGIN FIELD
               ================================================= */

            QLineEdit#LoginField {
                background: #f8fafc;
                color: #0f172a;
                border: 1px solid #cbd5e1;
                border-radius: 10px;
                padding: 0 13px;
                font-size: 13px;
            }

            QLineEdit#LoginField:hover {
                border: 1px solid #94a3b8;
            }

            QLineEdit#LoginField:focus {
                background: #ffffff;
                border: 1px solid #2563eb;
            }

            /* =================================================
               LOGIN BUTTON
               ================================================= */

            QPushButton#PrimaryButton {
                background: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 10px;
                font-size: 13px;
                font-weight: 700;
            }

            QPushButton#PrimaryButton:hover {
                background: #1d4ed8;
            }

            QPushButton#PrimaryButton:pressed {
                background: #1e40af;
            }

            QPushButton#PrimaryButton:disabled {
                background: #94a3b8;
                color: #e2e8f0;
            }
        """)

        # =====================================================
        # INITIAL FOCUS
        # =====================================================

        self.username.setFocus()

    # =========================================================
    # LOGIN
    # =========================================================

    def login(self):

        username = (
            self.username
            .text()
            .strip()
        )

        password = (
            self.password
            .text()
        )

        # =====================================================
        # VALIDATE USERNAME
        # =====================================================

        if not username:

            QMessageBox.warning(
                self,
                "Login",
                "Please enter your username."
            )

            self.username.setFocus()

            return

        # =====================================================
        # VALIDATE PASSWORD
        # =====================================================

        if not password:

            QMessageBox.warning(
                self,
                "Login",
                "Please enter your password."
            )

            self.password.setFocus()

            return

        # =====================================================
        # DISABLE BUTTON
        # =====================================================

        self.login_button.setEnabled(
            False
        )

        try:

            # =================================================
            # AUTHENTICATE
            # =================================================

            current_user = AuthService.login(
                username,
                password
            )

            # =================================================
            # LOGIN SUCCESS
            # =================================================

            if current_user:

                self.login_success.emit(
                    current_user
                )

                self.close()

                return

            # =================================================
            # LOGIN FAILED
            # =================================================

            QMessageBox.warning(
                self,
                "Login",
                "Username or Password is incorrect."
            )

            self.password.clear()

            self.password.setFocus()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Login Error",
                f"An error occurred while logging in:\n\n{e}"
            )

        finally:

            self.login_button.setEnabled(
                True
            )