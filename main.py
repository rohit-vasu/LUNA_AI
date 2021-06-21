from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QMovie
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import pyttsx3
import speech_recognition as sr
import os
import time
import webbrowser
import datetime
import wikipedia
import random

flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
# The Master
master = "User"

# LUNA voice settings
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 180)


# Speaking the audio
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


speak("Powering up LUNA")


# Wishing according to time of day
def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning" + master)
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon" + master)
    else:
        speak("Good evening" + master)

    speak("I am LUNA, how may I help you" + master)


class mainT(QThread):
    def __init__(self):
        super(mainT, self).__init__()

    def run(self):
        self.LUNA()

    def STT(self):
        R = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...........")
            audio = R.listen(source)
        try:
            print("Recognizing......")
            text = R.recognize_google(audio, language='en-in')
            print(">> ", text)
        except Exception:
            speak("Sorry, I did not hear you")
            return "None"
        text = text.lower()
        return text

    # LUNA class
    def LUNA(self):
        wish()
        while True:
            self.text = self.STT()
            # words that leads to invoke
            STR_TIME = ["what is the time now", "time please", "tell me the time", "what's the time now"]
            for inputs in STR_TIME:
                if inputs in self.text:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")
                    speak(f"...{master}the time right now is {strTime}")
                    break

            # LUNA will search on wikipedia for you
            # You have to phrase your topic as a question, like 'who is Tom Cruise?'
            STR_WIKI = ["wikipedia", "open wikipedia", "take me to wikipedia"]
            for inputs in STR_WIKI:
                if inputs in self.text:
                    speak("Searching wikipedia...please tell me what to search")
                    print("listening")
                    subtext = self.STT()
                    results = wikipedia.summary(subtext, sentences=5)
                    print(results)
                    speak(results)

            # LUNA will search on google for you
            STR_GOOG = ["google", "open google"]
            for inputs in STR_GOOG:
                if inputs in self.text:
                    speak('Opening Google for you')
                    webbrowser.open('google.com')

            # LUNA will open Youtube for you
            STR_YOU = ["youtube", "open youtube", "search youtube"]
            for inputs in STR_YOU:
                if inputs in self.text:
                    speak('Opening Youtube for you')
                    webbrowser.open("Youtube.com")

            # LUNA will tell you a joke
            STR_JOKE = ["tell me a joke", "do you know jokes"]
            STR_PUNLIN = ["An apple a day keeps the doctor away. At least it does if you throw it hard enough.",
                          "After an unsuccessful harvest, why did the farmer decide to try a career in music? Because he had a ton of sick beets",
                          "My friend was showing me his tool shed and pointed to a ladder. That's my stepladder, he said. I never knew my real ladder.",
                          "My hotel tried to charge me ten dollars extra for air conditioning. That wasn’t cool.",
                          "To whoever stole my copy of Microsoft Office, I will find you. You have my Word.",
                          "What’s Forrest Gump’s password? 1forrest1.",
                          "If prisoners could take their own mug shots…They’d be called cellfies.",
                          "Wanna hear a joke about paper? Never mind. It's tearable.",
                          "What do you call a sad cup of coffee? Depresso."]
            for inputs in STR_JOKE:
                if inputs in self.text:
                    speak("yes of course")
                    num = random.randint(0, 8)
                    joke = STR_PUNLIN[num]
                    print(num)
                    speak(joke)

            # Switches off LUNA
            STR_OFF = ["switch off", "log off", "see you later"]
            for inputs in STR_OFF:
                if inputs in self.text:
                    speak("ok then see you later...")
                    sys.exit()

# To call the GUI for LUNA

FROM_MAIN, _ = loadUiType(os.path.join(os.path.dirname(__file__), "./scifi.ui"))


class Main(QMainWindow, FROM_MAIN):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(1401, 751)
        self.label_7 = QLabel

        self.setWindowFlags(flags)
        Dspeak = mainT()
        self.label_7 = QMovie("./lib/brain.gif", QByteArray(), self)
        self.label_7.setCacheMode(QMovie.CacheAll)
        self.label_4.setMovie(self.label_7)
        self.label_7.start()

        self.ts = time.strftime("%A, %d %B")

        Dspeak.start()
        self.label.setPixmap(QPixmap("./lib/background.gif"))
        self.label_5.setText("<font size=12 color='light blue'>" + self.ts + "</font>")
        self.label_5.setFont(QFont(QFont('Acens', 12)))


app = QtWidgets.QApplication(sys.argv)
main = Main()
main.show()
exit(app.exec_())
