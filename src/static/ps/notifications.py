import asyncio
import json

import js
import websockets

AUTH_DATA = js.localStorage.getItem("auth_data")
TOKEN = json.loads(AUTH_DATA)["token"]


async def receive_notification():
    url = f"ws://localhost:8000/api/notifs/me?token={TOKEN}"
    async with websockets.connect(url) as websocket:
        print("WebSocket connection established.")

        try:
            while True:
                message = await websocket.recv()
                print(f"Received message: {message}")
        except websockets.ConnectionClosed:
            print("WebSocket connection closed.")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(receive_notification())
