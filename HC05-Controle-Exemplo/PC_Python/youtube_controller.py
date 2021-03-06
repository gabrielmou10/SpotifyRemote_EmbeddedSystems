import pyautogui
import serial
import argparse
import time
import logging
 
class MyControllerMap:
	def __init__(self):
		self.button = {'A':'space','B':['ctrl','right'],'C': ['ctrl','left']} # play, voltar,  passar
	   

class SerialControllerInterface:
	# Protocolo
	
	
	# a-> playpause
	# b-> next
	# c-> back

	# byte 1 -> Qual botão ('a','b','c')
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


		if data == b'A':
			data = self.ser.read()
			if data == b'1':
				logging.info("KEYDOWN PLAYPAUSE")
				pyautogui.keyDown(self.mapping.button['A'])	
			elif data == b'0':
				logging.info("KEYUP PLAYPAUSE")
				pyautogui.keyUp(self.mapping.button['A'])

		if data == b'B':
			data = self.ser.read()
			if data == b'1':
				#logging.info("KEYDOWN BACK")
				pyautogui.hotkey(self.mapping.button['B'][0],self.mapping.button['B'][1])
			# elif data == b'0':
			# 	logging.info("KEYUP BACK")
			# 	pyautogui.keyUp(self.mapping.button['B'])
		if data == b'C':
			data = self.ser.read()
			if data == b'1':
				logging.info("KEYDOWN NEXT")
				pyautogui.hotkey(self.mapping.button['C'][0],self.mapping.button['C'][1])
			# elif data == b'0':
			# 	logging.info("KEYUP NEXT")
			# 	pyautogui.keyUp(self.mapping.button['C'])


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
