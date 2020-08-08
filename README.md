
Joule is a free open-source high-performance G-code interpreter and
CNC/3D-printer controller. It can run on a variety of Linux-powered ARM-based
boards, such as Raspberry Pi, Odroid, Beaglebone and others. This gives you a
flexibility to pick a board you are most familiar with, and use everything
Linux has to offer, while keeping all your G-code runtime on the same board
without a need to have a separate microcontroller for real-time operation.
Our choice of Python as main programming language significantly reduces code
base compared to C/C++ projects, reduces boilerplate and microcontroller-specific
code, and makes the project accessible to a broader audience to tinker with.

# Realtime Motor Control in Linux?
Typically there is no way to control stepper motors from Linux runtime
environment due to the lack of real time GPIO control. Even kernel based
modules can not guarantee precise control of pulses for steppers.
However, we can use a separate hardware module, DMA (Direct Memory Access)
which provides high precision for GPIO outputs. This module can copy bytes which
represent GPIO states from RAM buffer directly to GPIO with some clock based
on main chip internal oscillator without using CPU's cores. Using such approach
this project generates impulses for moving stepper motors and that is very
precise way regardless CPU load and OS time jitter.  
This approach also allows to use Python language for this project. Typically,
Python is not good choice for real time application, but since project just
needs to set up DMA buffers and hardware will do the rest, Python become the
perfect choice for easy development of this project.

# Current gcode and features support
* Commands G0, G1, G2, G3, G4, G17, G18, G19, G20, G21, G28, G53, G90, G91, G92,
M2, M3, M5, M30, M84, M104, M105, M106, M107, M109, M114, M140, M190 are
supported. Commands can be easily added, see [gmachine.py](./cnc/gmachine.py)
file.
* Four axis are supported - X, Y, Z, E.
* Circular interpolation for XY, ZX, YZ planes is supported.
* Spindle with rpm control is supported.
* Hardware watchdog.

# Watchdog
Joule uses one of DMA channels as hardware watchdog for safety purpose. If
board, OS or Joule hangs this watchdog should disable all GPIO pins(by
switching them into input state, for RPi this would be GPIO0-29) in 15 seconds.
Since there is a high current and dangerous devices like heated bed, extruder
heater, this feature should prevent uncontrollable overheating. But don't count
on such software features too much, they can hang too or output MOSFET become
shorted, use hardware protection like thermal cutoff switches in your machines.

# Hardware
Currently, this project supports Raspberry Pi 1-3. Developed and tested with
RPI3. And there is a way to add new boards. See [hal.py](./cnc/hal.py) file.  
_Note: Current Raspberry Pi implementation uses the same resources as on board
3.5 mm jack(PWM module), so do not use it. HDMI audio works._

# Config
All configs are stored in [config.py](./cnc/config.py) and contain hardware
properties, limitations and pin names for hardware control.  
Raspberry Pi implementation should be connected to A4988, DRV8825 or any other
stepper motor drivers with DIR and STEP pin inputs.
Default config is created for Raspberry Pi 2-3 and this wiring config:


# Usage
Just clone this repo and run `./Joule` from repo root. It will start in
interactive terminal mode where gcode commands can be entered manually.  
To run file with gcode commands, just run `./Joule filename`.  
Optionally, `Joule` can be installed. Run
```bash
sudo pip install .
```
in repo root directory to install it. After than, `Joule` command will be added
to system path. To remove installation, just run:
```bash
sudo pip remove Joule
```

# Performance notice
Pure Python interpreter would not provide great performance for high speed
machines. Overspeeding setting causes motors mispulses and probably lose of
trajectory. According to my tests, Raspberry Pi 2 can handle axises with 400
 pulses on mm with top velocity ~800 mm per min. There is always way out! :)
Use JIT Python implementation like PyPy. RPi2 can handle up to 18000 mm per
minute on the machine with 80 steps per millimeter motors with PyPy.  


# License
see [LICENSE](./LICENSE) file.

# Author
Justin Cole

