import wikipedia
import requests
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
import imdb
import pyttsx3
from decouple import config

EMAIL = "bhanutejanedunuri@gmail.com"
PASSWORD = "fidp bwzt oqes xqnc"


def find_my_ip():
    ip_address = requests.get('https://api.ipify.org?format=json').json()
    return ip_address["ip"]


def search_on_wikipedia(query):
    result = wikipedia.summary(query, sentences=2)
    return result


def search_on_google(query):
    kit.search(query)


def youtube(video):
    kit.playonyt(video)


def send_email(reciver_add, subject, message):
    try:
        email = EmailMessage()
        email['To'] = reciver_add
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False


def get_news():
    news_headlines = []
    result = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=in&category=general&apiKey=fc5ce5d0848f49809b3e3813c8edb326").json()
    articles = result["articles"]
    for article in articles:
        news_headlines.append(article['title'])
    return news_headlines[:6]

def get_city_from_ip(ip_address):
    """Function to get the city based on the IP address."""
    response = requests.get(f'https://ipinfo.io/{ip_address}/json').json()
    return response.get('city')


def weather_forecast(city):
    """Function to get the weather forecast for the given city."""
    api_key = 'e6d106e178c12fbe7850a6e9fea3b21e'
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    res = requests.get(url).json()

    if res.get('cod') != 200:
        return res.get('message', 'Error fetching the weather data.')

    weather = res['weather'][0]['main']
    temp_k = res['main']['temp']
    feels_like_k = res['main']['feels_like']

    # Convert from Kelvin to Celsius
    temp_c = temp_k - 273.15
    feels_like_c = feels_like_k - 273.15
    return weather, f"{temp_c:.2f}°C", f"{feels_like_c:.2f}°C"



