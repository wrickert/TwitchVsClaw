import twitch
import serial
import time
import config
import io

Xpos = 0
Ypos = 0
Zpos = 0

class SerialWrapper:
    def __init__(self, device):
        self.ser = serial.Serial(device, 115200)
        self.io = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser), newline='\n')
        Xpos = 0
        Ypos = 0
        Ypos = 0

    def sendData(self, data):
        data += "\r\n"
        self.ser.write(data.encode())

    def readline(self):
         print("before")
         return self.io.readline(1)
         print("after")

def handle_message(message: twitch.chat.Message) -> None:
   global Xpos 
   global Ypos 
   global Zpos  

   #Start with the help message
   if message.text.startswith('!help'):
      message.chat.send("Test")
      message.chat.send('@{message.user().display_name}, I have several options:')
      message.chat.send(f' !forward, !back, !left, !right - These will move the claw in the direction specified')
      message.chat.send(f' !up, !down - Move the claw up or down')
      message.chat.send(f' !grab - this will lower the claw NOTE: you get one of these per day')
      message.chat.send(f' !reject - slap the prize out of the shoot NOTE: you get one of these per day')
      message.chat.send(f'DM me with your address and I will mail you your prize')

   if message.text.startswith('!grab'):
      ser.sendData('M106')   
      time.sleep(10)
      ser.sendData('M107')   

   if message.text.startswith('!up'):
      Zpos += 10
      ser.sendData('G0 Z' + str(Zpos))

   if message.text.startswith('!down'):
      ser.sendData('G0 Z10')

   if message.text.startswith('!forward'):
      Ypos += 50
      ser.sendData('G0 Y' + str(Ypos))

   if message.text.startswith('!back'):
      Ypos -= 50
      ser.sendData('G0 Y' + str(Ypos))

   if message.text.startswith('!right'):
      Xpos += 50
      ser.sendData('G0 X' + str(Xpos))
      print(Xpos)

   if message.text.startswith('!left'):
      Xpos -= 50
      ser.sendData('G0 X' + str(Xpos))
      print(Xpos)

   if message.text.startswith('!where'):
      ser.sendData('M114')
      message.chat.send(ser.readline())

def main():
   global ser

   ser = SerialWrapper('/dev/ttyUSB0')

#   ser.sendData('G92 100 100 100')
   ser.sendData('M121')

   chat = twitch.Chat(channel='#rickertbuilds',
                       nickname='the_claw',
                       oauth=config.OAuth,
                       helix=twitch.Helix(client_id='xxxxxx', use_cache=True))


   chat.subscribe(handle_message)

   


if __name__ == '__main__':
    main()
