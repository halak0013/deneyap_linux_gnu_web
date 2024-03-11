#! /bin/bash

sudo apt install python3-serial usbutils

mkdir -p ~/.local/bin
echo "export PATH=$PATH:~/.local/bin" >> ~/.bashrc
bash
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=~/.local/bin sh

#? command arduino-cli completion bash > arduino-cli.sh
arduino-cli completion bash > arduino-cli.sh

sudo mv arduino-cli.sh /etc/bash_completion.d/

#? without root acces
mv arduino-cli.sh ~/.local/share
echo "source ~/.local/share/arduino-cli.sh" >> .bashrc
bash


#? adding configuration file ->/home/luca/.arduino15/arduino-cli.yaml
arduino-cli config init

#yaml dosyası değişecek
#board_manager:
#    additional_urls:
#        - https://raw.githubusercontent.com/deneyapkart/deneyapkart-arduino-core/master/package_deneyapkart_index.json

#or
wget -c https://raw.githubusercontent.com/deneyapkart/deneyapkart-arduino-core/master/package_deneyapkart_index.json -P ~/.arduino15/
#derleme sırasında arduino-cli  core update-index --additional-urls ~/.arduino15/package_deneyapkart_index.json

#gerekli kart tanımlamamlır için
arduino-cli core install deneyap:esp32

#? update index
arduino-cli core update-index

#? new project
arduino-cli sketch new MyFirstSketch



#? board list
arduino-cli board list
#Port         Protocol Type              Board Name FQBN Core
#/dev/ttyACM0 serial   Serial Port (USB) Unknown

#?porta yazmak için gerekli izin
sudo adduser bismih dialout
sudo chmod a+rw /dev/ttyACM0


#?deneyap kartlarını listeliyor
arduino-cli board listall deneyap
Board Name         FQBN
Deneyap Kart       deneyap:esp32:dydk_mpv10
Deneyap Kart 1A    deneyap:esp32:dydk1a_mpv10
Deneyap Kart 1A v2 deneyap:esp32:dydk1a_mpv20
Deneyap Kart G     deneyap:esp32:dyg_mpv10
Deneyap Mini       deneyap:esp32:dym_mpv10
Deneyap Mini v2    deneyap:esp32:dym_mpv20

#hangi kartın yüklü olduğunu bulma
lsusb | grep "Turkish Technnology Team Foundation" | cut -d' ' -f12-
#DENEYAP MINI
#lsusb | grep "Turkish Technnology Team Foundation"
#Bus 001 Device 010: ID 303a:8141 Turkish Technnology Team Foundation (T3) DENEYAP MINI

arduino-cli board list --format json




arduino-cli compile --fqbn deneyap:esp32:dym_mpv10 MyFirstSketch
arduino-cli upload -p /dev/ttyACM0 --fqbn deneyap:esp32:dym_mpv10 MyFirstSketch
