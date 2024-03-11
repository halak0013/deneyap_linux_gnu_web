[Türkçe](readmeTr.md) --- [English](readme.md)
# Pardus and Debian Deneyap client

Comminication [Deneyap Board](https://deneyapkart.org/deneyapkart/deneyapblok/) and your deneyap board


<img src="data/deneyap.svg" width="200" style="display: block; margin-left: auto; margin-right: auto;">

## Features
You can 
* install Deneyap core on system
* comminication [Deneyap Board](https://deneyapkart.org/deneyapkart/deneyapblok/) and your deneyap board
* search and install librarry
* look lof if there is error
* run it wort on background
* check port permission



## Download
You can download from [release page](https://github.com/halak0013/deneyap_linux_gnu_web/releases)

## Installing
All you have to do is download the deb file, double click and install it. You will continue with the installation steps and allow port permissions if necessary.

## Dependencies

`pip install -r requirements.txt`

# Running

`python3 Main.py`

# Building

```console
sudo apt install devscripts git-buildpackage
sudo mk-build-deps -ir
gbp buildpackage --git-export-dir=/tmp/build/deneyap -us -uc --git-ignore-branch --git-ignore-new

```
I gave help from [Deneyap-Kart-Web](https://github.com/deneyapkart/Deneyap-Kart-Web) for some of websocket part. because I didn't which port is using
