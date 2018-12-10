from websocket_server import WebsocketServer
import threading
import picamera

### Functions for reading & writing to file
### These are use for signalling to recording 
### thread to stop
def write_status(status):
	with open('status.txt', 'w') as file:
		file.write(str(status))
	file.close()

def read_status():
	y = ''
	with open('status.txt', 'r') as file:
		y = file.readline()
	file.close()
	if y == '0': # Camera should stop recording
		return False
	if y == '1': # Camera should keep recording
		return True
	else:
		print("File read error")

### Camera set up
write_status(0)
cam = picamera.PiCamera()

### Recording thread. The thread will check every 2 seconds if the 
### camera should keep recording or not
class CamThread(threading.Thread):
	def run(self):
		while read_status() == True:
			if not cam.recording:
				cam.start_recording('video.h264')
			cam.wait_recording(2)
			print("Recording...")
		if cam.recording:
			print('Stopping recording...')
			cam.stop_recording()
			print("recording stopped")

#### Setup Doppler interface
def control_1(value):
	# button, do nothing with value
	if not cam.recording:
		write_status(1)
		CamThread().start()
	if cam.recording:
		write_status(0)

def message_split(message):
	return (message.split(':')[0], int(message.split(':')[1]))

def control_dispatch(message):
	control, value = message_split(message)
	if (control == '1'):
		control_1(value)
	elif (control == '2'):
		control_2(value)
	elif (control == '3'):
		control_3(value)
	elif (control == '4'):
		control_4(value)
	elif (control == '5'):
		control_5(value)
	elif (control == '6'):
		control_6(value)
	else:
		print("Error")


## Setup webSocket server
def new_client(client, server):
	print("Client joined from: " + client['address'][0])

def message_received(client, server, message):
	control_dispatch(message)

server = WebsocketServer(8000, host='0.0.0.0')
server.set_fn_new_client(new_client)
server.message_received = message_received

server.run_forever()
