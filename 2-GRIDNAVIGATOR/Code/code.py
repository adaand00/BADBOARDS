import rotaryio
import board
import usb_hid
import digitalio
import time
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from keyboard_layout_win_sw import KeyboardLayout 
import neopixel

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

pixels = neopixel.NeoPixel(board.D6, 2, brightness=0.15)

layer1 = [['a', 'b', 'c', 'd', 'e', 'f', 'g'],
    ['h', 'i', 'j', 'k', 'l', 'm', 'n'],
    ['o', 'p', 'q', 'r', 's', 't', 'u'],
    ['v', 'w', 'x', 'y', 'z', 'å', 'ä'],
    ['ö', ' ', '[<-]', '[ENTER]', '[TAB]', 'é', 'ü']
]

layer2 = [['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    ['H', 'I', 'J', 'K', 'L', 'M', 'N'], 
    ['O', 'P', 'Q', 'R', 'S', 'T', 'U'], 
    ['V', 'W', 'X', 'Y', 'Z', 'Å', 'Ä'], 
    ['Ö', ' ', '[<-]', '[ENTER]', '[TAB]', 'É', 'Ü']
]

layer3 = [['1', '2', '3', '4', '5', '6', '7', '8'],
    ['9', '0', '!', '@', '#', '$', '%', '^'],
    ['&', '*', '(', ')', '_', '+', '-', '='],
    ['[', ']', '\\', '{', '\\', '}', '|', ';'],
    ["'", ':', ',', '.', '/', '<', '>', '?'],
    ['`', '~', '"', '\\', ' ', '[<-]', '[ENTER]', '[TAB]']
]

layers = [layer1, layer2, layer3]

specials = {'[<-]': '\x08', '[ENTER]': '\x0A', '[TAB]': '\x09'}

Speeds = [10, 25, 50, 100]
Speedcolors = [(255, 0, 0), (130, 130, 0), (0, 255,0), (0, 0, 255)]

encoderX = rotaryio.IncrementalEncoder(board.D0, board.D1)
encoderY = rotaryio.IncrementalEncoder(board.D2, board.D3)

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayout(kbd)

lastEncoderX = 0
lastEncoderY = 0

lastLeft = 1
lastRight = 1

mouseSpeed = 0

currentlayer = 0

x = 0
y = 0

last_letter = 'a'

mode = mode_sw.value

while True:
    if mode == 0:
        if left_click.value == 0 and right_click.value == 0:
            mouseSpeed = (mouseSpeed + 1) % len(Speeds)
            # set colors to 
            pixels[0] = Speedcolors[mouseSpeed]
            pixels[1] = Speedcolors[mouseSpeed]
            time.sleep(0.3)
            pixels[0] = (0, 0, 0)
            pixels[1] = (0, 0, 0)
        
        elif right_click.value != lastRight:
            if right_click.value == 0:
                mouse.press(mouse.RIGHT_BUTTON)
            else:
                mouse.release(mouse.RIGHT_BUTTON)
            
            lastRight = right_click.value


        elif left_click.value != lastLeft:
            if left_click.value == 0:
                mouse.press(mouse.LEFT_BUTTON)
            else:
                mouse.release(mouse.LEFT_BUTTON)
            
            lastLeft = left_click.value

        

        if encoderX.position != lastEncoderX:
            mouse.move(x=-(encoderX.position - lastEncoderX)*Speeds[mouseSpeed])
            lastEncoderX = encoderX.position

        if encoderY.position != lastEncoderY:
            mouse.move(y=-(encoderY.position - lastEncoderY)*Speeds[mouseSpeed])
            lastEncoderY = encoderY.position

    else:
        # Get the current position of the encoder
        y -= encoderX.position - lastEncoderX
        x -= encoderY.position - lastEncoderY

        # Update the last position
        lastEncoderX = encoderX.position
        lastEncoderY = encoderY.position

        # constrain x and y positions
        x = min(max(x, 0), len(layers[currentlayer]) - 1)
        y = min(max(y, 0), len(layers[currentlayer][0]) - 1)

        # get the letter at the current position
        letter = layers[currentlayer][x][y]

        # if the letter has changed, print it
        if letter != last_letter:
            layout.write(chr(8)*len(last_letter))
            layout.write(letter)
            print(letter)
            last_letter = letter

        if left_click.value == 0 and lastLeft == 1:
            if letter in ['[<-]', '[ENTER]', '[TAB]']:
                layout.write(chr(8)*len(last_letter))
                layout.write(specials[letter])

            layout.write(letter)
            lastLeft = 0
        elif left_click.value == 1:
            lastLeft = 1

        if right_click.value == 0 and lastRight == 1:
            currentlayer = (currentlayer + 1) % len(layers)
            lastRight = 0
        elif right_click.value == 1:
            lastRight = 1
    mode = mode_sw.value 