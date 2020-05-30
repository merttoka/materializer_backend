


## TODO:
# get list of ports for connection
# listener for succesful connection
# Readme (printrun build and lighter gcode parser)

import argparse  # parse arguments
from datetime import datetime

import msvcrt    # detect keys (windows)

from utils import *
from printer import Printer
from osc import Network

x = 0.0
y = 0.0
z = 0.0

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=12000, help="The port the OSC server is listening on")
    parser.add_argument("--listenport", type=int, default=5876, help="The port to listen on")
    parser.add_argument("--serial", default="COM4", help="The serial port that 3D Printer is using")
    args = parser.parse_args()

    # Start printer
    printer = Printer(args.serial)

    # Start OSC network
    net = Network(args.listenport, args.ip, args.port)
    net.Bind(printer)

    # main loop
    while True:
        #
        #

        # OnKeyDown
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            # escape on ESC
            if ord(ch) == 27:
                break

            if printer.IsPrinterOnline():
                if ch == b'r':
                    printer.SendAutoHome()
                    x = 0
                    y = 0
                    z = 0
                
                step = 0.5
                if ch == b'x': x += step
                if ch == b's': x -= step
                if ch == b'y': y += step
                if ch == b'h': y -= step
                if ch == b'z': z += step
                if ch == b'a': z -= step
                
                x = constrain(x, 0,220)
                y = constrain(y, 0,220)
                z = constrain(z, 0,220)
                
                PrintManager("x={}, y={}, z={}".format(x,y,z), 1)
                net.SendMessage([float(x),float(y),float(z)])

    printer.Retract()
    printer.SendAutoHome()
    printer.Destroy()