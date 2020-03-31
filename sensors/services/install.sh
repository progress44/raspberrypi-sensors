#!/bin/sh

chmod 0644 ./*.service
cp ./*.service /etc/systemd/system/

systemctl enable --now fast-sensors
systemctl enable --now slow-sensors

systemctl daemon-reload

systemctl restart fast-sensors
systemctl restart slow-sensors