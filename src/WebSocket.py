import asyncio
import json
import websockets
from multiprocessing import Queue
from common.Logging import Log
from Proccess import Process


class WebSocket:
    
    def __init__(self, url, port, pro):
        print("WebSocket started")
        self.queue = Queue() # TODO: ileride eklenebilir
        self.log = Log()
        self.websocket = None
        self.pro = pro
        self.ws = websockets.serve(self.mainLoop, url, port)
        asyncio.get_event_loop().run_until_complete(self.mainLoop)
        asyncio.get_event_loop().run_forever()

    async def mainLoop(self, websocket, path):
        # TODO: kuyruk eklenebilir
        self.websocket = websocket
        try:
            while True:
                body = {"command":None}
                msg = await asyncio.wait_for(self.ws.recv(), timeout=1)
                body = json.loads(msg)
                await self.commandParser(body)

        except Exception as e:
            self.log.log(str(e), "e")
            print(e)

    async def commandParser(self, body: dict) -> None:
        """
        message send from front-end is first comes to here to redirect appropriate function
        messages related to main communication comes to this class. other messages goes to SerialMonitor class.
        upload message is sent both this class and SerialMonitor class. when new code is uploading serial monitor has to be closed.

        :param body: data that sent from front-end. %100 has 'command' other keys are depended on command
        :type body: dict
        """
        command = body['command']
        res = None

        if command == None:
            return
        else:
            await self.sendResponse()

        if command == "upload":
            await self.pro.compile_upload(body['board'], body['port'], body["code"])
        elif command == "compile":
            await self.pro.compile_upload(body['board'], body['port'])
        elif command == "getBoards":
            res = await self.pro.board_infos()
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

        await self.websocket.send(res)

    async def sendResponse(self) -> None:
        bodyToSend = {"command": "response"}
        bodyToSend = json.dumps(bodyToSend)
        await self.websocket.send(bodyToSend)