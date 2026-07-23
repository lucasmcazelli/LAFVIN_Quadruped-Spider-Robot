# Emotiv EPOC X → LAFVIN Spider Robot

Control the LAFVIN quadruped spider (ESP8266 + 8 servos) two ways at once:

- a **local browser control panel** with buttons (Forward / Back / Left / Right / Stop), and
- **Emotiv EPOC X mental commands** (think *push / pull / left / right* to move).

Both paths send the same one-character command to the robot over Wi-Fi (UDP), so you
can verify everything with the buttons **before** dealing with the headset.

```
   Browser @ http://localhost:8080  ──┐  (button click → /cmd?c=F)
   (Forward/Back/Left/Right/Stop)      │
                                       ├──▶ emotiv_bridge.py ──UDP :4210──▶ ESP8266
   Emotiv EPOC X ──USB/BT──▶ Cortex ───┘   (send_command)     (same LAN)   (WiFiUDP → gait)
   (wss://localhost:6868, "com" stream)
```

The **only firmware** is `firmware/emotiv_spider/emotiv_spider.ino` (C/Arduino), flashed to
the ESP8266. The **PC program** `bridge/emotiv_bridge.py` (Python) hosts the control panel
and talks to the Emotiv Cortex service on your computer.

## Command reference

| Char | Robot action | Button | Mental command (default) | Arrow key |
|------|--------------|--------|--------------------------|-----------|
| `F`  | walk forward | ▲ Forward | push    | ↑ |
| `B`  | walk backward| ▼ Back    | pull    | ↓ |
| `L`  | turn left    | ◄ Left    | left    | ← |
| `R`  | turn right   | ► Right   | right   | → |
| `S`  | stop (standby)| ■ Stop   | neutral | space |

---

## 1. Flash the ESP8266

1. In the Arduino IDE, install ESP8266 board support and make sure the `Servo` library is
   available (bundled with the ESP8266 core).
2. Open `firmware/emotiv_spider/emotiv_spider.ino`.
3. Set your home Wi-Fi credentials near the top:
   ```cpp
   const char* WIFI_SSID     = "YOUR_WIFI_SSID";
   const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
   ```
4. Flash the board, then open **Serial Monitor @ 115200**. It prints the IP address the
   board received, e.g. `ESP8266 IP address: 192.168.1.50`. **Write this down.**

> The PC and the ESP8266 must be on the **same Wi-Fi network** for UDP to reach the robot.

## 2. Set up the PC bridge

```bash
cd bridge
pip install -r requirements.txt        # installs websocket-client
cp config.example.py config.py         # then edit config.py
```

In `config.py` set at least:
```python
ESP8266_IP = "192.168.1.50"   # the IP from the Serial Monitor
```
(`config.py` is git-ignored so your credentials stay private.)

## 3. Verify with the control panel — no headset needed

```bash
python emotiv_bridge.py --ui-only
```
Open **http://localhost:8080** and click the buttons (or use the arrow keys). The spider
should walk, turn, and stop. Each command is echoed in the terminal and on the ESP8266
Serial Monitor. **Do this first** — it proves the Wi-Fi → UDP → servo path independent of
Emotiv, and it's the easiest way to tune the gaits (see *Tuning* below).

## 4. Add the Emotiv headset

1. Install the **EMOTIV Launcher**, log in, fit the EPOC X with hydrated felts, and confirm a
   good contact-quality signal.
2. Create a **Cortex app** at <https://www.emotiv.com/developer/> to get a **Client ID** and
   **Client Secret**; put them in `config.py`.
3. In **EmotivBCI**, train your mental commands — at minimum **Neutral** plus the actions you
   want (Push / Pull / Left / Right). Save the profile and put its name in `config.py`:
   ```python
   PROFILE_NAME = "MyProfile"
   ```
4. Run the full bridge (control panel **and** mental commands):
   ```bash
   python emotiv_bridge.py
   ```
   First run only: approve the app in the EMOTIV Launcher when prompted. Then *think* to
   drive — and the browser buttons still work as a manual override.

### Run order recap
router on → flash ESP8266 → note its IP → fill `config.py` → verify with `--ui-only` →
start EMOTIV Launcher with good signal → `python emotiv_bridge.py`.

---

## Tuning the gaits

Only the **forward** gait comes from the official LAFVIN course; **backward** and the
**turns** are authored here and are *starter values*. If a movement looks off:

- **Backward** replays the forward keyframes in reverse — usually fine as-is.
- **Turns** are the forward gait with one side's stride damped. In `emotiv_spider.ino`:
  - If *Left* turns right (or vice-versa), swap `LEFT_H_SERVOS` and `RIGHT_H_SERVOS`.
  - If turns are too weak/strong, change `TURN_DAMP` (`0.0` = spins hard in place,
    `1.0` = walks straight).
- For per-servo trim, follow the LAFVIN **servo calibration** guide:
  <https://lafvin-quadruped-spider-robot.readthedocs.io/en/latest/AssemblyTutorial.html#servo-calibration-and-debug>

Use `--ui-only` mode while tuning so you can trigger each movement on demand.

## Troubleshooting

| Symptom | Likely cause / fix |
|---------|--------------------|
| Buttons do nothing on the robot | PC and ESP8266 on different networks; wrong `ESP8266_IP`; firewall blocking UDP. Check the ESP Serial Monitor for `UDP command: …`. |
| Only `neutral`/Stop ever fires | Mental commands not trained, or `PROFILE_NAME` empty/wrong. Train in EmotivBCI and set the profile name. |
| `authorize failed` / cert error | EMOTIV Launcher not running/logged in; the script already disables cert verification for the local self-signed cert. |
| `No headset found` | EPOC X off, or USB dongle not inserted / Bluetooth not paired. |
| Servos twitch / robot unstable | Servo calibration — see the *Tuning* link above. |
| `Address already in use` on start | Another process holds `UI_PORT`; change `UI_PORT` in `config.py`. |
| Robot keeps walking after Stop | Make sure `neutral` maps to `S`; Stop must be sent to break the gait loop. |

## Files

```
emotiv_control/
├── README.md
├── firmware/emotiv_spider/emotiv_spider.ino   # ESP8266: Wi-Fi + UDP + gaits
└── bridge/
    ├── emotiv_bridge.py        # control panel + Emotiv → UDP
    ├── config.example.py       # copy to config.py and edit
    ├── requirements.txt        # websocket-client
    └── .gitignore              # keeps config.py out of git
```
