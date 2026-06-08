from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

# Administrador de conexiones WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
def home_tickets():
    return {"modulo": "Tickets y Llamados", "estado": "Operativo"}

# Endpoint WebSocket: Aquí se conectan las "pantallas de la sala de espera"
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Mantenemos la conexión viva
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Endpoint REST: El médico llama a un paciente y esto dispara un mensaje por WebSocket
@app.post("/llamar/{paciente}/{box}")
async def llamar_paciente(paciente: str, box: str):
    mensaje = f"ATENCIÓN: Paciente {paciente} dirigirse al Box {box}"
    await manager.broadcast(mensaje)
    return {"status": "Llamado emitido", "mensaje": mensaje}
