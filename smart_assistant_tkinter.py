import tkinter as tk
import pyttsx3
import speech_recognition as sr
import mysql.connector
import cv2
import pytesseract
import datetime
import subprocess
import pyautogui
import webbrowser
import time
import pywhatkit

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize speech recognition
recognizer = sr.Recognizer()

# Establish MySQL connection
connection = mysql.connector.connect(host="localhost", port="3306", user="root", password="MySQL1601#div", database="smartAssistant")
cursor = connection.cursor()

if connection.is_connected():
    print("Connected to MySQL")
else:
    print("Not connected to MySQL")



def text_to_speech(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

def perform_ocr():
    engine.say("Please hold a document in front of the camera.")
    engine.runAndWait()

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    key = cv2.waitKey(1)
    webcam = cv2.VideoCapture(0)
    while True:
        try:
            check, frame = webcam.read()
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            if key == ord('z'):
                cv2.imwrite(filename='C:/SAImages/saved_img.jpg', img=frame)
                webcam.release()
                string = pytesseract.image_to_string('C:/SAImages/saved_img.jpg')
                print(string)
                engine.say(string)
                engine.runAndWait()
                cv2.destroyAllWindows()
                break

        except KeyboardInterrupt:
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break

def voice_assistant():
    text_to_speech("How can I assist you today?")
    print("Listening...")
    while True:
        command = get_voice_input()
        if "notepad" in command:
            text_to_speech("Opening Notepad. Please dictate the content.")
            subprocess.Popen(["notepad.exe"])
            content = get_voice_input()
            if content:
                pyautogui.typewrite(content)
                text_to_speech("Content typed successfully. Do you want to save it?")
                save_command = get_voice_input()
                if "yes" in save_command:
                    pyautogui.hotkey('ctrl', 's')
                    text_to_speech("Content saved successfully. Please provide the file name.")
                    file_name = get_voice_input()
                    if file_name:
                        pyautogui.typewrite(file_name)
                        pyautogui.press('enter')
                        text_to_speech(f"File {file_name} saved successfully.")
                   

        elif "command prompt" in command:
            webbrowser.open("cmd")
            time.sleep(2)  # Wait for 2 seconds to open Command Prompt
            text_to_speech("Opening Command Prompt. Please dictate the command.")
            command_text = get_voice_input()
            if command_text:
                pyautogui.typewrite(command_text, interval=0.1)  # Typing the command with an interval of 0.1 seconds
                pyautogui.press('enter')  # Pressing Enter to execute the command
                text_to_speech("Command executed successfully.")
            else:
                text_to_speech("No command was provided.")
                time.sleep(5)  # Wait for 5 seconds before listening for the next command



        elif "find" in command:
            text_to_speech("What do you want to search on Google?")
            search_query = get_voice_input()
            url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(url)
            time.sleep(10)
    
        elif "play" in command:
            text_to_speech("What do you want to search on YouTube?")
            search_query = get_voice_input()
            pywhatkit.playonyt(search_query)
            time.sleep(10)
        elif "maps" in command:
            text_to_speech("Opening Maps")
            webbrowser.open("https://www.google.com/maps")
            time.sleep(5)
        elif "control panel" in command:
            text_to_speech("Opening Control Panel")
            webbrowser.open("control")
            time.sleep(5)
        elif "microsoft news" in command:
            text_to_speech("Opening Microsoft News")
            webbrowser.open("https://www.microsoft.com/en-us/news")
            time.sleep(5)
        elif "calendar" in command:
            text_to_speech("Opening Calendar")
            webbrowser.open("https://calendar.google.com")
            time.sleep(5)
        elif "calculator" in command:
            text_to_speech("Opening Calculator")
            webbrowser.open("calc")
            time.sleep(5)
        elif "date" in command:
            now = datetime.datetime.now()
            date = now.strftime("%A, %B %d, %Y")
            text_to_speech(f"The current date is {date}")
            time.sleep(5)
        
        elif "exit" in command:
            text_to_speech("Goodbye! see you soon")
            break
        else:
            text_to_speech("Sorry, I didn't catch that. Can you repeat?")
        text_to_speech("How can I help you today?")
        print("Listening...")



def retrieve_from_database():
    text_to_speech("Welcome to the Java Book Voice Assistant.")
    text_to_speech("Please say the chapter name.")
    chapter_name = get_voice_input()
    result = search_chapter(chapter_name)
    text_to_speech(result)

def get_voice_input():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        user_input = recognizer.recognize_google(audio)
        print("User said:", user_input)
        return user_input
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print("Error fetching results: {0}".format(e))
        return ""

def search_chapter(chapter_name):
    cursor.execute("SELECT jfile FROM jbook WHERE chapter_name LIKE %s", ('%' + chapter_name + '%',))
    result = cursor.fetchall()
    if result:
        if len(result) == 1:
            return result[0][0]
        elif len(result) > 1:
            return "Please be more specific."
    return "Chapter not found."

def get_user_name():
    text_to_speech("May I know your name?")
    user_name = get_voice_input()
    return user_name

def offer_wishes():
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        text_to_speech("Good morning!")
    elif 12 <= current_hour < 18:
        text_to_speech("Good afternoon!")
    elif 18 <= current_hour < 22:
        text_to_speech("Good evening!")
    else:
        text_to_speech("Good night!")

def exit_program():
    root.destroy()

root = tk.Tk()
root.title("Smart Assistant")
root.geometry("800x600")  # Set the size of the screen to 800x600

user_name = get_user_name()
if user_name:
    text_to_speech(f"Hello, {user_name}!")
offer_wishes()

btn_voice_assistant = tk.Button(root, text="Voice Assistant", command=voice_assistant)
btn_voice_assistant.pack()

btn_ocr = tk.Button(root, text="OCR", command=perform_ocr)
btn_ocr.pack()

btn_database = tk.Button(root, text="Database", command=retrieve_from_database)
btn_database.pack()

btn_exit = tk.Button(root, text="Exit", command=exit_program)
btn_exit.pack()

root.mainloop()

# Close MySQL connection and cursor
cursor.close()
connection.close()
