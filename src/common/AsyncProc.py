import json
import re
from static.commands import Commands as co

import requests
import os
import asyncio
import subprocess

import gi
gi.require_version("Gtk", "3.0")


class AsyncFileDownloader:

    async def download_data(self, url, path, name):
        r = requests.get(url, stream=True)

        with open(path+name, "wb") as f:
            for c in r.iter_content(chunk_size=1024):
                if c:
                    f.write(c)


class CommandRunner:

    async def run_command(self, command, websocket=None):
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=os.environ.copy(),
            preexec_fn=os.setsid
        )

        output = ""
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            line = line.decode("utf-8").rstrip()  # Satır sonundaki newline karakterini kaldır
            print(line)
            output += line + '\n'
            if websocket:
                await websocket.send(json.dumps({"command": "consoleLog", "log": self.remove_ansi_color_codes(line)+"\n"}))

        # Hata çıktısını oku
        error = await process.stderr.read()
        if error:
            print("Hata:", error.decode())

        return output

    def remove_ansi_color_codes(self, text):
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', text)
