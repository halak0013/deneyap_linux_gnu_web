import yaml
import locale
from locale import gettext as _
from gi.repository import GLib, Gtk
from static.commands import Commands as co
from AsyncProc import AsyncFileDownloader, CommandRunner
import threading
import os
import asyncio
import gi
gi.require_version("Gtk", "3.0")


class Installer:
    def __init__(self, messageDialog: Gtk.MessageDialog):
        self.cr = CommandRunner()
        self.afd = AsyncFileDownloader()
        self.messageDialog = messageDialog

    async def install(self, lb_st: Gtk.Label, lb_op: Gtk.Label):
        self.preaparing(lb_st, lb_op, _("Generating project path..."))
        self.file_check(co.bin_path)

        self.preaparing(
            lb_st, lb_op, _("Downloading arduino-cli and installing..."))
        await self.cr.run_command(co.arduino_cli_install)

        self.preaparing(lb_st, lb_op, _("Downloading Deneyap Board core..."))
        t_downlod = asyncio.create_task(self.afd.download_data(
            co.deneyap_url, co.arduino15_path, co.d_json_name))

        self.preaparing(
            lb_st, lb_op, _("Deneyap Board configuration preaparing..."))
        await self.cr.run_command(co.a_cli_init)
        self.configure_yaml()
        await t_downlod

        self.preaparing(lb_st, lb_op, _("Deneyap Board core installing..."))
        await self.cr.run_command(co.a_cli_deneyap_install)

        self.preaparing(lb_st, lb_op, _("Deneyap Board index updating..."))
        await self.cr.run_command(co.a_cli_update_index)

    def preaparing(self, lb_st: Gtk.Label, lb_op: Gtk.Label, text):
        lb_st.set_text(text)
        lb_op.set_text(text+lb_op.get_text())

    async def compile_upload(self, board, port):
        self.file_check(co.deneyap_pro)
        os.chdir(co.deneyap_pro)
        await self.cr.run_command(co.compile_code(board))
        await self.cr.run_command(co.upload_code(port, board))

    def file_check(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def configure_yaml(self):
        with open(co.d_yaml_path, 'r') as file:
            config = yaml.safe_load(file)

        config['board_manager']['additional_urls'].append(co.deneyap_url)

        with open(co.d_yaml_path, 'w') as file:
            yaml.dump(config, file)

    async def board_name(self) -> dict:
        board_dict = {}
        input_string = await self.cr.run_command(co.a_cli_board_list_all)
        # print(input_string,co.a_cli_board_list_all)
        lines = input_string.strip().split("\n")
        for line in lines:
            if line.startswith("Board Name"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                board_name = " ".join(parts[:-1])
                fqbn = parts[-1]
                board_dict[board_name] = fqbn
        print(board_dict)
        return board_dict

    async def port_name(self):
        board_str = await self.cr.run_command(co.a_cli_board_list)
        words = board_str.split()
        port = list(filter(lambda word: "/dev/" in word, words))[0]

        port_permission = await self.cr.run_command("ls -l "+port)
        if port_permission.startswith("crw"):
            return port
        else:
            self.messageDialog.set_visible(True)
            self.messageDialog.set_markup(
                _(f"You don't have permission to use {port} port.\nDo you want to give permission."))
            co.port = port
        return port

    async def add_port_permission(self):
        await self.cr.run_command(co.port_user_permission)
        await self.cr.run_command(co.add_port_permission(co.port))
        self.messageDialog.set_visible(False)
        self.messageDialog.set_markup("")

