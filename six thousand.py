from os import system
from time import time, sleep
from colorama import init, Fore, Back, Style
from utils import getTerminalSize, hideCursor
from random import randint
from audio import stream, p, getFreqs
import math
import keyboard
init(autoreset=True)
BPM = 87*32
LPS = BPM/60
POINT_COUNT = 3
MAX_VISIBLE_FREQ = 700
palette = [Fore.MAGENTA, Fore.CYAN]
backPalette = [Back.BLUE, Back.RED, Back.CYAN, Back.MAGENTA, Back.WHITE]
textPalette = [Fore.WHITE, Fore.LIGHTWHITE_EX, Fore.YELLOW, Fore.LIGHTYELLOW_EX, Fore.BLACK, Fore.LIGHTBLACK_EX]


def getPointForFreq(freq, freqSteps):
    # every freq lower than freqsteps[point] gets this point
    for point in range(0, len(freqSteps)):
        if freq <= freqSteps[point]:
            return point
    return len(freqSteps)-1


def fallingUp():
    global POINT_COUNT
    y = 0
    running = True
    while running:
        hideCursor()
        COLUMNS, ROWS = getTerminalSize()
        line = ""
        start = time()
        freqs, heights = getFreqs()
        pointIndex = 0
        points = []
        pointHeights = []

        freqSteps = [(i+1)*MAX_VISIBLE_FREQ/POINT_COUNT for i in range(POINT_COUNT)]
        points = [(COLUMNS-2)/(POINT_COUNT+1)*(i+1)-(i) for i in range(POINT_COUNT)]
        if freqs != None:
            pointHeights = [list() for i in range(POINT_COUNT)]
            for freqI in range(len(freqs)):
                i = getPointForFreq(freqs[freqI], freqSteps)
                pointHeights[i].append(heights[freqI] + heights[freqI] * freqs[freqI]/MAX_VISIBLE_FREQ/3)
            for i in range(len(pointHeights)):
                if pointHeights[i] == []:
                    pointHeights[i] = [0]
                pointHeights[i] = max(pointHeights[i])
        else:
            pointHeights = [0]*POINT_COUNT
        pointDistance = (points[1] - points[0]) if len(points) > 1 else COLUMNS/2

        backWaveAmplitudes = [pointDistance * ((i+1)/POINT_COUNT) for i in range(POINT_COUNT-1, -1, -1)]

        backWaves = [round(((math.sin(y*1.4/(backWaveAmplitudes[i])*2*math.pi)+1)/2) * (backWaveAmplitudes[i]) + (pointDistance)*(i+1) - (backWaveAmplitudes[i])/2) for i in range(POINT_COUNT)]

        for x in range(COLUMNS-2):
            word = " "
            textColor = ""
            backColor = ""
            for waveIndex in range(len(backWaves)):
                if x == backWaves[waveIndex]:
                    if y % 3 == 0:
                        backColor = backPalette[waveIndex % len(backPalette)]
                        textColor = textPalette[waveIndex % len(backPalette)]
                        word = chr(randint(33, 1000))

            if pointIndex < len(pointHeights):

                allFactor = 2.5
                pointCountFactor = 1/(POINT_COUNT*5)
                width = 1 + (COLUMNS-2) * pointCountFactor * pointHeights[pointIndex] * allFactor
                width = 0.7 + width - (width/10)/math.exp(width)
                if x == 0:
                    line += " "
                else:
                    if x > points[pointIndex] - width/2 and x < points[pointIndex] + width/2:
                        word = str(randint(0, 9))
                        textColor = Style.BRIGHT + palette[randint(3, 100) % len(palette)]
                if x > points[pointIndex] + width/2:
                    pointIndex += 1

            line += backColor + textColor + word + Back.RESET + Style.RESET_ALL

        print(line, end="\n")
        duration = time() - start
        if duration < 1/LPS:
            sleep(1/LPS-duration)
        y += 1
        if keyboard.is_pressed("escape"):
            print("finished :c")
        elif keyboard.is_pressed("1"):
            POINT_COUNT = 1
        elif keyboard.is_pressed("2"):
            POINT_COUNT = 2
        elif keyboard.is_pressed("3"):
            POINT_COUNT = 3
        elif keyboard.is_pressed("4"):
            POINT_COUNT = 4
        elif keyboard.is_pressed("5"):
            POINT_COUNT = 5
        elif keyboard.is_pressed("6"):
            POINT_COUNT = 6
        elif keyboard.is_pressed("7"):
            POINT_COUNT = 7
        elif keyboard.is_pressed("8"):
            POINT_COUNT = 8
        elif keyboard.is_pressed("9"):
            POINT_COUNT = 9


fallingUp()
stream.stop_stream()
stream.close()
p.terminate()
