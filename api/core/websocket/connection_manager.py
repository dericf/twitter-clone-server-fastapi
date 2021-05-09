# FastAPI
from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder

# Standard Library
from typing import Union, Dict, Any
import json
from datetime import date, datetime

from ...schemas.websockets import WSMessage, WSMessageAction


class ConnectionManager:
    def __init__(self):
        # Map user id to a websocket
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        try:
            await websocket.accept()
            self.active_connections[user_id] = websocket
        except Exception as e:
            print("Error connecting", e)

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
            await self.active_connections[user_id].send_text(json.dumps(jsonable_encoder(message)))
        except:
            print("Error Sending Message")

    async def broadcast(self, message: Union[Dict, WSMessage[Any]], current_user_id: int):
        for user_id, connection in self.active_connections.items():
            if(current_user_id != user_id):
                try:
                    await connection.send_json(jsonable_encoder(message))
                except:
                    print(f"could not send to user: {user_id}")

    def user_is_online(self, user_id: int):
        return user_id in self.active_connections

    async def show_all_connections(self):
        print("\n** Listing Active WebSocket Connections **")
        for user_id, connection in self.active_connections.items():
            print(f"\tUser ID: {user_id} |  Conn: {connection}")
        print("********************************\n")


ws_manager = ConnectionManager()
