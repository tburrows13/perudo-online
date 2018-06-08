from random import random, choice
import sys
import time

from PyQt5.QtWidgets import QPushButton, QApplication, QLabel, QVBoxLayout, \
	QWidget, QGridLayout, QGroupBox, QScrollArea, QFrame, QStackedLayout, \
	QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QObjectCleanupHandler

from client.client import Client


class Display(QWidget):
	def __init__(self, parent=None):
		super(Display, self).__init__(parent)

		self.setWindowTitle("Perudo Online")
		self.menu_layout = self.create_menu_layout()
		self.name_layout = self.create_insert_name_layout()
		self.game_layout = self.create_other_player_layout("North")
		stacked_layout = QStackedLayout(self)
		stacked_layout.addWidget(self.menu_layout)
		stacked_layout.addWidget(self.name_layout)
		stacked_layout.addWidget(self.game_layout)

		self.setLayout(stacked_layout)

		# We have to keep a reference to `Client` as it is a QThread
		self.client = Client()
		self.client.start()
		self.client.connection_made.connect(self.update_connection_status)

	def create_menu_layout(self):
		menu_layout = QVBoxLayout()

		self.connection_status = QLabel("No Connection")
		menu_layout.addWidget(self.connection_status)
		self.start_button = QPushButton("New Game")
		menu_layout.addWidget(self.start_button)
		quit_button = QPushButton("Quit")
		menu_layout.addWidget(quit_button)

		self.start_button.setEnabled(False)
		self.start_button.clicked.connect(self.start_game)
		quit_button.clicked.connect(self.quit)
		frame = QFrame()
		frame.setLayout(menu_layout)
		return frame

	def create_insert_name_layout(self):
		layout = QVBoxLayout()

		text = QLabel("Enter your name:")
		layout.addWidget(text)
		self.name_input = QLineEdit()
		layout.addWidget(self.name_input)
		enter_button = QPushButton("Enter")
		layout.addWidget(enter_button)

		enter_button.clicked.connect(self.enter_name)

		frame = QFrame()
		frame.setLayout(layout)
		return frame

	def create_play_layout(self, player_names):
		play_layout = QGridLayout

	def create_other_player_layout(self, name):
		# Creates a dice mat, a cup, a name label and the place to write what
		# bids the player made
		layout = QVBoxLayout()
		player_name = QLabel(name)

		scroll = QScrollArea()
		scroll.setMaximumHeight(90)
		scroll.setWidgetResizable(True)  # CRITICAL

		inner = QFrame(scroll)
		inner.setLayout(QVBoxLayout())

		scroll.setWidget(inner)  # CRITICAL

		for i in range(50):
			inner.layout().addWidget(QLabel(f"{i} threes"))

		layout.addWidget(player_name)
		layout.addWidget(scroll)

		frame = QFrame()
		frame.setLayout(layout)
		return frame

	def enter_name(self):
		print(f"Starting game with name {self.name_input.text()}")
		self.layout().setCurrentIndex(2)

	def start_game(self):
		self.layout().setCurrentIndex(1)

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
			self.start_button.setEnabled(True)

		else:
			print("We have lost connection")
			self.connection_status.setText("No Connection")
			self.start_button.setEnabled(False)


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