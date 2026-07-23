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
