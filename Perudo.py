"""
LEGACY CODE, NOT USED BY CURRENT IMPLEMENTATION
"""

import random
from Perudo_Bots.Bots import *
from Player import *
# from numCheckModule import *
# print("You are playing as South")

    
class Round:
    def __init__(self, player_list, total_no_of_dice):  # Called immediately before play round
        print("======= Round start =======")
        self.dudo = False  # Turned to True when dudo called
        self.no_of_each_value = [0, 0, 0, 0, 0, 0]  # A tuple of the number of each dice in play
        self.player_list = player_list
        self.current_bid = (0, 6)
        for i in range(len(self.player_list)):
            self.no_of_each_value = self.player_list[i].reset_dice(self.no_of_each_value)
        print("")
        # print(self.no_of_each_value)
        # print("[1, 2, 3, 4, 5, 6]")
        # print("")

        print("Total number of dice is: ", total_no_of_dice)
        

        print("")

    def play_round(self, starting_player_no):  # Called to play each round (until dudo called)
        round_over = False
        current_player_no = starting_player_no
        while round_over == False:
            self.current_bid, self.dudo = self.player_list[current_player_no].take_turn(self.current_bid, total_no_of_dice)  # Individual turn is taken and result returned
            if self.dudo == True: # Then dudo has been called
                losing_player_no = self.call_dudo(current_player_no, previous_player_no)
                return losing_player_no  # Return the player that lost the dice and end the round
            # Transition to next turn
            previous_player_no = current_player_no # Sets previous player
            
            if current_player_no >= len(self.player_list)-1:  # If we have reached the last player, go back to the beginning
                current_player_no = 0
                
            else:  # If it isn't the last player, then increase the player number
                current_player_no += 1

    def call_dudo(self, current_player_no, previous_player_no):
        print(str(self.current_bid) + " has been 'dudo'ed")
        print("")

        # Work out whether to add the aces into the check
        if self.current_bid[1] != 1:
            total_check = self.no_of_each_value[self.current_bid[1]-1] + self.no_of_each_value[0]
        elif self.current_bid[1] == 1:
            total_check = self.no_of_each_value[self.current_bid[1]-1]
        else:
            raise ValueError("Perudo Error:  current_bid[1] is incompatible in call_dudo()")
            
        if total_check < self.current_bid[0]:  # Checks whether the bid is over the actual number of dice showing that value
            self.losing_player_no = previous_player_no
            print("Called correctly")
            
        elif total_check >= self.current_bid[0]:
            self.losing_player_no = current_player_no
            print("Called incorrectly")
            
        else:
            print("ERROR")
        print("There were " + str(self.no_of_each_value[self.current_bid[1]-1]) + " " + str(self.current_bid[1]) + "s and " + str(self.no_of_each_value[0]) + " aces.")
        print("")
        
        return self.losing_player_no

    def finish_round(self, total_no_of_dice, losing_player_no):  # Called after playround() has finished and takes away dice from the losingplayer
        self.player_list[losing_player_no].no_of_dice -= 1  # Take away a dice from the loser
        if self.player_list[losing_player_no].no_of_dice <= 0:  # If the last dice has been lost
            print("========= " + self.player_list[losing_player_no].name + " has been eliminated =========")
            player_out = True
        else:
            print("========= " + self.player_list[losing_player_no].name + " has lost a dice =========")
            player_out = False
        total_no_of_dice -= 1
        print("")
        _ = input("Press Return to continue")
        print("")
        return total_no_of_dice, player_out


def main():
    game_over = False
    global total_no_of_dice
    total_no_of_dice = 0

    #Bots.get_bid_1((2,3),[(2,3),(3,4),(4,5)])
    player_list = []  # 0 Means player-controlled
    north = RandBot("North", 1)  # 0
    player_list.append(north)
    east = Player("East", 0)   # 1
    player_list.append(east)
    south = Player("South", 0)  # 2
    player_list.append(south)
    west = Player("West", 0)  # 3
    player_list.append(west)

    for player in player_list:
        total_no_of_dice += player.no_of_dice

    starting_player_no = random.randrange(len(player_list))
    # startingplayer = player_list[starting_player_no] # Not currently used
    losing_player_no = starting_player_no # just coz


    # Play turns
    while game_over is False:
        round1 = Round(player_list, total_no_of_dice)
        losing_player_no = round1.play_round(losing_player_no)
        total_no_of_dice, player_out = round1.finish_round(total_no_of_dice, losing_player_no)
        if player_out is True:  # i.e. a player is out
            player_list.pop(losing_player_no)  # Remove player from playlist
            if losing_player_no > len(player_list)-1:  # If the eliminated player was the last player, then the starting player will be the first player
                losing_player_no = 0
        if len(player_list) == 1:  # Game Over!
            print("")
            print("======= GAME OVER =======")
            print(player_list[0].name + " has won with " + str(player_list[0].no_of_dice) + " dice remaining")
            game_over = True


if __name__ == "__main__":
    main()
