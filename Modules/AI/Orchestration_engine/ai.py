import pyttsx3
import speech_recognition as sr


class AI():
    __name = ""
    __skill = []

    def __init__(self, name=None):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[2].id)
        self.engine.say('Hello I am helix')
        self.engine.runAndWait()
        self.r = sr.Recognizer()
        self.m = sr.Microphone()

        if name is not None:
            self._name = name

        print("Listening")
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        sentence = "Hello my name is " + self.__name
        self.name = value
        self.engine.say(sentence)
        self.engine.runAndWait()

    def say(self, sentence):
        self.engine.say(sentence)
        self.engine.runAndWait()

    def listen(self):
        global phrase
        print("Say something")
        with self.m as source:
            audio = self.r.listen(source)
            print("Got it:")
        try:
            phrase = self.r.recognize_google(audio, show_all=False, language="en_us")
            sentence = "got it you said " + phrase
            self.engine.say(sentence)
            self.engine.runAndWait()

        except:
            print("sorry didnt get that")
            self.engine.say("Sorry I didn't get that")
            self.engine.runAndWait()
            pass

        print("You said ", phrase)
        return phrase
