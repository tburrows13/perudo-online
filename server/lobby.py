from time import sleep, time

from settings import MAX_PLAYERS


def sleepn(t):
    if t < 0:
        t = 0
    sleep(t)


class Lobby:
    def __init__(self, player_queue, lobby_queue, lobby_id):
        self.queue = player_queue
        self.info_queue = lobby_queue
        self.lobby_id = lobby_id

        self.players = []
        self.new_players = []  # List containing strings
        self.lost_players = []  # ''
        self.player_names = []
        self.time_to_start = 30
        self.update_frequency = 5  # How often it notifies the players of info

    def wait(self):
        start = time()
        while len(self.players) < MAX_PLAYERS and self.time_to_start > 0:
            self.check_new_players()

            for player in self.players:
                # index 4 is whether we've started
                player.update(self.time_to_start, len(self.players),
                              self.new_players, self.lost_players, False)
            self.new_players = []
            self.lost_players = []
            while (time() - start) < self.update_frequency:
                for player in self.players:
                    connected = player.receive()
                    if connected == "disconnected":
                        self.lost_players.append(player.nickname)
                        self.players.remove(player)
                        self.player_names.remove(player.nickname)
                        print("Player disconnected " + player.nickname)
                        # If we go down to one player, keep the timer back at 30
                        if len(self.players) == 1:
                            self.time_to_start = 30
                sleep(0.1)
            start = time()
            if len(self.players) >= 2:
                self.time_to_start -= self.update_frequency
        # We have reached capacity
        # Tell the main thread that we are starting:
        self.info_queue.put("starting")

        # Tell all players that we are starting:
        for player in self.players:
            player.update(self.time_to_start, len(self.players),
                          self.new_players, self.lost_players, True)

        print("Starting game...")
        return self.players

    def check_new_players(self):
        while not self.queue.empty():
            new_player = self.queue.get()
            print("Player joined: " + new_player.nickname)
            new_player.send_names(self.player_names, self.lobby_id)
            self.new_players.append(new_player.nickname)
            self.player_names.append(new_player.nickname)
            self.players.append(new_player)
            # self.time_to_start += 5


def create_lobby(pq, lq):
    _ = Lobby(pq, lq)


