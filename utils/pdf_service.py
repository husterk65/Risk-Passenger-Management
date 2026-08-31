from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from datetime import datetime
import os


class PdfService:

    # ==================================================
    # EXPORT RISK ALERTS
    # ==================================================

    @staticmethod
    def export_risk_alerts(
        alerts,
        file_path: str,
        flight_name: str = "All Flights",
        keyword: str = "",
    ):
        if not alerts:
            raise ValueError(
                "Không có dữ liệu Risk Alert để xuất PDF."
            )

        # --------------------------------------------------
        # Create output directory if needed
        # --------------------------------------------------

        directory = os.path.dirname(file_path)

        if directory:
            os.makedirs(
                directory,
                exist_ok=True
            )

        # --------------------------------------------------
        # Register Unicode font
        # --------------------------------------------------

        PdfService._register_font()

        # --------------------------------------------------
        # PDF document
        # --------------------------------------------------

        document = SimpleDocTemplate(
            file_path,
            pagesize=landscape(A4),
            rightMargin=10 * mm,
            leftMargin=10 * mm,
            topMargin=10 * mm,
            bottomMargin=10 * mm,
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            fontName="DejaVuSans",
            fontSize=18,
            leading=22,
            alignment=TA_LEFT,
            spaceAfter=4,
        )

        info_style = ParagraphStyle(
            "ReportInfo",
            parent=styles["Normal"],
            fontName="DejaVuSans",
            fontSize=8.5,
            leading=12,
        )

        header_style = ParagraphStyle(
            "TableHeader",
            parent=styles["Normal"],
            fontName="DejaVuSans-Bold",
            fontSize=7.5,
            leading=9,
            alignment=TA_CENTER,
            textColor=colors.white,
        )

        cell_style = ParagraphStyle(
            "TableCell",
            parent=styles["Normal"],
            fontName="DejaVuSans",
            fontSize=7,
            leading=8.5,
        )

        story = []

        # ==================================================
        # TITLE
        # ==================================================

        story.append(
            Paragraph(
                "RISK ALERTS REPORT",
                title_style
            )
        )

        # ==================================================
        # REPORT INFORMATION
        # ==================================================

        exported_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        keyword_display = (
            keyword
            if keyword
            else "None"
        )

        info_data = [
            [
                Paragraph(
                    f"<b>Flight:</b> "
                    f"{PdfService._escape(flight_name)}",
                    info_style
                ),
                Paragraph(
                    f"<b>Total Alerts:</b> "
                    f"{len(alerts)}",
                    info_style
                ),
                Paragraph(
                    f"<b>Search:</b> "
                    f"{PdfService._escape(keyword_display)}",
                    info_style
                ),
                Paragraph(
                    f"<b>Exported At:</b> "
                    f"{exported_at}",
                    info_style
                ),
            ]
        ]

        info_table = Table(
            info_data,
            colWidths=[
                65 * mm,
                40 * mm,
                65 * mm,
                65 * mm,
            ],
        )

        info_table.setStyle(
            TableStyle([
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    2
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    2
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    3
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    3
                ),
            ])
        )

        story.append(info_table)
        story.append(Spacer(1, 6 * mm))

        # ==================================================
        # TABLE HEADER
        # ==================================================

        table_data = [
            [
                Paragraph("Flight", header_style),
                Paragraph("Full Name", header_style),
                Paragraph("Passport", header_style),
                Paragraph("Nationality", header_style),
                Paragraph("Date of Birth", header_style),
                Paragraph("Gender", header_style),
                Paragraph("Risk Level", header_style),
                Paragraph("Risk Reason", header_style),
                Paragraph("Checked At", header_style),
            ]
        ]

        # ==================================================
        # TABLE DATA
        # ==================================================

        for alert in alerts:

            risk_level = (
                str(
                    getattr(
                        alert,
                        "risk_level",
                        ""
                    )
                    or ""
                )
                .strip()
                .upper()
            )

            table_data.append([
                PdfService._cell(
                    getattr(
                        alert,
                        "flight_number",
                        ""
                    ),
                    cell_style
                ),

                PdfService._cell(
                    getattr(
                        alert,
                        "full_name",
                        ""
                    ),
                    cell_style
                ),

                PdfService._cell(
                    getattr(
                        alert,
                        "passport_number",
                        ""
                    ),
                    cell_style
                ),

                PdfService._cell(
                    getattr(
                        alert,
                        "nationality",
                        ""
                    ),
                    cell_style
                ),

                PdfService._cell(
                    getattr(
                        alert,
                        "date_of_birth",
                        ""
                    ),
                    cell_style
                ),

                PdfService._cell(
                    getattr(
                        alert,
                        "gender",
                        ""
                    ),
                    cell_style
                ),

                PdfService._cell(
                    risk_level,
                    cell_style
                ),

                PdfService._cell(
                    getattr(
                        alert,
                        "risk_reason",
                        ""
                    ),
                    cell_style
                ),

                PdfService._cell(
                    getattr(
                        alert,
                        "created_at",
                        ""
                    ),
                    cell_style
                ),
            ])

        # ==================================================
        # COLUMN WIDTHS
        # ==================================================

        column_widths = [
            22 * mm,   # Flight
            35 * mm,   # Full Name
            29 * mm,   # Passport
            25 * mm,   # Nationality
            25 * mm,   # DOB
            18 * mm,   # Gender
            23 * mm,   # Risk
            70 * mm,   # Reason
            35 * mm,   # Checked At
        ]

        table = Table(
            table_data,
            colWidths=column_widths,
            repeatRows=1,
            splitByRow=True,
        )

        # ==================================================
        # TABLE STYLE
        # ==================================================

        table_style_commands = [
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#334155")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.3,
                colors.HexColor("#CBD5E1")
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
        ]

        # --------------------------------------------------
        # Alternating rows
        # --------------------------------------------------

        for row in range(
            1,
            len(table_data)
        ):
            if row % 2 == 0:
                table_style_commands.append(
                    (
                        "BACKGROUND",
                        (0, row),
                        (-1, row),
                        colors.HexColor("#F8FAFC")
                    )
                )

        # --------------------------------------------------
        # Risk level colors
        # --------------------------------------------------

        for row_index, alert in enumerate(
            alerts,
            start=1
        ):
            risk_level = (
                str(
                    getattr(
                        alert,
                        "risk_level",
                        ""
                    )
                    or ""
                )
                .strip()
                .upper()
            )

            if risk_level == "HIGH":
                table_style_commands.extend([
                    (
                        "TEXTCOLOR",
                        (6, row_index),
                        (6, row_index),
                        colors.HexColor("#B91C1C")
                    ),
                    (
                        "FONTNAME",
                        (6, row_index),
                        (6, row_index),
                        "DejaVuSans-Bold"
                    ),
                ])

            elif risk_level == "MEDIUM":
                table_style_commands.extend([
                    (
                        "TEXTCOLOR",
                        (6, row_index),
                        (6, row_index),
                        colors.HexColor("#B45309")
                    ),
                    (
                        "FONTNAME",
                        (6, row_index),
                        (6, row_index),
                        "DejaVuSans-Bold"
                    ),
                ])

            elif risk_level == "LOW":
                table_style_commands.extend([
                    (
                        "TEXTCOLOR",
                        (6, row_index),
                        (6, row_index),
                        colors.HexColor("#15803D")
                    ),
                    (
                        "FONTNAME",
                        (6, row_index),
                        (6, row_index),
                        "DejaVuSans-Bold"
                    ),
                ])

        table.setStyle(
            TableStyle(table_style_commands)
        )

        story.append(table)

        # ==================================================
        # BUILD PDF
        # ==================================================

        document.build(story)

    # ==================================================
    # REGISTER FONT
    # ==================================================

    @staticmethod
    def _register_font():

        if "DejaVuSans" in pdfmetrics.getRegisteredFontNames():
            return

        font_path = (
            "/usr/share/fonts/truetype/dejavu/"
            "DejaVuSans.ttf"
        )

        bold_font_path = (
            "/usr/share/fonts/truetype/dejavu/"
            "DejaVuSans-Bold.ttf"
        )

        if not os.path.exists(font_path):
            raise RuntimeError(
                "Không tìm thấy font DejaVuSans."
            )

        pdfmetrics.registerFont(
            TTFont(
                "DejaVuSans",
                font_path
            )
        )

        if os.path.exists(
            bold_font_path
        ):
            pdfmetrics.registerFont(
                TTFont(
                    "DejaVuSans-Bold",
                    bold_font_path
                )
            )

    # ==================================================
    # CREATE CELL
    # ==================================================

    @staticmethod
    def _cell(
        value,
        style
    ):

        if value is None:
            value = ""

        value = str(value)

        if not value.strip():
            value = ""

        return Paragraph(
            PdfService._escape(value),
            style
        )

    # ==================================================
    # ESCAPE HTML
    # ==================================================

    @staticmethod
    def _escape(value):

        value = str(value)

        return (
            value
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
