import speech_recognition as sr
import webbrowser
import pyttsx3
import openai
import requests
from PIL import Image
from io import BytesIO
import wikipedia
import datetime
import json
from urllib.request import urlopen
import time

# Set your OpenAI API key here
openai.api_key = 'API KEY'

# Initialize speech recognition, TTS engine, and web browser
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()


# Define the speak function
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Define the takeCommand function
def takeCommand():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        print("You said:", query)
        return query

    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        speak("Sorry, I didn't catch that. Please try again.")
        return ""
    except sr.RequestError as e:
        print(f"Sorry, there was an error connecting to the speech recognition service: {e}")
        speak(f"Sorry, there was an error connecting to the speech recognition service. Please try again later.")
        return ""



# Define the wishMe function
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir !")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir !")

    else:
        speak("Good Evening Sir !")
def greet():
    speak("Welcome to the Jarvis, How can I help you?")


chat_history = []


# Function to add user and assistant messages to the chat history
def add_to_chat_history(user_message, assistant_message):
    chat_history.append(f"You: {user_message}")
    chat_history.append(f"Jarvis: {assistant_message}")
    speak(assistant_message)


# Function to fetch and save NASA picture of the day
def fetch_nasa_apod():
    apod_url = "https://api.nasa.gov/planetary/apod"
    api_key = "YOUR_API_KEY"  # Get your API key from NASA

    response = requests.get(apod_url, params={"api_key": api_key})

    if response.status_code == 200:
        apod_data = response.json()
        image_url = apod_data["url"]
        image_response = requests.get(image_url)
        image_data = image_response.content

        image = Image.open(BytesIO(image_data))
        image.save("nasa_apod.jpg")

        print("NASA Picture of the Day saved successfully.")
    else:
        print(f"Error fetching NASA Picture of the Day. Status code: {response.status_code}")


# Function to search Wikipedia and save as a text file
def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=1)  # Limit to 1 sentence for brevity
        with open("wikipedia_result.txt", "w") as file:
            file.write(result)
        print("Wikipedia search result saved as wikipedia_result.txt")
        speak("Wikipedia search result saved.")
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"Ambiguous term. Please be more specific.")
        speak("Ambiguous term. Please be more specific.")
    except wikipedia.exceptions.HTTPTimeoutError as e:
        print(f"Failed to connect to Wikipedia. Please try again later.")
        speak("Failed to connect to Wikipedia. Please try again later.")


# Function to get and speak current date and time
def get_date_time():
    now = datetime.datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    return current_date, current_time


# Function to fetch and speak news
def get_news():
    try:
        jsonObj = urlopen(
            '''https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey=YOUR_API_KEY''')
        data = json.load(jsonObj)
        i = 1

        speak('Here are some top news from the Times of India')
        print('''=============== TIMES OF INDIA ============''' + '\n')

        for item in data['articles']:
            print(str(i) + '. ' + item['title'] + '\n')
            print(item['description'] + '\n')
            speak(str(i) + '. ' + item['title'] + '\n')
            i += 1
    except Exception as e:
        print(str(e))
        speak("Sorry, I couldn't fetch the news at the moment.")


# Greet the user
wishMe()
greet()

listening = True

while True:
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)

        print("You said:", user_input)

        if "exit" in user_input:
            print("Exiting program...")
            speak("Exiting program...")
            listening = False  # Set listening to False to break out of the loop

        # Check for specific commands
        elif "open Google" in user_input:
            print("Opening Google...")
            speak("Opening Google...")
            webbrowser.open("https://www.google.com")
            speak("Google is now open.")

        elif "open YouTube" in user_input:
            print("Opening YouTube...")
            speak("Opening YouTube...")
            webbrowser.open("https://www.youtube.com")
            speak("youtube is now open.")

        elif "search on Google" in user_input:
            query = user_input.replace("search on Google", "").strip()
            print(f"Searching on Google: {query}")
            speak(f"Searching on Google: {query}")
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            speak("Search is now open.")

        # Check for fetching NASA Picture of the Day
        elif "NASA picture of the day" in user_input:
            print("Fetching NASA Picture of the Day...")
            speak("Fetching NASA Picture of the Day...")
            fetch_nasa_apod()
            speak("NASA Picture of the Day is now open.")

        # Check for searching on Wikipedia
        elif "search on Wikipedia" in user_input:
            query = user_input.replace("search on Wikipedia", "").strip()
            print(f"Searching on Wikipedia: {query}")
            speak(f"Searching on Wikipedia: {query}")
            search_wikipedia(query)
            speak("Wikipedia Search is now open.")

        # Check for asking for date
        elif "date" in user_input:
            current_date, _ = get_date_time()
            print(f"Current date is: {current_date}")
            speak(f"The current date is {current_date}")
            print(current_date)

        # Check for asking for time
        elif "time" in user_input:
            _, current_time = get_date_time()
            print(f"Current time is: {current_time}")
            speak(f"The current time is {current_time}")
            print(current_time)

        # Check for news
        elif "news" in user_input:
            get_news()
            speak("News is now open.")

        # Check for stopping listening
        elif "don't listen" in user_input or "stop listening" in user_input:
            speak("For how much time you want to stop Jarvis from listening to commands?")
            a = int(takeCommand())
            time.sleep(a)
            print(a)
            speak("Ok, I will stop listening to commands.")

        else:
            # Add the user's message to the chat history
            add_to_chat_history(user_input, "")

            # Combine the chat history into a single string
            chat_input = "\n".join(chat_history)

            # Use OpenAI to generate a response based on the chat history
            response = openai.Completion.create(
                engine="davinci",
                prompt=chat_input,
                max_tokens=50
            )

            # Get the assistant's response from OpenAI
            assistant_response = response.choices[0].text.strip()

            print("Assistant:", assistant_response)

            # Add the assistant's response to the chat history
            add_to_chat_history("", assistant_response)

    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        speak("Sorry, I didn't catch that.")
    except sr.RequestError as e:
        print(f"Sorry, there was an error connecting to the speech recognition service: {e}")
        speak("Sorry, there was an error connecting to the speech recognition service.")
