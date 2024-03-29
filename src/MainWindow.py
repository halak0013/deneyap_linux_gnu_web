#Bismillahirrahmanirrahim
from utils.socket_con.SerialMonitorWebsocket import SerialMonitorWebsocket
from utils.socket_con.WebSocket import WebSocket
from utils.Installer import Installer
from utils.Process import Process
from static.configs import Configs as cf
from threading import Thread
import locale
from locale import gettext as _
import os
import gi
import asyncio
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, Gio


# https://github.com/pardus/pardus-update/blob/f53931dcdb9743ec0bcf7f5574bcddc3d8246c2a/src/MainWindow.py#L23
try:
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import AppIndicator3
except:
    # fall back to Ayatana
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as AppIndicator3

# Translation Constants:
APPNAME = "deneyap"
TRANSLATIONS_PATH = "/usr/share/locale"
# SYSTEM_LANGUAGE = os.environ.get("LANG")

# Translation functions:
locale.bindtextdomain(APPNAME, TRANSLATIONS_PATH)
locale.textdomain(APPNAME)
# locale.setlocale(locale.LC_ALL, SYSTEM_LANGUAGE)


class MainWindow(Gtk.Window):
    def __init__(self, application):
        # Gtk Builder
        self.application = application
        self.builder = Gtk.Builder()

        # Translate things on glade:
        self.builder.set_translation_domain(APPNAME)

        self.builder.add_from_file(os.path.dirname(
            os.path.abspath(__file__)) + "/../ui/deneyap.glade")
        self.builder.connect_signals(self)

        # Add Window
        self.window: Gtk.Window = self.builder.get_object("window")
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.set_application(application)
        self.window.set_default_size(400, 300)
        # self.window.connect('destroy', application.onExit)
        self.window.connect("delete-event", self.on_delete_event)
        # self.window.set_wmclass("my_app", "MyApp")

        self.defineComponents()

        self.init_variables()

        self.window.show_all()

        self.stck_swither.hide()

    def init_variables(self):
        self.ins = Installer(self.dialog_info)
        self.pro = Process(self.message_dialog_port)
        self.is_reset_clicked = False

        self.indicator = AppIndicator3.Indicator.new(
            "notifier",
            os.path.dirname(
                os.path.abspath(__file__)) + "/../data/deneyap.svg",  # İkonunuzun dosya yolunu buraya ekleyin
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_title("Deneyap")

        self.menu = Gtk.Menu()

        self.quit_item = Gtk.MenuItem(label=_("Quit"))
        self.quit_item.connect("activate", self.destroy)
        self.menu.append(self.quit_item)

        self.open_item = Gtk.MenuItem(label=_("Open"))
        self.open_item.connect("activate", self.on_open_item_activate)
        self.menu.append(self.open_item)
        
        self.log_item = Gtk.MenuItem(label=_("Log"))
        self.log_item.connect("activate", self.on_log_item_activate)
        self.menu.append(self.log_item)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)

        if not self.ins.check():
            self.stack_main.set_visible_child_name("install")
        else:
            self.stack_main.set_visible_child_name("main")
            asyncio.run(self.board_info())
            cf.upadet_board_fn = self.board_info
            Thread(target=self.startWebsocket).start()

    def startWebsocket(self):
        #loop = GLib.MainLoop() değiştirilebilir
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        w = WebSocket(self.pro)
        ws = SerialMonitorWebsocket(self.pro)
        loop.run_until_complete(w.start_server("localhost", 49182))
        loop.run_until_complete(ws.start_server("localhost", 49183))
        loop.run_forever()

    def defineComponents(self):
        self.btn_about: Gtk.Button = self.builder.get_object("btn_about")
        self.dialog_about: Gtk.AboutDialog = self.builder.get_object(
            "dialog_about")

        self.stack_main: Gtk.Stack = self.builder.get_object("stack_main")
        self.stck_swither = self.builder.get_object("stck_swither")

        self.lb_subpro_output: Gtk.Label = self.builder.get_object(
            "lb_subpro_output")
        self.lb_dialog_wait_status: Gtk.Label = self.builder.get_object(
            "lb_dialog_wait_status")

        self.lb_board_info: Gtk.Label = self.builder.get_object(
            "lb_board_info")

        self.btn_install: Gtk.Button = self.builder.get_object("btn_install")

        self.message_dialog_port: Gtk.MessageDialog = self.builder.get_object(
            "message_dialog_port")
        self.dialog_info: Gtk.MessageDialog = self.builder.get_object(
            "dialog_info")

    async def board_info(self):
        b_info = await self.pro.ui_board_infos()
        GLib.idle_add(self.lb_board_info.set_text, b_info)

    def on_btn_about_clicked(self, b):
        #https://github.com/pardus/pardus-image-writer/blob/master/src/MainWindow.py#L221
        self.dialog_about.run()
        self.dialog_about.hide()

    def on_btn_install_clicked(self, b):
        self.stack_main.set_visible_child_name("wait")
        Thread(target= self.install_cli).start()
    
    def install_cli(self):
        asyncio.run(self.ins.install(
            self.lb_dialog_wait_status, self.lb_subpro_output))
        
    def startMain(self):
        self.stack_main.set_visible_child_name("main")
        asyncio.run(self.board_info())
        Thread(target=self.startWebsocket).start()

    def on_btn_msg_cancel_clicked(self, b):
        self.message_dialog_port.set_visible(False)

    def on_btn_msg_ok_clicked(self, b):
        asyncio.run(self.pro.add_port_permission())

    def on_btn_reset_clicked(self, b):
        self.dialog_info.set_visible(True)
        self.dialog_info.set_markup(
            _("Are you sure you want to remove files and reset it?"))

    def on_bt_dialog_info_clicked(self, b):
        self.dialog_info.set_visible(False)
        if not self.is_reset_clicked:
            self.is_reset_clicked = True
            cf.is_websocket_running = False
            self.pro.reset_system()
            self.stack_main.set_visible_child_name("install")

    def destroy(self, b):
        print("destroy")
        cf.is_main_thread_running = False
        cf.is_websocket_running = False
        self.window.destroy()
        import signal
        os.kill(os.getpid(), signal.SIGKILL)

    def on_delete_event(self, widget, event):
        # it hides the window
        self.window.hide_on_delete()
        
        return True

    def on_open_item_activate(self, b):
        self.window.show()

    def on_log_item_activate(self, b):
        self.pro.open_log()
