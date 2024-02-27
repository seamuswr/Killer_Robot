"""!
@file motor_driver.py
This file contains a class for controlling a motor driver.

@Author ME405 team 8
@date 20-Feb-2024
"""

from pyb import Pin, Timer
import time


class MotorDriver:
    """!
    Class for controlling a motor driver.

    This class provides methods to control a motor driver, including setting the duty cycle
    for motor control.
    """

    def __init__(self, en_pin, IN1A_pin, IN2A_pin, PWM_tim):
        """!
        Creates a motor driver by initializing GPIO pins and turning off the motor for safety.

        @param en_pin: Pin connected to the enable pin of the motor driver.
        @param IN1A_pin: Pin connected to IN1A of the motor driver.
        @param IN2A_pin: Pin connected to IN2A of the motor driver.
        @param PWM_tim: Timer used for PWM control.
        """
        self.EN = Pin(en_pin, Pin.OUT_OD, Pin.PULL_UP)
        self.IN1A = Pin(IN1A_pin, Pin.OUT_PP)
        self.IN2A = Pin(IN2A_pin, Pin.OUT_PP)

        self.tim = PWM_tim

        self.PWM1 = self.tim.channel(1, mode=Timer.PWM, pin=self.IN1A)  # Initialize PWM channel 1
        self.PWM2 = self.tim.channel(2, mode=Timer.PWM, pin=self.IN2A)  # Initialize PWM channel 2

        self.EN.value(0)

    def set_duty_cycle(self, duty):
        """!
        Sets the duty cycle to be sent to the motor.

        Positive values cause torque in one direction, negative values in the opposite direction.

        @param duty: A signed integer holding the duty cycle of the voltage sent to the motor.
        """
        try:
            int(duty)
        except (ValueError, IndexError):
            self.PWM1.pulse_width_percent(0)
            self.PWM2.pulse_width_percent(0)
            print("Invalid duty cycle")
        else:
            if duty > 0:
                if duty > 100:
                    self.PWM1.pulse_width_percent(100)
                else:
                    self.PWM1.pulse_width_percent(duty)  # Set duty cycle for forward motion
                self.PWM2.pulse_width_percent(0)
            elif duty < 0:
                if duty < -100:
                    self.PWM2.pulse_width_percent(100)
                else:
                    self.PWM2.pulse_width_percent((-1) * duty)  # Set duty cycle for backward motion
                self.PWM1.pulse_width_percent(0)
            else:
                self.PWM1.pulse_width_percent(0)
                self.PWM2.pulse_width_percent(0)
            self.EN.value(1)


if __name__ == '__main__':
    """!
    Entry point of the script.
    """

    # Initialize motor object
    moe = MotorDriver(pyb.Pin.board.PC1, pyb.Pin.board.PA0, pyb.Pin.board.PA1, pyb.Timer(5, freq=20000))

    # Test the motor control
    moe.set_duty_cycle(-42)
    time.sleep(4)
    moe.set_duty_cycle(73)
    time.sleep(4)
    moe.set_duty_cycle(0)
    time.sleep(4)
    moe.set_duty_cycle(-150)
    time.sleep(4)
    moe.set_duty_cycle(150)
    time.sleep(4)
    moe.set_duty_cycle(0)
