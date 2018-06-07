from PyQt5.QtCore import QThread


class Client(QThread):
	def __init__(self):
		super(Client, self).__init__()
		print("Client initialised demo")

	#def run(self):
	#	print("Client Running")