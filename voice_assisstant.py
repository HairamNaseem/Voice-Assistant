import datetime
import winsound
import pyttsx3
import speech_recognition
import speech_recognition as sr
import pyaudio
import wikipedia
import webbrowser
import os
import smtplib
import pywhatkit
import pyjokes
import cv2

email_to={
    "umar":"k213066@nu.edu.pk",
    "h":"hairam90@gmail.com"
}
engine = pyttsx3.init("sapi5")  # to take api for voices in windows
voices = engine.getProperty("voices")  # use voices available in windows
engine.setProperty("voices", voices[0].id)  # set a voice of male[0], female[1]

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def SendEmail(to,content):
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.login("projectpai07@gmail.com","ppap_0707")
    server.sendmail("projectpai07@gmail.com",to,content)
    server.close()


def WishMe(name):
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("good morning"+name)
    elif (hour >= 12 and hour < 18):
        speak("good afternoon"+name)
    else:
        speak("good evening"+name)
    speak("I am Vat. How may I help you")


def TakeCommand():  # takes user input and returns a string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1  # seconds of non-speaking audio before a phrase is considered complete
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"you said: {query}\n")

    except Exception as e:
        print(e)
        speak("say that again please")
        print("Say that again please...")
        return "None"
    return query

if __name__ == "__main__":
    speak("hello there, what do you want me to call you?")
    name = TakeCommand()
    WishMe(name)
    while True:
        query = TakeCommand().lower()
        # logic for executing task based on user voice
        if "who is" in query or "who" in query or "what is" in query or "what" in query:
            speak("searching wikipedia...")
            results = wikipedia.summary(query, sentences=1)
            speak("according to wikipedia")
            print(results)
            speak(results)

        elif "add to todo list" in query or "make a todo list" in query:
            done = False
            while not done:
                try:
                    speak("what do you want me to write?")
                    note = TakeCommand().lower()
                    speak("choose a file name")
                    filename = TakeCommand().lower()
                    with open(filename,"w") as f:
                        f.write(note+"\n")
                        speak(f"{filename} added to your todo list")
                        done = True
                except speech_recognition.UnknownValueError:
                    speak("please say again")

        elif "show my todo list" in query or "show todo list" in query:
            speak("your todo list contains the following items")
            speak(note)
            print(note)

        elif "joke" in query or "tell me a joke" in query:
            speak(pyjokes.get_joke())

        elif "open youtube" in query:
            webbrowser.open("youtube.com")

        elif "open google" in query:
            webbrowser.open("google.com")

        elif "play music" in query:
            music_dir = "C:\\Users\\haira\\Music\\Good Life one republic.mp3"
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif "play video of" in query or "play a song" in query:
            pywhatkit.playonyt(query)

        elif "the time" in query or "what is the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"{name}, the time is {strTime}")
            print(strTime)

        elif "open pycharm" in query:
            codepath = "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2022.2.1\\bin\\pycharm64.exe"
            os.startfile(codepath)

        elif "send email" in query:
            try:
                speak(f"available options are, {email_to.keys()}")
                speak("who do you want to send email to")
                receiver = TakeCommand()
                to = email_to[receiver]
                speak("what do you want to write?")
                content = TakeCommand()
                SendEmail(to, content)
                speak("email has been sent")
            except Exception as e:
                print(e)
                speak("email could not be sent")

        elif "open security camera" in query or "watch behind me" in query:
            speak("say exit whenever you want to end security camera")
            cam = cv2.VideoCapture(0)
            while cam.isOpened():
                ret, frame1 = cam.read()
                ret, frame2 = cam.read()
                diff = cv2.absdiff(frame1, frame2)
                gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
                blur = cv2.GaussianBlur(gray, (5, 5), 0)
                _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
                dilated = cv2.dilate(thresh, None, iterations=3)
                contours,_ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                for c in contours:
                    if cv2.contourArea(c) < 5000:
                        continue
                    x, y, w, h = cv2.boundingRect(c)
                    cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    winsound.Beep(500,200)
                fin = TakeCommand()
                if fin == "exit":
                    break
                cv2.imshow("security cam",frame1)

        elif "open camera" in query or "open webcam" in query:
            speak("say exit whenever you want to end camera")
            cam = cv2.VideoCapture(0)
            while cam.isOpened():
                ret, frame = cam.read()
                fin = TakeCommand()
                if fin == "exit":
                    break
                cv2.imshow("web cam", frame)



        elif "quit" in query:
            speak("good bye")
            exit(0)

