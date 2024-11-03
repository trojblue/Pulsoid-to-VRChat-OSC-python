import os
import json
import asyncio
import websockets
import requests
import uuid
import socket

# Pulsoid API configuration
PULSOID_API = {
    "baseUrl": "https://pulsoid.net/oauth2/authorize",
    "client_id": bytes.fromhex("64666163653963612d306663622d346233312d383837342d646434616461646262623037").decode(),
    "redirect_uri": "",
    "response_type": "token",
    "scope": "data:heart_rate:read",
    "state": str(uuid.uuid4()).replace("-", ""),
    "response_mode": "web_page"
}

# Helper functions
def read_file(path):
    """Reads a file if it exists; returns empty string if not."""
    return open(path, "r").read() if os.path.exists(path) else ""

def string_is_null_or_empty(s):
    """Check if a string is None or empty."""
    return s is None or s == ""

def write_file(path, content):
    """Writes content to a file."""
    with open(path, "w") as f:
        f.write(content)

# Pulsoid authentication
def pulsoid_auth_page():
    """Generates Pulsoid authorization URL."""
    return (f"{PULSOID_API['baseUrl']}?client_id={PULSOID_API['client_id']}&redirect_uri={PULSOID_API['redirect_uri']}"
            f"&response_type={PULSOID_API['response_type']}&scope={PULSOID_API['scope']}&state={PULSOID_API['state']}"
            f"&response_mode={PULSOID_API['response_mode']}")

async def start_auth():
    """Initiates Pulsoid authentication."""
    print("Open Pulsoid Auth Page...")
    os.system(f"start {pulsoid_auth_page()}")
    token = input("Enter Pulsoid Auth Token: ")
    if string_is_null_or_empty(token):
        print("No Enter.")
        return None
    write_file("token.txt", token)
    print("token.txt saved.")
    return token

# WebSocket connection for heart rate
class PulsoidWS:
    def __init__(self, ip="dev.pulsoid.net", path="/api/v1/data/real_time", token=None):
        self.url = f"wss://{ip}{path}?access_token={token}"
        self.ws = None
        self.hb_toggle = False

    async def connect(self):
        async with websockets.connect(self.url) as ws:
            self.ws = ws
            print("Connected to Pulsoid.")
            await self.receive_data()

    async def receive_data(self):
        """Receives data and sends heart rate to OSC."""
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            try:
                msg = await self.ws.recv()
                data = json.loads(msg)
                heart_rate = data.get("data", {}).get("heart_rate", 0)
                print(f"Got heart rate: {heart_rate} bpm")

                heart_rate_params = [
                    ("/avatar/parameters/Heartrate", float(heart_rate) / 127 - 1),
                    ("/avatar/parameters/HeartRateFloat", float(heart_rate) / 127 - 1),
                    ("/avatar/parameters/Heartrate2", float(heart_rate) / 255),
                    ("/avatar/parameters/HeartRateFloat01", float(heart_rate) / 255),
                    ("/avatar/parameters/Heartrate3", heart_rate),
                    ("/avatar/parameters/HeartRateInt", heart_rate),
                    ("/avatar/parameters/HeartBeatToggle", self.hb_toggle)
                ]
                for address, value in heart_rate_params:
                    osc_message = f"{address} {value}"
                    client.sendto(osc_message.encode(), ("localhost", 9000))
                    if address == "/avatar/parameters/HeartBeatToggle":
                        self.hb_toggle = not self.hb_toggle
            except json.JSONDecodeError:
                print(f"Failed to parse data: {msg}")
                continue

# Main application
async def main():
    token = read_file("token.txt")
    if string_is_null_or_empty(token):
        token = await start_auth()
        if token is None:
            print("Failed to retrieve token.")
            return
    pulsoid_ws = PulsoidWS(token=token)
    await pulsoid_ws.connect()

# Run the application
if __name__ == "__main__":
    asyncio.run(main())
