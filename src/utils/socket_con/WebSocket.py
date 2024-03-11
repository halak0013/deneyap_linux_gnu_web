import asyncio
import json
import websockets
from multiprocessing import Queue
from common.Logging import Log
from static.configs import Configs as cf


class WebSocket:
    
    def __init__(self, pro):
        print("WebSocket started")
        self.queue = Queue() # TODO: ileride eklenebilir
        self.l = Log()
        self.websocket = None
        self.pro = pro
        self.board_infos = None

    async def start_server(self, url, port):
        await websockets.serve(self.mainLoop, url, port)

    async def mainLoop(self, websocket, path):
        # TODO: kuyruk eklenebilir
        self.websocket = websocket
        cf.websocket = websocket
        print("websocket started")
        chck_board = asyncio.create_task(self.check_board())
        try:
            while cf.is_websocket_running and cf.is_main_thread_running:
                body = {"command": None}
                #msg = await asyncio.wait_for(websocket.recv(), timeout=5)
                msg = await websocket.recv()
                print("msg", msg)
                body = json.loads(msg)
                await self.commandParser(body)
            await self.websocket.close()
            chck_board.cancel()
            self.l.log("Serial Monitor Websocket closed", "i")
        except Exception as e:
            print("armut")
            self.l.log(str(e), "e")
            print(e)
            raise e

    async def commandParser(self, body: dict) -> None:
        command = body['command']
        res = None

        if command == None:
            return
        else:
            await self.sendResponse()
        if command == "upload":
            await self.pro.compile_upload(body['board'], body['port'], body["code"])
        elif command == "compile":
            #await self.pro.compile_upload(body['board'], body['port'], body["code"])
            await self.pro.compile_code(body['board'], body['code'])
        elif command == "getBoards":
            res = await self.pro.board_infos()
            self.board_infos = res
        elif command == "getVersion":
            res = await self.pro.get_version()
        elif command == "changeVersion":
            #TODO: diğer versiyonlarda eklenecek
            pass
        elif command == "searchLibrary":
            res = await self.pro.searcn_lib(body['searchTerm'])
        elif command == "downloadLibrary":
            res = await self.pro.download_lib(body['libName'], body['libVersion'])
        elif command == "getCoreVersion":
            res = await self.pro.get_core_version()
        await asyncio.sleep(1)
        if res != None:
            print("res", res)
            await self.websocket.send(res)

    async def sendResponse(self) -> None:
        bodyToSend = {"command": "response"}
        bodyToSend = json.dumps(bodyToSend)
        await self.websocket.send(bodyToSend)

    async def check_board(self):
        while cf.is_websocket_running and cf.is_main_thread_running:
            res = await self.pro.board_infos()
            if res != None and res != self.board_infos:
                print("res", res)
                self.board_infos = res
                await self.websocket.send(res)
                await cf.upadet_board_fn()
            else:
                await asyncio.sleep(1)
                continue
            await asyncio.sleep(1)
            continue