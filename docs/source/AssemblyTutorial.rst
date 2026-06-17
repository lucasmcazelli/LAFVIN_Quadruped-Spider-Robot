Assembly Tutorial
=================

Video Assembly Tutorial
-----------------------

.. video:: _static/AssemblyTutorial/0.ASSEMBLY.mp4
    :width: 100%

----

- The video provides a step-by-step assembly tutorial for the quadruped spider robot. Watching this video will help you assemble it quickly.

- For a more detailed assembly guide with text and images, please continue reading below.

----

Illustrated Assembly Tutorial
-----------------------------

STEP 1: Assemble expansion board
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Parts list：** Expansion board、Acrylic body panel、M3*10mm screw(4 PCS)、M3*25mm copper pillar(4 PCS).

.. image:: _static/AssemblyTutorial/2.8266.png
   :width: 800
   :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

----

STEP 2: Assemble development board
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Parts list：** ESP8266 development board.

.. image:: _static/AssemblyTutorial/3.8266.png
   :width: 800
   :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

.. note::

   Ensure the development board orientation matches the silk-screen markings on the expansion board to avoid incorrect installation.

----

STEP 3: Assemble  body servo 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Parts list：** MG90S Servo(4 PCS)、M2*12mm screw(8 PCS)、M2 nut(8 PCS).

.. image:: _static/AssemblyTutorial/4.BODYSERVO.png
   :width: 800
   :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

.. note::

   Make sure the four servos are installed with the correct orientation: the two upper servos face upward while the two lower servos face downward.

----

STEP 4: Wiring of the body servo  
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. attention::

 The MG90S servo motors are crucial components for controlling the robot's leg movements. Each servo has three wires with specific colors and functions:

 .. image:: _static/AssemblyTutorial/1.servo.png
   :width: 800
   :align: center

 .. raw:: html

   <div style="margin-top: 30px;"></div>

 - **Brown Wire**: Ground (GND) - Connect to the ground pin on the expansion board
 - **Red Wire**: Power (VCC) - Connect to the 5V power pin on the expansion board
 - **Orange Wire**: Signal (PWM) - Connect to the corresponding GPIO pin on the ESP8266 board

----

**The wiring diagram for the servo motors in the body is shown in the figure:**

 .. image:: _static/AssemblyTutorial/5.body.png
   :width: 800
   :align: center

 .. raw:: html

   <div style="margin-top: 30px;"></div>

----

**Image of the assembled spider body parts:**

 .. image:: _static/AssemblyTutorial/6.bodycom.png
   :width: 800
   :align: center

 .. raw:: html

   <div style="margin-top: 30px;"></div>

----

.. raw:: html

.. attention::

  - After connecting the servos to the body, install the battery while ensuring the development board is properly mounted on the expansion board. Then, turn on the power of the expansion board. The system will automatically reset, and the servos will rotate to their initial positions. 
  
  - The development board must be programmed before this step; otherwise, the servo will not respond. For instructions,see :ref:`Programming Program`.

----

STEP 5: Assemble the spider's thigh 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Parts list：** Acrylic plate for thigh(8 PCS)、One-swing arm(8 PCS)、M2*8mm self-tapping screw(16 PCS).

 .. image:: _static/AssemblyTutorial/7.baibi.png
   :width: 800
   :align: center

 .. raw:: html

   <div style="margin-top: 30px;"></div>

.. note::

 - The one-swing arm and M2*8mm self-tapping screws used in this step are all included in the servo package.
 - A total of 8 need to be installed for use in subsequent steps.

----

STEP 6: Trim swing arm
~~~~~~~~~~~~~~~~~~~~~~~

To ensure smooth movement of the spider robot, please trim the servo arms to the appropriate length as shown in the diagram. Please handle with care during operation.

 .. image:: _static/AssemblyTutorial/38.XJ2.gif
   :width: 800
   :align: center

 .. raw:: html

   <div style="margin-top: 30px;"></div>

 .. image:: _static/AssemblyTutorial/8.xiujian.png
   :width: 800
   :align: center

 .. raw:: html

   <div style="margin-top: 30px;"></div>

----

STEP 7: Assemble the thigh and femur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Parts list：** The thigh of the assembled swing arm(8 PCS)、Femoral acrylic plate(4 PCS)、M3*10mm screw(8 PCS)、M3 Nut(8 PCS).

.. attention::

   The femoral plates consist of two groups with different orientations. Each group contains 2 pieces, for a total of 4 pieces. Continue reading below for detailed assembly instructions.


