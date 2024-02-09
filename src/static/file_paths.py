import os


class Paths:

    # ? environments
    HOME = os.path.expanduser("~")
    env = os.environ.copy()

    bin_path = HOME+"/.local/bin/"
    arduino_cli = bin_path+"arduino-cli "
    arduino15_path = HOME+"/.arduino15/"

    log_path = HOME+"/.deneyap/log/"

    deneyap_url = "https://raw.githubusercontent.com/deneyapkart/deneyapkart-arduino-core/master/package_deneyapkart_index.json"
    d_json_name = "package_deneyapkart_index.json"
    d_json_path = arduino15_path+d_json_name
    d_yaml_path = arduino15_path+"arduino-cli.yaml"
    deneyap_pro = "/tmp/deneyap/deneyap_pro/"
    deneyap_p_f = "/tmp/deneyap/"

    @classmethod
    def file_check(self, path, reset=False):
        if not os.path.exists(path):
            os.makedirs(path)
        elif reset:
            os.system("rm -rf "+path)
            os.makedirs(path)
