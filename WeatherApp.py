# # Create a commandline weather app in Python that fetches and displays current weather data for a user specified location (eg : city or ZIP code) using a weather API. Show basic information such as temp,humidity,weather conditions,wind speed etc.

import requests
import tkinter as tk
from tkinter import messagebox

def get_weather(api_key, location):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    complete_url = f"{base_url}?q={location}&appid={api_key}&units=metric"
    
    response = requests.get(complete_url)
    if response.status_code == 200:
        # Convert the response to JSON
        data = response.json()

        # Parse data
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        weather = data['weather'][0]['description']
        wind_speed = data['wind']['speed']

        # Display the weather information
        weather_info = (f"Weather in {location}:\n"
                        f"Temperature: {temp}°C\n"
                        f"Humidity: {humidity}%\n"
                        f"Conditions: {weather}\n"
                        f"Wind speed: {wind_speed} m/s")
        return weather_info
    else:
        return "Error fetching weather data. Please check the location or your network connection."

def display_weather():
    location = location_entry.get()
    weather_info = get_weather(api_key, location)
    result_label.config(text=weather_info)

# Tkinter setup
root = tk.Tk()
root.title("Weather App")

api_key = "57e304a6f7460127ac00c1502219a0c0"  # Use your actual OpenWeatherMap API key

# Create the layout
location_label = tk.Label(root, text="Enter a city or ZIP code:")
location_label.pack()

location_entry = tk.Entry(root)
location_entry.pack()

get_weather_button = tk.Button(root, text="Get Weather", command=display_weather)
get_weather_button.pack()

result_label = tk.Label(root, text="", justify=tk.LEFT)
result_label.pack()

root.mainloop()
