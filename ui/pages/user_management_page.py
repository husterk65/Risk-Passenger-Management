import bcrypt

from PyQt6.QtCore import (
    Qt,
    QSortFilterProxyModel,
)

from PyQt6.QtGui import (
    QStandardItem,
    QStandardItemModel,
)

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableView,
    QMessageBox,
    QFrame,
    QHeaderView,
    QDialog,
)

from services.user_service import UserService
from services.audit_log_service import AuditLogService
from ui.dialogs.user_dialog import UserDialog


class UserManagementPage(QWidget):

    def __init__(self, current_user):
        super().__init__()

        self.current_user = current_user
        self.users = []

        self.init_ui()
        self.load_data()

    # =========================================================
    # UI
    # =========================================================

    def init_ui(self):

        self.setObjectName("UserManagementPage")

        root_layout = QVBoxLayout(self)

        root_layout.setContentsMargins(
            35,
            30,
            35,
            30
        )

        root_layout.setSpacing(20)

        # =====================================================
        # Header
        # =====================================================

        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        title_label = QLabel("User Management")
        title_label.setObjectName("PageTitle")

        subtitle_label = QLabel(
            "Manage application users and access roles"
        )
        subtitle_label.setObjectName("PageSubtitle")

        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        root_layout.addLayout(header_layout)

        # =====================================================
        # Content Card
        # =====================================================

        content_card = QFrame()
        content_card.setObjectName("ContentCard")

        card_layout = QVBoxLayout(content_card)

        card_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        card_layout.setSpacing(15)

        # =====================================================
        # Toolbar
        # =====================================================

        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        # Search
        self.search_edit = QLineEdit()

        self.search_edit.setPlaceholderText(
            "Search username or full name..."
        )

        self.search_edit.setClearButtonEnabled(True)
        self.search_edit.setMinimumHeight(38)

        toolbar.addWidget(
            self.search_edit,
            1
        )

        # Refresh
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setMinimumHeight(38)

        toolbar.addWidget(
            self.refresh_button
        )

        # Add User
        self.add_button = QPushButton("Add User")
        self.add_button.setObjectName("PrimaryButton")
        self.add_button.setMinimumHeight(38)

        toolbar.addWidget(
            self.add_button
        )

        # Edit
        self.edit_button = QPushButton("Edit")
        self.edit_button.setMinimumHeight(38)

        toolbar.addWidget(
            self.edit_button
        )

        # Activate / Deactivate
        self.toggle_button = QPushButton("Deactivate")
        self.toggle_button.setMinimumHeight(38)

        toolbar.addWidget(
            self.toggle_button
        )

        card_layout.addLayout(toolbar)

        # =====================================================
        # Table
        # =====================================================

        self.table = QTableView()
        self.table.setObjectName("UsersTable")

        self.model = QStandardItemModel()

        self.model.setHorizontalHeaderLabels([
            "Username",
            "Full Name",
            "Role",
            "Status",
            "Created At",
        ])

        # =====================================================
        # Proxy Model
        # =====================================================

        self.proxy_model = QSortFilterProxyModel()

        self.proxy_model.setSourceModel(
            self.model
        )

        self.proxy_model.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )

        # Search all columns
        self.proxy_model.setFilterKeyColumn(-1)

        self.table.setModel(
            self.proxy_model
        )

        # =====================================================
        # Table Behavior
        # =====================================================

        self.table.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QTableView.SelectionMode.SingleSelection
        )

        self.table.setEditTriggers(
            QTableView.EditTrigger.NoEditTriggers
        )

        self.table.setAlternatingRowColors(True)

        self.table.verticalHeader().setVisible(
            False
        )

        self.table.setShowGrid(False)

        # =====================================================
        # Header
        # =====================================================

        header = self.table.horizontalHeader()

        # Username
        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.ResizeToContents
        )

        # Full Name
        # Keep Stretch so it occupies remaining space
        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.Stretch
        )

        # Role
        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeMode.ResizeToContents
        )

        # Status
        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeMode.ResizeToContents
        )

        # Created At
        header.setSectionResizeMode(
            4,
            QHeaderView.ResizeMode.ResizeToContents
        )

        card_layout.addWidget(
            self.table
        )

        root_layout.addWidget(
            content_card,
            1
        )

        # =====================================================
        # Signals
        # =====================================================

        self.search_edit.textChanged.connect(
            self.on_search
        )

        self.refresh_button.clicked.connect(
            self.load_data
        )

        self.add_button.clicked.connect(
            self.add_user
        )

        self.edit_button.clicked.connect(
            self.edit_user
        )

        self.toggle_button.clicked.connect(
            self.toggle_user
        )

        self.table.doubleClicked.connect(
            self.edit_user
        )

        self.table.selectionModel().selectionChanged.connect(
            self.update_buttons
        )

        # =====================================================
        # Style
        # =====================================================

        self.setStyleSheet("""
            QWidget#UserManagementPage {
                background-color: #f4f7fb;
                color: #0f172a;
            }

            QLabel {
                color: #0f172a;
                background-color: transparent;
            }

            QLabel#PageTitle {
                font-size: 28px;
                font-weight: 700;
                color: #0f172a;
            }

            QLabel#PageSubtitle {
                font-size: 14px;
                color: #64748b;
            }

            QFrame#ContentCard {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }

            QLineEdit {
                min-height: 34px;
                background-color: white;
                color: #0f172a;
                border: 1px solid #d1d5db;
                border-radius: 7px;
                padding: 0 12px;
                selection-background-color: #bfdbfe;
                selection-color: #0f172a;
            }

            QLineEdit:focus {
                border: 1px solid #2563eb;
            }

            QPushButton {
                min-height: 34px;
                padding: 0 15px;
                border-radius: 7px;
                border: 1px solid #d1d5db;
                background-color: white;
                color: #0f172a;
            }

            QPushButton:hover {
                background-color: #f8fafc;
            }

            QPushButton:pressed {
                background-color: #e2e8f0;
            }

            QPushButton:disabled {
                background-color: #f1f5f9;
                color: #94a3b8;
            }

            QPushButton#PrimaryButton {
                background-color: #2563eb;
                color: white;
                border: none;
            }

            QPushButton#PrimaryButton:hover {
                background-color: #1d4ed8;
            }

            QPushButton#PrimaryButton:pressed {
                background-color: #1e40af;
            }

            QTableView#UsersTable {
                background-color: white;
                color: #0f172a;
                border: none;
                gridline-color: #e2e8f0;
                alternate-background-color: #f8fafc;
                selection-background-color: #dbeafe;
                selection-color: #0f172a;
            }

            QTableView#UsersTable::item {
                color: #0f172a;
                background-color: white;
                padding: 6px;
            }

            QTableView#UsersTable::item:alternate {
                background-color: #f8fafc;
                color: #0f172a;
            }

            QTableView#UsersTable::item:selected {
                background-color: #dbeafe;
                color: #0f172a;
            }

            QHeaderView::section {
                background-color: #f8fafc;
                color: #475569;
                font-weight: 600;
                border: none;
                border-bottom: 1px solid #e2e8f0;
                padding: 10px;
            }

            QScrollBar:vertical {
                background-color: #f8fafc;
                width: 10px;
                margin: 0;
            }

            QScrollBar::handle:vertical {
                background-color: #cbd5e1;
                border-radius: 5px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #94a3b8;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        self.update_buttons()

    # =========================================================
    # Load Data
    # =========================================================

    def load_data(self):

        try:

            self.users = UserService.get_all()

            self.model.removeRows(
                0,
                self.model.rowCount()
            )

            for user in self.users:

                # Username
                username_item = QStandardItem(
                    str(
                        user.get(
                            "username",
                            ""
                        )
                    )
                )

                # Keep Username centered
                username_item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                # Full Name
                full_name_item = QStandardItem(
                    str(
                        user.get(
                            "full_name",
                            ""
                        )
                    )
                )

                # Full Name centered
                full_name_item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                # Role
                role_item = QStandardItem(
                    str(
                        user.get(
                            "role",
                            ""
                        )
                    )
                )

                role_item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                # Status
                is_active = user.get(
                    "active",
                    False
                )

                status_item = QStandardItem(
                    "Active"
                    if is_active
                    else "Inactive"
                )

                status_item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                # Created At
                created_item = QStandardItem(
                    self.format_created_at(
                        user.get(
                            "created_at"
                        )
                    )
                )

                created_item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                self.model.appendRow([
                    username_item,
                    full_name_item,
                    role_item,
                    status_item,
                    created_item,
                ])

            self.update_buttons()

        except Exception as e:

            self.show_message(
                "Load Error",
                f"Failed to load users:\n{e}",
                QMessageBox.Icon.Critical
            )

    # =========================================================
    # Format Created At
    # =========================================================

    @staticmethod
    def format_created_at(value):

        if not value:
            return ""

        value = str(value)

        if "T" in value:

            value = value.replace(
                "T",
                " ",
                1
            )

        if "+" in value:

            value = value.split(
                "+",
                1
            )[0]

        return value

    # =========================================================
    # Search
    # =========================================================

    def on_search(self, text):

        self.proxy_model.setFilterFixedString(
            text
        )

    # =========================================================
    # Get Selected User
    # =========================================================

    def get_selected_user(self):

        selection = (
            self.table
            .selectionModel()
            .selectedRows()
        )

        if not selection:
            return None

        proxy_index = selection[0]

        source_index = (
            self.proxy_model.mapToSource(
                proxy_index
            )
        )

        row = source_index.row()

        if row < 0:
            return None

        if row >= len(self.users):
            return None

        return self.users[row]

    # =========================================================
    # Update Buttons
    # =========================================================

    def update_buttons(self):

        user = self.get_selected_user()

        has_selection = user is not None

        self.edit_button.setEnabled(
            has_selection
        )

        self.toggle_button.setEnabled(
            has_selection
        )

        if not user:

            self.toggle_button.setText(
                "Deactivate"
            )

            return

        is_active = user.get(
            "active",
            False
        )

        self.toggle_button.setText(
            "Deactivate"
            if is_active
            else "Activate"
        )

    # =========================================================
    # Add User
    # =========================================================

    def add_user(self):

        dialog = UserDialog(
            parent=self
        )

        if (
            dialog.exec()
            != QDialog.DialogCode.Accepted
        ):
            return

        data = dialog.get_data()

        username = data["username"]

        try:

            if UserService.username_exists(
                username
            ):

                self.show_message(
                    "Username Exists",
                    f"Username '{username}' already exists.",
                    QMessageBox.Icon.Warning
                )

                return

            password_hash = self.hash_password(
                data["password"]
            )

            UserService.create(
                username=username,
                password_hash=password_hash,
                full_name=data["full_name"],
                role=data["role"],
                active=data["active"],
            )

            AuditLogService.log(
                user_id=self.current_user.id,
                username=self.current_user.username,
                action="ADD",
                module="Users",
                details=f"Added user: {username}",
            )

            self.show_message(
                "Success",
                "The new user has been added successfully.",
                QMessageBox.Icon.Information
            )

            self.load_data()

        except Exception as e:

            self.show_message(
                "Error",
                f"Failed to add user:\n{e}",
                QMessageBox.Icon.Critical
            )

    # =========================================================
    # Edit User
    # =========================================================

    def edit_user(self):

        user = self.get_selected_user()

        if not user:

            self.show_message(
                "Edit User",
                "Please select a user first.",
                QMessageBox.Icon.Warning
            )

            return

        dialog = UserDialog(
            user=user,
            parent=self
        )

        if (
            dialog.exec()
            != QDialog.DialogCode.Accepted
        ):
            return

        data = dialog.get_data()

        old_active = user.get(
            "active",
            False
        )

        new_active = data["active"]

        # Prevent user from deactivating themselves
        if (
            user.get("id")
            == self.current_user.id
            and old_active
            and not new_active
        ):

            self.show_message(
                "Action Not Allowed",
                "You cannot deactivate your own account.",
                QMessageBox.Icon.Warning
            )

            return

        username = user["username"]

        try:

            UserService.update(
                user_id=user["id"],
                full_name=data["full_name"],
                role=data["role"],
                active=new_active,
            )

            # Update password only if user entered one
            if data["password"]:

                password_hash = self.hash_password(
                    data["password"]
                )

                UserService.update_password(
                    user_id=user["id"],
                    password_hash=password_hash,
                )

            AuditLogService.log(
                user_id=self.current_user.id,
                username=self.current_user.username,
                action="EDIT",
                module="Users",
                details=f"Updated user: {username}",
            )

            # Log status change separately
            if old_active != new_active:

                if new_active:

                    action = "ACTIVATE"
                    status_text = "Activated"

                else:

                    action = "DEACTIVATE"
                    status_text = "Deactivated"

                AuditLogService.log(
                    user_id=self.current_user.id,
                    username=self.current_user.username,
                    action=action,
                    module="Users",
                    details=(
                        f"{status_text} user: "
                        f"{username}"
                    ),
                )

            self.show_message(
                "Success",
                "Your changes have been saved successfully.",
                QMessageBox.Icon.Information
            )

            self.load_data()

        except Exception as e:

            self.show_message(
                "Error",
                f"Failed to update user:\n{e}",
                QMessageBox.Icon.Critical
            )

    # =========================================================
    # Activate / Deactivate
    # =========================================================

    def toggle_user(self):

        user = self.get_selected_user()

        if not user:

            self.show_message(
                "User",
                "Please select a user first.",
                QMessageBox.Icon.Warning
            )

            return

        user_id = user["id"]
        username = user["username"]

        current_active = user.get(
            "active",
            False
        )

        new_active = not current_active

        # Prevent self deactivation
        if (
            user_id == self.current_user.id
            and not new_active
        ):

            self.show_message(
                "Action Not Allowed",
                "You cannot deactivate your own account.",
                QMessageBox.Icon.Warning
            )

            return

        action_text = (
            "activate"
            if new_active
            else "deactivate"
        )

        msg = QMessageBox(self)

        msg.setWindowTitle(
            "Confirm Action"
        )

        msg.setText(
            f"Are you sure you want to "
            f"{action_text} user '{username}'?"
        )

        msg.setIcon(
            QMessageBox.Icon.Question
        )

        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No
        )

        msg.setDefaultButton(
            QMessageBox.StandardButton.No
        )

        self.style_message_box(msg)

        reply = msg.exec()

        if (
            reply
            != QMessageBox.StandardButton.Yes
        ):
            return

        try:

            UserService.set_active(
                user_id=user_id,
                active=new_active
            )

            if new_active:

                action = "ACTIVATE"
                status_text = "Activated"

            else:

                action = "DEACTIVATE"
                status_text = "Deactivated"

            AuditLogService.log(
                user_id=self.current_user.id,
                username=self.current_user.username,
                action=action,
                module="Users",
                details=(
                    f"{status_text} user: "
                    f"{username}"
                ),
            )

            if new_active:

                success_message = (
                    f"User '{username}' "
                    "has been activated successfully."
                )

            else:

                success_message = (
                    f"User '{username}' "
                    "has been deactivated successfully."
                )

            self.show_message(
                "Success",
                success_message,
                QMessageBox.Icon.Information
            )

            self.load_data()

        except Exception as e:

            self.show_message(
                "Error",
                f"Failed to update user status:\n{e}",
                QMessageBox.Icon.Critical
            )

    # =========================================================
    # Custom Message
    # =========================================================

    def show_message(
        self,
        title,
        message,
        icon=QMessageBox.Icon.Information
    ):

        dialog = QDialog(self)

        dialog.setWindowTitle(title)
        dialog.setModal(True)

        dialog.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.FramelessWindowHint
        )

        dialog.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground,
            True
        )

        # =====================================================
        # Icon
        # =====================================================

        if icon == QMessageBox.Icon.Information:

            icon_text = "✓"
            icon_color = "#16a34a"
            icon_background = "#dcfce7"

        elif icon == QMessageBox.Icon.Warning:

            icon_text = "!"
            icon_color = "#d97706"
            icon_background = "#fef3c7"

        elif icon == QMessageBox.Icon.Critical:

            icon_text = "!"
            icon_color = "#dc2626"
            icon_background = "#fee2e2"

        else:

            icon_text = "i"
            icon_color = "#2563eb"
            icon_background = "#dbeafe"

        # =====================================================
        # Style
        # =====================================================

        dialog.setStyleSheet(f"""
            QDialog {{
                background: transparent;
            }}

            QFrame#MessageDialogContainer {{
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
            }}

            QLabel#MessageIcon {{
                background-color: {icon_background};
                color: {icon_color};
                font-size: 25px;
                font-weight: 700;
                border-radius: 28px;
                min-width: 56px;
                min-height: 56px;
                max-width: 56px;
                max-height: 56px;
            }}

            QLabel#MessageTitle {{
                color: #0f172a;
                font-size: 18px;
                font-weight: 700;
                background: transparent;
            }}

            QLabel#MessageText {{
                color: #475569;
                font-size: 14px;
                font-weight: 400;
                background: transparent;
            }}

            QPushButton#MessageOKButton {{
                min-width: 88px;
                min-height: 38px;
                padding: 0 18px;
                border-radius: 8px;
                border: none;
                background-color: #2563eb;
                color: white;
                font-size: 14px;
                font-weight: 600;
            }}

            QPushButton#MessageOKButton:hover {{
                background-color: #1d4ed8;
            }}

            QPushButton#MessageOKButton:pressed {{
                background-color: #1e40af;
            }}
        """)

        # =====================================================
        # Container
        # =====================================================

        container = QFrame(dialog)

        container.setObjectName(
            "MessageDialogContainer"
        )

        container_layout = QVBoxLayout(
            container
        )

        container_layout.setContentsMargins(
            28,
            24,
            28,
            22
        )

        container_layout.setSpacing(16)

        # =====================================================
        # Header
        # =====================================================

        header_layout = QHBoxLayout()

        header_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        header_layout.setSpacing(16)

        icon_label = QLabel(
            icon_text
        )

        icon_label.setObjectName(
            "MessageIcon"
        )

        icon_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "MessageTitle"
        )

        title_label.setAlignment(
            Qt.AlignmentFlag.AlignVCenter
        )

        header_layout.addWidget(
            icon_label
        )

        header_layout.addWidget(
            title_label,
            1
        )

        container_layout.addLayout(
            header_layout
        )

        # =====================================================
        # Message text
        # =====================================================

        text_label = QLabel(
            message
        )

        text_label.setObjectName(
            "MessageText"
        )

        text_label.setWordWrap(True)

        container_layout.addWidget(
            text_label
        )

        # =====================================================
        # OK button
        # =====================================================

        button_layout = QHBoxLayout()

        button_layout.setContentsMargins(
            0,
            4,
            0,
            0
        )

        button_layout.addStretch()

        ok_button = QPushButton(
            "OK"
        )

        ok_button.setObjectName(
            "MessageOKButton"
        )

        ok_button.setDefault(True)

        ok_button.clicked.connect(
            dialog.accept
        )

        button_layout.addWidget(
            ok_button
        )

        container_layout.addLayout(
            button_layout
        )

        # =====================================================
        # Outer layout
        # =====================================================

        outer_layout = QVBoxLayout(
            dialog
        )

        outer_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        outer_layout.addWidget(
            container
        )

        dialog.resize(
            500,
            210
        )

        dialog.exec()

        return 0

    # =========================================================
    # QMessageBox Style
    # =========================================================

    @staticmethod
    def style_message_box(msg):

        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }

            QMessageBox QLabel {
                color: #0f172a;
                font-size: 14px;
            }

            QMessageBox QPushButton {
                min-width: 80px;
                min-height: 34px;
                padding: 0 14px;
                border-radius: 7px;
                border: 1px solid #d1d5db;
                background-color: white;
                color: #0f172a;
                font-weight: 600;
            }

            QMessageBox QPushButton:hover {
                background-color: #f8fafc;
            }
        """)

    # =========================================================
    # Password Hash
    # =========================================================

    @staticmethod
    def hash_password(password):

        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")