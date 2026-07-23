"""
Configuration for emotiv_bridge.py.

Copy this file to config.py and fill in your values:

    cp config.example.py config.py

config.py is what the bridge actually imports. Keeping your real Client ID /
Secret in config.py (and out of version control) avoids committing credentials.
"""

# ----------------------------- Robot / network ------------------------------
# The IP address the ESP8266 printed on its Serial Monitor after connecting to
# Wi-Fi. The PC running this script and the ESP8266 must be on the SAME network.
ESP8266_IP = "192.168.1.50"      # <-- change to your board's IP
UDP_PORT = 4210                  # must match LOCAL_UDP_PORT in emotiv_spider.ino

# Port for the local browser control panel (http://localhost:<UI_PORT>)
UI_PORT = 8080

# ----------------------------- Emotiv Cortex --------------------------------
# Create a Cortex app at https://www.emotiv.com/developer/ to get these.
CLIENT_ID = "YOUR_EMOTIV_CLIENT_ID"
CLIENT_SECRET = "YOUR_EMOTIV_CLIENT_SECRET"

# Name of the trained mental-command profile (created/trained in EmotivBCI).
# Mental commands only fire reliably AFTER you train them. Leave "" to skip
# loading a profile (then only "neutral" will be detected).
PROFILE_NAME = ""

# Minimum command "power" (0.0-1.0) required before a non-neutral action is
# sent. Raise it if the robot reacts to weak/uncertain thoughts.
POWER_THRESHOLD = 0.6

# Map Emotiv mental-command actions -> robot command characters.
#   F = forward   B = backward   L = left   R = right   S = stop
# Adjust to match the actions you actually trained.
COMMAND_MAP = {
    "push":    "F",
    "pull":    "B",
    "left":    "L",
    "right":   "R",
    "neutral": "S",
}
