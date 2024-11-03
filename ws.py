import asyncio
from websockets.sync.client import connect
from websockets.exceptions import WebSocketException
from websockets.server import serve


def send_ws_message(text: str):
    try:
        with connect("ws://localhost:8765") as websocket:
            websocket.send(text)
    except WebSocketException as e:
        print(f"WebSocket error: {e}")
    except ConnectionError as e:
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":

    async def echo(websocket):
        async for message in websocket:
            print(f"Received: {message}")

    async def main():
        async with serve(echo, "localhost", 8765):
            await asyncio.get_running_loop().create_future()

    asyncio.run(main())
