#!/bin/bash

set -e

sudo apt-get update && apt-get upgrade

## Configuring Wifi
sudo cp -vrf ./conf/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf 


## Installing zsh and oh-my-zsh
sudo apt-get install zsh
sudo sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
cp -vrf ./conf/.zshrc ~/.zshrc


## Installing nodejs
sudo curl -sL https://deb.nodesource.com/setup_9.x | sudo -E bash -
sudo apt-get install nodejs


## Installing Docker
sudo curl -sSL https://get.docker.com | sh


## Installing other software

sudo apt-get install ovpn hostapd dnsmasq python3-pip

pip install bme680 envirophat requests