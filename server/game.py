from random import randint

from Player import GamePlayer
from perudo_funcs import calc_possible_bids


class Game:
	def __init__(self, number_of_players):

		self.dice = 0
		self.players = []
		self.players_in = []  # Will contain bools

		for name in range(number_of_players):
			p = GamePlayer()
			self.players.append(p)
			self.players_in.append(True)
			self.dice += p.no_of_dice

		# Attribute initialisation
		# self.round = None
		self.current_player = randint(0, (len(self.players)-1))
		#self.current_player = 0
		self.previous = None
		self.no_of_each_value = []

	def start_round(self):

		# A list of the number of each dice in play
		self.no_of_each_value = [0, 0, 0, 0, 0, 0]
		self.previous = (0, 6)
		for player in self.players:
			self.no_of_each_value = player.reset_dice(self.no_of_each_value)
		print("No of each value: " + str(self.no_of_each_value))
		all_dice_list = []
		for player in self.players:
			all_dice_list.append(player.dice_list)

		# Create a list of how many dice each player has
		all_dice_quantities_list = []
		for dice in all_dice_list:
			all_dice_quantities_list.append(len(dice))
		return all_dice_list, all_dice_quantities_list

	def get_current_player(self):
		return self.current_player

	def is_valid_turn(self, bid):
		if bid == "dudo":
			if not self.previous:
				return False
			else:
				return True

		valid_bids = calc_possible_bids(self.previous, self.dice)
		if bid in valid_bids:
			return True
		else:
			return False

	def take_turn(self, turn):
		# Deal with turn, it has already been validated
		# We don't need to 'tell' the players, just update info
		self.previous = turn
		self.increment_player_no()

	def increment_player_no(self):
		print("Incrementing player number from {} to ".format(self.current_player), end="")
		# Make sure that we aren't giving the turn to a 'dead' player
		while True:
			self.current_player += 1
			if self.current_player >= (len(self.players)):
				# self.current_player is 0-indexed, so with 4 players, when
				# player 4 plays, current_player = 3, len(self.players) = 4
				# so (3+1) >= 4
				self.current_player = 0
			if self.players_in[self.current_player] is True:
				break
				# If self.current_player is not still in, we run the loop again
		print(self.current_player)

	def remove_player(self, player_no):
		# Remove a player, either because he disconnected or
		# because he ran out of dice
		self.increment_player_no()

		self.dice -= self.players[player_no].no_of_dice
		self.players_in[player_no] = False

		# Check if there is only one player left
		if sum(self.players_in) == 1:
			# Game is over!
			return True
		else:
			return False

	def dudo(self):
		# TODO NEXT TIME fix this return value
		# self.previous is the turn to be using
		print("Dudo called on " + str(self.previous))
		value = self.previous[1]
		proposed_num_of = self.previous[0]
		real_num_of = self.no_of_each_value[value-1]  # -1 because 0-indexed

		num_of = real_num_of
		# Add the aces into the check if we are not already checking aces
		if value != 1:
			num_of += self.no_of_each_value[0]

		# self.current_player is not the player who called dudo at this point
		if num_of < proposed_num_of:
			self.increment_player_no()
			print("Dudo called correctly. Bid was wrong")
		else:
			print("Dudo called incorrectly. Bid was right")

		# "There were 5 3s and 4 aces."
		print("There were " + str(real_num_of) + " " + str(value) + "s and " + str(self.no_of_each_value[0]) + " aces.")
		# TODO send this info out, or they can work it out themselves

		# We don't need to deal with setting the starting player for the next round, because
		# it should be whoever lost a dice on the previous round, which is current_player.
		# If they are removed, then the previous index will point to the next player

		return self.current_player  # This is the player who lost

	def finish_round(self):
		# Deal with what happens after the dudo call
		# Remove dice
		self.players[self.current_player].no_of_dice -= 1
		self.dice -= 1

		# Remove player if needed
		if self.players[self.current_player].no_of_dice <= 0:
			# The player is out
			print("Player has been removed")
			player_out = True
		else:
			# The player is not out
			player_out = False

		return player_out
