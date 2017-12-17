#!/bin/bash

set -e

apt-get update && apt-get upgrade

## Configuring Wifi
cp -vrf ./conf/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf 


## Installing zsh and oh-my-zsh
apt-get install zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
cp -vrf ./conf/.zshrc ~/.zshrc


## Installing nodejs
sudo curl -sL https://deb.nodesource.com/setup_9.x | sudo -E bash -
apt-get install nodejs


## Installing Docker
sudo curl -sSL https://get.docker.com | sh


## Installing other software

apt-get install ovpn hostapd dnsmasq