**The assembly of the first group is shown in the figure:**

 .. image:: _static/AssemblyTutorial/9.摆臂安装支架1-1.png
   :width: 800
   :align: center

 .. raw:: html

   <div style="margin-top: 30px;"></div>

 .. image:: _static/AssemblyTutorial/10.摆臂安装支架1-2.png
   :width: 800
   :align: center

 .. raw:: html

   <div style="margin-top: 30px;"></div>


**The assembly of the second group is shown in the figure:**

 .. image:: _static/AssemblyTutorial/11.摆臂连接支架2-1.png
   :width: 800
   :align: center

 .. raw:: html

   <div style="margin-top: 30px;"></div>

 .. image:: _static/AssemblyTutorial/12.摆臂连接支架2-2.png
   :width: 800
   :align: center

 .. raw:: html

   <div style="margin-top: 30px;"></div>


**The differences between the two different assembly methods are shown in the following figure.**

 .. image:: _static/AssemblyTutorial/13.ljj.png
   :width: 800
   :align: center

----

STEP 8: Assemble Tibia 
~~~~~~~~~~~~~~~~~~~~~~~

**Parts list：** MG90S Servo(4 PCS)、Tibial acrylic plate(4 PCS)、M2*12mm screw(8 PCS)、M2 Nut(8 PCS)

.. attention::

  Assembling the servo motors to the tibia is also done in two groups with different orientations, two in each group. This step requires assembling a total of four tibias.

**The first set of tibias is installed as shown in the figure.**

 .. image:: _static/AssemblyTutorial/14.tibia1.png
   :width: 800
   :align: center

 .. raw:: html

   <div style="margin-top: 30px;"></div>


**The second set of tibias is installed as shown in the figure.**

 .. image:: _static/AssemblyTutorial/15.tibia2.png
   :width: 800
   :align: center

 .. raw:: html

   <div style="margin-top: 30px;"></div>

**Completed assembly of two sets of tibias:**

 .. image:: _static/AssemblyTutorial/16.tibia3.png
   :width: 800
   :align: center

 .. raw:: html

   <div style="margin-top: 30px;"></div>
  
----

STEP 9: Assemble the tibia and femur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. attention::

  Tibia and femur assembly is also divided into two different assembly directions, with two in each group, requiring the assembly of four bones per group.

**The first group of tibia and femur assembly is shown in the figure.**

 .. image:: _static/AssemblyTutorial/17.leg.png
   :width: 800
   :align: center

 .. raw:: html

   <div style="margin-top: 30px;"></div>
  
  
**The second group of tibia and femur assembly is shown in the figure.**

 .. image:: _static/AssemblyTutorial/18.leg.png
   :width: 800
   :align: center

 .. raw:: html

   <div style="margin-top: 30px;"></div>

**The completed results of the two groups of tibia and femur are shown in the figure.**

 .. image:: _static/AssemblyTutorial/19.触角3.png
   :width: 800
   :align: center

 .. raw:: html

   <div style="margin-top: 30px;"></div>

----

STEP 10: Tibia and femur assemble into the body
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: _static/AssemblyTutorial/21.servo1.png
   :width: 800
   :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

.. image:: _static/AssemblyTutorial/37.servo.png
   :width: 800
   :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

.. image:: _static/AssemblyTutorial/22.chuizhi1.png
   :width: 800
   :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

----


STEP 11: Servo connected to the tibia
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**The servo connection on the tibia is shown in the figure.**

.. image:: _static/AssemblyTutorial/20.SERVO2.png
   :width: 800
   :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

.. image:: _static/AssemblyTutorial/23.servo3.png
   :width: 800
   :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

.. attention::

 The MG90S servo motors are crucial components for controlling the robot's leg movements. Each servo has three wires with specific colors and functions:

 .. image:: _static/AssemblyTutorial/1.servo.png
   :width: 800
   :align: center

 .. raw:: html

   <div style="margin-top: 30px;"></div>

 - **Brown Wire**: Ground (GND) - Connect to the ground pin on the expansion board
 - **Red Wire**: Power (VCC) - Connect to the 5V power pin on the expansion board
 - **Orange Wire**: Signal (PWM) - Connect to the corresponding GPIO pin on the ESP8266 board

----

STEP 12: Organize the servo motor connection cables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Use cable ties to organize the servo wiring harness as shown in the diagram below.**

.. image:: _static/AssemblyTutorial/24.xiansu.png
   :width: 800
   :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

.. note::

  When securing the wiring harness with cable ties, it's necessary to leave sufficient redundancy for the servo motor to rotate, to prevent the servo motor from being unable to operate if the wiring harness is too short.

----

STEP 13: Assemble the body cover plate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Parts list：** Acrylic cover plate for the body、 M3*10mm screw(4 PCS)

