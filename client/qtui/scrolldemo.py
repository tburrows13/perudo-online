from PyQt5.QtWidgets import *

app = QApplication([])

scroll = QScrollArea()
scroll.setWidgetResizable(True) # CRITICAL

inner = QFrame(scroll)
inner.setLayout(QVBoxLayout())

scroll.setWidget(inner) # CRITICAL

for i in range(40, 0, -1):
    b = QPushButton(inner)
    b.setText(str(i))
    inner.layout().addWidget(b)

scroll.show()
app.exec_()