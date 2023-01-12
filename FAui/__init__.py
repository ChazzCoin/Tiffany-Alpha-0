import sys
from PyQt6 import QtWidgets
from FAui.jarticleMain import LucasUI


def launchUI():
    app = QtWidgets.QApplication(sys.argv)
    window = LucasUI()
    sys.exit(app.exec())
