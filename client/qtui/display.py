from random import random, choice
import sys
from PyQt5.QtWidgets import QPushButton, QApplication, QLabel, QVBoxLayout, \
	QWidget, QGridLayout, QGroupBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from client.client import Client


class Display(QWidget):
	def __init__(self, parent=None):
		super(Display, self).__init__(parent)

		self.setWindowTitle("Perudo Online")
		self.menu_layout = self.create_menu_layout()
		self.setLayout(self.menu_layout)

		# We have to keep a reference to `Client` as it is a QThread
		self.client = Client()
		self.client.start()
		self.client.connection_made.connect(self.update_connection_status)


	def create_menu_layout(self):
		menu_layout = QVBoxLayout()

		self.connection_status = QLabel("No Connection")
		menu_layout.addWidget(self.connection_status)
		start_button = QPushButton("New Game")
		menu_layout.addWidget(start_button)
		quit_button = QPushButton("Quit")
		menu_layout.addWidget(quit_button)

		#start_button.clicked.connect()
		quit_button.clicked.connect(self.quit)

		return menu_layout

	def set_up(self):
		print("Creating window...")
		print("[Enter name here:]")
		print("[Start Game] (Disabled)")
		print("[Quit]")

	def quit(self):
		print("Closing window...")

	def update_connection_status(self, status):
		self.connected = status
		if self.connected:
			print("We have a connection, can click on [Start Game] now")
			self.connection_status.setText("Connected")
		else:
			print("We have lost connection")
			self.connection_status.setText("No Connection")


	def get_menu_input(self):
		# Return whether any buttons have been pressed
		rand = random()
		if rand > 0.99:
			print("Clicked on 'start'")
			return "start"
		#elif rand < 0.01:
		#	print("Clicked on 'quit'")
		#	return "quit"
		else:
			return None

	def get_name(self):
		# Returns what was in the entry box
		#name = choice(["Oin", "Gloin", "Gimli", "Thorin", "Ori",
		#					  "Nori", "Dori", "Fili", "Kili", "Bifur", "Bofur",
		#					  "Bombur", "Balin", "Dwalin"])
		name = choice(["Oin", "Gloin", "Ori"])
		return name


	def load_lobby(self):
		print("Displaying lobby...")
		print("No lobby joined yet")

	def ask_for_new_name(self):
		print("You need to input a different name")

	def get_new_name(self):
		# Merge with get_name()?
		name = choice(["Oin", "Gloin", "Gimli", "Thorin", "Ori",
							  "Nori", "Dori", "Fili", "Kili", "Bifur", "Bofur",
							  "Bombur", "Balin", "Dwalin"])
		return name

	def join_lobby(self, init_names):
		print("Joined lobby with players {} already in".format(init_names))

	def update_lobby(self, time_left, player_name_list, starting_soon):
		print("{} seconds left".format(time_left))
		print("{} players in lobby".format(player_name_list))
		if starting_soon:
			print("Starting game soon")

	def load_game(self, player_name_list):
		print("Loading game screen with player {}".format(player_name_list))

	def start_round(self, dice_list, dice_quantities):
		print("Resetting round: \nYour dice: {}\nOther dice:".format(dice_list, dice_quantities))


def start_app():
	# Create the Qt Application
	app = QApplication(sys.argv)
	# Create and show the form
	window = Display()
	window.show()
	# Run the main Qt loop
	sys.exit(app.exec_())


if __name__ == '__main__':
	start_app()