#!/usr/bin/python3

import RPi.GPIO as GPIO
import signal
import sys
import time

RX = 11
r_count = 0     # signals recieved
l_count = 0     # signals lost

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(RX, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def get_signal(event=None):
    """
    :param event: Pin number
    """
    global r_count
    r_count += 1
    print('Received signal. cnt = ', r_count)

def loop():
    GPIO.add_event_detect(RX, GPIO.FALLING, callback=get_signal) # wait for falling
    while True:
        pass

def destroy():
    GPIO.cleanup()

def start():
    setup()
    loop()


# This global variable is to keep track of multiple presses of Ctrl^C
handling_sigint = False


# This function handles the interrupt signal when Ctrl^C is pressed
def signal_handler(signal_num=None, frame=None):
    """Gracefully handle a SIGINT - triggered by Ctrl+c"""
    def flush():
        sys.stderr.write("\n")
        sys.stderr.flush()
    try:
        global handling_sigint
        if handling_sigint:
            # If they give another interrupt signal during handling, exit
            flush()
            destroy()
            sys.exit()
        else:
            handling_sigint = True
        flush()
        ans = '.'
        while ans and ans not in 'nN':
            sys.stderr.write("Do you want to quit? (y/N): ")
            sys.stderr.flush()
            try:
                ans = sys.stdin.readline().strip()
            except RuntimeError:
                # avoid crashing due to standard out collisions
                pass
            if ans and ans in 'yY':
                destroy()
                sys.exit()
        handling_sigint = False
        flush()
    except RuntimeError:
        handling_sigint = False
        pass

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    try:
        start()
    except EOFError:
        # Handle presses of Ctrl^D gracefully
        print("^D")
        destroy()

