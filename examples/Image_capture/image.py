from websocket_server import WebsocketServer
import picamera

## See https://picamera.readthedocs.io/en/release-1.13/recipes1.html
cam = picamera.PiCamera()

###################################
## Edit this code to do what you wish
def control_1(value):
	print("Recieved data from control 1: " + str(value))
	cam.capture('image.jpg')
	pass

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

#### Server setup
def message_received(client, server, message):
	control_dispatch(message)

def new_client(client, server):
	print("Client joined")

server = WebsocketServer(8000, host='0.0.0.0')
server.set_fn_new_client(new_client)

server.message_received = message_received

server.run_forever()