.. image:: _static/AssemblyTutorial/36.gb.png
   :width: 800
   :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

----

STEP 14: Assemble an ultrasonic distance sensor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Parts list：** Spider Eye Decorative Acrylic Panel、Ultrasonic distance sensor

.. image:: _static/AssemblyTutorial/34.CSB1.png
   :width: 800
   :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

.. image:: _static/AssemblyTutorial/34.CSB2.png
   :width: 800
   :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

.. image:: _static/AssemblyTutorial/35.csb.png
   :width: 800
   :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

----

STEP 15: Assemble anti-slip rubber sleeves
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Because of the smooth surface of acrylic, installing anti-slip grips can help the spider walk more accurately. Please install the anti-slip grips on the four legs of the spider as shown in the picture.**

.. image:: _static/AssemblyTutorial/27.JT.png
   :width: 800
   :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

----

Complete assembly result image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: _static/AssemblyTutorial/25.com.png
   :width: 800
   :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

----

.. _Servo calibration and debug:

Servo calibration and debug
----------------------------

**To ensure proper movement and coordinated gait during operation, the servos must be calibrated according to the following steps.**

.. note::

 - Install one 18650 battery in the battery compartment at the bottom of the expansion board, ensuring it is fully charged.

 - Please ensure that the ESP8266 development board has been programmed. For detailed programming instructions, please click here. :ref:`Programming Program`

 - Please install the mobile control app for the quadrupedal spider robot.

 - The servo screws fixed to the femur do not need to be installed for now. If they have already been installed, please remove them first and then fix them after the servo is properly calibrated.

 .. image:: _static/AssemblyTutorial/26.notinstall.png
    :width: 400
    :align: center

 .. raw:: html

   <div style="margin-top: 30px;"></div>

----

**Step 1: Manually adjust the servo motor**

1. Each time the power switch on the expansion board is turned on, the servo will perform a reset action and rotate back to the initial position shown in the figure below.

 .. image:: _static/AssemblyTutorial/28.CHUSHIWEIZHI.png
    :width: 800
    :align: center

 .. raw:: html

   <div style="margin-top: 30px;"></div>

----

2. If a servo motor is not in the correct position, the incorrect femur or tibia section can be removed and manually reinstalled to a parallel position.

.. image:: _static/AssemblyTutorial/1.gif
    :width: 800
    :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

.. attention::

    When disassembling and reassembling, keep the power supply on and do not manually rotate the servo motor. Instead, remove the acrylic structure and then install it in the correct horizontal position.

----

3. After manually adjusting all servos to a parallel position, turn off the power, turn the power back on, and check if the spider's four legs are in a parallel position after the servos automatically reset.

4. If the position doesn't shift too much, no manual adjustment is needed. Next, use the app to set the offset, ensuring the four legs are as parallel as possible.

5. Install the screws to secure the servo motor.

.. image:: _static/AssemblyTutorial/33.DJLS.png
    :width: 400
    :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

.. note::

   - After adjusting all four legs to a parallel position, install the fixing screws here.

   - The fixing screws here are the screws included in the Servo pack.

----

**Step 2: Adjust the servo using the APP**

After manually adjusting the servo to a parallel position, you can use the servo calibration function in the APP to fine-tune the servo and make the spider achieve the best movement gait effect when moving.

1. Connect the quadruped spider robot to the App. Click here for app connection and usage instructions. :ref:`APP control`

2. Click the top right corner of the App interface to access the servo calibration page.

.. image:: _static/AssemblyTutorial/29.JZ.png
    :width: 800
    :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

.. image:: _static/AssemblyTutorial/30.JZ2.png
    :width: 800
    :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

----

3. Click "Read value" to read the current offset data for each servo.

.. image:: _static/AssemblyTutorial/31.JZ3.png
    :width: 800
    :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

----

4. The following is an explanation of the data for adding and subtracting values ​​during servo motor adjustment.

- Servo 1, 3, 5, 7 Addition: Servo rotates forward.

- Servo 1, 3, 5, 7 decrement: Servo rotates backward.

- Servo 2, 4,6, 8 Addition: Servo rotates downwards.

- Servo 2, 4, 6, 8 decrement: Servo motors rotate upwards.

----

5. Select a servo motor with a larger offset based on the actual situation and make corresponding adjustments.

----

6. Adjust the servo offset by increasing or decreasing the value. After determining the value to be adjusted, first click "Save calibration", then click "Reset Preview". The adjusted value will take effect, and the servo will rotate accordingly.

.. image:: _static/AssemblyTutorial/32.JZ4.png
    :width: 800
    :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

----
