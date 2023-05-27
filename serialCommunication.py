import serial,os
from tkinter import *
from time import sleep as delay

#<<<--- Internal variables--->>>
def loadInternalVariables():
    CWD = os.getcwd()
    programDir = 'C:/Program Files/ArduinoPyBhutuu'
    if not os.path.exists(programDir):
        print("Compiler not find")
def mainWindow():
    winroot = Tk()
    winroot.title("ArduinoPyBhutuu")
    winroot.geometry("800x600")
    winroot.minsize(500, 500)
    winroot.mainloop()
mainWindow()