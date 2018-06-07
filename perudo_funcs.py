def calc_possible_bids(current_bid, total_no_of_dice):
	# Calculate all the possible moves that can be taken

	possible_bids = []  # Create a list of possible moves that will be added too
	value_was_ace = False
	number_of, value = current_bid

	if value == 1:
		number_of *= 2
		value_was_ace = True  # So that the same amount of aces cannot be called again
	# TODO add doubling allowed number_of if current number_of is ace - done now?

	# Adds the quantities of aces to below the other possible bids
	if number_of % 2 == 1:  # If number_of is odd
		number_of1 = int((number_of / 2) + 0.5)  # Halve and round up
	elif number_of % 2 == 0:
		number_of1 = number_of // 2
	else:
		raise ValueError("ERROR in calc_possible_bids")
	if value_was_ace is True:
		number_of += 1
	while number_of1 <= number_of and number_of1 <= total_no_of_dice:
		# Until we get to the bit covered by the rest of this method
		possible_bids.append((number_of1, 1))
		number_of1 += 1

	while number_of <= total_no_of_dice:

		while value < 6:
			value += 1
			possible_bids.append((number_of, value))

			# Increase 1st number, reset 2nd number to 1

		number_of += 1
		value = 0  # Which will get increased to 1

	return possible_bids
