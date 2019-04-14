import pyautogui
import serial
import argparse
import time
import logging
 

#  python controle_spotify.py COM19 -b 9600


class MyControllerMap:
	def __init__(self):
		self.button = {'A':'space','B':['ctrl','right'],'C': ['ctrl','left'], 'U':['ctrl','up'], 'D':['ctrl','down'], 'M':['ctrl','shiftright','shiftleft','down'], 'X':['ctrl','shiftright','shiftleft','up']} # play, passar, voltar, vol up, vol down
		self.volumes = {"D": 0, "E": 1, "F": 2, "G": 3, "H": 4, "I": 5, "J": 6, "K": 7, "L": 8, "M": 9, "N": 10, "O": 11, "P": 12, "Q": 13, "R": 14, "S": 15, "T": 16}

class SerialControllerInterface:
	# Protocolo
	
	
	# a-> play/pause
	# b-> next
	# c-> previous
	# u-> volume up
	# d-> volume down
	# m-> mute
	# x-> max volume

	# byte 1 -> Qual botão ('a','b','c','u','d','m','x')
	# byte 2 (estado - Apertado 1 ou não 0)
	# byte 3 -> EOP - End of Packet -> valor reservado 'X'

	def __init__(self, port, baudrate):
		self.ser = serial.Serial(port, baudrate=baudrate)
		self.mapping = MyControllerMap()
		self.incoming = '0'
		pyautogui.PAUSE = 0  ## remove delay
	
	def update(self):
		## Sync protocol
		while self.incoming != b'X':
			self.incoming = self.ser.read()
			logging.debug("Received INCOMING: {}".format(self.incoming))

		data = self.ser.read()
		logging.debug("Received DATA: {}".format(data))
		print(data)
		

		if data == b'A':
			logging.info("KEYPRESS PLAYPAUSE")
			pyautogui.hotkey(self.mapping.button['A'])

		elif data == b'B':
			logging.info("KEYPRESS NEXT")
			pyautogui.hotkey(self.mapping.button['B'][0], self.mapping.button['B'][1])

		elif data == b'C':
			logging.info("KEYPRESS PREVIOUS")
			pyautogui.hotkey(self.mapping.button['C'][0], self.mapping.button['C'][1])


		elif data == b'T':
			#16
			logging.info("KEYPRESS MAX VOLUME")
			pyautogui.hotkey(self.mapping.button['X'][0], self.mapping.button['X'][1], self.mapping.button['X'][2], self.mapping.button['X'][3])





		elif data == b'S':
			#15
			logging.info("KEYPRESS MAX VOLUME + VOLUME DOWN")
			pyautogui.hotkey(self.mapping.button['X'][0], self.mapping.button['X'][1], self.mapping.button['X'][2], self.mapping.button['X'][3])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])

		elif data == b'R':
			#14
			logging.info("KEYPRESS MAX VOLUME + 2VOLUME DOWN")
			pyautogui.hotkey(self.mapping.button['X'][0], self.mapping.button['X'][1], self.mapping.button['X'][2], self.mapping.button['X'][3])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])

		elif data == b'Q':
			#13
			logging.info("KEYPRESS MAX VOLUME + 3VOLUME DOWN")
			pyautogui.hotkey(self.mapping.button['X'][0], self.mapping.button['X'][1], self.mapping.button['X'][2], self.mapping.button['X'][3])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])

		elif data == b'P':
			#12
			logging.info("KEYPRESS MAX VOLUME + 4VOLUME DOWN")
			pyautogui.hotkey(self.mapping.button['X'][0], self.mapping.button['X'][1], self.mapping.button['X'][2], self.mapping.button['X'][3])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])

		elif data == b'O':
			#11
			logging.info("KEYPRESS MAX VOLUME + 5VOLUME DOWN")
			pyautogui.hotkey(self.mapping.button['X'][0], self.mapping.button['X'][1], self.mapping.button['X'][2], self.mapping.button['X'][3])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])

		elif data == b'N':
			#10
			logging.info("KEYPRESS MAX VOLUME + 6VOLUME DOWN")
			pyautogui.hotkey(self.mapping.button['X'][0], self.mapping.button['X'][1], self.mapping.button['X'][2], self.mapping.button['X'][3])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])

		elif data == b'M':
			#9
			logging.info("KEYPRESS MAX VOLUME + 7VOLUME DOWN")
			pyautogui.hotkey(self.mapping.button['X'][0], self.mapping.button['X'][1], self.mapping.button['X'][2], self.mapping.button['X'][3])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])

		elif data == b'L':
			#8
			logging.info("KEYPRESS MAX VOLUME + 7VOLUME DOWN")
			pyautogui.hotkey(self.mapping.button['X'][0], self.mapping.button['X'][1], self.mapping.button['X'][2], self.mapping.button['X'][3])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])
			pyautogui.hotkey(self.mapping.button['D'][0], self.mapping.button['D'][1])

		elif data == b'K':
			#7
			logging.info("KEYPRESS MIN VOLUME + 7VOLUME UP")
			pyautogui.hotkey(self.mapping.button['M'][0], self.mapping.button['M'][1], self.mapping.button['M'][2], self.mapping.button['M'][3])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])

		elif data == b'J':
			#6
			logging.info("KEYPRESS MIN VOLUME + 6VOLUME UP")
			pyautogui.hotkey(self.mapping.button['M'][0], self.mapping.button['M'][1], self.mapping.button['M'][2], self.mapping.button['M'][3])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])

		elif data == b'I':
			#5
			logging.info("KEYPRESS MIN VOLUME + 5VOLUME UP")
			pyautogui.hotkey(self.mapping.button['M'][0], self.mapping.button['M'][1], self.mapping.button['M'][2], self.mapping.button['M'][3])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])

		elif data == b'H':
			#4
			logging.info("KEYPRESS MIN VOLUME + 4VOLUME UP")
			pyautogui.hotkey(self.mapping.button['M'][0], self.mapping.button['M'][1], self.mapping.button['M'][2], self.mapping.button['M'][3])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])

		elif data == b'G':
			#3
			logging.info("KEYPRESS MIN VOLUME + 3VOLUME UP")
			pyautogui.hotkey(self.mapping.button['M'][0], self.mapping.button['M'][1], self.mapping.button['M'][2], self.mapping.button['M'][3])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])

		elif data == b'F':
			#2
			logging.info("KEYPRESS MIN VOLUME + 2VOLUME UP")
			pyautogui.hotkey(self.mapping.button['M'][0], self.mapping.button['M'][1], self.mapping.button['M'][2], self.mapping.button['M'][3])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])

		elif data == b'E':
			#1
			logging.info("KEYPRESS MIN VOLUME + 1VOLUME UP")
			pyautogui.hotkey(self.mapping.button['M'][0], self.mapping.button['M'][1], self.mapping.button['M'][2], self.mapping.button['M'][3])
			pyautogui.hotkey(self.mapping.button['U'][0], self.mapping.button['U'][1])







		self.incoming = self.ser.read()


