#!/usr/bin/python3

# Sends out a number
# Asks the client send back the number

import socket
import threading

# Create a socket object
s = socket.socket()
# Host (localhost) and port
host = '0.0.0.0'
port = 33333
# Bind to a port on localhost
s.bind((host, port))

# Checking if user input is correct
# Returns boolean
def input_check(c, number):
    # Outgoing message
    outgoing = 'Please print the following number: ' + str(number) + '\n'
    # Send the message using connection object
    c.send(outgoing.encode('UTF-8'))

    # Try to get incoming message using connection object
    try:
        incoming = c.recv(2048).decode('UTF-8')
    # Return false if it times out
    except socket.timeout:
        return False

    # Strip the incoming message of whitespace and compare it to intended result
    if incoming.strip() == str(number):
        return True
    # Return false if the message does not equal intended result
    return False

# Listen for connections and create a new thread for each connection
def listen():
    # Listen for connections (Allow for a 5 connection backlog)
    s.listen(5)
    while True:
        # Accept the connection (which returns a connection object and the client address)
        c, addr = s.accept()
        # Set the timeout on socket blocking operations
        # In this case, if more than two seconds elapse before user gives answer, it will timeout
        c.settimeout(2)
        # Create a thread that will run the puzzle function and pass in the connection object as the argument
        # Arguments that are passed need to be a tuple
        # Start the thread object
        threading.Thread(target = puzzle, args = (c,)).start()

def puzzle(conn):
    # Set the connection object to c
    c = conn
    # Set variable that will be incremented by while loop
    number = 1
    while number <= 100:
        # Call input_check function
        # Check if user input will match the number variable
        if (input_check(c, number)):
            # If number has incremented to 100, send the flag back
            if number == 100:
                c.send('Flag: SSTCTF{B4S1C_S0CK4T}\n'.encode('UTF-8'))
                break
            # Otherwise, increment number
            number += 1
        else:
            # If the input was incorrect, send failure message
            c.send('Better luck next time!\n'.encode('UTF-8'))
            break
    # Disconnect user
    c.shutdown(1)
    c.close()

if __name__ == '__main__':
    # Call function that listens to connections
    listen()
