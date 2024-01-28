# Pardus and Debian Deneyap client

You can communicate with deneyap web and your deneyap board,


<img src="data/deneyap.svg" width="200" style="display: block; margin-left: auto; margin-right: auto;">


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

