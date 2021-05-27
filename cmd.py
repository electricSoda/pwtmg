from tkinter import *
from tkinter import font

class commandLine():
    def __init__(self, root, prompt):
        self.root = root
        self.prompt = prompt

    def printLine(self, message):
        self.prompt.insert(END, message)


