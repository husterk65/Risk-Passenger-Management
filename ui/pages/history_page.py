
from PyQt6.QtCore import Qt, QSortFilterProxyModel, QRegularExpression
from PyQt6.QtGui import QStandardItemModel, QStandardItem

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableView,
    QFrame,
    QHeaderView,
    QMessageBox,
)

from services.audit_log_service import AuditLogService


class HistoryPage(QWidget):

    def __init__(self):
        super().__init__()

        self.logs = []

        self.model = QStandardItemModel()

        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)

        self.proxy_model.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )
        self.proxy_model.setFilterKeyColumn(-1)
        self.proxy_model.setDynamicSortFilter(True)

        self.init_ui()
        self.load_data()

    # =========================================================
    # UI
    # =========================================================

    def init_ui(self):

        self.setObjectName("HistoryPage")

        self.setStyleSheet("""
            QWidget#HistoryPage {
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
                color: #0f172a;
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

            /* =========================
               TABLE
               ========================= */

            QTableView {
                background: white;
                color: #0f172a;

                border: 1px solid #e2e8f0;
                border-radius: 12px;

                gridline-color: #f1f5f9;

                selection-background-color: #dbeafe;
                selection-color: #0f172a;
            }

            QTableView::item {
                color: #0f172a;
                padding: 8px;
                border: none;
            }

            QTableView::item:selected {
                background: #dbeafe;
                color: #0f172a;
            }

            QTableView::item:alternate {
                background: #fafafa;
                color: #0f172a;
            }

            QTableView::item:alternate:selected {
                background: #dbeafe;
                color: #0f172a;
            }

            /* =========================
               TABLE HEADER
               ========================= */

            QHeaderView::section {
                background: #f8fafc;
                color: #334155;

                padding: 8px;

                border: none;

                font-weight: 600;
            }

            QHeaderView {
                background: #f8fafc;
            }

            /* =========================
               SCROLLBAR
               ========================= */

            QScrollBar:vertical {
                background: #f8fafc;
                width: 10px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 5px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background: #94a3b8;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QScrollBar:horizontal {
                background: #f8fafc;
                height: 10px;
                margin: 0px;
            }

            QScrollBar::handle:horizontal {
                background: #cbd5e1;
                border-radius: 5px;
                min-width: 30px;
            }

            QScrollBar::handle:horizontal:hover {
                background: #94a3b8;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)

        # =====================================================
        # ROOT
        # =====================================================

        root = QVBoxLayout(self)

        root.setContentsMargins(
            20,
            20,
            20,
            20
        )

        root.setSpacing(0)

        # =====================================================
        # CONTENT CARD
        # =====================================================

        card = QFrame()
        card.setObjectName("contentCard")

        card_layout = QVBoxLayout(card)

        card_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        card_layout.setSpacing(16)

        # =====================================================
        # HEADER
        # =====================================================

        header_layout = QHBoxLayout()

        # ---------- Title ----------

        title_layout = QVBoxLayout()

        title_layout.setSpacing(4)

        title = QLabel("History")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Track user activities and system changes."
        )

        subtitle.setObjectName("pageSubtitle")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        header_layout.addLayout(title_layout)

        header_layout.addStretch()

        # ---------- Count ----------

        self.lbl_count = QLabel("0 record(s)")

        self.lbl_count.setObjectName("countBadge")

        header_layout.addWidget(
            self.lbl_count
        )

        card_layout.addLayout(
            header_layout
        )

        # =====================================================
        # TOOLBAR
        # =====================================================

        toolbar = QHBoxLayout()

        toolbar.setSpacing(10)

        # ---------- Search ----------

        self.search_box = QLineEdit()

        self.search_box.setPlaceholderText(
            "Search user / action / module / details..."
        )

        self.search_box.textChanged.connect(
            self.search
        )

        toolbar.addWidget(
            self.search_box,
            1
        )

        # ---------- Refresh ----------

        self.btn_refresh = QPushButton(
            "Refresh"
        )

        self.btn_refresh.clicked.connect(
            self.refresh
        )

        toolbar.addWidget(
            self.btn_refresh
        )

        card_layout.addLayout(
            toolbar
        )

        # =====================================================
        # TABLE
        # =====================================================

        self.table = QTableView()

        self.table.setModel(
            self.proxy_model
        )

        # Sorting

        self.table.setSortingEnabled(
            True
        )

        # Alternating rows

        self.table.setAlternatingRowColors(
            True
        )

        # Remove grid

        self.table.setShowGrid(
            False
        )

        # Select entire row

        self.table.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QTableView.SelectionMode.SingleSelection
        )

        # Read-only

        self.table.setEditTriggers(
            QTableView.EditTrigger.NoEditTriggers
        )

        # Remove focus outline

        self.table.setFocusPolicy(
            Qt.FocusPolicy.NoFocus
        )

        # Hide row numbers

        self.table.verticalHeader().setVisible(
            False
        )

        # =====================================================
        # HEADER RESIZE
        # =====================================================

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        header.setStretchLastSection(
            True
        )

        card_layout.addWidget(
            self.table
        )

        root.addWidget(
            card
        )

    # =========================================================
    # LOAD DATA
    # =========================================================

    def load_data(self):

        try:

            self.logs = AuditLogService.get_all()

            self.populate_table(
                self.logs
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"Failed to load history:\n{e}"
            )

    # =========================================================
    # POPULATE TABLE
    # =========================================================

    def populate_table(self, logs):

        self.model.clear()

        headers = [
            "Time",
            "User",
            "Action",
            "Module",
            "Details",
        ]

        self.model.setHorizontalHeaderLabels(
            headers
        )

        for log in logs:

            row = [

                QStandardItem(
                    str(
                        log.get(
                            "created_at",
                            ""
                        )
                    )
                ),

                QStandardItem(
                    str(
                        log.get(
                            "username",
                            ""
                        )
                    )
                ),

                QStandardItem(
                    str(
                        log.get(
                            "action",
                            ""
                        )
                    )
                ),

                QStandardItem(
                    str(
                        log.get(
                            "module",
                            ""
                        )
                    )
                ),

                QStandardItem(
                    str(
                        log.get(
                            "details",
                            ""
                        )
                    ),
                ),
            ]

            # Explicitly force text color
            for item in row:
                item.setForeground(
                    Qt.GlobalColor.black
                )

            self.model.appendRow(
                row
            )

        self.lbl_count.setText(
            f"{len(logs)} record(s)"
        )

        self.table.resizeColumnsToContents()

    # =========================================================
    # SEARCH
    # =========================================================

    def search(self):

        keyword = (
            self.search_box
            .text()
            .strip()
        )

        # Empty search
        if not keyword:

            self.proxy_model.setFilterRegularExpression(
                ""
            )

            return

        regex = QRegularExpression(
            keyword,
            QRegularExpression.PatternOption.CaseInsensitiveOption
        )

        self.proxy_model.setFilterRegularExpression(
            regex
        )

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):

        self.search_box.clear()

        self.proxy_model.setFilterRegularExpression(
            ""
        )

        self.load_data()
