import socket
import random
import json

from BaseClass import ProtocolObject
from settings import server_port, server_ip


class Client(ProtocolObject):
	def __init__(self):
		conn = socket.socket()
		super().__init__(conn)
		# '81.135.254.250'
		self.conn.connect((server_ip, server_port))

		# Check that we are connected correctly
		self.send_command("1")
		init = self.get_command()
		if init == "9":
			print("Successfully connected")
		else:
			raise ConnectionError("Unexpected return value from server")

		name_unique_confirm = False
		while name_unique_confirm is False:
			name = random.choice(["Gloin", "Gimli", "Oin", "Thorin", "Ori", "Nori", "Dori", "Fili", "Kili", "Bifur", "Bofur", "Bombur"])
			print("Logging in as " + name)
			self.send_command(json.dumps({"name": name}, separators=(',', ':')))
			name_unique_confirm = json.loads(self.get_command())["cf"]
			print("Name allowed: {}".format(name_unique_confirm))
		names = self.get_command()
		if names == "disconnected":
			print("Disconnected")
			return
		else:
			name_list = json.loads(names)["names"]
			for name in name_list:
				print(name + " is already in the lobby")

		while True:
			command_list = []

			command = self.get_command()

			if command == "disconnected":
				print("Disconnected")
				return
			command = json.loads(command)
			time_left = command["time"]
			print("{} seconds left".format(time_left))
			print("{} players in lobby".format(command["players"]))
			print("Players added: {}".format(command["new"]))
			print("Players lost: {}".format(command["lost"]))
			if command["st"]:
				break
			self.send_command(json.dumps({"cf": 5}, separators=(',', ':')))
		print("Starting...")
		game_info = self.get_command()
		game_info = json.loads(game_info)
		print(game_info["names"])
		index = game_info["index"]
		print("Your index is " + str(index))
		while True:
			command = self.get_command()
			if command == "disconnected":
				print("Disconnected")
				return
			elif not command:
				print("No command received")
				return
			command = json.loads(command)
			if command["i"] == "?" and command["player"] == index:
				print("Your turn:")
				bid = input()
				to_send = {}
				if bid == "dudo":
					to_send["bid"] = "dudo"
				else:
					bid = map(int, bid.split(","))
					to_send["bid"] = tuple(bid)
				to_send = json.dumps(to_send, separators=(',', ':'))
				self.send_command(to_send)
			#elif command["i"] == "@":
			#	command = command[1:]
			#	commands = command.split(",")
			#	print("Your dice:")
			#	for dice in commands[0]:
			#		print(dice + ",", end="")
			#	print()
			#	print("Other dice:")
			#	for num in commands[1]:
			#		print(num + ",", end="")
			#	print()
			#elif command["i"] == "?":
			#	print("Turn " + str(command[1]))
			#	print()
			else:
				print(command)


if __name__ == "__main__":
	done = False
	#while not done:
	done = Client()
