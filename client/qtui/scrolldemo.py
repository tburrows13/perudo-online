from PyQt5.QtWidgets import *

app = QApplication([])

scroll = QScrollArea()
scroll.setWidgetResizable(True) # CRITICAL

inner = QFrame(scroll)
inner.setLayout(QVBoxLayout())

scroll.setWidget(inner) # CRITICAL

for i in range(20):
    b = QPushButton(inner)
    b.setText(str(i))
    inner.layout().addWidget(b)

inner.layout().removeWidget(b)
b.close()

scroll.show()
app.exec_()