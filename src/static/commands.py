import os


class Commands:

    # ? environments
    HOME = os.path.expanduser("~")
    env = os.environ.copy()

    bin_path = HOME+"/.local/bin/"
    arduino_cli = bin_path+"arduino-cli "
    arduino15_path = HOME+"/.arduino15/"

    arduino_cli_install = "curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=~/.local/bin sh"
    a_cli_init = arduino_cli + "config init"
    a_cli_deneyap_install = arduino_cli+"core install deneyap:esp32"
    a_cli_project = arduino_cli+"sketch new deneyap_pro"
    a_cli_update_index = arduino_cli+"core update-index"
    a_cli_board_list = arduino_cli+"board list"
    a_cli_board_list_all = arduino_cli+"board listall deneyap"

    deneyap_board = '#lsusb | grep "Turkish Technnology Team Foundation"'

    port_user_permission = "sudo adduser "+HOME.split("/")[2]+" dialout"

    deneyap_url = "https://raw.githubusercontent.com/deneyapkart/deneyapkart-arduino-core/master/package_deneyapkart_index.json"
    d_json_name = "package_deneyapkart_index.json"
    d_yaml_path = arduino15_path+"arduino-cli.yaml"
    deneyap_pro = "/tmp/deneyap/"

    port=""

    @classmethod
    def add_port_permission(self, port):
        return "sudo chmod a+rw " + port

    @classmethod
    def compile_code(self, board):
        return self.arduino_cli + "compile --fqbn " + board + "deneyap_pro"

    @classmethod
    def upload_code(self, port, board):
        return f"upload -p {port} --fqbn {board} deneyap_pro"

    def __init__(self):
        print(Commands.port_user_permission)


c = Commands()
