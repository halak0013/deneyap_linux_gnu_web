import json
from locale import gettext as _
from static.commands import Commands as co
from static.file_paths import Paths as p
from common.AsyncProc import CommandRunner

import os


class Process:
    # TODO: buralara loglama eklenecek
    # TODO: çalışan kod çıktıları loglanacak
    # TODO: hata durumlarında belirlenecek
    def __init__(self, messageDialog):
        self.cr = CommandRunner()
        self.messageDialog = messageDialog

    async def compile_code(self, bord, code):
        # TODO: bu kısmılaraın göndermelerine bakılcak
        p.file_check(p.deneyap_pro)
        os.chdir(p.deneyap_pro)
        with open("deneyap_pro.ino", "w") as f:
            f.write(code)
        os.chdir(p.deneyap_p_f)
        await self.cr.run_command(co.compile_code(bord))

    async def compile_upload(self, board, port, code):
        co.port = port
        await self.check_port_permission()
        await self.compile_code(board, code)

        await self.cr.run_command(co.upload_code(port, board))

    async def board_infos(self):
        boards = await self.cr.run_command(co.a_cli_board_list)
        print(boards)
        body = {"command": "returnBoards", "boards": []}
        u = _("Unknown")
        for p in json.loads(boards):
            body["boards"].append({"boardName": u, "port": p['port']['label']})
        return json.dumps(body,indent=4)

    async def get_core_version(self):
        ver = {}
        with open(p.d_json_path, 'r') as f:
            ver = json.load(f)
        version = ver["packages"][0]["platforms"][0]["version"]
        bodyToSend = {"command": "returnCoreVersion", "version": version}
        return json.dumps(bodyToSend)

    async def get_version(self):
        return json.dumps({"command": "returnVersion", "version": p.AGENT_VERSION})

    async def searcn_lib(self, lib):
        libs = await self.cr.run_command(co.search_lib(lib))
        bodyToSend = {
            "command": "searchLibraryResult",
            "libraries": libs
        }
        return json.dumps(bodyToSend)
    
    async def download_lib(self, lib, version):
        res = await self.cr.run_command(co.download_lib(lib, version))
        bodyToSend = {
            "command": "downloadLibraryResult",
            "result": res
        }
        return json.dumps(bodyToSend)

    async def check_port_permission(self):
        res = await self.cr.run_command(co.check_port_permission(co.port))
        if 'rw' not in res.splitlines()[0].split()[0]:
            self.messageDialog.set_visible(True)
            self.messageDialog.set_markup(
                _("You don't have permission to access the port.\nDo you want to give permission?"))
            return False
        return True

    async def add_port_permission(self):
        await self.cr.run_command(co.port_user_permission)
        await self.cr.run_command(co.add_port_permission(co.port))
        self.messageDialog.set_visible(False)
        self.messageDialog.set_markup("")
