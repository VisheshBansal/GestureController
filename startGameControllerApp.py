import sys
from PyQt5.QtWidgets import QDialog, QApplication

from gameControllerApp import *
from helper_func_final import gameControllerFunction

class GameController(QDialog):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.start.clicked.connect(self.startController)
        self.setWindowTitle("Game Controller")
        self.show()

    def startController(self):
        topLeft = self.ui.topLeft.text().strip().lower()
        topCenter = self.ui.topCenter.text().strip().lower()
        topRight = self.ui.topRight.text().strip().lower()
        centerLeft = self.ui.centerLeft.text().strip().lower()
        center = self.ui.center.text().strip().lower()
        centerRight = self.ui.centerRight.text().strip().lower()
        bottomLeft = self.ui.bottoLeft.text().strip().lower()
        bottomCenter = self.ui.bottomCenter.text().strip().lower()
        bottomRight = self.ui.bottomRight.text().strip().lower()

        if topLeft=="":
            topLeft = None
        if topCenter=="":
            topCenter = None
        if topCenter=="":
            topCenter = None
        if centerLeft=="":
            centerLeft = None
        if center=="":
            center = None
        if centerRight=="":
            centerRight = None
        if bottomLeft=="":
            bottomLeft = None
        if bottomRight=="":
            bottomRight = None
        if bottomCenter=="":
            bottomCenter = None

        gameControllerFunction(topLeft, centerLeft, bottomLeft, topCenter, center, bottomCenter, topRight, centerRight, bottomCenter)

if __name__=="__main__":
    app = QApplication(sys.argv)
    w = GameController()
    w.show()
    sys.exit(app.exec_())