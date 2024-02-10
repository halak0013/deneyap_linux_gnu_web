import json
import re
from common.Logging import Log
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

    async def run_command(self, command, websocket=None, print_on_ui=None):
        self.l.log("Running command: " + command, "i")
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
        while True:
            line = process.stdout.readline()
            if not line:
                break
            # Satır sonundaki newline karakterini kaldır
            line = line.rstrip()
            self.l.log(line, "i")
            if print_on_ui:
                print_on_ui(line)
            output += line + '\n'
            if websocket:
                await websocket.send(json.dumps({"command": "consoleLog", "log": self.remove_ansi_color_codes(line)+"\n"}))

        # Hata çıktısını oku
        error = process.stderr.read()
        if error:
            self.l.log("Subprocces error: " + error.decode(), "e")

        return output

    def remove_ansi_color_codes(self, text):
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', text)
