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
)

from services.risk_profile_service import RiskProfileService
from ui.dialogs.risk_profile_dialog import RiskProfileDialog
from PyQt6.QtWidgets import QHeaderView
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

        root = QVBoxLayout()

        root.setContentsMargins(20,20,20,20)

        root.setSpacing(15)

        title = QLabel("Risk Profiles")

        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        root.addWidget(title)

        toolbar = QHBoxLayout()

        self.search_box = QLineEdit()

        self.search_box.setPlaceholderText(
            "Search by name / passport / nationality..."
        )
        self.btn_search = QPushButton("Search")

        self.btn_refresh = QPushButton("Refresh")

        self.btn_add = QPushButton("Add")

        self.btn_delete = QPushButton("Delete")

        toolbar.addWidget(self.search_box)

        toolbar.addWidget(self.btn_search)

        toolbar.addWidget(self.btn_refresh)

        toolbar.addStretch()

        toolbar.addWidget(self.btn_add)

        toolbar.addWidget(self.btn_delete)

        root.addLayout(toolbar)

        self.table = QTableView()

        self.table.setModel(self.proxy_model)

        self.table.setSortingEnabled(True)

        self.table.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QTableView.SelectionMode.SingleSelection
        )

        self.table.setEditTriggers(
            QTableView.EditTrigger.NoEditTriggers
        )

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        header.setStretchLastSection(True)

        root.addWidget(self.table)

        self.lbl_count = QLabel()

        root.addWidget(self.lbl_count)

        self.setLayout(root)

        self.btn_refresh.clicked.connect(self.refresh)

        self.btn_search.clicked.connect(self.search)
        self.search_box.textChanged.connect(self.search)

        self.btn_add.clicked.connect(self.add_profile)

        self.btn_delete.clicked.connect(self.delete_profile)

        self.table.doubleClicked.connect(self.edit_profile)

    def load_data(self):

        try:
            self.profiles = RiskProfileService.get_all()
            self.populate_table(self.profiles)
        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    def search(self):

        keyword = self.search_box.text().strip()
        regex = QRegularExpression(
            keyword,
            QRegularExpression.PatternOption.CaseInsensitiveOption
        )
        self.proxy_model.setFilterRegularExpression(regex)

    def add_profile(self):
        pass

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

    def edit_profile(self):
        profile = self.get_selected_profile()

        if profile is None:
            QMessageBox.information(
                self,
                "Notice",
                "Please select a profile to edit."
            )
            return

    def populate_table(self, profiles):

        self.profiles = profiles

        TableBuilder.build(
            model=self.model,
            objects=self.profiles,
            columns=RISK_PROFILE_COLUMNS
        )

        self.table.resizeColumnsToContents()

        self.lbl_count.setText(
            f"Total : {len(profiles)} record(s)"
        )

    def refresh(self):

        self.search_box.clear()

        self.proxy_model.setFilterRegularExpression("")

        self.load_data()