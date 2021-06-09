from tkinter import *
from playsound import playsound

class commandLine():
    def __init__(self, root, prompt):
        self.root = root
        self.prompt = prompt

    def printLine(self, message):
        self.prompt.insert(END, message)
        self.prompt.yview(END)

    def checkCommand(self, text):
        self.printLine("> /"+text)
        if text == 'play':
            playsound('cykablyat.mp3')
        if text == 'help':
            self.printLine("Just look at our documentation.")
        if text == 'getstarted':
            self.printLine("Let's get you set up!")
            self.printLine("First, please select a coding challenge (please type a number):")
            self.printLine(("1 - Cyber Attacks 2 - Attacking Super Computers 3 - Having thing with hot girls"))


