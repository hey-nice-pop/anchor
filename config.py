from dotenv import load_dotenv
load_dotenv()

import os

BOT_TOKEN = os.getenv('BOT_TOKEN')#bottoken
WEATHER_KEY = os.getenv('WEATHER_KEY')#openweatherAPI