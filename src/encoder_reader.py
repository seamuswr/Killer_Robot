"""!
@file encoder_interface.py
This file contains code for interfacing with an encoder.

@authorME405 team 8
@date 20-Feb-2024
"""

import pyb
import time


class Encoder:
    """!
    Class to interface with an encoder.

    This class provides methods to interact with an encoder and read its position.
    """

    def __init__(self, enc1_pin, enc2_pin, timer):
        """!
        Initializes the Encoder instance.

        @param enc1_pin: Pin for encoder channel 1.
        @param enc2_pin: Pin for encoder channel 2.
        @param timer: Timer object for the encoder.
        """
        self.tim = timer
        self.enc1 = self.tim.channel(1, mode=pyb.Timer.ENC_AB, pin=enc1_pin)
        self.enc2 = self.tim.channel(2, mode=pyb.Timer.ENC_AB, pin=enc2_pin)
        self.position = 0
        self.last = self.position

    def read(self):
        """!
        Reads the encoder position and prints it.

        @return: the position
        """
        temp = self.tim.counter() - self.last
        if temp > 32767:
            temp -= 65535
        elif temp < -32767:
            temp += 65535
        self.last = self.tim.counter()
        self.position += temp
        return self.position // 16

    def zero(self):
        """!
        Resets the encoder position to zero.

        @return: None
        """
        self.position = 0


if __name__ == '__main__':
    """!
    Entry point of the script.
    """

    # Initialize encoder object
    enc1 = Encoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7, pyb.Timer(8, prescaler=0, period=65535))
    enc2 = Encoder(pyb.Pin.board.PB6, pyb.Pin.board.PB7, pyb.Timer(4, prescaler=0, period=65535))

    # Main loop to continuously read and print encoder position
    while (True):
        print(enc2.read())
        time.sleep(.1)
