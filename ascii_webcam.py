from os import get_terminal_size, system, remove
from PIL import Image
import cv2
import signal


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
        data += '\n'
    # Clear the terminal before printing.
    system('cls')
    print(data)


def signal_handler(*args):
    """
     Signal handler that terminates the program.
    """
    global alive
    alive = False


# Set program alive, it will be set to false when the user presses Ctrl+C to terminate program.
alive = True

# ASCII art palette from https://www.youtube.com/watch?v=55iwMYv8tGI
# Added a couple of characters, original one is commented below.
# colors = ' _.,-=+;:cba!?0123456789$W#@Ñ'
colors = '  ¨_.,-=+;:cbøaåπ!?∆©0123456789ß$W#@¥Ñ'

if __name__ == '__main__':
    # Define a video capture object
    vid = cv2.VideoCapture(0)

    # Initialize ctrl+c signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Capturing frame by frame from webcam
    while alive:
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
        image = image.resize((get_terminal_size().columns, get_terminal_size().lines))
        # Convert image to RGB array
        pxls = image.load()
        # Render image to terminal
        vid_printer(pxls, image.size[1], image.size[0], colors)
    # while terminating, release the webcam
    vid.release()
    # Remove temporary file
    remove('img.png')

    exit(0)
