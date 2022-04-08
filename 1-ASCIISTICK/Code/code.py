import time
#from turtle import delay
import board
from digitalio import DigitalInOut, Direction, Pull
from adafruit_hid.keyboard import Keyboard
from keyboard_layout_win_sw import KeyboardLayout
import usb_hid

enterkey = 0

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayout(kbd)

pins = [board.D0, board.D1, board.D2, board.D3, board.D4, board.D5, board.D6, board.D7]
dios = []

for pin in pins:
    dio = DigitalInOut(pin)
    dio.direction = Direction.INPUT
    dio.pull = Pull.UP
    dios.append(dio)


while True:

    # time.sleep(1)
    # led.value = True
    # time.sleep(0.1)
    # led.value = False
    # print("blink")


    if not dios[enterkey].value:
        led.value = False

        stri = ""
        for dio in dios:
            stri += str(int(not dio.value))

        stri = stri[:enterkey] + stri[enterkey+1:] 

        try:
            layout.write(chr(int(stri, 2)))
            time.sleep(0.5)
        except ValueError:
            print(chr(int(stri, 2)))
            print("NULL")
        # print(chr(int(stri, 2)))

    else:
        led.value = True

    time.sleep(0.01)