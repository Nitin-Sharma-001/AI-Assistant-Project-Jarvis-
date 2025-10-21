import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary  
from together import Together
import re
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv


load_dotenv()
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()
# def speak(text):
#     engine = pyttsx3.init()
#     engine.say(text)
#     engine.runAndWait()
#     engine.stop()



client = Together(
    api_key= "24fe1d13d8e09bdb2396fdbecdbd0c8b0b29c592e718cce3a40f8d67dee8c477"
) 




def clean_text(text):
    # Remove markdown bold, bullet points, and strange characters
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # remove **bold**
    text = re.sub(r'[-•–]', '', text)             # remove bullets/dashes
    text = re.sub(r'\s+', ' ', text)              # collapse newlines
def Ai_ans(query):
    try:
        response = client.chat.completions.create(
            model="Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8",
            messages=[
            {
                "role": "user",
                "content": query
            }
            ]
        )
        data = response.choices[0].message.content
        clean_ans = clean_text(data)
        speak(clean_ans)
        print(clean_ans)
    except Exception as e:
        speak("I could not find the processed")
        print(e)


def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c:
        webbrowser.open("https://www.youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://www.linkedin.com")
    elif "open facebook" in c:
        webbrowser.open("https://www.facebook.com")
    elif "open instagram" in c:
        webbrowser.open("https://www.instagram.com")
    elif "open github" in c:
        webbrowser.open("https://www.github.com")
    elif c.startswith("play"):
        parts = c.split(" ")
        if len(parts) > 1:
            song = " ".join(parts[1:])  
            if song in musicLibrary.music:
                webbrowser.open(musicLibrary.music[song])
                speak(f"Playing {song}")
            else:
                speak(f"Could not find the song '{song}'")
        else:
            speak("Please say the song name after 'play'")

def send_mail(c):
        
        sender = os.getenv("EMAIL")
        receiver = input("Enter Email ID to send mail : ")
        password = os.getenv("EMAIL_PASSWORD")

        subject = "From Nitin"
        body = input("Enter Email (Body) : ")

        msg = MIMEText(body)
        msg['subject'] = subject
        msg['from'] = sender
        msg['to'] = receiver

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender, password)
                server.sendmail(sender, receiver, msg.as_string())
            speak("Mail send successfully")
            print("Mail send successfully")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    speak("Initializing AI Assistant!")

    while True:
        try:
            with sr.Microphone() as source:
                print("Say 'hello' to activate assistant...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
            word = recognizer.recognize_google(audio).lower()

            if word == "hello":
                speak("Yes, how can I help you?")
                with sr.Microphone() as source:
                    print("Listening for your command...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                    command = recognizer.recognize_google(audio)
                    print(command)
                    if "send mail" in command.lower():
                        send_mail(command)
                    elif "stop" in command.lower():
                        speak("Good Bye !")
                        break
                    else:
                        Ai_ans(command)
                        processCommand(command)
            

        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.WaitTimeoutError:
            print("Listening timed out.")
        except Exception as e:
            print(f"Error: {e}")
