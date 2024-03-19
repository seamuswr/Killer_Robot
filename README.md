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


Overview of the Software design
-Doxygen Link

Result
Testing and Performance

What went well and what did not?

Doxygen Main page

- summary of the software
- purpose of each files
- discussion of tasks and states  (multitasking)
