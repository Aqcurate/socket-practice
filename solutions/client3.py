#!/usr/bin/python3

# Receieves a system of 3 equations (non-singular coefficient matrix)
# Returns the solution to the system

import socket
import numpy

s = socket.socket()
host = '0.0.0.0'
port = 22222
s.connect((host, port))

print(s.recv(2048).decode('UTF-8'))

while(True):
    # Let a be the coefficient matrix
    a = []
    # Let b be the answer matrix
    b = []

    message = s.recv(2048).decode('UTF-8')
    print(message)
    # Split the messages into lines (each line contains on equation)
    lines = message.split('\n')
    # Loop through each equation (splitting by newline gives us a junk value at the end of the list)
    for line in lines[:-1]:
        # Split the equations into words (the words list contains the coefficients among other things)
        words = line.split(' ')
        # Get the values in the word lists containing coefficients (EX: 5x, 4y, -3y, 9z, etc.)
        # Get rid of the last letter to isolate the coefficients (EX: 5, 4, -3, 9, etc.)
        # Cast the coefficients to integers
        equation = [int(words[0][:-1]), int(words[2][:-1]), int(words[4][:-1])]
        # Add the list to the coefficients matrix
        a.append(equation)
        # Add the last word (containing answer value) to the answer matrix
        b.append(int(words[-1]))

    # Use numpy to solve the system of equation
    answer = numpy.linalg.solve(a, b)
    # Round the answer to avoid rounding off by one errors due to truncation
    # Cast the answer from floats to integers
    answer = numpy.rint(answer).astype(int)
    # Format the answer and send
    answer_string = '{}, {}, {}'.format(answer[0], answer[1], answer[2])
    print(answer_string)
    s.send(answer_string.encode('UTF-8'))
