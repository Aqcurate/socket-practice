#!/usr/bin/python3

# Takes three numbers from the server
# Returns the largest number if the three numbers can form a valid triangle
# Otherwise return the smallest number

import socket

s = socket.socket()
host = '0.0.0.0'
port = 44444
s.connect((host, port))

# Receieve the introduction message
print(s.recv(2048).decode('UTF-8'))

while(True):
    # Receieve puzzle
    message = s.recv(2048).decode('UTF-8')
    print(message)
    # Split the puzzle into words using spaces as a delimiter
    words = message.split(' ')
    # Get the last three words (which contain the important numbers)
    nums = [int(words[-3]), int(words[-2]), int(words[-1])]
    # Sort the numbers (ascending order)
    sorted(nums)
    # Check if the numbers allow for a valid triangle
    if nums[0] + nums[1] > nums[2]:
        # Return the largest number if it is valid
        answer = nums[2]
    else:
        # Return the smallest number if it is not valid
        answer = nums[0]
    # Send the answer
    s.send(str(answer).encode('UTF-8'))
