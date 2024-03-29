from gi.repository import Gtk, GLib
from locale import gettext as _
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
            self.lb_st = lb_st
            self.lb_op = lb_op
            self.preaparing(_("Generating project paths...\n"))
            p.file_check(p.bin_path)
            p.file_check(p.log_path)

            self.preaparing(
                _("Downloading arduino-cli and installing...\n"))
            await self.cr.run_command(co.arduino_cli_install, print_on_ui = self.show_output)

            self.preaparing(
                _("Deneyap Board configuration preaparing...\n"))
            await self.cr.run_command(co.a_cli_init, print_on_ui = self.show_output)

            self.preaparing(_(
                "Downloading Deneyap Board core...\n"))
            await self.cr.run_command(co.a_cil_add_deneyap_url, print_on_ui = self.show_output)

            self.preaparing(_(
                "Deneyap Board core installing...\n"))
            await asyncio.sleep(1)
            await self.cr.run_command(co.a_cli_deneyap_install, print_on_ui = self.show_output)

            self.preaparing(_("Deneyap Board index updating...\n"))
            await self.cr.run_command(co.a_cli_update_index, print_on_ui = self.show_output)
            # stck_switcher.set_visible_child_name("main")
            self.preaparing(_("Installing succesed, please close Deneyap app from your taskbar icon and restart it\n"))
        except Exception as e:
            self.l.log(str(e), "e")
            self.messageDialog.set_markup(_("An error occured.")+"\n"+str(e))
            self.messageDialog.set_visible(True)
            raise e

    def preaparing(self, text):
        GLib.idle_add(self.lb_st.set_text, text)
        GLib.idle_add(self.lb_op.set_text, text+ "\n" +self.lb_op.get_text())
        # lb_op.set_text(text+lb_op.get_text())
        self.l.log(text, "i")

    def show_output(self, text):
        GLib.idle_add(self.lb_st.set_text, text)
