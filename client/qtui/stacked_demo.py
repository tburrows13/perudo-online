# https://stackoverflow.com/questions/14268356/pyside-changing-layouts

import sys
from PyQt5 import QtWidgets


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.textEdit = QtWidgets.QTextEdit('Text Edit')
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.addItem('List Widget')
        self.label = QtWidgets.QLabel('Label')

        self.stackedLayout = QtWidgets.QStackedLayout()
        self.stackedLayout.addWidget(self.textEdit)
        self.stackedLayout.addWidget(self.listWidget)
        self.stackedLayout.addWidget(self.label)

        self.frame = QtWidgets.QFrame()
        self.frame.setLayout(self.stackedLayout)

        self.button1 = QtWidgets.QPushButton('Text Edit')
        self.button1.clicked.connect(lambda: self.stackedLayout.setCurrentIndex(0))
        self.button2 = QtWidgets.QPushButton('List Widget')
        self.button2.clicked.connect(lambda: self.stackedLayout.setCurrentIndex(1))
        self.button3 = QtWidgets.QPushButton('Label')
        self.button3.clicked.connect(lambda: self.stackedLayout.setCurrentIndex(2))

        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addWidget(self.button1)
        buttonLayout.addWidget(self.button2)
        buttonLayout.addWidget(self.button3)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(buttonLayout)
        layout.addWidget(self.frame)


app = QtWidgets.QApplication(sys.argv)
# Create and show the form
window = Window()
window.show()
# Run the main Qt loop
sys.exit(app.exec_())