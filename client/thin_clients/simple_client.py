import socket
import random
import json

from BaseClass import ProtocolObject

host = "localhost"
port = 10004
print(host, port)


class Client(ProtocolObject):
    def __init__(self):
        conn = socket.socket()
        super().__init__(conn)
        # '81.135.254.250'
        self.conn.connect((host, port))

        # Check that we are connected correctly
        self.send_command("1")
        init = self.get_command()
        if init == "9":
            print("Successfully connected")
        else:
            raise ConnectionError("Unexpected return value from server")

        print(self.get_command())
        name = random.choice(["Gloin", "Gimli", "Oin", "Thorin", "Ori", "Nori", "Dori", "Fili", "Kili", "Bifur", "Bofur", "Bombur"])
        print("Logging in as " + name)
        self.send_command("*" + name)

        names = self.get_command()
        if names == "disconnected":
            print("Disconnected")
            return
        else:
            name_list = names.split("|")
            for name in name_list:
                print(name + " is already in the lobby")

        while True:
            command_list = []
            for i in range(3):
                while True:
                    command = self.get_command()
                    if command:
                        break
                if command == "disconnected":
                    print("Disconnected")
                    return
                else:
                    command_list.append(command)
            time_left = command_list[0][1:]
            print(time_left + " seconds left")
            print(command_list[1][1:] + " players in lobby")
            print(command_list[2][1:])
            if time_left == "start":
                break
            self.send_command("5")
        print("Starting...")
        input()


if __name__ == "__main__":
    done = False
    #while not done:
    done = Client()
