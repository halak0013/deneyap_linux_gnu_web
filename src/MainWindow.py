import locale
from locale import gettext as _
import os
import gi
import asyncio
from threading import Thread

from AsyncProc import CommandRunner
from Installer import Installer
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk
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
        #self.window.connect('destroy', application.onExit)
        self.window.connect("delete-event", self.on_delete_event)
        #self.window.set_wmclass("my_app", "MyApp")

        self.defineComponents()

        self.init_variables()

        self.window.show_all()

    def init_variables(self):
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

        self.menu.show_all()
        self.indicator.set_menu(self.menu)

        self.ins = Installer(self.message_dialog)
        Thread(target=self.fill_cmb(self.cmb_board)).start()
        

    def defineComponents(self):
        self.btn_about: Gtk.Button = self.builder.get_object("btn_about")
        self.dialog_about: Gtk.AboutDialog = self.builder.get_object(
            "dialog_about")

        self.stack_main: Gtk.Stack = self.builder.get_object("stack_main")

        self.lb_subpro_output: Gtk.Label = self.builder.get_object(
            "lb_subpro_output")
        self.lb_dialog_wait_status: Gtk.Label = self.builder.get_object(
            "lb_dialog_wait_status")

        self.btn_install: Gtk.Button = self.builder.get_object("btn_install")
        self.cmb_board: Gtk.ComboBox = self.builder.get_object("cmb_board")

        self.message_dialog: Gtk.Dialog = self.builder.get_object("message_dialog")

    def fill_cmb(self, cmb):
        cmb.remove_all()
        lst=asyncio.run(self.ins.board_name()).keys()
        #print(lst)
        for c in lst:
            cmb.append_text(c)
        cmb.set_active(0)

    def on_btn_about_clicked(self, b):
        self.dialog_about.set_visible(True)

    def on_cmb_board_changed(self, c):
        GLib.idle_add(asyncio.run(self.ins.board_name.keys))

    def on_btn_install_clicked(self, b):
        self.stack_main.set_visible_child_name("wait")
        GLib.idle_add(asyncio.run(self.ins.install(self.lb_dialog_wait_status, self.lb_subpro_output)))

    def on_btn_msg_cancel_clicked(self, b):
        self.message_dialog.set_visible(False)

    def on_btn_msg_ok_clicked(self, b):
        asyncio.run(self.ins.add_port_permission(self.message_dialog))

    def destroy(self, b):
        self.window.destroy()

    def on_delete_event(self, widget, event):
            # Uygulama kapatılmak istendiğinde sadece pencereyi gizle
            print("delete-event")
            self.window.hide_on_delete()
            return True
    
    def on_open_item_activate(self, b):
        self.window.show()