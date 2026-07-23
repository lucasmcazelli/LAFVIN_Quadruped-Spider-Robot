kit For Learning Course
======================

**In this section, we will use the components in this kit to expand our learning, gradually mastering the principles and functional characteristics of each component in order of depth, and completing the corresponding program writing.**

----

Course 1：Make the servo motor turn
------------------------------------

Wiring diagram
~~~~~~~~~~~~~~

- MG90 Servo —— ESP8266 D4

----

Example code
~~~~~~~~~~~~

.. code-block:: cpp

 #include <Servo.h>

 Servo myservo;
 #define SERVO_PIN D4

 void setup() {
  myservo.attach(SERVO_PIN);
  myservo.write(0);
 }

 void loop() {
  myservo.write(180);
  delay(3000);
  
  myservo.write(0);
  delay(3000);
 }

----

Achieved Effect
~~~~~~~~~~~~~~~~

- Connect the servo motor to pin D4; the servo motor will rotate 180° every 3 seconds.

- You can use this program to sequentially switch between connecting 8 servos to test whether the servos are working properly.

.. raw:: html

   <div style="margin-top: 30px;"></div>

.. image:: _static/course/1.1servo.gif
   :width: 800
   :align: center

----

Course 2：Rotate two servo motors
----------------------------------

Wiring diagram
~~~~~~~~~~~~~~

- MG90 Servo —— ESP8266 D4

- MG90 Servo —— ESP8266 D8

----

Example code
~~~~~~~~~~~~

.. code-block:: cpp

 #include <Servo.h>

 Servo myservo1;  // Pin D4 SERVO
 Servo myservo2;  // Pin D8 SERVO
 
 #define SERVO_PIN1 D4
 #define SERVO_PIN2 D8

 void setup() {
  myservo1.attach(SERVO_PIN1);
  myservo2.attach(SERVO_PIN2);
  
  myservo1.write(0);
  myservo2.write(0);
 }

 void loop() {
  // Both servos rotate 180 degrees simultaneously

  myservo1.write(180);
  myservo2.write(180);
  delay(2000);
  
  // Both servos return to 0 degrees simultaneously

  myservo1.write(0);
  myservo2.write(0);
  delay(2000);
 }

----

Achieved Effect
~~~~~~~~~~~~~~~~

- Similar to the previous lesson, you only need to add one more servo and one more definition in the code to make both servos move simultaneously.

.. raw:: html

   <div style="margin-top: 30px;"></div>

.. image:: _static/course/8.servo2.gif
   :width: 800
   :align: center

----


Course 3：Let the spider move forward
-------------------------------------

In the previous two lessons, we've already gotten two servos moving. Next, we'll get all eight servos moving simultaneously to propel the spider forward.

----

Wiring diagram
~~~~~~~~~~~~~~

Please connect the wires as shown in the diagram below.

.. raw:: html

   <div style="margin-top: 30px;"></div>

.. image:: _static/course/2.body.png
   :width: 800
   :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

.. image:: _static/course/3.SERVO2.png
   :width: 800
   :align: center

----

Example code
~~~~~~~~~~~~

.. code-block:: cpp

  #include <Servo.h>
  #include <Arduino.h>

  // Servo pin definitions
  const int SERVO_PINS[] = {14, 12, 13, 15, 16, 5, 4, 2};  // G14, G12, G13, G15, G16, G5, G4, G2
  const int ALLSERVOS = 8;
  const int ALLMATRIX = 9;  // 8 servos + time

  // Servo angle range
  const int SERVOMIN = 400;
  const int SERVOMAX = 2400;
  const int ANGLE_MIN = 1;
  const int ANGLE_MAX = 180;

  // Servo zero position
  const int Servo_Zero[] = { 135, 45, 135, 45, 45, 135, 45, 135, 500 };

  // Forward motion sequence
  const int Servo_Forward_Step = 11;
  const int Servo_Forward[][ALLMATRIX] = {
    // G14, G12, G13, G15, G16, G5,  G4,  G2,  ms
    {  70,  90,  90, 110, 110,  90,  90,  70, 200 }, // standby
    {  90,  90,  90, 110, 110,  90,  45,  90, 200 }, // leg1,4 lift up
    {  70,  90,  90, 110, 110,  90,  45,  70, 200 }, // leg1,4 put down
    {  70,  90,  90,  90,  90,  90,  45,  70, 200 }, // leg2,3 lift up
    {  70,  39, 141,  90,  90,  90,  90,  70, 200 }, // leg1,4 backward, leg2 forward
    {  70,  39, 141, 110, 110,  90,  90,  70, 200 }, // leg2,3 put down
    {  90,  90, 141, 110, 110,  90,  90,  90, 200 }, // leg1,4 lift up
    {  90,  90,  90, 110, 110, 135,  90,  90, 200 }, // leg2,3 backward
    {  70,  90,  90, 110, 110, 135,  90,  70, 200 }, // leg1,4 put down
    {  70,  90,  90, 110,  90, 135,  90,  70, 200 }, // leg3 lift up
    {  70,  90,  90, 110, 110,  90,  90,  70, 200 }, // leg3 put down forward
  };

  class SpiderBotMotion {
  public:
      Servo servos[8];
      
      // Initialize servos
      void init() {
          for (int i = 0; i < ALLSERVOS; i++) {
              servos[i].attach(SERVO_PINS[i], SERVOMIN, SERVOMAX);
          }
          delay(200);
      }
      
      // Move all servos to zero position
      void zero() {
          for (int i = 0; i < ALLSERVOS; i++) {
              int angle = constrain(Servo_Zero[i], ANGLE_MIN, ANGLE_MAX);
              servos[i].write(angle);
          }
          delay(Servo_Zero[8]);
      }
      
      // Forward motion
      void forward() {
          for (int step = 0; step < Servo_Forward_Step; step++) {
              for (int servo = 0; servo < ALLSERVOS; servo++) {
                  int angle = constrain(Servo_Forward[step][servo], ANGLE_MIN, ANGLE_MAX);
                  servos[servo].write(angle);
              }
              delay(Servo_Forward[step][8]);
          }
      }
      
      // Standby pose
      void standby() {
          int standby_angles[] = {60, 90, 90, 120, 120, 90, 90, 60};
          for (int i = 0; i < ALLSERVOS; i++) {
              int angle = constrain(standby_angles[i], ANGLE_MIN, ANGLE_MAX);
              servos[i].write(angle);
          }
          delay(500);
      }
  };

  SpiderBotMotion robot;

  void setup() {
      Serial.begin(9600);
      Serial.println("QuadBot Starting...");
      
      // 1. Initialize servos
      robot.init();
      
      // 2. Move servos to zero position on power-up
      Serial.println("Moving to zero position...");
      robot.zero();
      delay(500);
      
      // 3. Enter standby state
      Serial.println("Standby position...");
      robot.standby();
      delay(500);
      
      Serial.println("Ready! Robot will move forward.");
  }

  void loop() {
      // Execute forward motion repeatedly
      robot.forward();
      delay(100);
  }

