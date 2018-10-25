#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time

os.system("clear")
os.system("figlet 'WiFi Access Point'")
os.system("airmon-ng check kill")
os.system("iptables -t nat -F")

target = raw_input("SSID: ")
iface = "wlp2s0"
ip = "192.168.100.1"
nm = "255.255.255.0"

os.system("sysctl net.ipv4.ip_forward=1")
os.system("iptables -t nat -A POSTROUTING -o enp1s0f1 -j MASQUERADE")
os.system("ifconfig "+iface+" "+ip+" netmask "+nm)

time.sleep(3)

os.system("echo '' > /etc/dnsmasq.conf")
dnsfile = open("/etc/dnsmasq.conf","a")
dnsfile.write("interface="+iface+"\n")
dnsfile.write("dhcp-range="+'.'.join(ip.split(".")[0:-1])+".10,"+'.'.join(ip.split(".")[0:-1])+".100,24h")
dnsfile.close()

os.system("killall -9 dnsmasq")
os.system("dnsmasq &")

time.sleep(3)

os.system("rm -rf hostapd.conf")
hostfile = open("hostapd.conf","a")
hostfile.write("interface="+iface+"\n")
hostfile.write("driver=nl80211\n")
hostfile.write("ssid="+target+"\n")
hostfile.write("hw_mode=g\n")
hostfile.write("channel=9\n")
hostfile.close()

os.system("killall -9 hostapd")
os.system("hostapd hostapd.conf &")

time.sleep(1)

q = raw_input("Exit")

print("Exiting")

os.system("service NetworkManager restart")
os.system("killall -9 dnsmasq")
os.system("killall -9 hostapd")
os.system("rm -rf hostapd.conf")
