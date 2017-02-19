#!/usr/bin/python3

# Sends out three numbers
# Asks that the client return the largest number if the three numbers can form a valid triangle
# Otherwise, asks the client to return the smallest number

import socket
import threading
import random

s = socket.socket()
host = '0.0.0.0'
port = 44444
s.bind((host, port))

def input_check(c):
    # Generate three random numbers
    nums = random.sample(range(100, 800), 3)
    # Format the three random numbers and send outgoing message to client
    outgoing = 'Numbers: {} {} {}\n'.format(nums[0], nums[1], nums[2])
    c.send(outgoing.encode('UTF-8'))

    try:
        incoming = c.recv(2048).decode('UTF-8')
    except socket.timeout:
        return False
    
    # Find the actual solution
    # Sort the list
    sorted(nums)
    # Check if the numbers allow for a valid triangle
    if nums[0] + nums[1] > nums[2]:
        # Return the largest number if it is valid
        answer = nums[2]
    else:
        # Return the smallest number if it is not valid
        answer = nums[0]
    # Check if the answer the user gives is the same as the actual answer
    if incoming.strip() == str(answer):
        return True
    return False

def listen():
    s.listen(5)
    while True:
        c, addr = s.accept()
        c.settimeout(2)
        threading.Thread(target = puzzle, args = (c,)).start()

def puzzle(conn):
    c = conn
    number = 1
    # Introduction message
    message = '''You are given three numbers representing triangle side lengths.
If the triangle is possible, return the largest side length.
If the triangle is not possible, return the smallest side length.\n'''
    # Send introduction message
    c.send(message.encode('UTF-8'))
    while number <= 100:
        if (input_check(c)):
            if number == 100:
                c.send('Flag: SSTCTF{3Z_TR14NGL3S}\n'.encode('UTF-8'))
                break
            number += 1
        else:
            c.send('Better luck next time!\n'.encode('UTF-8'))
            break
    c.shutdown(1)
    c.close()

if __name__ == '__main__':
    listen()
