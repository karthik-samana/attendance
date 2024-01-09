# myapp/consumers.py

import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

class TimerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Simulate timer update every second (replace with your logic)
        timer_value = 0  # Initial timer value
        while True:
            await asyncio.sleep(1)
            timer_value += 1  # Increment the timer value

            # Send the updated timer value to all connected clients
            await self.send(text_data=str(timer_value))
