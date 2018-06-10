import json
import time

from BaseClass import ProtocolObject


class NetworkPlayer(ProtocolObject):
	def __init__(self, conn, addr):
		# Assigns self.buffer and self.conn
		super().__init__()
		self.conn = conn
		self.ip_address = addr[0]
		self.port = addr[1]

		self.nickname = None
		self.init = None
		self.waiting = 0
		self.game_player = None
		self.index = None

	def validate(self):
		# Called before player is assigned a lobby
		init = self.get_command()
		if init == "1":
			self.send_command("9")
			return True
		else:
			return False

	def get_nickname(self):
		# Called before player is assigned a lobby
		command = self.get_command()
		if command == "disconnected":
			# TODO
			raise Exception

		if not command:
			# If we didn't get anything
			return False, None
		else:
			command = json.loads(command)
			self.nickname = command["name"]
			return True, self.nickname

	def accept_name(self):
		to_send = json.dumps({"cf": True})
		self.send_command(to_send)

	def reject_name(self):
		to_send = json.dumps({"cf": False})
		self.send_command(to_send)

	def send_names(self, names, lobby_id):
		# Called once after a player has been added to a lobby
		to_send = json.dumps({"names": names, "id": lobby_id}, separators=(',', ':'))
		self.send_command(to_send)

	def update(self, time_left, no_of_players, new_players, lost_players, started):
		# Called once every few seconds while we're in the lobby
		# Send info to the client
		to_send = {}
		to_send["time"] = time_left
		to_send["players"] = no_of_players
		to_send["new"] = new_players
		to_send["lost"] = lost_players
		to_send["st"] = started

		to_send = json.dumps(to_send, separators=(',', ':'))

		self.send_command(to_send)
		self.waiting += 1

	def receive(self):
		# Called while we are in the lobby to check if the client is responding
		if self.waiting > 0:
			s = self.get_command()
			if s == "disconnected" or self.waiting > 5:
				return "disconnected"
			elif not s:
				return False
			s = json.loads(s)
			if s and (s["cf"] != 5):
				raise Exception("5 not returned from client")
			if s["cf"] == 5:
				self.waiting -= 1
				return True
		return False

	def start_game(self, index, names):
		self.index = index
		to_send = {"index": index, "names": names}
		to_send = json.dumps(to_send, separators=(',', ':'))
		self.send_command(to_send)

	def start_round(self, dice_list, dice_quantities):
		# Called at the beginning of each round to tell the client how many dice
		# there are, and what their dice are.
		# Convert a list of ints into a string
		to_send = {"i": "@", "dice": dice_list, "dice_q": dice_quantities}
		to_send = json.dumps(to_send, separators=(',', ':'))
		self.send_command(to_send)

	def send_current_player(self, player_no):
		# Tell every player who's turn it is
		to_send = {"i": "?", "player": player_no}
		to_send = json.dumps(to_send, separators=(',', ':'))
		self.send_command(to_send)

	def get_turn(self):
		# Called when it is this player's turn, so we wait until they respond
		while True:
			command = self.get_command()
			if command:
				if command == "disconnected":
					# TODO something
					print("Client " + self.nickname + " disconnected")
					exit()

				else:
					turn = json.loads(command)
					bid = turn["bid"]
					if bid == "dudo":
						return "dudo"
					bid = tuple(bid)
					print("Bid received from " + self.nickname + ": " + str(bid))
					return bid

	def send_turn(self, bid):
		# Called after a turn has happened, we are telling our player what
		# the turn was.
		to_send = {"i": "sendturn", "bid": bid}
		to_send = json.dumps(to_send, separators=(',', ':'))
		self.send_command(to_send)

	def send_dudo(self, player_no, is_out, all_dice):
		to_send = {"i": "senddudo", "player": player_no, "out": is_out, "alldice": all_dice}
		to_send = json.dumps(to_send, separators=(',', ':'))
		self.send_command(to_send)

	def send_player_out(self, player_no):
		to_send = {"i": "sendplayerout", "player": player_no}
		to_send = json.dumps(to_send, separators=(',', ':'))
		self.send_command(to_send)

	def end_game(self):
		# TODO
		to_send = {"i": "endgame"}
		to_send = json.dumps(to_send, separators=(',', ':'))
		self.send_command(to_send)