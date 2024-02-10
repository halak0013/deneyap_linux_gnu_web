#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import subprocess


def generate_mo_files():
    podir = "po"
    mo = []
    for po in os.listdir(podir):
        if po.endswith(".po"):
            os.makedirs("{}/{}/LC_MESSAGES".format(podir,
                        po.split(".po")[0]), exist_ok=True)
            mo_file = "{}/{}/LC_MESSAGES/{}".format(
                podir, po.split(".po")[0], "deneyap.mo")
            msgfmt_cmd = 'msgfmt {} -o {}'.format(podir + "/" + po, mo_file)
            subprocess.call(msgfmt_cmd, shell=True)
            mo.append(("/usr/share/locale/" + po.split(".po")[0] + "/LC_MESSAGES",
                       ["po/" + po.split(".po")[0] + "/LC_MESSAGES/deneyap.mo"]))
    return mo


changelog = "debian/changelog"
if os.path.exists(changelog):
    head = open(changelog).readline()
    try:
        version = head.split("(")[1].split(")")[0]
    except:
        print("debian/changelog format is wrong for get version")
        version = "0.0.0"
    f = open("data/version", "w")
    f.write(version)
    f.close()

data_files = [
    ("/usr/bin", ["deneyap"]),

    ("/usr/share/applications",
     ["tr.org.deneyap.desktop"]),  # /usr/share/icons

    ("/usr/share/icons",
     ["data/deneyap.svg"]),

    ("/usr/share/icons/hicolor/scalable/apps/",
     ["data/deneyap.svg"]),



    ("/usr/share/deneyap/ui",
     ["ui/deneyap.glade"]),

    ("/usr/share/deneyap/src",
     ["src/MainWindow.py",
      "src/Main.py",]),

    ("/usr/share/deneyap/src/utils",
     ["src/utils/Installer.py",
      "src/utils/Process.py"
      ]),

    ("/usr/share/deneyap/src/utils/socket_con",
     ["src/utils/socket_con/WebSocket.py",
      "src/utils/socket_con/SerialMonitorWebsocket.py"
      ]),

    ("/usr/share/deneyap/src/static",
     ["src/static/commands.py",
      "src/static/configs.py",
      "src/static//file_paths.py"
      ]),

    ("/usr/share/deneyap/src/common",
     ["src/common/AsyncProc.py",
      "src/common/Logging.py"
      ]),

    ("/usr/share/deneyap/data",
     ["data/deneyap.svg",
      "data/version"]),

] + generate_mo_files()

setup(
    name="deneyap",
    version=version,
    packages=find_packages(),
    scripts=["deneyap"],
    install_requires=["PyGObject", "serial",
                      "requests", "pyyaml", "websockets", "coloredlogs"],
    data_files=data_files,
    author="Muhammet Halak",
    author_email="halak@vuhuv.com",
    description="Deneyap web communication for Linux Pardus",
    license="GPLv3",
    keywords="deneyap, kart, pardus",
    url="https://github.com/halak0013/deneyap_linux_gnu_web",
)
