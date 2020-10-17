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
        arduinoData = serial.Serial('com3', 9600) # Arduino Connection - "Change com3 to your arduino port connection"
        break
    except (serial.serialutil.SerialException, FileNotFoundError):
        print("Arduino Not Found ..." + "\n")
        time.sleep(5)

# create matplotlib figure and axes
fig, ax = plt.subplots(1, figsize=(15, 7))

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

# variable for plotting
x = np.arange(0, 2 * CHUNK, 2)

# create a line object with random data
line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=1)

# basic formatting for the axes
ax.set_title('AUDIO WAVEFORM')
ax.set_xlabel('samples')
ax.set_ylabel('amplitude')
ax.set_ylim(0, 255)
ax.set_xlim(0, 2 * CHUNK)
plt.setp(ax, xticks=[0, CHUNK, 2 * CHUNK], yticks=[-255, 0, 255])

# show the plot
plt.show(block=False)

# for measuring frame rate
sampleCount = 0
volCum = 0
avg = 0
start_time = time.time()

while True:

    # binary data
    data = stream.read(CHUNK)

    # convert data to integers, make np array
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)

    # create np array
    data_np = np.array(data_int, dtype='b')[::2]

    line.set_ydata(data_np)

    # update figure canvas
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        sampleCount += 1
        volCum += data_np[1]

    # Sending data to Arduino
        if sampleCount % 2 == 0:
            arduinoData.write(volCum / sampleCount)
            volCum = 0
            sampleCount = 0

    # When user clicks the exit window of the graphic
    except TclError:

        print('stream stopped')
        break

    # Error handling for lost Arduino connection
    except (serial.serialutil.SerialException, FileNotFoundError):

        print("Connection Lost ... Program has ended")
        break
