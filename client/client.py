from client.network import Networker
from client.dummy_display import Display
from client.game import Game
from PyQt5.QtCore import QThread, pyqtSignal


class Client(QThread):
	# Define signals
	connection_made = pyqtSignal(bool)

	def __init__(self):
		super(Client, self).__init__()
		print("Client initialised")

	def run(self):
		print("Client running")
		self.display = Display()
		self.networker = Networker()
		self.game = Game()

		self.display.set_up()

		self.connected = False
		while not self.connected:
			self.connected = self.networker.init_connection()

		self.connected_cf = False
		while not self.connected_cf:
			self.connected_cf = self.networker.check_connection()

		self.connection_made.emit(True)

		started = False
		while not started:
			inp = self.display.get_menu_input()
			if inp == "quit":
				self.display.quit()
				self.networker.quit()
				return
			elif inp == "start":
				started = True

		# We are now looking for a lobby
		self.nickname = self.display.get_name()
		self.display.load_lobby()
		self.networker.join_lobby(self.nickname)

		name_allowed = False
		recheck = False
		while not name_allowed:
			if not recheck:
				allowed = self.networker.check_name_allowed()
				if allowed is False:  # As opposed to allowed is None
					recheck = True
					self.display.ask_for_new_name()
				elif allowed:
					name_allowed = True
			else:
				self.nickname = self.display.get_new_name()
				if self.nickname:
					self.networker.join_lobby(self.nickname)
					recheck = False

		joined_lobby = False
		while not joined_lobby:
			joined, other_names = self.networker.check_join_lobby()
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
