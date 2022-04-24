import time
import board
from digitalio import DigitalInOut, Direction, Pull
from adafruit_hid.keyboard import Keyboard
from keyboard_layout_win_sw import KeyboardLayout
import usb_hid
import neopixel


pixels = neopixel.NeoPixel(board.D8, 8, brightness=0.3)

pixels.fill((0, 0, 0))
pixels.show()

enterkey = 0

lastkey = "00000000"
newkey = True

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

    for i in range(8):
        if not dios[i].value:
            pixels[i] = (255, 0, 0)
        else:
            pixels[i] = (0, 0, 0) 
    
    # Save keys pressed in string (example "01000001")
    stri = ""
    for dio in dios:
        stri += str(int(not dio.value))

    # If key pressed is different from last key pressed, send key
    stri = stri[:enterkey] + stri[enterkey+1:]
    if stri != lastkey and int(stri, 2) != 8: 
        lastkey = stri 
        
        # remove letter
        if not newkey:
            layout.write(chr(8))

        # send key
        try:
            layout.write(chr(int(stri, 2)))
            newkey = False
        except ValueError:
            newkey = True
            continue  

    # Enter key pressed: advance to next key
    if not dios[enterkey].value:
        if stri == "0001000":
            layout.write(chr(8))
        newkey = True
        lastkey = "00000000"
        pixels[enterkey] = (0, 255, 0)
        time.sleep(0.2)

    time.sleep(0.01)
