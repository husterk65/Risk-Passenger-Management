import sys

from PyQt6.QtWidgets import QApplication

from ui.login_window import LoginWindow
from ui.main_window import MainWindow


def main():

    app = QApplication(sys.argv)

    login_window = LoginWindow()

    windows = {}

    def open_main(current_user):

        windows["main"] = MainWindow(current_user)
        windows["main"].show()

    login_window.login_success.connect(open_main)

    login_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()