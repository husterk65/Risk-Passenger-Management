import sys

from PyQt6.QtWidgets import QApplication

from ui.pages.risk_profile_page import RiskProfilePage


app = QApplication(sys.argv)

window = RiskProfilePage()

window.resize(1200, 700)

window.show()

sys.exit(app.exec())