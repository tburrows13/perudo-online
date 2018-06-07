from random import random, choice

class Display:
	def __init__(self):
		self.connected = False
		pass

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

