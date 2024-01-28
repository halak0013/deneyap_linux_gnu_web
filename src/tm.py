import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Arka Planda Çalışan Uygulama")
        self.connect("delete-event", self.on_delete_event)
        self.set_default_size(300, 200)

        # Arka planda çalışan uygulama için bu özelliği kullanabilirsiniz
        self.set_wmclass("my_app", "MyApp")

        # Diğer arayüz bileşenlerinizi buraya ekleyin
        label = Gtk.Label(label="Uygulama arka planda çalışıyor.")

        self.add(label)
        self.show_all()

    def on_delete_event(self, widget, event):
        # Uygulama kapatılmak istendiğinde sadece pencereyi gizle
        self.hide_on_delete()
        return True

if __name__ == "__main__":
    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()
