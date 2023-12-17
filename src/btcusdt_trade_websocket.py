import asyncio
import websockets
import json
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)

async def logdata(json_message):
    print("Trade: ", json_message)
    print("----------------------------------")

async def binance_ws(callback):
    url = "wss://stream.binance.com:9443/ws/imxusdt@trade"

    while True:
        try:
            async with websockets.connect(url) as websocket:
                while True:
                    message = await websocket.recv()
                    await callback(json.loads(message))
        except Exception as e:
            logging.error(f"WebSocket error: {e}")
            logging.info("Attempting to reconnect...")
            await asyncio.sleep(5)  # Sleep for a short time before retrying

if __name__ == '__main__':
    asyncio.run(binance_ws(logdata))
