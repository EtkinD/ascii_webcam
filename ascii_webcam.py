from os import get_terminal_size, system, remove, system
from PIL import Image
import cv2
import curses

# Change color of the terminal
"""
Colors codes:
0 = Black       8 = Gray
1 = Blue        9 = Light Blue
2 = Green       A = Light Green
3 = Aqua        B = Light Aqua
4 = Red         C = Light Red
5 = Purple      D = Light Purple
6 = Yellow      E = Light Yellow
7 = White       F = Bright White
"""
system('color F')

# Initialize curses
s = curses.initscr()
curses.noecho()
curses.cbreak()
s.keypad(True)
s.nodelay(True)

# Get terminal size
rows, cols = get_terminal_size()


def vid_printer(pixels, rows, columns, palette):
    """
    Prints the captured frame to the terminal.
    Clears the terminal before printing.
    """
    data = ''
    for row in range(rows):
        for column in range(columns):
            # Red, green, blue data of pixel
            red = pixels[column, row][0]
            green = pixels[column, row][1]
            blue = pixels[column, row][2]
            # Average of RGB data. This helps to determine brightness.
            brightness  = (red + green + blue) / 3
            # Brightness is converted to a character from the palette.
            data += palette[round((brightness / 255 * (len(palette) - 1)))]
    # Print the data to the terminal.
    s.clear()
    s.addstr(0, 0, data)
    s.refresh()


# Set program alive, it will be set to false when the user presses Ctrl+C to terminate program.
alive = True

# ASCII art palette from https://www.youtube.com/watch?v=55iwMYv8tGI
# Added a couple of characters, original one is commented below.
# colors = ' _.,-=+;:cba!?0123456789$W#@Ñ'
colors = '  ¨_.,-=+;:cbøaåπ!?∆©0123456789ß$W#@¥Ñ'

if __name__ == '__main__':
    # Define a video capture object
    vid = cv2.VideoCapture(0)

    q = -1
    # Capturing frame by frame from webcam
    while q < 0:
        # Capture frame
        ret, img = vid.read()
        if not ret:
            continue
        
        # Belowe code is the only solution that I found to get size of captured image.
        # It's very expensive, but it works currently.
        # Captured image is written to a file, then read from it. This process is for getting size of image and resizing it.

        # Write captured image to a file
        cv2.imwrite(filename='img.png', img=img)
        # Read from file
        image = Image.open(fp='img.png')
        # Resize image to fit terminal.
        image = image.resize((rows, cols-1))
        # Convert image to RGB array
        pxls = image.load()
        # Render image to terminal
        vid_printer(pxls, image.size[1], image.size[0], colors)
        # If user press any key, terminate program.
        q = s.getch()
    # while terminating, release the webcam
    vid.release()
    # Remove temporary file
    remove('img.png')
    # Clean up curses
    s.clear()
    s.refresh()
    # Terminate curses
    curses.nocbreak()
    s.keypad(False)
    curses.echo()
    curses.endwin()

    exit(0)
