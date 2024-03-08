"""!
@file main.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2.
    
    The original file has been modified to run a cooperative multitasking program. Task 1 rotates a the robot 180˚,
    task 2 pulls the trigger on the turret, and task 3 operates the camera. 
"""

import gc
import pyb
import cotask
import task_share
import encoder_reader
import MotorDriver
import closed_loop
import mlx_cam
import utime as time
from machine import Pin, I2C
from mlx90640 import MLX90640
from mlx90640.calibration import NUM_ROWS, NUM_COLS, IMAGE_SIZE, TEMP_K
from mlx90640.image import ChessPattern, InterleavedPattern


def task1_fun(shares):
    """!
    Task which operates the panning motor
    @param shares A list holding the share and queue used by this task
    """
    # Get references to the share and queue which have been passed to this task
    enc1 = encoder_reader.Encoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7, pyb.Timer(8, prescaler=0, period=65535))
    moe1 = MotorDriver.MotorDriver(pyb.Pin.board.PC1, pyb.Pin.board.PA0, pyb.Pin.board.PA1, pyb.Timer(5, freq=20000))
    moe1.set_duty_cycle(0)
    enc1.zero()
    close1 = closed_loop.ClosedLoop(0, .5)
    output1 = 0

    while(output1 != "End"):
        output1 = close1.run(512, enc1.read())
        moe1.set_duty_cycle(output1)

        yield 0
    #close1.print_values()

    while(ready_to_fire.get() != 1):
        enc1.zero()
        output1 = 0
        target = target_share.get() - 17
        while(output1 != "End"):
            output1 = close1.run(target, enc1.read())
            moe1.set_duty_cycle(output1)

            yield 0
    
    while True:
        yield

    
    the_share, the_queue = shares

#     while True:
#         # Show everything currently in the queue and the value in the share
#         print(f"Share: {the_share.get ()}, Queue: ", end='')
#         while q0.any():
#             print(f"{the_queue.get ()} ", end='')
#         print('')
# 
#         yield 0

def task2_fun(shares):
    """!
    Task which waits five seconds then fires
    @param shares A tuple of a share and queue from which this task gets data
    """
    # Get references to the share and queue which have been passed to this task
    
    start_time = time.ticks_ms()
    
    while(time.ticks_diff(time.ticks_ms(), begintime) < 5500):
        yield
    
    ready_to_fire.put(1)
    
    while(time.ticks_diff(time.ticks_ms(), begintime) < 500):
        yield
    print(f"Fire")
    
    while True:
        yield
#     enc2 = encoder_reader.Encoder(pyb.Pin.board.PB6, pyb.Pin.board.PB7, pyb.Timer(4, prescaler=0, period=65535))
#     moe2 = MotorDriver.MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4, pyb.Pin.board.PB5, pyb.Timer(3, freq=20000))
#     moe2.set_duty_cycle(0)
#     enc2.zero()
#     close2 = closed_loop.ClosedLoop(0, .5)
#     output2 = 0
# 
#     while(output2 != "End"):
#         output2 = close2.run(2048, enc2.read())
#         moe2.set_duty_cycle(output2)
#         
#         yield 0
#     close2.print_values()
#     doneShare2.put(1)
#     while (doneShare1.get() != 1):
#         yield 0
#     print("Done")
    
#     the_share, the_queue = shares
# #    doneShare2.put(1)
#     while True:
#         # Show everything currently in the queue and the value in the share
# #         print(f"Share: {the_share.get ()}, Queue: ", end='')
# #         while q0.any():
# #             print(f"{the_queue.get ()} ", end='')
# #         print('')

#         yield 0

def task3_fun(shares):
    """!
    Task which puts things into a share and a queue.
    @param shares A list holding the share and queue used by this task
    """
    # Get references to the share and queue which have been passed to this task
    i2c_bus = I2C(1)
    i2c_address = 0x33
    camera = mlx_cam.MLX_Cam(i2c_bus)
    camera._camera.refresh_rate = 10.0
    
    while True:
        image = None
        while not image:
            image = camera.get_image_nonblocking()
            yield 0
    
        target = camera.get_target(image, limits=(0, 99))
        target_share.put(target)
        yield 0
    

# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")

    # Create a share and a queue to test function and diagnostic printouts
    share0 = task_share.Share('h', thread_protect=False, name="Share 0")
    q0 = task_share.Queue('L', 16, thread_protect=False, overwrite=False,
                          name="Queue 0")
    doneShare1 = task_share.Share('B', thread_protect=False, name="Done Share 1")
    doneShare2 = task_share.Share('B', thread_protect=False, name="Done Share 2")
    doneShare1.put(0)
    doneShare2.put(0)
    target_share = task_share.Share('B', thread_protect=False, name="Target")
    ready_to_fire = task_share.Share('B', thread_protect=False, name="Ready to fire")
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(task1_fun, name="Task_1", priority=1, period=100,
                        profile=True, trace=False, shares=(share0, q0))
    task2 = cotask.Task(task2_fun, name="Task_2", priority=2, period=70,
                        profile=True, trace=False, shares=(share0, q0))
    task3 = cotask.Task(task3_fun, name="Task_3", priority=3, period=120,
                        profile=True, trace=False, shares=(share0, q0))
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    cotask.task_list.append(task3)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break

    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(task1.get_trace())
    print('')

