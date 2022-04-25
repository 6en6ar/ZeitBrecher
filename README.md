# ZeitBrecher
Basic program that uses vulnerable NTP servers for DNS UDP amplification attacks. 
It also performs basic UDP flood exhausting the target with port unreachable ICMP responses. 

Note: This is used only for educational purposes, to better understand the attacks and how to protect against them. The author is not responsible for your actions!

Usage --> Populate ntp.txt with ntp servers. The script also checks if the server is vulnerable sending it a monlist payload to measure the response.
