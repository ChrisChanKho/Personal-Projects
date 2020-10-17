import serial
import pyaudio
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
from tkinter import TclError

# constants
CHUNK = 1024 * 2             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 44100                 # samples per second

#Searching for Arduino Board
while True:
    try:
        print("Searching For Arduino board ... ")
        time.sleep(2)
        arduinoData = serial.Serial('com3', 9600) # arduino Connection - "Change com3 to your arduino port connection"
        break
    except (serial.serialutil.SerialException, FileNotFoundError):
        print("Arduino Not Found ..." + "\n")
        time.sleep(5)

# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data from microphone
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

# for measuring volume
sampleCount = 0
volCum = 0
start_time = time.time()

while True:

    # binary data
    data = stream.read(CHUNK)

    # convert data to integers, make np array
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)

    # create np array
    data_np = np.array(data_int, dtype='b')[::2]

    # updating variable trackers per sample
    try:
        sampleCount += 1
        volCum += data_np[1]

    # sending data to Arduino
        if sampleCount % 2 == 0:
            arduinoData.write(volCum / sampleCount)
            volCum = 0
            sampleCount = 0

    # error handling for lost Arduino connection
    except (serial.serialutil.SerialException, FileNotFoundError):

        print("Connection Lost ... Program has ended")
        break



