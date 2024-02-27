"""!
@file main.py
This file runs the control system on the microcontroller

@Author ME405 team 8
@date 20-Feb-2024
"""


import utime
import encoder_reader
import MotorDriver
import closed_loop
import pyb

enc = encoder_reader.Encoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7, pyb.Timer(8, prescaler=0, period=65535))
moe = MotorDriver.MotorDriver(pyb.Pin.board.PC1, pyb.Pin.board.PA0, pyb.Pin.board.PA1, pyb.Timer(5, freq=20000))
data = pyb.USB_VCP()

while(True):
    try:
        while not data.any():
            print(1)
            pass
        temp = data.read(4).decode('utf-8')
        #temp = "0.5\n"
#        temp = temp.decode('utf-8')
        Kp = float(temp)
    except (ValueError, IndexError):
        print("Invalid Kp")
    else:
        enc.zero()
        close = closed_loop.closed_loop(0, Kp)
        output = close.run(1024, enc.read())

        while(output != "End"):
            output = close.run(1024, enc.read())
            moe.set_duty_cycle(output)
            utime.sleep_ms(10)

        close.print_values()
                
