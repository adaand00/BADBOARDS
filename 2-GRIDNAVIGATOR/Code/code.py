import rotaryio
import board
import usb_hid
import digitalio
import time
from adafruit_hid.mouse import Mouse

mouse = Mouse(usb_hid.devices)

# set pin 5 as input pullup (right click)
right_click = digitalio.DigitalInOut(board.D5)
right_click.direction = digitalio.Direction.INPUT
right_click.pull = digitalio.Pull.UP

# set pin 4 as input pullup (left click)
left_click = digitalio.DigitalInOut(board.D4)
left_click.direction = digitalio.Direction.INPUT
left_click.pull = digitalio.Pull.UP

# mode switch on pin D7
mode_sw = digitalio.DigitalInOut(board.D7)
mode_sw.direction = digitalio.Direction.INPUT


keymap = [
    ['a', 'b', 'c', 'd', 'e'],
    ['f', 'g', 'h', 'i', 'j'],
    ['k', 'l', 'm', 'n', 'o'],
    ['p', 'q', 'r', 's', 't'],
    ['u', 'v', 'w', 'x', 'y'],
    ['z', '1', '2', '3', '4'],
    ['5', '6', '7', '8', '9']
]

encoderX = rotaryio.IncrementalEncoder(board.D0, board.D1)
encoderY = rotaryio.IncrementalEncoder(board.D2, board.D3)

lastEncoderX = 0
lastEncoderY = 0

x = 0
y = 0

last_letter = 'a'

mode = mode_sw.value

while True:
    if mode == 0:
        if right_click.value == 0:
            mouse.click(mouse.RIGHT_BUTTON)
            time.sleep(0.2)

        if left_click.value == 0:
            mouse.click(mouse.LEFT_BUTTON)
            time.sleep(0.2)

        if encoderX.position != lastEncoderX:
            mouse.move(x=(encoderX.position - lastEncoderX)*10)
            lastEncoderX = encoderX.position

        if encoderY.position != lastEncoderY:
            mouse.move(y=(encoderY.position - lastEncoderY)*10)
            lastEncoderY = encoderY.position

    else:
        # Get the current position of the encoder
        x += encoderX.position - lastEncoderX
        y += encoderY.position - lastEncoderY

        # Update the last position
        lastEncoderX = encoderX.position
        lastEncoderY = encoderY.position

        # constrain x and y positions
        x = min(max(x, 0), len(keymap) - 1)
        y = min(max(y, 0), len(keymap[0]) - 1)

        # get the letter at the current position
        letter = keymap[x][y]

        # if the letter has changed, print it
        if letter != last_letter:
            print(letter)
            last_letter = letter

    mode = mode_sw.value
