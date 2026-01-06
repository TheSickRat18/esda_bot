# esda_bot

ENCODER TESTING

Hardware needed:

Arduino Mega board
STM32 board
Encoder sensor (A3144)
jumper wires

Software needed:

encoder_final.zip (STM32CubeIDE)
ESC_programming_code.ino (ArduinoIDE)

Software Setup

STM32CubeIDE Setup

  Download the encoder_final.zip. 
  Open STM32CubeIDE and create a workspace
  Go to File -> Import -> Archive File -> Open encoder_final.zip
  Once you have imported it should appear on the left hand side of the screen in the Project Explorer.
  In the project explorer, Right click on the project and click build project to build the project. It should build without any errors, but if any errors try cleaning the project and        rebuilding.
  Click OK for code generation.

Now go to Core -> Src -> main.c - This is the code that continuously collects encoder data from the sensor and calculates the encoder speed. You want to run this and view the RPM measurement. 
Running the code:
  1. first ensure the STM32 is connected to the USB port on your computer, otherwise you will get an error saying no ST-Link detected.
  2. Go to Command Shell console
     <img width="1921" height="487" alt="image" src="https://github.com/user-attachments/assets/1e34ea73-27c0-4609-a8c3-e21011bdab83" />
  3. Here we need to establish which port the STM32 board is connected to on our laptop. To find the right port, go to your laptop settings in: Device Manager -> Ports. Find the COM port number thats has the STLink connection or described as something similar.
  4. Enter the details like so, leave encoding as default. For example, my stm32 was connected to COM3
      <img width="843" height="403" alt="image" src="https://github.com/user-attachments/assets/42226bb0-07cc-4665-8795-f98728913914" />
  5. THen click the run button (green Play icon) on the top to run the program and wait for the program to boot.
  6. Open the console you just created. Now we can view the RPM as it is being printed every 1sec.

ArduinoIDE Setup

  Now that you have run the STM32 program successfully, we need to run the ESC_programming_code.ino file simultaneously. THis code allows the Arduino Mega to control the direction and speed   of the motor. You will need to 
  1. OPen the file
  2. ensure the Arduino Mega is also connected to your computer's usb port.
  3. In Tools -> Port, ensure the correct COM port is selected (check Device manager)
  4. Click Verify (Tick icon) and wait for the code to compile
  5. Click Upload to boot the program. You should hear the ESC beeping.
  6. In Tools -> Serial Monitor, the motor controlled by entering a value from 1000 - 2000:
  - 1500 = brake 
  - Any value > 1500 = forward
  - Any value < 1500 = backward
  Notes:
  - Due to the limited power supply, we can only operate at a speed thats quite slow. Please only enter 1570 for forward or 1450 for backward or close to those values.
  - Everytime you want to reverse the direction, you must enter 1500 first to stop the motor.
  
Now that you have got the motor to work, you can test the motor by going forward, backward, braking and view the measured rpm by going back to the STM32CubeIDE console.


Troubleshooting

Issue: No encoder reading

- Ensure the encoder jumper wire connections are secure and correct.
  
- Ensure encoder pins are connected to the correct pins on the STM32. Pin configuration of encoder:
<img width="656" height="953" alt="image" src="https://github.com/user-attachments/assets/a4a2b155-39a9-42b2-85e6-7ace6b7c9e71" />

  The correct pin configuration is found in encoder_2.ioc. Check that the encoder digital output is connected pin A0 on stm32. 
  Also ensure the 5V pin is connected and powering the encoder.
  <img width="1026" height="768" alt="image" src="https://github.com/user-attachments/assets/f56402f4-df38-4c8d-a228-5438c397adee" />

Issue: motor not working

- Ensure the 24V power cable is connected to the red and black wires of the ESC as seen in digram below. The power cable is inside Asterius in the empty space below the circuitry.
  <img width="1256" height="590" alt="image" src="https://github.com/user-attachments/assets/735899c6-1bf6-4378-b20f-b504d1950af9" />
- Ensure the power supply is ON and set to 24.00V and the current limit at 3.00A.
- Ensure the Arduino pin (Pin 9) that outputs the PWM signal is connected to the RX wire on ESC as seen in diagram below.
  <img width="1256" height="590" alt="image" src="https://github.com/user-attachments/assets/a38f8fc2-9ad7-407d-b7ab-4e33de0f77ee" />
- Ensure motor wires are connected properly to the ESC as in the diagram above.

