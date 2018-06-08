from random import random
import json
import socket

from BaseClass import ProtocolObject
from settings import server_ip, server_port


class Networker(ProtocolObject):
	def __init__(self):
		conn = socket.socket()
		conn.connect((server_ip, server_port))

		super().__init__(conn, timeout=True)
		self.connected = False

	def quit(self):
		print("Networker closing connection")

	def init_connection(self):
		# Send initial message
		self.send_command("1")

	def check_connection(self):
		# Check for received connection
		command = self.get_command()
		if command == "disconnected":
			# TODO
			print("Disconnected")
			raise ConnectionError

		elif command == "9":
			return True

		elif command:
			# TODO
			raise ConnectionAbortedError

		else:
			return False

	def join_lobby(self, name):
		to_send = json.dumps({"name": name})
		self.send_command(to_send)

	def check_name_allowed(self):
		# Checks if our name is allowed
		command = self.get_command()
		if command == "disconnected":
			raise ConnectionError
		elif command:
			dic = json.loads(command)
			if dic["cf"]:
				return True
			else:
				return False
		return None

	def check_join_lobby(self):
		# Checks if we've received confirmation on joining the lobby
		command = self.get_command()
		if command == "disconnected":
			raise ConnectionError
		elif command:
			dic = json.loads(command)
			return True, dic["names"]
		else:
			return False, None

	def lobby_update(self):
		command = self.get_command()
		if command == "disconnected":
			raise ConnectionError
		elif command:
			# Send confirmation
			self.send_command(json.dumps({"cf": 5}))
			dic = json.loads(command)
			return dic
		else:
			return None

	def game_start(self):
		command = self.get_command()
		if command == "disconnected":
			raise ConnectionError
		elif command:
			dic = json.loads(command)
			return dic
		else:
			return None