class DummyControllerInterface:
	def __init__(self):
		self.mapping = MyControllerMap()

	def update(self):
		#A
		pyautogui.keyDown(self.mapping.button['A'])
		time.sleep(0.5)
		pyautogui.keyUp(self.mapping.button['A'])
		logging.info("[Dummy] Pressed A button")
		time.sleep(1)
		 #B
		pyautogui.hotkey(self.mapping.button['B'][0],self.mapping.button['B'][1])
		#logging.info(")
		# time.sleep(1)
		# #c
		pyautogui.hotkey(self.mapping.button['C'][0],self.mapping.button['C'][1])
		#logging.info(")
		# time.sleep(1)





if __name__ == '__main__':
	interfaces = ['dummy', 'serial']
	argparse = argparse.ArgumentParser()
	argparse.add_argument('serial_port', type=str)
	argparse.add_argument('-b', '--baudrate', type=int, default=9600)
	argparse.add_argument('-c', '--controller_interface', type=str, default='serial', choices=interfaces)
	argparse.add_argument('-d', '--debug', default=False, action='store_true')
	args = argparse.parse_args()
	if args.debug:
		logging.basicConfig(level=logging.DEBUG)

	print("Connection to {} using {} interface ({})".format(args.serial_port, args.controller_interface, args.baudrate))
	if args.controller_interface == 'dummy':
		controller = DummyControllerInterface()
	else:
		controller = SerialControllerInterface(port=args.serial_port, baudrate=args.baudrate)

	while True:
		controller.update()
