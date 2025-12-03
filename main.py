import time
import requests
import speech_recognition as sr
from decouple import config
from datetime import datetime
from random import choice
import pyttsx3
import keyboard
import os
import subprocess as sp
import webbrowser
import imdb
import wolframalpha
import openai  # Make sure openai is imported

import pyautogui
from conv import random_text
from online import find_my_ip, search_on_wikipedia, search_on_google, youtube, send_email, get_news, weather_forecast

# Initialize the pyttsx3 engine
engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.0)
engine.setProperty('rate', 200)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

USER = config('USER')
HOSTNAME = config('BOT')

openai.api_key = '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'  # Replace with your actual OpenAI API key


def speak(text):
    """Function to make the bot speak the provided text."""
    engine.say(text)
    engine.runAndWait()


def greet_me():
    """Function to greet the user based on the current time."""
    hour = int(datetime.now().hour)
    if 6 <= hour < 12:
        speak(f"Good Morning {USER}")
    elif 12 <= hour < 16:
        speak(f"Good Afternoon {USER}")
    elif 16 <= hour < 19:
        speak(f"Good Evening {USER}")
    speak(f"I am {HOSTNAME}. How may I assist you, {USER}?")


listening = False


def start_listening():
    global listening
    listening = True
    print("Started Listening...")


def pause_listening():
    global listening
    listening = False
    print("Stopped Listening...")


keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)


