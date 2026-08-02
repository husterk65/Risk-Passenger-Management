from PyQt6.QtWidgets import QApplication

from ui.dialogs.risk_profile_dialog import RiskProfileDialog

app = QApplication([])

dialog = RiskProfileDialog()

if dialog.exec():

    profile = dialog.get_profile()

    print(profile)

app.exec()