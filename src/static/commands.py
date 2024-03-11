from static.file_paths import Paths as p


class Commands:

    arduino_cli_install = "curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=~/.local/bin sh"
    a_cli_init = p.arduino_cli + "config init"
    a_cli_deneyap_install = p.arduino_cli+"core install deneyap:esp32"
    a_cli_project = p.arduino_cli+"sketch new deneyap_pro"
    a_cli_update_index = p.arduino_cli+"core update-index"
    a_cli_board_list = p.arduino_cli+"board list --format json"
    a_cli_board_list_all = p.arduino_cli+"board listall deneyap --format json"
    a_cil_add_deneyap_url = p.arduino_cli+"config add board_manager.additional_urls "+p.deneyap_url


    deneyap_board = 'lsusb | grep "Turkish Technnology Team Foundation"'

    port_user_permission = "pkexec sudo adduser "+p.HOME.split("/")[2]+" dialout"

    restart ="/sbin/reboot"


    @classmethod
    def add_port_permission(self, port):
        return "pkexec sudo chmod a+rw " + port

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
    @classmethod
    def is_user_in_group(self):
        groupname = "dialout"
        username = p.HOME.split("/")[2]
        with open('/etc/group', 'r') as file:
            for line in file:
                parts = line.split(':')
                print(parts)
                if parts[0] == groupname and username in parts[3]:
                    return True
        return False