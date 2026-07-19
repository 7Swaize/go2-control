#!/bin/bash -xe

# Only needed on robot, therefore, no Windows equivalent is needed.

nmcli device wifi hotspot ifname wlan0 ssid wireless-Go2 password 00000000
