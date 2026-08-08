from PyQt6.QtCore import Qt
from PyQt6.QtCore import QSortFilterProxyModel
from PyQt6.QtCore import QRegularExpression

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
    QDialog,
    QFrame,
    QHeaderView,
)

from services.risk_profile_service import RiskProfileService
from ui.dialogs.risk_profile_dialog import RiskProfileDialog
from utils.column_config import RISK_PROFILE_COLUMNS
from utils.table_builder import TableBuilder

class RiskProfilePage(QWidget):

    def __init__(self):

        super().__init__()

        self.model = QStandardItemModel()

        self.proxy_model = QSortFilterProxyModel()

        self.proxy_model.setSourceModel(self.model)

        self.proxy_model.setSortCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )

        self.proxy_model.setDynamicSortFilter(True)
        self.proxy_model.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )
        self.proxy_model.setFilterKeyColumn(-1)

        self.profiles = []

        self.init_ui()

        self.load_data()

    def init_ui(self):

        self.setObjectName("RiskProfilePage")
        self.setStyleSheet("""
            QWidget#RiskProfilePage {
                background: #f4f7fb;
            }
            QFrame#contentCard {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
            }
            QLabel#pageTitle {
                font-size: 24px;
                font-weight: 700;
                color: #0f172a;
            }
            QLabel#pageSubtitle {
                color: #64748b;
                font-size: 12px;
            }
            QLabel#countBadge {
                background: #e0f2fe;
                color: #0369a1;
                border-radius: 999px;
                padding: 6px 12px;
                font-weight: 600;
            }
            QLineEdit {
                background: #f8fafc;
                border: 1px solid #dbe2ea;
                border-radius: 8px;
                padding: 8px 12px;
                min-height: 34px;
                color: #0f172a;
            }
            QLineEdit:focus {
                border: 1px solid #2563eb;
                background: white;
            }
            QPushButton {
                background: #f8fafc;
                color: #334155;
                border: 1px solid #dbe2ea;
                border-radius: 8px;
                padding: 8px 14px;
                min-height: 34px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #e2e8f0;
            }
            QPushButton#primaryButton {
                background: #2563eb;
                color: white;
                border: none;
            }
            QPushButton#primaryButton:hover {
                background: #1d4ed8;
            }
            QPushButton#dangerButton {
                background: #fee2e2;
                color: #b91c1c;
                border: 1px solid #fecaca;
            }
            QPushButton#dangerButton:hover {
                background: #fecaca;
            }
            QTableView {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                gridline-color: #f1f5f9;
                selection-background-color: #dbeafe;
                selection-color: #0f172a;
            }
            QHeaderView::section {
                background: #f8fafc;
                color: #334155;
                padding: 8px;
                border: none;
                font-weight: 600;
            }
            QTableView::item {
                padding: 8px;
                border: none;
            }
        """)

        root = QVBoxLayout()
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(0)

        card = QFrame()
        card.setObjectName("contentCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(16)

        header_layout = QHBoxLayout()
        title_col = QVBoxLayout()
        title_col.setSpacing(4)

        title = QLabel("Risk Profiles")
        title.setObjectName("pageTitle")

        subtitle = QLabel("Manage passenger risk records with a clean internal operations view.")
        subtitle.setObjectName("pageSubtitle")

        title_col.addWidget(title)
        title_col.addWidget(subtitle)

        header_layout.addLayout(title_col)
        header_layout.addStretch()

        self.lbl_count = QLabel("0 record(s)")
        self.lbl_count.setObjectName("countBadge")
        header_layout.addWidget(self.lbl_count)

        card_layout.addLayout(header_layout)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(
            "Search by name / passport / nationality..."
        )
        self.search_box.setClearButtonEnabled(True)

        self.btn_import  = QPushButton("Import")
        self.btn_import .setObjectName("primaryButton")

        self.btn_refresh = QPushButton("Refresh")
        self.btn_add = QPushButton("Add")
        self.btn_add.setObjectName("primaryButton")
        self.btn_delete = QPushButton("Delete")
        self.btn_delete.setObjectName("dangerButton")

        toolbar.addWidget(self.search_box, 1)
        toolbar.addWidget(self.btn_import )
        toolbar.addWidget(self.btn_refresh)
        toolbar.addStretch()
        toolbar.addWidget(self.btn_add)
        toolbar.addWidget(self.btn_delete)

        card_layout.addLayout(toolbar)

        self.table = QTableView()
        self.table.setModel(self.proxy_model)
        self.table.setSortingEnabled(False)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QTableView.SelectionMode.SingleSelection
        )
        self.table.setEditTriggers(
            QTableView.EditTrigger.NoEditTriggers
        )
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.verticalHeader().setVisible(False)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        header.setStretchLastSection(True)

        card_layout.addWidget(self.table)

        root.addWidget(card)
        self.setLayout(root)

        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_import.clicked.connect(self.import_profiles)
        self.search_box.textChanged.connect(self.search)
        self.btn_add.clicked.connect(self.add_profile)
        self.btn_delete.clicked.connect(self.delete_profile)
        self.table.doubleClicked.connect(self.edit_profile)

    def load_data(self):

        print("========== RISK PROFILE DEBUG ==========")

        self.profiles = RiskProfileService.get_all()

        print("profiles type:", type(self.profiles))
        print("profiles:", self.profiles)

        if self.profiles:
            print("first profile type:", type(self.profiles[0]))
            print("first profile:", self.profiles[0])

        self.populate_table(self.profiles)

    def search(self):

        keyword = self.search_box.text().strip()
        regex = QRegularExpression(
            keyword,
            QRegularExpression.PatternOption.CaseInsensitiveOption
        )
        self.proxy_model.setFilterRegularExpression(regex)

    def add_profile(self):

        dialog = RiskProfileDialog(
            parent=self
        )

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        profile = dialog.get_profile()

        try:

            RiskProfileService.create(
                profile
            )

            self.load_data()

            QMessageBox.information(
                self,
                "Success",
                "Risk profile added successfully."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    def get_selected_profile(self):

        index = self.table.currentIndex()

        if not index.isValid():
            return None

        source_index = self.proxy_model.mapToSource(index)

        row = source_index.row()

        if row < 0 or row >= len(self.profiles):
            return None

        return self.profiles[row]

    def delete_profile(self):

        profile = self.get_selected_profile()

        if profile is None:
            QMessageBox.information(
                self,
                "Notice",
                "Please select a profile to delete."
            )
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            (
                f"Are you sure you want to delete "
                f"'{profile.full_name}'?"
            ),
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        try:

            RiskProfileService.delete(
                profile.id
            )

            QMessageBox.information(
                self,
                "Success",
                "Risk profile deleted successfully."
            )

            self.load_data()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    def edit_profile(self):

        profile = self.get_selected_profile()

        if profile is None:
            QMessageBox.information(
                self,
                "Notice",
                "Please select a profile to edit."
            )
            return

        dialog = RiskProfileDialog(
            profile=profile,
            parent=self
        )

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        updated_profile = dialog.get_profile()

        try:

            RiskProfileService.update(
                updated_profile
            )

            self.load_data()

            QMessageBox.information(
                self,
                "Success",
                "Risk profile updated successfully."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    def populate_table(self, profiles):

        self.profiles = profiles

        TableBuilder.build(
            model=self.model,
            objects=self.profiles,
            columns=RISK_PROFILE_COLUMNS
        )

        self.table.resizeColumnsToContents()

        self.lbl_count.setText(
            f"Total: {len(profiles)} record(s)"
        )

    def refresh(self):

        self.search_box.clear()

        self.proxy_model.setFilterRegularExpression("")

        self.load_data()

    def import_profiles(self):
        pass  # Placeholder for the import functionality, to be implemented later