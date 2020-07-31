# using a fork of pyaudio with as_loopback capabilities https://github.com/intxcc/pyaudio_portaudio
import pyaudio
import struct
import math
import numpy
from scipy.signal import find_peaks
from scipy.fft import fft as fourier
from collections import deque

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1200
MAX_FREQ = 1500
p = pyaudio.PyAudio()
que = deque(maxlen=1)
# for i in range(p.get_device_count()):
#     print(p.get_device_info_by_index(i))


def callback(in_data, frame_count, time_info, status):
    que.append(in_data)
    return (in_data, pyaudio.paContinue)


stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=10,
                frames_per_buffer=CHUNK,
                as_loopback=True,
                stream_callback=callback)


def getChunk():
    chunk = None
    if len(que) == 1:
        chunk = [x[0] for x in struct.iter_unpack("=i", que.pop())]
    return chunk


def getFreqs():
    chunk = getChunk()
    if chunk != None:
        fft = numpy.absolute(numpy.fft.fft(chunk))
        peaks, properties = find_peaks(fft, height=numpy.max(fft)/6)
        freqs = []
        heights = []
        for i in range(len(peaks)):
            freq = peaks[i]*RATE/CHUNK
            if freq < MAX_FREQ:
                freqs.append(int(freq))
                heights.append(int(properties['peak_heights'][i]))
            else:
                break
        for i in range(len(heights)):
            heights[i] = round(heights[i]/230000000000, 3)
        return freqs, heights
    else:
        return None, None


# while True:
#     freqs, heights = getFreqs()
#     if freqs != None:
#         print(str(heights), "\n")
