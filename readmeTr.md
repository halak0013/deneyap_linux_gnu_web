[text](readme.md)
# Pardus and Debian Deneyap iletişim programı

[Deneyap Board](https://deneyapkart.org/deneyapkart/deneyapblok/) ile kartlarınız arasındaki iletişimi sağlayacağın

<img src="data/deneyap.svg" width="200" style="display: block; margin-left: auto; margin-right: auto;">

## Özellikler
Yapabileceklerin
* sistemine Deneyap derleyicisini yükleyin
* Kütüphane arayıp indirin
* Hata kayıtlarına bakın
* arka planda çalıştırabilirsin
* port izinlerini kurulumda ayarlayın



## İndir
[Sürümler sayfasında](https://github.com/halak0013/deneyap_linux_gnu_web/releases) indirebilirsiniz

## Yükleme
Tek yapmanız gereken deb dosyasını indirip çift tıklayıp kurmak. Karşınıza gelen kurulm kısmlarında devam edeip gerekirse port izinleri için izin vermek olacak.


## Geliştirme için

## Bağımlılıklar

`pip install -r requirements.txt`

# Çalıştırmak için

`python3 Main.py`

# Derlemek için

```console
sudo apt install devscripts git-buildpackage
sudo mk-build-deps -ir
gbp buildpackage --git-export-dir=/tmp/build/deneyap -us -uc --git-ignore-branch --git-ignore-new

```
Yardım aldığım yerler:
[Deneyap-Kart-Web](https://github.com/deneyapkart/Deneyap-Kart-Web) bazı web socket port ve iletişim kısımlarını bilme imkanım olmadığı için bazı yerleri almam gerekti. Ek olarak bazı kısmılarını da kullandım.
