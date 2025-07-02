import asyncio 
import datetime 
import webbrowser 
import platform 
try:
    import pyttsx3
except ImportError:
    pyttsx3 = None
try:
    import speech_recognition as sr
except ImportError:
    sr = None
try:
    import wikipedia
except ImportError:
    wikipedia = None
try:
    import requests
except ImportError:
    requests = None

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5') if pyttsx3 else None
if engine:
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)  

def speak(audio):
    """Speak the provided text if TTS is available."""
    if engine:
        try:
            engine.say(audio)
            engine.runAndWait()
        except Exception as e:
            print(f"Error in speak: {e}")
    else:
        print(f"Speech not available: {audio}")

def wish_me():
    """Greet user based on time of day."""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis, your assistant. How can I assist you today?")

def take_command():
    """Capture voice input and return text query."""
    if not sr:
        print("Speech recognition not available.")
        return input("Type your command: ").lower()
    
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            print("No input detected. Please try again.")
            return "None"
        except Exception as e:
            print(f"Error recognizing speech: {e}")
            return "None"

def get_weather(city):
    """Fetch weather data for a given city using a free API."""
    if not requests:
        return "Weather service not available."
    api_key = "8b5c375f3def9a6d908a1f37d6dd8cb4"  
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != 200:
            return f"Could not fetch weather for {city}."
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"The weather in {city} is {desc} with a temperature of {temp} degrees Celsius."
    except Exception as e:
        return f"Error fetching weather: {e}"

def get_news():
    """Fetch top news headlines using a free API."""
    if not requests:
        return "News service not available."
    api_key = "4033cb3b14094cefa8a17bed295d762f"  
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get("articles", [])[:3]  
        if not articles:
            return "No news available at the moment."
        news_summary = "Here are the top news headlines: "
        for i, article in enumerate(articles, 1):
            news_summary += f"{i}. {article['title']}. "
        return news_summary
    except Exception as e:
        return f"Error fetching news: {e}"

async def main():
    """Main loop for the voice assistant."""
    wish_me()
    while True:
        query = take_command()
        if query == "none":
            continue
        if "exit" in query or "stop" in query:
            speak("Goodbye, sir!")
            break
        elif "wikipedia" in query:
            if wikipedia:
                speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "").strip()
                try:
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)
                except Exception as e:
                    speak(f"Sorry, I couldn't find anything on Wikipedia about {query}.")
                    print(f"Wikipedia error: {e}")
            else:
                speak("Wikipedia service is not available.")
        elif "open youtube" in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
        elif "open google" in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
        elif "the time" in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {str_time}")
        elif "open code" in query:
            speak("Visual Studio Code opening is not supported in this environment.")
        elif "weather in" in query:
            city = query.replace("weather in", "").strip()
            weather_info = get_weather(city)
            speak(weather_info)
            print(weather_info)
        elif "news" in query:
            news_info = get_news()
            speak(news_info)
            print(news_info)
        else:
            speak("Sorry, I didn't understand that command. Please try again.")
        await asyncio.sleep(0.1)  
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
