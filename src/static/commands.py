from static.file_paths import Paths as p


class Commands:

    arduino_cli_install = "curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=~/.local/bin sh"
    a_cli_init = p.arduino_cli + "config init"
    a_cli_deneyap_install = p.arduino_cli+"core install deneyap:esp32"
    a_cli_project = p.arduino_cli+"sketch new deneyap_pro"
    a_cli_update_index = p.arduino_cli+"core update-index"
    a_cli_board_list = p.arduino_cli+"board list --format json"
    a_cli_board_list_all = p.arduino_cli+"board listall deneyap --format json"


    deneyap_board = 'lsusb | grep "Turkish Technnology Team Foundation"'

    port_user_permission = "sudo adduser "+p.HOME.split("/")[2]+" dialout"


    @classmethod
    def add_port_permission(self, port):
        return "sudo chmod a+rw " + port

    @classmethod
    def compile_code(self, board):
        return p.arduino_cli + "compile --fqbn " + board + " deneyap_pro"

    @classmethod
    def upload_code(self, port, board):
        return f"{p.arduino_cli} upload -p {port} --fqbn {board} deneyap_pro"
    
    @classmethod
    def check_port_permission(self, port):
        return "ls -l " + port
    
    @classmethod
    def search_lib(self, lib):
        return f"{p.arduino_cli} lib search \"{lib}\" --format json"
    
    @classmethod
    def download_lib(self, lib, version):
        return f"{p.arduino_cli} lib install \"{lib}\"@{version}"

    def __init__(self):
        print(Commands.port_user_permission)


c = Commands()
