# FastAPI
from fastapi import WebSocket

# Standard Library
from typing import Union, Dict
import json
from datetime import date, datetime


class ConnectionManager:
    def __init__(self):
        # Map user id to a websocket
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    async def disconnect(self, user_id: int):
        try:
            await self.active_connections[user_id].close()
            self.active_connections.pop(user_id)
        except:
            print("Error disconnecting...")

    async def send_personal_message(self, message: Union[Dict, str], user_id: int):
        # TODO: I need to work out a better way to send proper json
        # print("user is online? ", user_id in self.active_connections)
        if user_id not in self.active_connections:
            return
        if type(message) is str:
            message = {"message": message}
        try:
            await self.active_connections[user_id].send_text(json.dumps(message))
        except:
            print("Error Sending Message")

    async def broadcast(self, message: Dict):
        for user_id, connection in self.active_connections.items():
            try:
                await connection.send_json(message)
            except:
                print(f"could not send to user: {user_id}")

    async def show_all_connections(self):
        print("\n** Listing Active WebSocket Connections **")
        for user_id, connection in self.active_connections.items():
            print(f"\tUser ID: {user_id} |  Conn: {connection}")
        print("********************************\n")


ws_manager = ConnectionManager()
