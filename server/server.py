import socket
from queue import Queue
from threading import Thread

from server.lobby import Lobby
from server.network_player import NetworkPlayer
from server.game import Game

from settings import server_port
print("Listening on port " + str(server_port))


class Server:
	def __init__(self, player_queue, info_queue, server_id):
		lobby = Lobby(player_queue, info_queue, server_id)
		self.server_id = server_id
		self.players = lobby.wait()
		# shuffle order?
		player_names = []
		for player in self.players:
			player_names.append(player.nickname)
		for i, player in enumerate(self.players):
			player.start_game(i, player_names)

		self.removed_players = []

		self.game = Game(len(self.players))

		self.run_game()

	def run_game(self):
		# We are starting
		# Everyone roll dice, send each player their dice
		while True:
			# Playing a round
			dice_lists, dice_quantity_lists = self.game.start_round()

			for i, player in enumerate(self.players):
				player.start_round(dice_lists[i], dice_quantity_lists)

			while True:
				# Get who's turn it is
				current_player = self.game.get_current_player()
				for player in self.players:
					player.send_current_player(current_player)

				# Wait for them to respond
				turn = self.players[current_player].get_turn()

				valid = self.game.is_valid_turn(turn)
				if not valid:
					# Remove player
					print("Bid {} not valid... removing player {}".format(turn, current_player.nickname))
					self.remove_player(current_player)
					break

				if turn == "dudo":
					self.dudo(dice_lists)
					break

				# Send all players the turn that happened
				for player in self.players:
					player.send_turn(turn)

				self.game.take_turn(turn)

	def dudo(self, dice_lists):
		# Now dudo has been called
		losing_player_no = self.game.dudo()

		is_player_out = self.game.finish_round()

		for player in self.players:
			# The players haven't been told that dudo has been called yet
			# Tell them who lost, whether that player is out, and send all the dice that were in play
			player.send_dudo(losing_player_no, is_player_out, dice_lists)

		if is_player_out:
			# We need to remove the player from the game
			self.remove_player(losing_player_no)

	def remove_player(self, player_no):
		print("Removing player {}".format(player_no))
		# Remove from game
		game_over = self.game.remove_player(player_no)

		if game_over:
			self.game_over()

		# Tell all players that they have been removed, end round
		for player in self.players:
			player.send_player_out(player_no)

		# Remove from server and add to the removed players list
		self.removed_players.append(self.players.pop(player_no))

		# TODO implement communication with removed players, telling them the game state

	def game_over(self):
		for player in self.players:
			player.end_game()


def manage_lobbies(player_in_queue):
	"""
	Runs in thread, dealing with new players, assigning them names, and putting
	them in lobbies
	"""
	lobby = False
	lobby_id = 651
	lobby_info = Queue()
	unvalidated_players = []
	unnamed_players = []
	not_allowed_player_names = []

	while True:
		if not player_in_queue.empty():
			conn, addr = player_in_queue.get()
			unvalidated_players.append(NetworkPlayer(conn, addr))

		for i, player in enumerate(unvalidated_players):
			validated = player.validate()
			if validated:
				# Remove the player from unvalidated_players and add it to unnamed_players
				unnamed_players.append(unvalidated_players.pop(i))
				print("Player from {} : {} validated".format(player.ip_address, player.port))

		for i, player in enumerate(unnamed_players):
			named, name = player.get_nickname()
			if named:
				# Check if name is allowed:
				if name in not_allowed_player_names:
					player.reject_name()
				else:
					player.accept_name()
					not_allowed_player_names.append(name)
					# Remove the player from unnamed_players and add send it to a waiting lobby
					while not lobby_info.empty():
						message = lobby_info.get()
						if message == "starting":
							# Lobby is full, we need to create a new lobby, reset all lobby info
							lobby = False
							lobby_info = Queue()
							not_allowed_player_names = []
							print("Lobby full, creating new lobby")

					if not lobby:
						# Create lobby
						player_out_queue = Queue()
						new_lobby_id = str(lobby_id).zfill(6)
						t = Thread(target=create_server, args=(player_out_queue, lobby_info, new_lobby_id))
						t.start()
						lobby_id += 1
						lobby = True
					player_out_queue.put(unnamed_players.pop(i))


def create_server(q, info_q, server_id):
	_ = Server(q, info_q, server_id)


def start_server():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.bind(("", server_port))

	s.listen(5)

	print("Waiting for connection...")
	player_q = Queue()
	Thread(target=manage_lobbies, args=(player_q,)).start()

	while True:
		conn, addr = s.accept()
		print("Received connection from " + addr[0] + " : " + str(addr[1]))
		player_q.put((conn, addr))
