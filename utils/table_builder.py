from PyQt6.QtGui import QStandardItem

class TableBuilder:

    @staticmethod
    def build(model, objects, columns):

        model.clear()

        headers = [
            column["title"]
            for column in columns
        ]

        model.setHorizontalHeaderLabels(headers)

        for obj in objects:

            row = []

            for column in columns:

                field = column["field"]

                value = getattr(obj, field, "")

                if value is None:
                    value = ""

                if isinstance(value, bool):
                    value = "Yes" if value else "No"

                row.append(
                    QStandardItem(str(value))
                )

            model.appendRow(row)