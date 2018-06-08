from random import randint

from perudo_funcs import calc_possible_bids


class GamePlayer:
	def __init__(self):
		self.no_of_dice = 5
		self.dice_list = []
		self.past_turns = []

	def reset_dice(self, no_of_each_value):
		# Called at the beginning of each round to reassign dice values
		# Returns the updated `no_of_each_value`
		self.dice_list = []
		for i in range(self.no_of_dice):  # Assign dice values
			dice_value = int(randint(1, 6))
			self.dice_list.append(dice_value)
			# own_no_of_each_value[dice_value - 1] += 1
			no_of_each_value[dice_value - 1] += 1  # Add the the relevant place in no_of_each_value

		# We also need to reset our turns, as it is the beginning of the round
		self.reset_turns()

		return no_of_each_value

	def reset_turns(self):
		self.past_turns = []

	def turn_taken(self, turn):
		self.past_turns.append(turn)

	def take_turn(self, current_bid, total_no_of_dice):
		possible_bids = calc_possible_bids(current_bid, total_no_of_dice)  # Get a list of tuples of possible moves

		current_bid, dudo = self.player_turn(current_bid, possible_bids)

		return current_bid, dudo

	def player_turn(self, current_bid, possible_moves):
		"""Mostly to do with command-line inputting, not needed"""
		move_is_valid = False  # Turn to True if move is successfully checked
		while move_is_valid is False:
			number_of = input('Enter "dudo" or the first value of your bid:  ')  # Input bid or dudo

			# If dudo input, then return current_bid and True which will initiate dudo method
			if number_of == "dudo" or number_of == "Dudo":

				return current_bid, True

			# If dudo is not input then work out if the bid is valid
			else:

				value = input('Enter the second value of your bid: ')  # Input bid or dudo

				try:  # Check if temp_bid can be turned into digits
					number_of = int(number_of)
					value = int(value)

					# Check if temp_bid is higher than the current_bid
					temp_bid = (number_of, value)

					for i in range(len(possible_moves)):
						if move_is_valid is False:
							if temp_bid == possible_moves[i]:
								move_is_valid = True

					if move_is_valid is False:
						print("Error: Bid value invalid")

					elif move_is_valid is True:
						print("Bid of " + str(temp_bid) + " accepted")
						print("")
						current_bid = temp_bid
						return current_bid, False  # False means that dudo has not been called
				except:
					print("Error: Bid format invalid")
				print("")  # Space before it loops back
