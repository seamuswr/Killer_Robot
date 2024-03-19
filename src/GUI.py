"""!
@file lab0example.py
Run real or simulated dynamic response tests and plot the results. This program
demonstrates a way to make a simple GUI with a plot in it. It uses Tkinter, an
old-fashioned and ugly but useful GUI library which is included in Python by
default.

This file is based loosely on an example found at
https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html

@author Spluttflob
@date   2023-12-24 Original program, based on example from above listed source
@copyright (c) 2023 by Spluttflob and released under the GNU Public Licenes V3
"""

import time
import math
import tkinter
from random import random
from serial import Serial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
KP = "0"


def KP_input():
    global KP
    KP = input("Enter KP: ")


def plot_example(plot_axes, plot_canvas, xlabel, ylabel):
    """!
    Make an example plot to show a simple(ish) way to embed a plot into a GUI.
    The data is just a nonsense simulation of a diving board from which a
    typically energetic otter has just jumped.
    @param plot_axes The plot axes supplied by Matplotlib
    @param plot_canvas The plot canvas, also supplied by Matplotlib
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    """
    # Here we create some fake data. It is put into an X-axis list (times) and
    # a Y-axis list (boing). Real test data will be read through the USB-serial
    # port and processed to make two lists like these
    ser = Serial('/dev/tty.usbmodem204F377739472')
#     # Seamus's serial /dev/tty.usbmodem204F377739472
#     # Paul's serial /dev/tty.usbmodem204F377739472
    ser.write(b'\x02')
    ser.write(b'\x04')
    # Wait for MCU to response back
    # while not ser.inWaiting():
    #     pass
    # time.sleep(0.1)
    # temp = KP.encode('utf-8')
    # ser.write(temp)
    
    time_data = []
    voltage_data = []
    while not ser.inWaiting():
        pass
    line = ser.readline().decode('utf-8').rstrip().split(",", 1)
    while line[0] != "Done":
        try:
            float(line[0])
            float(line[1])
        except (ValueError, IndexError):
            print("Exception: bad data")
        else:
            time_data.append(float(line[0]))
            voltage_data.append(float(line[1]))
        finally:
            line = ser.readline().decode('utf-8').rstrip().split(",", 1)

    # Draw the plot. Of course, the axes must be labeled. A grid is optional
    plot_axes.plot(time_data, voltage_data)
    plot_axes.set_xlabel(xlabel)
    plot_axes.set_ylabel(ylabel)
    plot_axes.grid(True)
    plot_canvas.draw()
    ser.close()


def tk_matplot(plot_function, input_fun, xlabel, ylabel, title):
    """!
    Create a TK window with one embedded Matplotlib plot.
    This function makes the window, displays it, and runs the user interface
    until the user closes the window. The plot function, which must have been
    supplied by the user, should draw the plot on the supplied plot axes and
    call the draw() function belonging to the plot canvas to show the plot. 
    @param plot_function The function which, when run, creates a plot
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    @param title A title for the plot; it shows up in window title bar
    """
    # Create the main program window and give it a title
    tk_root = tkinter.Tk()
    tk_root.wm_title(title)

    # Create a Matplotlib 
    fig = Figure()
    axes = fig.add_subplot()

    # Create the drawing canvas and a handy plot navigation toolbar
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()

    # Create the buttons that run tests, clear the screen, and exit the program
    button_quit = tkinter.Button(master=tk_root,
                                 text="Quit",
                                 command=tk_root.destroy)
    button_clear = tkinter.Button(master=tk_root,
                                  text="Clear",
                                  command=lambda: axes.clear() or canvas.draw())
    button_run = tkinter.Button(master=tk_root,
                                text="Run Test",
                                command=lambda: plot_function(axes, canvas,
                                                              xlabel, ylabel))
    button_KP = tkinter.Button(master=tk_root, text="KP",
                               command=lambda: input_fun())

    # Arrange things in a grid because "pack" is weird
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=4)
    toolbar.grid(row=1, column=0, columnspan=4)
    button_run.grid(row=2, column=0)
    button_clear.grid(row=2, column=1)
    button_quit.grid(row=2, column=3)
    button_KP.grid(row=2, column=2)

    # This function runs the program until the user decides to quit
    tkinter.mainloop()


# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program
if __name__ == "__main__":
#     ser = Serial('/dev/tty.usbmodem204F377739472')
#      # Seamus's serial /dev/tty.usbmodem204F377739472
#      # Paul's serial /dev/tty.usbmodem204F377739472
#     ser.write(b'\x02')
#     ser.write(b'\x04')
    
    tk_matplot(plot_example, KP_input, 
               xlabel="Time (ms)",
               ylabel="Position",
               title="Step Response")
    
    #ser.close()