ME 405 Term Project - The Glue Boys -
Autonomous Nerf Launcher with Target Lock On

This final project for our Cal Poly Mechatronics class combined a cooperatively multitasking software base with 
a robust mechanical system. The robot was tasked with autonomosly dueling another team. A few special rules include 
the target freezing after 5 seconds, 3 points for first team to hit, 1 point for the second team to hit, and -1 points
for a miss. With some refinement the device is best suited for keeping younger siblings out of certain areas. 

The hardware for this project consisted of a strongarm nerf launcher attained from class, two brushed dc motors and 
corresponding encoders, an Mlx90640 thermal camera, and an Nucleo-64 board with a motor driver and Shoe of Brian.
The 3D printed parts of the robot consisted of a nerf gun clamp, a gear train with a 1:1.6 speed reduction, mounting 
brackets for the motors, and a trigger. Components were attached to a plywood base. An emergency stop switch was wired
into the main motor power lines. 

<img width="1107" alt="Screenshot 2024-02-26 at 7 25 35 PM" src="https://github.com/seamuswr/Killer_Robot/assets/108034107/896ef53d-fcdc-4a2a-aefe-6c54da7810a9">
CAD rendering of the 3D printed gun clamp

The software consisted of a main program with 3 tasks: Motor panning, trigger actuation, and thermal image capture. The tasks 
work cooperatively to pan 180˚, wait 5 seconds, take a picture and calculate the hottest spot, pan to that spot, and fire.
More documentation can be found here: file:///Users/seamus/Desktop/ME405/ME405_KillerRobot/docs/index.html

The software was tested incrementally, first adjusting the controller gains and setpoint on the panning motor, then adding 
the thermal camera and adjusting the panning response to the hottest column of the thermal image, then adjusting the trigger
motor. Finally, simulated duels were used to test and refine the complete system. The system performed relatively well during 
these tests, but there was significant variability in the hotspot calculation. A majority of the testing was done to 
adjust the panning response to hottest location calculated by the camera task. 

The mechanical side of the project performed better than expected. Minimizing cost was deamed a priority for the project
which resulted in suboptimal materials. However, the 3D printed structure held up well and provided sufficient strength 
and stiffness. The software was also very reliable. The robot consistently spun 180˚, adjusted its position, and fired a 
projectile at the right time. The issues came from either the thermal camera reading a hot spot that was not the target or 
the motor not being able to acurately pan. The camera issues can be improved by narrowing the scope of the camera so 
it is less affected by noise at the edges of the image. The motor panning can be improved be implementing a more 
advanced control system than just proportinal control such as adding integral or derivative control. This can also be 
improved by shedding weight on the robot and using a more powerful panning motor.



Doxygen Main page

- summary of the software
- purpose of each files
- discussion of tasks and states  (multitasking)
