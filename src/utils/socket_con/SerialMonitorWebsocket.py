import asyncio
import json
import serial
import websockets
from static.configs import Configs as cf

from common.Logging import Log

# https://github.com/deneyapkart/Deneyap-Kart-Web/blob/main/SerialMonitorWebsocket.py


class SerialMonitorWebsocket:
    def __init__(self, pro):
        print("WebSocket started")
        self.l = Log()
        self.websocket = None
        self.serialOpen = False
        self.ser = None
        self.log_loop = None
        self.pro = pro

    async def start_server(self, url, port):
        ws = await websockets.serve(self.mainLoop, url, port)

    async def mainLoop(self, websocket, path):
        self.websocket = websocket
        while cf.is_websocket_running and cf.is_main_thread_running:
            try:
                if not self.serialOpen:
                    await asyncio.sleep(.3)
                body = {"command": None}
                try:
                    message = await websocket.recv()
                    self.l.log(
                        f"SerialMonitorWebsocket received {message}", "i")
                    body = json.loads(message)

                except (asyncio.TimeoutError, ConnectionRefusedError) as e:
                    if self.serialOpen:
                        self.l.log("Serial Monitor Timeout Error: ", str(e))
                        await self.serialLog()
                    raise e
                await self.commandParser(body)

            except Exception as e:
                self.l.log("Serial Monitor Error: ", "e")
                bodyToSend = {"command": "serialLog", "log": str(e)+"\n"}
                bodyToSend = json.dumps(bodyToSend)
                await self.websocket.send(bodyToSend)
                raise e
        await self.websocket.close()
        self.l.log("Serial Monitor Websocket closed", "i")

    async def commandParser(self, body: dict) -> None:

        command = body['command']

        if command == None:
            return
        else:
            await self.sendResponse()

        if command == "upload":
            await self.closeSerialMonitor()
        elif command == "openSerialMonitor":
            self.openSerialMontor(body["port"], body["baudRate"])
        elif command == "closeSerialMonitor":
            await self.closeSerialMonitor()
        elif command == "serialWrite":
            self.serialWrite(body["text"])

    async def sendResponse(self) -> None:

        bodyToSend = {"command": "response"}
        bodyToSend = json.dumps(bodyToSend)
        self.l.log("SerialMonitorWebsocket sending response back", "i")
        await self.websocket.send(bodyToSend)

    def serialWrite(self, text: str) -> None:

        if self.serialOpen:
            self.l.log(f"Writing to serial, data:{text}", "i")
            self.ser.write(text.encode("utf-8"))

    def openSerialMontor(self, port: str, baudRate: int) -> None:

        self.l.log("Opening serial monitor", "i")
        if not self.serialOpen:
            self.serialOpen = True

            self.ser = serial.Serial()
            self.ser.baudrate = baudRate
            self.ser.port = port
            self.log_loop = asyncio.create_task(self.serial_log_loop())

            if cf.board == cf.deneyapKart:
                self.ser.setDTR(False)
                self.ser.setRTS(False)
                self.ser.open()

            elif cf.board == cf.deneyapKart1A:
                self.ser.setDTR(False)
                self.ser.setRTS(False)
                self.ser.open()

            elif cf.board == cf.deneyapKartG:
                self.ser.setDTR(True)
                self.ser.setRTS(True)
                self.ser.open()

            else:
                self.ser.setDTR(True)
                self.ser.setRTS(True)
                self.ser.open()

    async def closeSerialMonitor(self) -> None:
        self.l.log("Closing serial monitor", "i")
        if self.serialOpen and self.ser != None:
            self.ser.close()
            bodyToSend = {"command": "closeSerialMonitor"}
            bodyToSend = json.dumps(bodyToSend)
            self.log_loop.cancel()
            print("log loop cancelled")
            await self.websocket.send(bodyToSend)

        self.serialOpen = False

    async def serial_log_loop(self):
        while self.serialOpen and self.ser is not None:
            try:
                if self.ser.in_waiting > 0:
                    await self.serialLog()
                else:
                    await asyncio.sleep(0.05)
            except serial.SerialException as e:
                self.l.log(e, "e")
                await asyncio.sleep(1)

    async def serialLog(self) -> None:
        if self.serialOpen and self.ser != None:
            try:
                waiting = self.ser.in_waiting
                line = self.ser.read(waiting).decode("utf-8")
            except serial.SerialException:
                await self.closeSerialMonitor()
                return
            except:
                return
            if line == "":
                return
            print(line)
            bodyToSend = {"command": "serialLog", "log": line}
            bodyToSend = json.dumps(bodyToSend)
            await self.websocket.send(bodyToSend)
