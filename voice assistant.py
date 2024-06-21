import speech_recognition as sr
import pywhatkit
import pyttsx3
import webbrowser
import subprocess
import datetime
import os
import pygame

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen and recognize speech
def listen():
    with sr.Microphone() as source:
        print("Clearing background noises... Please wait")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print('Ask me anything...')
        try:
            recorded_audio = recognizer.listen(source, timeout=5)
            print("Done recording!")
            return recorded_audio
        except sr.WaitTimeoutError:
            print("Timeout error: No speech detected.")
            return None

# Function to process recognized text
def process_command(text):
    text = text.lower()
    print('Your message:', text)

    if 'chrome' in text:
        speak('Opening Chrome')
        # List of potential Chrome paths
        potential_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        chrome_path = None
        for path in potential_paths:
            if os.path.exists(path):
                chrome_path = path
                break
        if chrome_path:
            subprocess.Popen([chrome_path])
        else:
            speak("Chrome executable not found. Please check the installation path.")
    elif 'time' in text:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        print(current_time)
        speak(f"The current time is {current_time}")
    elif 'play' in text:
        speak('Opening YouTube')
        pywhatkit.playonyt(text.replace('play', '').strip())
    elif 'youtube' in text:
        speak('Opening YouTube')
        webbrowser.open('http://www.youtube.com')
    elif 'music' in text:
        play_music(text)
    else:
        speak("Sorry, I didn't catch that. Please try again.")
        print("Sorry, I didn't catch that. Please try again.")

# Function to play music from Downloads directory
def play_music(query):
    music_dir = r'C:\Users\SONU\Downloads'
    if not os.path.exists(music_dir):
        speak("The specified music directory does not exist.")
        print(f"Directory does not exist: {music_dir}")
        return

    songs = os.listdir(music_dir)
    print(f"Songs found: {songs}")

    song_map = {
        'alone': 'alone.mp3',
        'faded': 'faded.mp3',
        'coldplay': 'coldplay.mp3',
        'alone pt. ii': 'alone, pt. ii.mp3',
        'unstoppable': 'unstoppable.mp3',
        'closer by charlie puth': 'closer by charlie puth.mp3',
        'let it go': 'let it go.mp3',
        'electronomia': 'electronomia.mp3',
        'spectre': 'spectre.mp3',
        'cheap thrills': 'cheap thrills.mp3',
        'believer': 'believer.mp3',
        'stereo hearts': 'stereo hearts.mp3',
        'my heart will go on': 'my heart will go on.mp3',
        'bad liar': 'bad liar.mp3',
        'bilionera': 'bilionera.mp3',
        'see you again': 'see you again.mp3',
        'a thousand years by christina perri': 'a thousand years by christina perri.mp3',
        'on the floor': 'on the floor.mp3',
        'fat rat': 'fat rat.mp3',
        'bones ft imagine dragons': 'bones ft imagine dragons.mp3',
        'on my way alan walker ft sebrina carpenter': 'on my way alan walker ft sebrina carpenter.mp3',
        'aviva princesses don\'t cry': 'aviva princesses don\'t cry.mp3',
        'lindsey stirling carol of the bells': 'lindsey stirling carol of the bells.mp3',
        'katy perry dark horse': 'katy perry dark horse.mp3',
        'hey mama ft nicki minaj': 'hey mama ft nicki minaj.mp3',
        'ava max kings and queens': 'ava max kings and queens.mp3',
        'let me down slowly ft alessia cara': 'let me down slowly ft alessia cara.mp3',
        'katty perry firework': 'katty perry firework.mp3',
        'into your arms ft ava max': 'into your arms ft ava max.mp3',
        'alan walker darkside': 'alan walker darkside.mp3',
        'ava max sweet but psycho': 'ava max sweet but psycho.mp3',
        'sweet but psycho by ava max speed up speedup': 'sweet but psycho by ava max speed up speedup.mp3',
        'celine dion my heart will go on lyrics': 'celine dion my heart will go on lyrics.mp3'
    }

    song_found = False
    for key, song in song_map.items():
        if key in query:
            song_path = os.path.join(music_dir, song)
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play()
                speak(f"Playing {song}")
                song_found = True
                break
            except pygame.error as e:
                speak("An error occurred while playing the song.")
                print(f"Error playing {song}: {e}")
                return

    if not song_found:
        speak("Sorry, I couldn't find the song in your music directory.")
        print(f"Song not found in directory: {query}")

# Main function to run the voice assistant
def main():
    while True:
        recorded_audio = listen()
        if recorded_audio is not None:
            try:
                text = recognizer.recognize_google(recorded_audio, language='en_US')
                process_command(text)
            except sr.UnknownValueError:
                speak("Sorry, I did not understand that.")
                print("Sorry, I did not understand that.")
            except sr.RequestError:
                speak("Could not request results; check your network connection.")
                print("Could not request results; check your network connection.")
        else:
            speak("No speech detected. Please try again.")
            print("No speech detected. Please try again.")

if __name__ == "__main__":
    speak("Initializing voice assistant.")
    main()
