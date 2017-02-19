#!/usr/bin/python3

# Sends a system of 3 equations (non-singular coefficient matrix)
# Asks the client return the solution to the system

import socket
import threading
import random
import numpy

s = socket.socket()
host = '0.0.0.0'
port = 22222
s.bind((host, port))

def input_check(c):
    # Set flag that will exit the while loop
    isSingular = True
    # Let a be the coefficient matrix
    a = []
    # Let ans be the variable matrix
    ans = []
    # Let b be the answer matrix
    b = []

    # While we have not generate a non-singular matrix
    while(isSingular):
        # Reset the values of a and b
        # Generate three random values for the variable matrix
        a = []
        ans = random.sample(range(-29, 29), 3)
        b = []

        # Generate a coefficient matrix and the corresponding answer matrix
        for k in range(3):
            # Append a row to the coefficient matrix
            a.append(random.sample(range(-10, 10), 3))
            # Generate the corresponding answer to the row and variable matrices
            b.append(a[k][0]*ans[0] + a[k][1]*ans[1] + a[k][2]*ans[2])

        # If the determinant of the coefficient matrix is 0, this means there are either no solutions or many
        # Generate a new problem
        if (numpy.linalg.det(a)) != 0:
            isSingular = False

    # Format the system of equations and send it to client
    outgoing = ''
    for k in range(3):
        outgoing += '{}x + {}y + {}z = {}\n'.format(a[k][0], a[k][1], a[k][2], b[k])
    c.send(outgoing.encode('UTF-8'))

    try:
        incoming = c.recv(2048).decode('UTF-8')
    except socket.timeout:
        return False

    # Put the answer in desired format
    answer = '{}, {}, {}'.format(ans[0], ans[1], ans[2])

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
    message = '''You are given a system of equations.
The coefficient matrix is nonsingular.
Solve the system and put it in the format 'x, y, z'.
Example: 2, -14, 6\n'''
    c.send(message.encode('UTF-8'))
    while number <= 100:
        if (input_check(c)):
            if number == 100:
                c.send('Flag: SSTCTF{L3T_3PISL0N_B3_L3S5_TH4N_Z3R0}\n'.encode('UTF-8'))
                break
            number += 1
        else:
            c.send('Better luck next time!\n'.encode('UTF-8'))
            break
    c.shutdown(1)
    c.close()

if __name__ == '__main__':
    listen()
