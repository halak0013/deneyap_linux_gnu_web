import yaml
from locale import gettext as _
from gi.repository import Gtk
from static.commands import Commands as co
from static.file_paths import Paths as p
from common.AsyncProc import AsyncFileDownloader, CommandRunner
from common.Logging import Log
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
        self.l = Log()

    def check(self):
        if not os.path.exists(p.arduino_cli.strip()):
            return False
        if not os.path.exists(p.arduino15_path):
            return False
        if not os.path.exists(p.d_yaml_path):
            return False
        return True

    async def install(self, lb_st: Gtk.Label, lb_op: Gtk.Label):
        try:
            self.preaparing(lb_st, lb_op, _("Generating project paths..."))
            p.file_check(p.bin_path)
            p.file_check(p.log_path)

            self.preaparing(
                lb_st, lb_op, _("Downloading arduino-cli and installing..."))
            await self.cr.run_command(co.arduino_cli_install)

            self.preaparing(lb_st, lb_op, _(
                "Downloading Deneyap Board core..."))
            t_downlod = asyncio.create_task(self.afd.download_data(
                co.deneyap_url, co.arduino15_path, co.d_json_name))

            self.preaparing(
                lb_st, lb_op, _("Deneyap Board configuration preaparing..."))
            await self.cr.run_command(co.a_cli_init)
            self.configure_yaml()
            await t_downlod

            self.preaparing(lb_st, lb_op, _(
                "Deneyap Board core installing..."))
            await self.cr.run_command(co.a_cli_deneyap_install)

            self.preaparing(lb_st, lb_op, _("Deneyap Board index updating..."))
            await self.cr.run_command(co.a_cli_update_index)
        except Exception as e:
            self.l.log(str(e), "e")
            self.messageDialog.set_markup(_("An error occured.")+"\n"+str(e))
            self.messageDialog.set_visible(True)

    def preaparing(self, lb_st: Gtk.Label, lb_op: Gtk.Label, text):
        lb_st.set_text(text)
        lb_op.set_text(text+lb_op.get_text())
        self.l.log(text, "i")


    def configure_yaml(self):
        with open(co.d_yaml_path, 'r') as file:
            config = yaml.safe_load(file)

        config['board_manager']['additional_urls'].append(co.deneyap_url)

        with open(co.d_yaml_path, 'w') as file:
            yaml.dump(config, file)
            