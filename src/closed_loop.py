"""!
@file closed_loop_controller.py
This file contains code for a closed-loop control system.

@Author ME405 team 8
@date 20-Feb-2024
"""

import cqueue
import utime
import encoder_reader
import MotorDriver


class ClosedLoop:
    """!
    Represents a closed-loop control system.
    This class implements a closed-loop control system with proportional control.
    """

    def __init__(self, setpoint, Kp, Ki):
        """!
        Initializes the ClosedLoop object with setpoint and proportional gain.

        @param setpoint (float): The desired value for the system to achieve.
        @param Kp (float): The proportional gain of the controller.
        """
        self.setpoint = setpoint
        self.Kp = Kp
        self.Ki = Ki
        self.i_integral = 0
        self.measured_output = 0
        self.prev_time = 0
        self.time_queue = cqueue.IntQueue(30)
        self.pos_queue = cqueue.IntQueue(30)
        self.start_time = utime.ticks_ms()

    def run(self, setpoint, measured_output):
        """!
        Runs one iteration of the closed-loop control system.

        This method calculates the actuation value based on the current setpoint
        and measured output, and updates internal data structures with timestamps
        and measured positions.

        @param setpoint (float): The desired value for the system to achieve.
        @param measured_output (float): The current measured output of the system.

        @returns float or str: The actuation value if the queue is not full, otherwise "End".
        """
        self.setpoint = setpoint
        self.measured_output = measured_output
        error = self.measured_output - self.setpoint
        self.i_integral += error*(utime.ticks_ms() - self.prev_time)/100
        self.prev_time = utime.ticks_ms()
        actuation_value = int(self.Kp * error + self.Ki * self.i_integral)     
        if not self.time_queue.full():
            self.time_queue.put(utime.ticks_ms() - self.start_time)
            self.pos_queue.put(self.measured_output)
        else:
            return "End"
        return actuation_value

    def set_setpoint(self, setpoint):
        """!
        Sets a new setpoint for the control system.

        @param setpoint (float): The new desired value for the system to achieve.
        """
        self.setpoint = setpoint

    def set_Kp(self, Kp):
        """!
        Sets a new proportional gain for the controller.

        @param Kp (float): The new proportional gain value.
        """
        self.Kp = Kp

    def print_values(self):
        """!
        Prints the stored timestamps and measured positions.

        This method prints the contents of the time and position queues.
        """
        for idx in range(self.time_queue.max_full()):
            print(f'{self.time_queue.get()}, {self.pos_queue.get()}')
        print('END')


if __name__ == '__main__':
    """
    Entry point of the script.
    """

    # Initialize encoder and motor objects
    enc1 = encoder_reader.Encoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7, pyb.Timer(8, prescaler=0, period=65535))
    moe1 = MotorDriver.MotorDriver(pyb.Pin.board.PC1, pyb.Pin.board.PA0, pyb.Pin.board.PA1, pyb.Timer(5, freq=20000))
    enc2 = encoder_reader.Encoder(pyb.Pin.board.PB6, pyb.Pin.board.PB7, pyb.Timer(4, prescaler=0, period=65535))
    moe2 = MotorDriver.MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4, pyb.Pin.board.PB5, pyb.Timer(3, freq=20000))
    enc1.zero()
    enc2.zero()
    
    # Initialize closed-loop control object
    close1 = ClosedLoop(0, .2, 0)
    close2 = ClosedLoop(0, .8, 0)
    #utime.sleep(1)
    # Main control loop
    while True:
        
        #output1 = close1.run(-800, enc1.read())
        #moe1.set_duty_cycle(output1)
        output2 = close2.run(-100, enc2.read())
        moe2.set_duty_cycle(output2)
        utime.sleep(.1)
