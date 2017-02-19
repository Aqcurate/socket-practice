#!/usr/bin/python3

# Receives a number from the server
# Returns the number back to the server

import socket

# Create a socket object
s = socket.socket()
# Hostname (localhost) and port
host = '0.0.0.0'
port = 33333 
# Connect to the port
s.connect((host, port))

while(True):
    # Receive bytes from socket object and decode it
    # Python3 needs you to explicitly decode
    message = s.recv(2048).decode('UTF-8')
    print(message)
    # Split the message by spaces (gives a list of words)
    # Take the last word (negative indexes loop back)
    number = message.split(' ')[-1]
    # Encode the bytes then send it using socket object
    # Remember to encode to bytes explicitly
    s.send(number.encode('UTF-8'))
