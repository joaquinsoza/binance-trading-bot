import asyncio
import websockets
import json
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)

async def binance_ws(callback):
    url = "wss://stream.binance.com:9443/ws/btcusdt@trade"

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
