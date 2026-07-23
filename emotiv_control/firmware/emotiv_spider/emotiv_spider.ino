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
