import socket

from BaseClass import ProtocolObject

host = "localhost"
port = 10005
print("Connecting to {} on port {}.".format(host, port))


class Client(ProtocolObject):
	def __init__(self):
		conn = socket.socket()
		super().__init__(conn)
		self.conn.connect((host, port))

		# Check that we are connected correctly
		self.send_command("1")
		init = self.get_command()
		if init == "9":
			print("Successfully connected")
		else:
			raise ConnectionError("Unexpected return value from server")

		# Receive "*" to ask for nickname
		self.get_command()



if __name__ == "__main__":
	c = Client()
