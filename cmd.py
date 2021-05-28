from tkinter import *
from playsound import playsound

class commandLine():
    def __init__(self, root, prompt):
        self.root = root
        self.prompt = prompt

    def printLine(self, message):
        self.prompt.insert(END, message)

    def checkCommand(self, text):
        if text == 'play':
            playsound('cykablyat.mp3')
        elif text == 'ping':
            print("")


