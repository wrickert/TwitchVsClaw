import twitch
import serial
import time
import config

class SerialWrapper:
    def __init__(self, device):
        self.ser = serial.Serial(device, 115200)

    def sendData(self, data):
        data += "\r\n"
        self.ser.write(data.encode())


def handle_message(message: twitch.chat.Message) -> None:
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
      ser.sendData('G0 Z10')

   if message.text.startswith('!down'):
      ser.sendData('G0 Z-10')

   if message.text.startswith('!forward'):
      ser.sendData('G0 Y10')

   if message.text.startswith('!back'):
      ser.sendData('G0 Y-10')

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