def take_command():
    """Function to take voice commands from the user."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()

    except Exception as e:
        print(e)
        speak("Sorry I couldn't understand. Can you please repeat that?")
        return None


def search_movie_info(movie_name):
    """Function to search and retrieve movie information from IMDb."""
    movies_db = imdb.IMDb()
    movies = movies_db.search_movie(movie_name)

    if not movies:
        speak(f"Sorry, I couldn't find any information for {movie_name}")
        return

    speak(f"Searching for {movie_name}")
    speak(f"I found these movies:")

    for idx, movie in enumerate(movies[:2], 1):  # Limiting to the top 2 results
        movies_db.update(movie)
        title = movie.get('title', 'Title not available')
        year = movie.get('year', 'Year not available')
        speak(f"{idx}. {title} - {year}")

        # Retrieve more detailed information
        movie_id = movie.movieID
        movie_info = movies_db.get_movie(movie_id)
        rating = movie_info.get('rating', 'Rating not available')
        directors = movie_info.get('directors', ['Director not available'])
        director_names = ', '.join(director['name'] for director in directors)
        cast = movie_info.get('cast', [])
        actors = ', '.join(actor['name'] for actor in cast[:5])
        plot = movie_info.get('plot', [])
        plot_summary = plot[0] if plot else 'Plot summary not available'

        print(f"{title} was released in {year}.")
        print(f"IMDb Rating: {rating}")
        print(f"Director(s): {director_names}")
        print(f"Cast: {actors}")
        print(f"Plot Summary: {plot_summary}\n")

        speak(f"{title} was released in {year}.")
        speak(f"IMDb Rating: {rating}")
        speak(f"Directed by {director_names}")
        speak(f"Cast: {actors}")
        speak(f"Plot Summary: {plot_summary}")


def ask_chatgpt(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error querying ChatGPT: {e}")
        return "Sorry, I couldn't understand that."


if __name__ == '__main__':
    greet_me()
    while True:
        if listening:
            query = take_command()
            if query:
                if "how are you" in query:
                    speak("I am absolutely fine sir. What about you?")
                elif "open notepad plus" in query:
                    speak("Opening Notepad++...")
                    print("Opening Notepad++...")
                    sp.run("start notepad++", shell=True)
                elif "open command prompt" in query:
                    speak("Opening Command Prompt...")
                    print("Opening Command Prompt...")
                    os.system("start cmd")
                elif "open camera" in query:
                    speak("Opening Camera...")
                    print("Opening Camera...")
                    sp.run("start microsoft.windows.camera:", shell=True)
                elif "open crome" in query:
                    speak("Opening Chrome...")
                    print("Opening Chrome...")
                    sp.run("start chrome", shell=True)
                elif "open brave" in query:
                    speak("Opening Brave...")
                    print("Opening Brave...")
                    sp.run("start brave", shell=True)
                elif "open file explorer" in query:
                    speak("Opening File Explorer...")
                    print("Opening File Explorer...")
                    os.system("explorer")
                elif "open microsoft edge" in query:
                    speak("Opening Microsoft Edge...")
                    print("Opening Microsoft Edge...")
                    os.system("start microsoft-edge:")
                elif "open microsoft store" in query:
                    speak("Opening Microsoft Store...")
                    print("Opening Microsoft Store...")
                    os.system("start ms-windows-store:")
                elif "open vs code" in query:
                    speak("Opening VS Code...")
                    print("Opening VS Code...")
                    os.system("start vscode:")
                elif "ip address" in query:
                    ip_address = find_my_ip()
                    speak(f"Your IP address is {ip_address}")
                    print(f"Your IP address is {ip_address}")
                elif "open youtube" in query:
                    speak("What do you want to play on YouTube?")
                    video = take_command().lower()
                    youtube(video)
                elif "open google" in query:
                    speak("What do you want to search on Google?")
                    query = take_command().lower()
                    search_on_google(query)
                elif "wikipedia" in query:
                    speak("What do you want to search on Wikipedia?")
                    search = take_command().lower()
                    results = search_on_wikipedia(search)
                    print(results)
                    speak(f"According to Wikipedia: {results}")
                elif "send an email" in query:
                    speak("To which email address do you want to send, sir? Please enter in the terminal.")
                    receiver_add = input("Enter address:")
                    speak("What should be the subject, sir?")
                    subject = take_command().capitalize()
                    speak("What is the message?")
                    message = take_command().capitalize()
                    if send_email(receiver_add, subject, message):
                        speak("I have sent the mail, sir.")
                        print("I have sent the mail, sir.")
                    else:
                        speak("Something went wrong. Please check the error log.")
                elif "news" in query:
                    speak(f"I am reading out the latest headlines of today, sir.")
                    speak("I am printing it on screen, sir.")
                    print(*get_news(), sep='\n')
                    speak(get_news())
                elif "weather" in query:
                    ip_address = find_my_ip()
                    speak("Please tell me your city name.")
                    city = take_command()
                    if city:
                        weather, temp, feels_like = weather_forecast(city)
                        print(f"The City is {city}")
                        print(f"Weather: {weather}\nTemperature: {temp}\nFeels like: {feels_like}")
                        speak(f"The weather is {weather}. The current temperature in {city} is {temp}, but it feels like {feels_like}.")
                    else:
                        print("Could not detect city from IP address.")
                        speak("Could not detect city from IP address.")
                elif "movie" in query:
                    speak("Please tell me the name of the movie.")
                    movie_name = take_command()
                    if movie_name:
                        search_movie_info(movie_name)
                elif "calculate" in query:
                    app_id = "7WTGPG-8G7JRX3AQJ"
                    client = wolframalpha.Client(app_id)
                    ind = query.lower().split().index("calculate")
                    text = query.split()[ind + 1:]
                    result = client.query(" ".join(text))
                    try:
                        ans = next(result.results).text
                        print("The answer is {}".format(ans))
                        speak("The answer is {}".format(ans))

                    except StopIteration:
                        speak("Sorry, I couldn't find the answer.")

                elif "stop" in query or "exit" in query or 'quit' in query:
                    hour = datetime.now().hour
                    if 21 <= hour < 6:
                        speak("Good night sir, take care!")
                    else:
                        speak("Have a good day sir!")
                    break
                else:
                    # Handle other commands or provide a random response
                    # Replace 'random_text' with your own list of responses
                    speak(choice(random_text))
                    response = ask_chatgpt(query)
                    speak(response)
