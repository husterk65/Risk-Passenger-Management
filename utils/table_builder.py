from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItem

class TableBuilder:

    @staticmethod
    def build(model, objects, columns):

        model.clear()

        # ==========================
        # Headers
        # ==========================

        headers = ["STT"] + [
            column["title"]
            for column in columns
        ]

        model.setHorizontalHeaderLabels(headers)

        # ==========================
        # Rows
        # ==========================

        for row_index, obj in enumerate(objects, start=1):

            # STT
            model.setItem(
                row_index - 1,
                0,
                QStandardItem(str(row_index))
            )
            model.item(row_index - 1, 0).setTextAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            # Data
            for column_index, column in enumerate(columns, start=1):

                value = getattr(
                    obj,
                    column["field"],
                    ""
                )

                item = QStandardItem(
                    "" if value is None else str(value)
                )

                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                model.setItem(
                    row_index - 1,
                    column_index,
                    item
                )