----

Achieved Effect
~~~~~~~~~~~~~~~~

- The spider robot will now continuously perform forward movement.

.. raw:: html

   <div style="margin-top: 30px;"></div>

.. image:: _static/course/4.com.png
   :width: 800
   :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

- If the spider robot's forward movement is abnormal, ensure that the spider robot's initial installation position is as shown below, and click here to jump to the servo calibration page. :ref:`Servo calibration and debug`

- Since the code here only contains forward motion, the servo cannot be calibrated using the app; you only need to check the manual servo calibration section.

----

Course 4：IR control button display
-----------------------------------

In this lesson, we will use the Wi-Fi function of the ESP8266 development board in conjunction with an infrared receiver module to design a webpage that displays infrared remote control buttons.

----

Wiring diagram
~~~~~~~~~~~~~~

The infrared receiver module is integrated into the spider robot's expansion board and connected to pin D3, so no additional wiring is required.

----

Example code
~~~~~~~~~~~~

.. code-block:: cpp

  #include <ESP8266WiFi.h>
  #include <ESP8266WebServer.h>
  #include <IRrecv.h>
  #include <IRutils.h>

  #define IR_RECEIVE_PIN D3

  String lastKey = "";
  String currentKey = "";

  const char* apSSID = "ESP8266_IR_Display";
  const char* apPassword = "12345678";
  const IPAddress apIP(192, 168, 4, 1);

  ESP8266WebServer server(80);
  IRrecv irrecv(IR_RECEIVE_PIN);
  decode_results results;

  String keyMap(uint32_t code) {
    switch(code) {
      case 0x16: return "1";
      case 0x19: return "2";
      case 0x0D: return "3";
      case 0x0C: return "4";
      case 0x18: return "5";
      case 0x5E: return "6";
      case 0x08: return "7";
      case 0x1C: return "8";
      case 0x5A: return "9";
      case 0x52: return "0";
      case 0x42: return "*";
      case 0x4A: return "#";
      case 0x46: return "UP";
      case 0x15: return "DOWN";
      case 0x40: return "OK";
      case 0x44: return "LEFT";
      case 0x43: return "RIGHT";
      default: return "";
    }
  }

  String htmlPage() {
    return R"rawliteral(
  <!DOCTYPE html>
  <html>
  <head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IR Remote</title>
  <style>
    *{margin:0;padding:0;box-sizing:border-box;}
    body{background:#fff;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px;}
    .card{max-width:500px;width:100%;text-align:center;}
    h1{color:#000;font-size:24px;font-weight:500;margin-bottom:40px;padding-bottom:15px;border-bottom:2px solid #000;display:inline-block;}
    .display{background:#fff;border:2px solid #000;border-radius:20px;padding:60px 20px;margin-bottom:30px;}
    .key{font-size:140px;color:#000;font-weight:600;line-height:1;}
    .hint{color:#666;font-size:14px;margin-top:20px;padding-top:15px;border-top:1px solid #eee;}
    .status{display:inline-block;padding:5px 12px;background:#f5f5f5;color:#333;font-size:12px;border-radius:20px;margin-top:15px;}
    @media(max-width:480px){.key{font-size:100px;}.display{padding:40px 20px;}}
  </style>
  </head>
  <body>
  <div class="card">
  <h1>IR Remote Display</h1>
  <div class="display">
  <div class="key" id="keyValue">—</div>
  </div>
  <div class="hint">
  <div>Point remote at receiver</div>
  <div class="status">● Ready</div>
  </div>
  </div>
  <script>
  function fetchKey(){
    fetch('/key').then(r=>r.text()).then(d=>{
      if(d&&d!=='-')document.getElementById('keyValue').innerText=d;
    }).catch(e=>console.error(e));
  }
  setInterval(fetchKey,200);
  fetchKey();
  </script>
  </body>
  </html>
  )rawliteral";
  }

  void handleRoot() { server.send(200, "text/html", htmlPage()); }
  void handleKey() { server.send(200, "text/plain", currentKey.length() > 0 ? currentKey : "-"); }

  void setup() {
    WiFi.mode(WIFI_AP);
    WiFi.softAPConfig(apIP, apIP, IPAddress(255, 255, 255, 0));
    WiFi.softAP(apSSID, apPassword);
    
    irrecv.enableIRIn();
    
    server.on("/", handleRoot);
    server.on("/key", handleKey);
    server.begin();
  }

  void loop() {
    server.handleClient();
    
    if (irrecv.decode(&results)) {
      String key = keyMap(results.command);
      if (key == "") key = keyMap(results.value & 0xFF);
      
      if (key != "" && key != lastKey) {
        currentKey = key;
        lastKey = key;
        delay(50);
      }
      irrecv.resume();
    }
  }

----

Achieved Effect
~~~~~~~~~~~~~~~~

.. video:: _static/course/6.IR.mp4
    :width: 60%
    :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

- After the code is successfully burned, connect the ultrasonic distance sensor to the expansion board and press the "RST" button on the ESP8266.

- Turn on your phone's Wi-Fi, find and connect to a Wi-Fi network named: **ESP8266-IR-Display** with the password: **12345678**.

- After successfully connecting to Wi-Fi, open any browser on your phone, enter the IP address: 192.168.4.1, and you can access the page. Press any button on the remote control, and the webpage will display the corresponding button..

----

Course 5：Infrared Control Servo
--------------------------------

In this lesson, we will control a servo motor using an infrared remote control.

----

Wiring diagram
~~~~~~~~~~~~~~

- SERVO1-D4

- SERVO2-D8

----

Example code
~~~~~~~~~~~~

.. code-block:: cpp

  #include <ESP8266WiFi.h>
  #include <IRrecv.h>
  #include <IRutils.h>
  #include <Servo.h>

  // ===== Pin Definitions =====
  #define IR_RECEIVE_PIN D3
  #define SERVO1_PIN D4
  #define SERVO2_PIN D8

  // ===== IR Key Mapping =====
  #define KEY_1 0x16
  #define KEY_2 0x19

  // ===== Servo Objects =====
  Servo servo1;
  Servo servo2;

  // ===== IR Receiver Object =====
  IRrecv irrecv(IR_RECEIVE_PIN);
  decode_results results;

  // ===== Key Mapping Function =====
  String getKeyName(uint32_t code) {
    switch(code) {
      case KEY_1: return "1";
      case KEY_2: return "2";
      default: return "";
    }
  }

  // ===== Control Servo Function =====
  void controlServo(String key) {
    if (key == "1") {
      servo1.write(180);
      delay(500);
      servo1.write(0);
    } 
    else if (key == "2") {
      servo2.write(180);
      delay(500);
      servo2.write(0);
    }
  }

  // ===== Setup =====
  void setup() {
    // Attach servos
    servo1.attach(SERVO1_PIN);
    servo2.attach(SERVO2_PIN);
    
    // Initialize servos to 0 degrees
    servo1.write(0);
    servo2.write(0);
    
    // Initialize IR receiver
    irrecv.enableIRIn();
  }

  // ===== Main Loop =====
  void loop() {
    // Detect IR signals
    if (irrecv.decode(&results)) {
      uint32_t command = results.command;
      String key = getKeyName(command);
      
      // Try using value's lower 8 bits if command mapping fails
      if (key == "") {
        key = getKeyName(results.value & 0xFF);
      }
      
      if (key != "") {
        controlServo(key);
        delay(100);
      }
      
      irrecv.resume();
    }
  }

----

Achieved Effect
~~~~~~~~~~~~~~~~

- Pressing the number 1 and number 2 buttons on the infrared remote control will cause the two servos to rotate 180 degrees each.

.. image:: _static/course/7.IRSERVO.gif
   :width: 400
   :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

----

Course 6：ESP8266 Rangefinder
-----------------------------

In this lesson, we will make full use of the built-in Wi-Fi function of the ESP8266 development board and combine it with an ultrasonic distance sensor to make a rangefinder.

----

Wiring diagram
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Ultrasonic Distance Sensor
     - Spider Robot Expansion Board
   * - VCC
     - 5V
   * - GND
     - GND
   * - TRIG
     - TX
   * - ECHO
     - RX

----

.. attention::

 Do not connect the ultrasonic distance sensor when programming the code, as this will cause a serial port conflict and prevent the code from being programmed.

----

Example code
~~~~~~~~~~~~

.. code-block:: cpp

  #include <ESP8266WiFi.h>
  #include <ESP8266WebServer.h>

  // WiFi hotspot configuration
  const char* ssid = "ESP8266-Distance-Meter";
  const char* password = "12345678";

  // Using RX/TX pins (GPIO1 and GPIO3)
  #define TRIG_PIN 1   // GPIO1 (TX pin)
  #define ECHO_PIN 3   // GPIO3 (RX pin)

  // Web server
  ESP8266WebServer server(80);

  // Distance variables
  float distance_cm = 0.0;
  unsigned long lastMeasurement = 0;
  const unsigned long MEASURE_INTERVAL = 100;
  bool measurementError = false;
  unsigned long measurementCount = 0;

  // Ultrasonic measurement function
  float measureDistance() {
    // Send trigger pulse
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
    
    // Measure echo time
    unsigned long duration = pulseIn(ECHO_PIN, HIGH, 30000); // 30ms timeout
    
    if (duration == 0) {
      return -1.0;
    }
    
    // Calculate distance
    float distance = duration * 0.0343 / 2;
    
    // Valid range check
    if (distance > 400.0 || distance < 2.0) {
      return -1.0;
    }
    
    return distance;
  }

  // Clean HTML page - white background, black text, only distance
  const char* htmlPage = R"rawliteral(
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Distance Meter</title>
      <style>
          * {
              margin: 0;
              padding: 0;
              box-sizing: border-box;
          }
          
          body {
              font-family: 'Courier New', monospace;
              background: white;
              min-height: 100vh;
              display: flex;
              justify-content: center;
              align-items: center;
          }
          
          .container {
              text-align: center;
          }
          
          .distance {
              font-size: 200px;
              font-weight: bold;
              color: black;
              font-family: 'Courier New', monospace;
          }
          
          .unit {
              font-size: 48px;
              color: black;
              margin-left: 10px;
          }
          
          @keyframes blink {
              0% { opacity: 1; }
              50% { opacity: 0.6; }
              100% { opacity: 1; }
          }
          
          .update {
              animation: blink 0.2s ease;
          }
          
          @media (max-width: 600px) {
              .distance {
                  font-size: 100px;
              }
              .unit {
                  font-size: 32px;
              }
          }
      </style>
  </head>
  <body>
      <div class="container">
          <div class="distance">
              <span id="value">0.0</span><span class="unit">cm</span>
          </div>
      </div>

      <script>
          function updateDistance() {
              fetch('/data')
                  .then(response => response.json())
                  .then(data => {
                      const valueSpan = document.getElementById('value');
                      
                      if (data.error) {
                          valueSpan.innerHTML = '--';
                      } else {
                          valueSpan.innerHTML = data.distance.toFixed(1);
                          
                          // Add animation effect
                          valueSpan.classList.add('update');
                          setTimeout(() => valueSpan.classList.remove('update'), 200);
                      }
                  })
                  .catch(error => {
                      document.getElementById('value').innerHTML = '--';
                  });
          }
          
          // Update every 300ms
          setInterval(updateDistance, 300);
          updateDistance();
      </script>
  </body>
  </html>
  )rawliteral";

  // Handle root path
  void handleRoot() {
    server.send(200, "text/html", htmlPage);
  }

  // Handle data request
  void handleData() {
    String json = "{";
    
    if (measurementError || distance_cm < 0) {
      json += "\"error\":\"Out of range\"";
      json += ",\"distance\":0";
    } else {
      json += "\"error\":null";
      json += ",\"distance\":" + String(distance_cm, 2);
    }
    
    json += ",\"count\":" + String(measurementCount);
    json += "}";
    
    server.send(200, "application/json", json);
  }

  // Handle not found
  void handleNotFound() {
    server.send(404, "text/plain", "404: Not Found");
  }

  void setup() {
    // Note: Serial.begin() not called to avoid RX/TX conflict
    
    // Initialize pins
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    digitalWrite(TRIG_PIN, LOW);
    
    // Create WiFi hotspot
    WiFi.mode(WIFI_AP);
    
    // Configure AP parameters
    IPAddress local_ip(192, 168, 4, 1);
    IPAddress gateway(192, 168, 4, 1);
    IPAddress subnet(255, 255, 255, 0);
    
    WiFi.softAPConfig(local_ip, gateway, subnet);
    WiFi.softAP(ssid, password);
    
    // Setup web server
    server.on("/", handleRoot);
    server.on("/data", handleData);
    server.onNotFound(handleNotFound);
    
    server.begin();
  }

  void loop() {
    server.handleClient();
    
    // Periodic distance measurement
    unsigned long currentMillis = millis();
    if (currentMillis - lastMeasurement >= MEASURE_INTERVAL) {
      float measuredDistance = measureDistance();
      
      if (measuredDistance > 0) {
        distance_cm = measuredDistance;
        measurementError = false;
        measurementCount++;
      } else {
        measurementError = true;
      }
      
      lastMeasurement = currentMillis;
    }
    
    delay(10);
  }

----


Achieved Effect
~~~~~~~~~~~~~~~~

.. video:: _static/course/5.WIFI1.mp4
    :width: 60%
    :align: center

.. raw:: html

   <div style="margin-top: 30px;"></div>

- After the code is successfully burned, connect the ultrasonic distance sensor to the expansion board and press the "RST" button on the ESP8266.

- Turn on your phone's Wi-Fi, find and connect to a Wi-Fi network named: **ESP8266-Distance-Meter** with the password: **12345678**.

- After successfully connecting to Wi-Fi, open any browser on your phone and enter the IP address: 192.168.4.1 to access the distance measurement display page.

----


Course 7：Emotiv EPOC X Mind Control
------------------------------------

In this lesson, we control the spider robot with an **Emotiv EPOC X** EEG headset, and with a
control panel in your web browser. The headset cannot talk to the ESP8266 directly, so a small
Python program on your computer acts as a bridge: it reads Emotiv **mental commands** (via the
EMOTIV Cortex service) *and* serves a local web page with buttons, then forwards a single
character to the ESP8266 over Wi-Fi (UDP). The robot turns that character into a gait.

Because both the browser buttons and the mental commands go through the same channel, you can
verify the whole robot with the buttons first, then add the headset.

.. note::

 Full, ready-to-run copies of both programs live in the repository under
 ``emotiv_control/`` (``firmware/emotiv_spider/emotiv_spider.ino`` and
 ``bridge/emotiv_bridge.py``), together with a README covering the Emotiv Cortex app,
 mental-command training, and troubleshooting.

----

Wiring diagram
~~~~~~~~~~~~~~

- No new wiring. This lesson reuses the fully assembled 8-servo spider from Course 3
  (servos on G14, G12, G13, G15, G16, G5, G4, G2).

- The ESP8266 and the computer running the Python bridge must be on the **same Wi-Fi
  network**.

----

Command reference
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 15 35 25 25

   * - Character
     - Robot action
     - Button
     - Mental command
   * - F
     - Walk forward
     - ▲ Forward
     - push
   * - B
     - Walk backward
     - ▼ Back
     - pull
   * - L
     - Turn left
     - ◄ Left
     - left
   * - R
     - Turn right
     - ► Right
     - right
   * - S
     - Stop (standby)
     - ■ Stop
     - neutral

----

Example code (ESP8266 — Arduino IDE)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set your Wi-Fi ``WIFI_SSID`` / ``WIFI_PASSWORD`` near the top, flash the board, then open the
Serial Monitor at 115200 baud to read the IP address the board was given. You will need that IP
for the Python program.

.. code-block:: cpp

  /*
   * emotiv_spider.ino  —  LAFVIN Quadruped Spider Robot
   * ----------------------------------------------------
   * Wi-Fi (station mode) + UDP command listener for the ESP8266.
   *
   * A companion program on your PC (bridge/emotiv_bridge.py) sends a single
   * character over UDP; this firmware turns that character into a spider gait:
   *
   *     'F' -> walk forward       'B' -> walk backward
   *     'L' -> turn left          'R' -> turn right
   *     'S' -> stop (standby)
   *
   * The PC program can send those characters from a browser control panel
   * (buttons) and/or from an Emotiv EPOC X mental command — this firmware does
   * not care where the character came from.
   *
   * Motion engine (SERVO_PINS, ranges, Servo_Zero, the Servo_Forward matrix,
   * init()/zero()/standby()/forward()) is reused unchanged from Course 3 of the
   * LAFVIN documentation. The backward() and turn() gaits are added here.
   *
   * Board:   ESP8266 (spider expansion board)
   * Libs:    ESP8266WiFi, WiFiUdp, Servo   (all bundled with the ESP8266 core)
   *
   * >>> Set your Wi-Fi SSID / PASSWORD below, flash, then open the Serial
   *     Monitor @115200 to read the IP address the board was given. Put that IP
   *     into bridge/config.py (ESP8266_IP).  The PC and the ESP8266 MUST be on
   *     the same Wi-Fi network.
   */

  #include <ESP8266WiFi.h>
  #include <WiFiUdp.h>
  #include <Servo.h>
  #include <Arduino.h>

  // ======================= Wi-Fi / network configuration =======================
  const char* WIFI_SSID     = "YOUR_WIFI_SSID";       // <-- change me
  const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";   // <-- change me

  const unsigned int LOCAL_UDP_PORT = 4210;           // must match UDP_PORT in config.py

  WiFiUDP Udp;
  char incomingPacket[8];                             // we only need the first byte

  // ============================ Servo / motion setup ===========================
  // (reused verbatim from Course 3)
  const int SERVO_PINS[] = {14, 12, 13, 15, 16, 5, 4, 2};  // G14, G12, G13, G15, G16, G5, G4, G2
  const int ALLSERVOS = 8;
  const int ALLMATRIX = 9;   // 8 servo angles + trailing delay (ms)

  // Servo pulse range (microseconds) and valid angle range
  const int SERVOMIN = 400;
  const int SERVOMAX = 2400;
  const int ANGLE_MIN = 1;
  const int ANGLE_MAX = 180;

  // Servo zero position (8 angles + settle time)
  const int Servo_Zero[] = { 135, 45, 135, 45, 45, 135, 45, 135, 500 };

  // Forward motion sequence (11 steps x [8 angles + ms])
  const int Servo_Forward_Step = 11;
  const int Servo_Forward[][ALLMATRIX] = {
    // G14, G12, G13, G15, G16, G5,  G4,  G2,  ms
    {  70,  90,  90, 110, 110,  90,  90,  70, 200 }, // standby
    {  90,  90,  90, 110, 110,  90,  45,  90, 200 }, // leg1,4 lift up
    {  70,  90,  90, 110, 110,  90,  45,  70, 200 }, // leg1,4 put down
    {  70,  90,  90,  90,  90,  90,  45,  70, 200 }, // leg2,3 lift up
    {  70,  39, 141,  90,  90,  90,  90,  70, 200 }, // leg1,4 backward, leg2 forward
    {  70,  39, 141, 110, 110,  90,  90,  70, 200 }, // leg2,3 put down
    {  90,  90, 141, 110, 110,  90,  90,  90, 200 }, // leg1,4 lift up
    {  90,  90,  90, 110, 110, 135,  90,  90, 200 }, // leg2,3 backward
    {  70,  90,  90, 110, 110, 135,  90,  70, 200 }, // leg1,4 put down
    {  70,  90,  90, 110,  90, 135,  90,  70, 200 }, // leg3 lift up
    {  70,  90,  90, 110, 110,  90,  90,  70, 200 }, // leg3 put down forward
  };

  // ------------------------------- Turn tuning ---------------------------------
  // The turn gaits below are DERIVED from the forward gait: we damp the stride of
  // the legs on one side so the body curves toward that side. The exact left/right
  // leg grouping depends on how YOUR robot is assembled. These are STARTER VALUES
  // — expect to fine-tune them on real hardware (use the browser control panel in
  // --ui-only mode, and the servo-calibration page in the LAFVIN docs).
  //
  // If "turn left" makes the robot turn right (or vice-versa), swap the two
  // index lists below. If turns are too weak/strong, change TURN_DAMP
  // (0.0 = spins hard in place, 1.0 = walks straight, no turn).
  const int  LEFT_H_SERVOS[]  = {0, 2};   // horizontal servos of the left-side legs
  const int  RIGHT_H_SERVOS[] = {4, 6};   // horizontal servos of the right-side legs
  const int  LEFT_H_COUNT     = 2;
  const int  RIGHT_H_COUNT    = 2;
  const float TURN_DAMP       = 0.35;     // fraction of stride kept on the damped side

  // Neutral (standby) horizontal-servo angles, used as the anchor when damping.
  // These are the horizontal columns of Servo_Forward row 0.
  const int Neutral_H[ALLSERVOS] = { 70, 90, 90, 110, 110, 90, 90, 70 };

  // Forward-declared so the gait loops can poll for a new UDP command mid-cycle
  // and abort early when the operator changes their mind.
  char pollCommand(char current);

  // =============================================================================
  class SpiderBotMotion {
  public:
      Servo servos[ALLSERVOS];

      // Attach all 8 servos
      void init() {
          for (int i = 0; i < ALLSERVOS; i++) {
              servos[i].attach(SERVO_PINS[i], SERVOMIN, SERVOMAX);
          }
          delay(200);
      }

      // Write one row of angles (indices 0..7) then wait `ms`
      void writeFrame(const int angles[ALLSERVOS], int ms) {
          for (int i = 0; i < ALLSERVOS; i++) {
              int angle = constrain(angles[i], ANGLE_MIN, ANGLE_MAX);
              servos[i].write(angle);
          }
          delay(ms);
      }

      // Move all servos to the zero position
      void zero() {
          for (int i = 0; i < ALLSERVOS; i++) {
              int angle = constrain(Servo_Zero[i], ANGLE_MIN, ANGLE_MAX);
              servos[i].write(angle);
          }
          delay(Servo_Zero[8]);
      }

      // Standby pose (legs down, ready)
      void standby() {
          int standby_angles[ALLSERVOS] = {60, 90, 90, 120, 120, 90, 90, 60};
          writeFrame(standby_angles, 500);
      }

      // ---- Forward: one full gait cycle, abortable between steps -------------
      // Returns the command that should run next (unchanged unless a new UDP
      // packet arrived while walking).
      char forward(char cmd) {
          for (int step = 0; step < Servo_Forward_Step; step++) {
              writeFrame(Servo_Forward[step], Servo_Forward[step][8]);
              char next = pollCommand(cmd);
              if (next != cmd) return next;          // operator changed command
          }
          return cmd;
      }

      // ---- Backward: the forward keyframes walked in reverse order ----------
      char backward(char cmd) {
          for (int step = Servo_Forward_Step - 1; step >= 0; step--) {
              writeFrame(Servo_Forward[step], Servo_Forward[step][8]);
              char next = pollCommand(cmd);
              if (next != cmd) return next;
          }
          return cmd;
      }

      // ---- Turn: forward gait with one side's stride damped ------------------
      // left == true  -> damp the LEFT legs  -> body curves/pivots left
      // left == false -> damp the RIGHT legs -> body curves/pivots right
      char turn(bool left, char cmd) {
          const int* damp   = left ? LEFT_H_SERVOS : RIGHT_H_SERVOS;
          int        dampN  = left ? LEFT_H_COUNT  : RIGHT_H_COUNT;

          for (int step = 0; step < Servo_Forward_Step; step++) {
              int frame[ALLSERVOS];
              for (int i = 0; i < ALLSERVOS; i++) frame[i] = Servo_Forward[step][i];

              // Pull the damped side's horizontal servos back toward neutral so
              // those legs take a shorter stride -> the robot turns.
              for (int k = 0; k < dampN; k++) {
                  int idx = damp[k];
                  int raw = Servo_Forward[step][idx];
                  frame[idx] = Neutral_H[idx] + (int)((raw - Neutral_H[idx]) * TURN_DAMP);
              }

              writeFrame(frame, Servo_Forward[step][8]);
              char next = pollCommand(cmd);
              if (next != cmd) return next;
          }
          return cmd;
      }
  };

  SpiderBotMotion robot;

  // Current active command; 'S' (stop/standby) at power-up.
  char currentCmd = 'S';

  // =============================================================================
  // Read a UDP packet if one is waiting and return the (possibly new) command.
  // Only F/B/L/R/S are accepted; anything else is ignored.
  char pollCommand(char current) {
      int packetSize = Udp.parsePacket();
      if (packetSize) {
          int len = Udp.read(incomingPacket, sizeof(incomingPacket) - 1);
          if (len > 0) {
              incomingPacket[len] = 0;
              char c = incomingPacket[0];
              if (c == 'F' || c == 'B' || c == 'L' || c == 'R' || c == 'S') {
                  if (c != current) {
                      Serial.printf("UDP command: %c\n", c);
                  }
                  return c;
              }
          }
      }
      return current;
  }

  void setup() {
      Serial.begin(115200);
      delay(100);
      Serial.println("\nQuadBot (Emotiv/UDP) starting...");

      // Bring up the servos and park in a known pose
      robot.init();
      Serial.println("Moving to zero position...");
      robot.zero();
      Serial.println("Standby position...");
      robot.standby();

      // Connect to Wi-Fi (station mode)
      Serial.printf("Connecting to Wi-Fi \"%s\"", WIFI_SSID);
      WiFi.mode(WIFI_STA);
      WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
      while (WiFi.status() != WL_CONNECTED) {
          delay(500);
          Serial.print(".");
      }
      Serial.println();
      Serial.print("Wi-Fi connected. ESP8266 IP address: ");
      Serial.println(WiFi.localIP());   // <-- copy this into config.py (ESP8266_IP)

      // Start listening for UDP commands
      Udp.begin(LOCAL_UDP_PORT);
      Serial.printf("Listening for UDP commands on port %u\n", LOCAL_UDP_PORT);
      Serial.println("Ready. Send F/B/L/R/S from the PC bridge.");
  }

  void loop() {
      // Pick up any newly-arrived command
      currentCmd = pollCommand(currentCmd);

      // Run one gait cycle for the active command (each returns early if the
      // command changes mid-cycle, keeping the robot responsive).
      switch (currentCmd) {
          case 'F': currentCmd = robot.forward(currentCmd);      break;
          case 'B': currentCmd = robot.backward(currentCmd);     break;
          case 'L': currentCmd = robot.turn(true,  currentCmd);  break;
          case 'R': currentCmd = robot.turn(false, currentCmd);  break;
          case 'S':
          default:
              robot.standby();     // hold the standby pose while stopped
              break;
      }
  }

----

Example code (PC bridge — Python)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install the one dependency with ``pip install websocket-client``. Copy ``config.example.py`` to
``config.py`` and set ``ESP8266_IP`` (from the Serial Monitor) plus, for mental commands, your
Emotiv ``CLIENT_ID`` / ``CLIENT_SECRET`` / ``PROFILE_NAME``. Run
``python emotiv_bridge.py --ui-only`` for the browser buttons alone, or
``python emotiv_bridge.py`` to add the headset.

.. code-block:: python

  #!/usr/bin/env python3
  """
  emotiv_bridge.py  —  PC-side bridge for the LAFVIN spider robot.

  Two ways to drive the spider, both funnelling through one send_command():

    1. A local browser control panel (http://localhost:8080) with buttons:
          Forward / Back / Left / Right / Stop
       -> works WITHOUT the headset, so you can verify the Wi-Fi/UDP/servo path
          first.

    2. The Emotiv EPOC X "mental command" (com) stream, via the EMOTIV Cortex
       service running on this same PC.

  Each input becomes a single character sent over UDP to the ESP8266:

          F = forward   B = backward   L = left   R = right   S = stop

  Usage:
      python emotiv_bridge.py --ui-only     # control panel only, no headset
      python emotiv_bridge.py               # control panel + Emotiv mental commands

  Setup:
      pip install -r requirements.txt       # installs websocket-client
      cp config.example.py config.py        # then edit config.py

  Only the Emotiv path needs the third-party 'websocket-client' package;
  the control panel and UDP sender use the Python standard library only.
  """

  import argparse
  import json
  import socket
  import ssl
  import sys
  import threading
  import time
  from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
  from urllib.parse import urlparse, parse_qs

  # --------------------------------------------------------------------------- #
  # Configuration: prefer a local config.py, fall back to config.example.py.
  # --------------------------------------------------------------------------- #
  try:
      import config
  except ImportError:
      print("ERROR: config.py not found.\n"
            "       Copy the template and edit it:  cp config.example.py config.py")
      sys.exit(1)

  VALID_COMMANDS = {"F", "B", "L", "R", "S"}

  # --------------------------------------------------------------------------- #
  # UDP sender — the single choke point every input path goes through.
  # --------------------------------------------------------------------------- #
  _udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  _last_sent = None
  _last_sent_lock = threading.Lock()


  def send_command(char, source=""):
      """Send a one-character command to the ESP8266 over UDP."""
      char = (char or "").upper()[:1]
      if char not in VALID_COMMANDS:
          print(f"  (ignored invalid command: {char!r})")
          return False
      global _last_sent
      with _last_sent_lock:
          _last_sent = char
      _udp_socket.sendto(char.encode(), (config.ESP8266_IP, config.UDP_PORT))
      tag = f" [{source}]" if source else ""
      print(f"-> sent '{char}' to {config.ESP8266_IP}:{config.UDP_PORT}{tag}")
      return True


  def last_sent():
      with _last_sent_lock:
          return _last_sent or "-"


  # --------------------------------------------------------------------------- #
  # Local browser control panel (standard library only).
  # --------------------------------------------------------------------------- #
  CONTROL_PANEL_HTML = """<!DOCTYPE html>
  <html lang="en">
  <head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Spider Control</title>
  <style>
    *{margin:0;padding:0;box-sizing:border-box;}
    body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
         background:#0f1115;color:#e8e8e8;min-height:100vh;display:flex;
         flex-direction:column;justify-content:center;align-items:center;padding:20px;}
    h1{font-weight:500;font-size:22px;margin-bottom:6px;}
    .sub{color:#8a8f98;font-size:13px;margin-bottom:28px;}
    .pad{display:grid;grid-template-columns:repeat(3,90px);grid-template-rows:repeat(3,90px);
         gap:12px;}
    button{font-size:15px;font-weight:600;color:#e8e8e8;background:#1c2230;
           border:1px solid #2c3444;border-radius:16px;cursor:pointer;
           transition:transform .05s,background .15s;user-select:none;}
    button:hover{background:#26304a;}
    button:active{transform:scale(.94);background:#3a4670;}
    .fwd{grid-column:2;grid-row:1;}
    .left{grid-column:1;grid-row:2;}
    .stop{grid-column:2;grid-row:2;background:#4a1f24;border-color:#6b2b32;}
    .stop:hover{background:#66272e;}
    .right{grid-column:3;grid-row:2;}
    .back{grid-column:2;grid-row:3;}
    .status{margin-top:26px;font-size:13px;color:#8a8f98;}
    .status b{color:#7dd3fc;font-size:15px;}
  </style>
  </head>
  <body>
    <h1>🕷️ Spider Control</h1>
    <div class="sub">Buttons and mental commands share the same robot.</div>
    <div class="pad">
      <button class="fwd"   onclick="cmd('F')">▲<br>Forward</button>
      <button class="left"  onclick="cmd('L')">◄<br>Left</button>
      <button class="stop"  onclick="cmd('S')">■<br>Stop</button>
      <button class="right" onclick="cmd('R')">►<br>Right</button>
      <button class="back"  onclick="cmd('B')">▼<br>Back</button>
    </div>
    <div class="status">Last command: <b id="last">-</b></div>
  <script>
  function cmd(c){
    fetch('/cmd?c='+c).then(r=>r.text()).then(()=>{
      document.getElementById('last').innerText=c;
    }).catch(e=>console.error(e));
  }
  // keyboard: arrow keys + space to stop
  document.addEventListener('keydown',e=>{
    const m={ArrowUp:'F',ArrowDown:'B',ArrowLeft:'L',ArrowRight:'R',' ':'S'};
    if(m[e.key]){e.preventDefault();cmd(m[e.key]);}
  });
  </script>
  </body>
  </html>
  """


  class ControlPanelHandler(BaseHTTPRequestHandler):
      def do_GET(self):
          parsed = urlparse(self.path)
          if parsed.path == "/" or parsed.path == "/index.html":
              body = CONTROL_PANEL_HTML.encode("utf-8")
              self.send_response(200)
              self.send_header("Content-Type", "text/html; charset=utf-8")
              self.send_header("Content-Length", str(len(body)))
              self.end_headers()
              self.wfile.write(body)
          elif parsed.path == "/cmd":
              params = parse_qs(parsed.query)
              char = (params.get("c", [""])[0] or "").upper()
              ok = send_command(char, source="ui")
              self.send_response(200 if ok else 400)
              self.send_header("Content-Type", "text/plain")
              self.end_headers()
              self.wfile.write(b"ok" if ok else b"invalid")
          else:
              self.send_response(404)
              self.end_headers()
              self.wfile.write(b"404")

      def log_message(self, *args):
          pass  # keep the console focused on command traffic


  def start_web_ui():
      """Start the control panel on a background thread; return the server."""
      server = ThreadingHTTPServer(("127.0.0.1", config.UI_PORT), ControlPanelHandler)
      t = threading.Thread(target=server.serve_forever, daemon=True)
      t.start()
      print(f"Control panel:  http://localhost:{config.UI_PORT}")
      return server


  # --------------------------------------------------------------------------- #
  # Emotiv Cortex client (mental commands).
  # --------------------------------------------------------------------------- #
  class CortexClient:
      """Minimal Cortex v2 client: authorize, session, load profile, subscribe."""

      def __init__(self):
          from websocket import create_connection  # imported lazily (only this path needs it)
          self._create_connection = create_connection
          self.ws = None
          self.req_id = 0
          self.token = None
          self.headset = None
          self.session = None

      def _rpc(self, method, params=None):
          self.req_id += 1
          self.ws.send(json.dumps({
              "jsonrpc": "2.0", "id": self.req_id,
              "method": method, "params": params or {},
          }))
          # Skip any streaming/warning frames until our matching response arrives.
          while True:
              msg = json.loads(self.ws.recv())
              if msg.get("id") == self.req_id:
                  if "error" in msg:
                      raise RuntimeError(f"{method} failed: {msg['error']}")
                  return msg.get("result")

      def connect(self):
          print("Connecting to Cortex (wss://localhost:6868)...")
          self.ws = self._create_connection(
              "wss://localhost:6868",
              sslopt={"cert_reqs": ssl.CERT_NONE},  # Cortex uses a self-signed cert
          )

          login = self._rpc("getUserLogin")
          if not login:
              raise RuntimeError("No user logged in. Open EMOTIV Launcher and log in first.")

          self._rpc("requestAccess", {
              "clientId": config.CLIENT_ID, "clientSecret": config.CLIENT_SECRET,
          })
          # First run only: approve this app in the EMOTIV Launcher when prompted.

          auth = self._rpc("authorize", {
              "clientId": config.CLIENT_ID, "clientSecret": config.CLIENT_SECRET,
              "debit": 1,
          })
          self.token = auth["cortexToken"]

          headsets = self._rpc("queryHeadsets")
          if not headsets:
              raise RuntimeError("No headset found. Turn on the EPOC X / insert the USB dongle.")
          self.headset = headsets[0]["id"]
          if headsets[0].get("status") == "discovered":
              self._rpc("controlDevice", {"command": "connect", "headset": self.headset})
              time.sleep(3)
          print(f"Headset: {self.headset}")

          sess = self._rpc("createSession", {
              "cortexToken": self.token, "headset": self.headset, "status": "active",
          })
          self.session = sess["id"]

          # Load the trained mental-command profile (required for real commands).
          if config.PROFILE_NAME:
              self._rpc("setupProfile", {
                  "cortexToken": self.token, "headset": self.headset,
                  "profile": config.PROFILE_NAME, "status": "load",
              })
              print(f"Loaded profile: {config.PROFILE_NAME}")
          else:
              print("WARNING: PROFILE_NAME is empty — only 'neutral' will fire until you "
                    "train mental commands in EmotivBCI and set PROFILE_NAME.")

          self._rpc("subscribe", {
              "cortexToken": self.token, "session": self.session, "streams": ["com"],
          })
          print("Subscribed to mental commands ('com'). Think to move!")

      def run(self):
          """Blocking receive loop: map mental commands to robot commands."""
          last_cmd = None
          while True:
              data = json.loads(self.ws.recv())
              if "com" not in data:
                  continue
              action, power = data["com"][0], data["com"][1]
              mapped = config.COMMAND_MAP.get(action)
              if mapped is None:
                  continue
              # Neutral always stops; other actions must clear the power threshold.
              if action != "neutral" and power < config.POWER_THRESHOLD:
                  continue
              if mapped != last_cmd:          # debounce: only send on change
                  last_cmd = mapped
                  send_command(mapped, source=f"com:{action} {power:.2f}")


  # --------------------------------------------------------------------------- #
  # Entry point.
  # --------------------------------------------------------------------------- #
  def main():
      parser = argparse.ArgumentParser(description="Emotiv -> Spider robot bridge")
      parser.add_argument("--ui-only", action="store_true",
                          help="Run only the browser control panel (no headset).")
      args = parser.parse_args()

      print("=" * 60)
      print("LAFVIN Spider — Emotiv / UDP bridge")
      print(f"Robot (ESP8266): {config.ESP8266_IP}:{config.UDP_PORT}")
      print("=" * 60)

      start_web_ui()

      if args.ui_only:
          print("Mode: UI only. Open the control panel and click to drive.")
          print("Press Ctrl+C to quit.")
          try:
              while True:
                  time.sleep(1)
          except KeyboardInterrupt:
              print("\nBye.")
          return

      # Full mode: also connect to Emotiv Cortex.
      try:
          client = CortexClient()
          client.connect()
          client.run()
      except KeyboardInterrupt:
          print("\nBye.")
      except Exception as e:
          print(f"\nEmotiv connection error: {e}")
          print("The control panel is still running — you can keep using the buttons.")
          print("Press Ctrl+C to quit.")
          try:
              while True:
                  time.sleep(1)
          except KeyboardInterrupt:
              print("\nBye.")


  if __name__ == "__main__":
      main()

----

Achieved Effect
~~~~~~~~~~~~~~~~

- Run ``python emotiv_bridge.py --ui-only`` and open ``http://localhost:8080`` in a browser on
  the same computer. Click **Forward / Back / Left / Right / Stop** (or use the arrow keys) and
  the spider walks, turns, and stops — no headset required. This confirms the Wi-Fi and servo
  path.

- With a trained EMOTIV profile loaded, run ``python emotiv_bridge.py`` and *think* the trained
  actions (push / pull / left / right / neutral) to drive the spider. The browser buttons keep
  working as a manual override.

- The forward gait is from Course 3; the backward and turn gaits are starting points you can
  fine-tune (see the ``TURN_DAMP`` / ``LEFT_H_SERVOS`` settings in the sketch and the servo
  calibration page).

----
