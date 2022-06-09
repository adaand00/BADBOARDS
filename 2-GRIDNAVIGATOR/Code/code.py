import rotaryio
import board

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

last_letter = 'a'

while True:
    # Get the current position of the encoder
    x = encoderX.position
    y = encoderY.position

    # constrain x and y positions
    x = min(max(x, 0), len(keymap) - 1)
    y = min(max(y, 0), len(keymap[0]) - 1)

    # get the letter at the current position
    letter = keymap[x][y]

    # if the letter has changed, print it
    if letter != last_letter:
        print(letter)
        last_letter = letter
