import sys
from PyQt5.QtWidgets import QApplication
from src.GUI.HomePageProgramma.HomePageUI import HomePageUI


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWidget = HomePageUI()
    mainWidget.show()
    sys.exit(app.exec_())