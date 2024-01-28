from static.commands import Commands as co

import requests
import os
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

    async def run_command(self, command):
        self.process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            env=co.env,
            preexec_fn=os.setsid
        )

        line = "tmp"
        output = ""
        while line:
            line = self.process.stdout.readline()
            line = line.replace('\n\n', '\n')
            print(line)
            output += line
        return output

