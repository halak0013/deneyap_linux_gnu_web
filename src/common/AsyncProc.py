import json
import re
from common.Logging import Log
from static.configs import Configs as cf
import requests
import os
import subprocess

import gi
gi.require_version("Gtk", "3.0")


class AsyncFileDownloader:

    async def download_data(self, url, path, name):
        try:
            r = requests.get(url, stream=True)

            with open(path+name, "wb") as f:
                for c in r.iter_content(chunk_size=1024):
                    if c:
                        f.write(c)
        except Exception as e:
            print(e)
            raise e


class CommandRunner:
    def __init__(self):
        self.l = Log()
        self.old_log_c = ""
        self.old_log_o = ""

    async def run_command(self, command, websocket=None, print_on_ui=None):

        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            env=os.environ.copy(),
            preexec_fn=os.setsid
        )

        output = ""
        while cf.is_main_thread_running:
            line = process.stdout.readline()
            if not line:
                break
            # Satır sonundaki newline karakterini kaldır
            line = line.rstrip()
            if print_on_ui:
                print_on_ui(line)
            output += line + '\n'
            if websocket:
                await websocket.send(json.dumps({"command": "consoleLog", "log": self.remove_ansi_color_codes(line)+"\n"}))

        if output != self.old_log_o or command != self.old_log_c:
        #if True:
            self.l.log("Command output:\n" + output, "i")
            self.l.log("Running command:\n" + command, "i")
            self.old_log_c = command
            self.old_log_o = output

        # Hata çıktısını oku
        error = process.stderr.read()
        if error:
            self.l.log("Subprocces error: " + error, "e")
            #hata her zaman olabilir. isteller dışında da gönderilmesi gerekibilir
            await cf.websocket.send(json.dumps({"command": "consoleLog", "log": self.remove_ansi_color_codes(error)+"\n"}))
        if cf.is_main_thread_running:
            process.terminate()
        return output

    def remove_ansi_color_codes(self, text):
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', text)
