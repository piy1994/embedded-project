##Fire Detection System


Most of the traditional fire detectors use smoke sensors. However, it can take a significant amount of time for such sensors to detect fire as enough smoke is needed for successful detection. Hence, we implemented an image processing based fire detection system using Raspberry Pi where we intend to use camera for visual recognition of fire. Since we are using image processing techniques to detect fire, the main advantage of this system is the early warning benefit. The system is also capable of remotely sending text/email alerts.


The system is enabled by starting the program and confirming your identity using a GUI interface. The frames are continuously scanned for heat signatures and fire illumination patterns to determine if it is a fire. On detecting fire, the system switches ON the LED, and a text message as well as an email (containing an image of the place) is sent to the concerned authorities. The system also has the option to change its sensitivity by providing minimum area of detection as an input to the program.

##Instructions


To start the program, run 'python fire_main.py' into the terminal.

use argument -v 'video name' and -a 'area of detection in pixels' to provide sample inputs to test the program.
	if no -v input is provided, system uses webcam for capturing the frames in real time.
	if no -a is provided, default value is taken to be 500.

use keyboard interrupt to exit the program. 
