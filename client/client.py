import time

from client.network import Networker
from client.dummy_display import Display
from client.game import Game
from PyQt5.QtCore import QThread, pyqtSignal


class Client(QThread):
	# Define signals
	connection_made = pyqtSignal(bool)
	name_allowed = pyqtSignal(bool)

	def __init__(self):
		super(Client, self).__init__()
		print("Client initialised")
		self.nickname = None

	def run(self):
		print("Client running")
		self.display = Display()
		self.networker = Networker()
		self.game = Game()
		#self.display.set_up()

		self.connected = False
		while not self.connected:
			self.connected = self.networker.init_connection()

		self.connected_cf = False
		while not self.connected_cf:
			self.connected_cf = self.networker.check_connection()

		self.connection_made.emit(True)

		# We are now looking for a lobby
		while self.nickname is None:
			# Will be update by the display
			pass

		print("Found nickname {}".format(self.nickname))
		self.networker.join_lobby(self.nickname)

		name_allowed = False
		recheck = False
		while not name_allowed:
			if not recheck:
				allowed = self.networker.check_name_allowed()
				if allowed is False:  # As opposed to allowed is None
					recheck = True
					self.name_allowed.emit(False)
				elif allowed:
					name_allowed = True
					self.name_allowed.emit(True)
			else:
				self.nickname = None
				while self.nickname is None:
					pass
				self.networker.join_lobby(self.nickname)
				recheck = False

		# We have an allowed name now
		joined_lobby = False
		while not joined_lobby:
			joined, other_names, self.lobby_id = self.networker.check_join_lobby()
			if joined:
				joined_lobby = True

		self.display.join_lobby(other_names)
		# We are now in a lobby, so we wait for the game to start
		game_started = False
		self.starting_soon = False
		self.players = other_names
		self.time_to_start = 60
		while not game_started:
			if not self.starting_soon:
				updated = self.lobby_update()
				if updated:
					self.display.update_lobby(self.time_to_start, self.players, self.starting_soon)
			else:
				start_info = self.networker.game_start()
				if start_info:
					game_started = True
		print("Game started")
		print("Game info of " + str(start_info))

	def lobby_update(self):
		update = self.networker.lobby_update()
		if update:
			self.time_to_start = update["time"]
			new_players = update["new"]
			if self.nickname in new_players:
				new_players.remove(self.nickname)
			self.players += new_players
			for player in update["lost"]:
				self.players.remove(player)

			assert len(self.players) + 1 == update["players"], \
				"\n{} not equal to {}.\nself.players: {}"\
				.format(len(self.players)+1, update["players"], self.players)

			if update["st"]:
				self.starting_soon = True
			return True
		else:
			return False

	def set_nickname(self, name):
		self.nickname = name

	def quit(self):
		self.display.quit()
		self.networker.quit()