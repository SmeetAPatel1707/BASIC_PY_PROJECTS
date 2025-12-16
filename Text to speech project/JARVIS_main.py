# Importing all necessory libraries.
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
# Import pygame for music control
import pygame  
from pyzbar.pyzbar import decode
# Weather
from bs4 import BeautifulSoup
# News , weather 
import requests

# __________________________________________________________________________________________________________________________________________________

engine = pyttsx3.init('sapi5') 
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
print(voices[0].id)


# __________________________________________________________________________________________________________________________________________________
# speak function :  it takes a string as an argument and converts the text to speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
# WishMe function : Wishing To you according  to the time of day: Morning, Afternoon or Night.
def WishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>0 and hour<12 :
        speak("Good Morning Sir")
    if hour>12 and hour<18 :
        speak("Good Afternoon Sir")
    if hour>18 and hour<24:
        speak("Good Evening Sir")
        
    speak("I am JARVIS. Just A Rather Virtual Intelligent System, Made by Smeet Industries corporation.")
    speak("You need to authenticate yourself.")
    speak("Please enter your password sir")

    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            speak("Enter the password sir :")
            password = input("Enter password :")
            if password == "23031972":
                speak("Welcome back sir")
                return "Welcome back sir"
            else:
                speak("Incorrect password sir. please try again")
                return "Incorrect password sir"
        except sr.UnknownValueError:
            speak("Please say the password again sir")
            return "Please say the password again"
        except sr.RequestError as e:
            speak("Could not request results from Google Speech Recognition service; {0}".format(e))
            return "Could not request results from Google Speech Recognition service; {0}".format(e)
# _________________________________________________________________________________________________________________________
# Take Command() : it take  the command from the user using microphone and returns output in form of string.
def TakeCommand():
    r = sr.Recognizer()
    with  sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said:{query}\n")
    except Exception as e:
        # print(e)
        print("Say that again !")
        return "None"
    return query

# _________________________________________________________________________________________________________________________
# Send Mail function: This Function is used to send email to any recipient via Gmail server.
def SendMail(to,content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("smit99738@gmail.com", "SpA@17jul2003")
    server.sendmail( "smit99738@gmail.com", to , content)
    server.close()
    
# _________________________________________________________________________________________________________________________
# Play Music from library.
def PlayMusic(song_name=None):
    pygame.mixer.init()
    music_path = 'C:\\Users\\ASHOK PATEL\\Music'
    songs = os.listdir(music_path)
    if song_name:
        for song in songs:
            if song_name.lower() in song.lower():
                pygame.mixer.music.load(os.path.join(music_path, song))
                pygame.mixer.music.play()
                speak(f"Playing {song_name}")
                return
        speak("Song not found.")
    else:
        pygame.mixer.music.load(os.path.join(music_path, songs[0]))
        pygame.mixer.music.play()
        speak("Playing music")
        
# _________________________________________________________________________________________________________________________
# Tell about weather : 925104c6e5607bb45e9a0082ec74aca0
def Get_weather():
    api_key = "925104c6e5607bb45e9a0082ec74aca0"  # Replace with your OpenWeatherMap API key
    speak("Please tell me the city name.")
    city = TakeCommand().lower()
    
    # Make an API call to OpenWeatherMap
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    
    try:
        # Parse the JSON response
        data = response.json()
        
        # Debugging: Print the full response to check what's coming back
        print(f"API Response: {data}")
        
        if data.get("cod") == 200:
            # Extract weather information if the response is valid
            main = data['main']
            temperature = main['temp']
            weather_desc = data['weather'][0]['description']
            city_name = data['name']
            country = data['sys']['country']

            # Speak out the weather details
            speak(f"The weather in {city_name}, {country} is currently {weather_desc} with a temperature of {temperature} degrees Celsius.")
            print(f"The weather in {city_name}, {country}: {weather_desc}, {temperature}°C")
        else:
            # Handle different error codes and provide feedback
            error_message = data.get("message", "Unknown error occurred.")
            speak(f"Sorry, I couldn't retrieve the weather. Error: {error_message}")
            print(f"Error: {error_message}")

    except Exception as e:
        # Handle unexpected errors
        speak("Sorry, there was an error processing the request.")
        print(f"Error: {str(e)}")

# _________________________________________________________________________________________________________________________
# Tell about news:
def Get_news(): 
    api_key = "240bde8c08fe4e0a84aef51fbd23ba16"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    news_data = response.json()

    articles = news_data["articles"]
    news_headlines = []
    for article in articles[:5]:  # Get top 5 headlines
        news_headlines.append(article["title"])
    
    return news_headlines
# Example usage
def news_command():
    speak("Here are the top news headlines.")
    headlines = Get_news()
    for headline in headlines:
        speak(headline)
        print(headline)
        
# _________________________________________________________________________________________________________________________
def Get_Motivate():
    response = requests.get("https://zenquotes.io/api/random")
    quote_data = response.json()
    quote = quote_data[0]["q"] + " -" + quote_data[0]["a"]
    return quote
# Example usage
def quote_command():
    quote = Get_Motivate()
    speak(quote)
    print(quote)

# _________________________________________________________________________________________________________________________
def Tell_Joke():
    url = "https://v2.jokeapi.dev/joke/Any"
    response = requests.get(url)
    joke_data = response.json()

    if joke_data["type"] == "single":
        return joke_data["joke"]
    else:
        return f"{joke_data['setup']} ... {joke_data['delivery']}"
# Example usage
def joke_command():
    joke = Tell_Joke()
    speak(joke)
    print(joke)
    
# _______________________________________________________________________________________________________________________________
# Function to track a flight using the AviationStack API
def TrackFlight():
    api_key = "f91ac50b461aa9b475363dac18705f6a"  # Replace with your AviationStack API key
    speak("Please tell me the flight number.")
    
    # Get the flight number from the user
    flight_number = TakeCommand().upper()  # Convert to uppercase to match flight code format

    url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&flight_iata={flight_number}"

    try:
        # Make an API call to AviationStack
        response = requests.get(url)
        flight_data = response.json()

        # Check if flight information is available
        if flight_data["data"]:
            # Extract relevant flight information
            flight              = flight_data["data"][0]
            airline             = flight["airline"]["name"]
            departure_airport   = flight["departure"]["airport"]
            arrival_airport     = flight["arrival"]["airport"]
            departure_time      = flight["departure"]["scheduled"]
            arrival_time        = flight["arrival"]["scheduled"]
            status              = flight["flight_status"]

            # Construct a message with the flight details
            flight_info = (f"Flight {flight_number} operated by {airline} is currently {status}. "
                           f"It departed from {departure_airport} ,and is scheduled to arrive at {arrival_airport}. "
                          )

            # Speak the flight information
            print(flight_info, f"Departure time: {departure_time}, Arrival time: {arrival_time}.")
            speak(flight_info)
        
        else:
            speak(f"Sorry, I couldn't find information of flight {flight_number}.")
            print(f"No information found of flight {flight_number}.")

    except Exception as e:
        speak("Sorry, there was an error processing your request.")
        print(f"Error: {str(e)}")
        
# __________________________________________________________________________________________________________________________________________________
# RESOLVE AN ERROR >>>>>>>>>>>>>>

def get_phone_details(phone_number):
    # api_key = "fdffa27a6adab953eba57b1eff35cee6"
    api_key = "adde46ee895bb99b205bbb7452ba3e49"   #gzMwwKjXjrh8ynKSXstkOpWgT0tj7NuW
    url = f"http://apilayer.net/api/validate?access_key={api_key}&number={phone_number}"
    try:
        response = requests.get(url)
        data = response.json()
        
        # Check if the API request was successful
        if response.status_code != 200:
            return f"API Error: {data.get('error', {}).get('info', 'Unknown error')}"
        
        # Check if the response contains the 'valid' key
        if 'valid' not in data:
            return f"Invalid response from API: {data}"
        
        # If the phone number is valid, return the details
        if data['valid']:
            return {
                "Country": data.get('country_name', 'N/A'),
                "Location": data.get('location', 'N/A'),
                "Carrier": data.get('carrier', 'N/A'),
                "Line Type": data.get('line_type', 'N/A')
            }
        else:
            return "Invalid phone number"
    
    except Exception as e:
        return f"An error occurred: {e}"

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< GUI FOR THIS by using Gradio library >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Gradio GUI
import gradio as gr

def launch_gui():
    with gr.Blocks() as gui:
        gr.Markdown("JARVIS GUI")
        
        # Email Section
        with gr.Row():
            email_to = gr.Textbox(label="Recipient Email")
            email_content = gr.Textbox(label="Email Content")
            email_button = gr.Button("Send Email")
            email_output = gr.Textbox(label="Email Status")
            email_button.click(SendMail, inputs=[email_to, email_content], outputs=email_output)

        # Music Section
        with gr.Row():
            song_name = gr.Textbox(label="Song Name")
            play_music_button = gr.Button("Play Music")
            music_output = gr.Textbox(label="Music Status")
            play_music_button.click(PlayMusic, inputs=song_name, outputs=music_output)

        # Weather Section
        with gr.Row():
            city_name = gr.Textbox(label="City")
            weather_button = gr.Button("Get Weather")
            weather_output = gr.Textbox(label="Weather Details")
            weather_button.click(Get_weather, inputs=city_name, outputs=weather_output)

        # News Section
        with gr.Row():
            news_button = gr.Button("Get News")
            news_output = gr.Textbox(label="News Headlines")
            news_button.click(Get_news, outputs=news_output)

        # Quote Section
        with gr.Row():
            quote_button = gr.Button("Get Motivation")
            quote_output = gr.Textbox(label="Motivational Quote")
            quote_button.click(Get_Motivate, outputs=quote_output)

        # Joke Section
        with gr.Row():
            joke_button = gr.Button("Tell a Joke")
            joke_output = gr.Textbox(label="Joke")
            joke_button.click(Tell_Joke, outputs=joke_output)

        # Flight Tracking Section
        with gr.Row():
            flight_number = gr.Textbox(label="Flight Number")
            flight_button = gr.Button("Track Flight")
            flight_output = gr.Textbox(label="Flight Status")
            flight_button.click(TrackFlight, inputs=flight_number, outputs=flight_output)

        # Phone Tracking Section
        with gr.Row():
            phone_number = gr.Textbox(label="Phone Number")
            phone_button = gr.Button("Track Phone Number")
            phone_output = gr.Textbox(label="Phone Details")
            phone_button.click(get_phone_details, inputs=phone_number, outputs=phone_output)

    gui.launch()

# __________________________________________________________________________________________________________________________________________________

# Main function :  Calling the WishMe() function & Listening for voice commands
if __name__ == '__main__':
    
    launch_gui()
    # Wishing to me at the biginig :
    WishMe()
    
# if 1: # If we don't want to keep running this program !

    while True : # When we want to run continuously this program !
        query = TakeCommand().lower()
        # Tasks :
        
        # _________________________________________________________________________________
        
        # Search anything accordig  to wikipedia :
        
        if 'according to you' in query:
            speak("searching...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=5)
            speak("According to me")
            print(results)
            speak(results)
        
        # _________________________________________________________________________________

        # Opening my personal youtube channel :
        elif 'my youtube channel' in query :
            webbrowser.open("https://www.youtube.com/channel/UCmRqUynrJUdZgVs-zy91i9w")
               
        # _________________________________________________________________________________
        # Opening Google :
        elif 'open google' in query :
            speak("What would you like to search on Google?")
            search_query = TakeCommand().lower()
            if search_query != "None":
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
            else:
                speak("Sorry, I couldn't understand. Please try again.")
        
        # _________________________________________________________________________________
        
        # Play music by song name
        elif 'play music' in query:
            speak("Which song would you like to play?")
            song_name = TakeCommand().lower()
            PlayMusic(song_name)
            
        elif 'play another music' in query or 'please play another music' in query:
            speak("Which song would you like to play?")
            song_name = TakeCommand().lower()
            PlayMusic(song_name)
            
        # Pause music
        elif 'Stop' in query:
            pygame.mixer.music.pause()
            speak("Music paused")

        # Resume music
        elif 'Continue' in query:
            pygame.mixer.music.unpause()
            speak("Music resumed")
            
        # _________________________________________________________________________________
        
        # Display the current time :
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print("TIME :",strTime)
            speak(f"Sir, the current time is {strTime}")
        
        # _________________________________________________________________________________
           
        # Opening my V.S.Code  editor :
        elif 'vs code' in query:
            VS_code = 'C:\\VS Code\\Code.exe'
            os.startfile(VS_code)
            
        # _________________________________________________________________________________
        
        # Opening my GitHub Profile :
        elif 'github' in query:
            git = 'C:\\Users\\ASHOK PATEL\\OneDrive\\Desktop\\GitHub.lnk'
            os.startfile(git)
            
        # _________________________________________________________________________________
            
        # Sending Email to Recipent automatically :
        elif 'email' in query:
            try :
                speak('What should I say ?')
                content = TakeCommand()
                speak("Please enter email id of recipent:")
                to = input("To :")
                SendMail(to,content)
                speak("Email has been sent.")
                
            except Exception as e:
                print(e)
                speak("Sorry sir , I am unable to send this email.")
                
        # _________________________________________________________________________________

        # Giving an information about weather in your region.
        elif 'weather' in query:
            Get_weather()
            
        # _________________________________________________________________________________
        
        # NEWS :
        elif 'news' in query:
            speak('News is being read out to you')
            news_command()

        # _________________________________________________________________________________
        
        # Motivation Quotes :
        elif 'motivation' in query:
            quote_command()
            
        # _________________________________________________________________________________
        
        # Tell us a joke :
        elif 'joke' in query:
            joke_command()
            
        # _________________________________________________________________________________
        
        # Generate a code :
        elif 'code' in query:
            generate_and_open_python_file()
            
        # _________________________________________________________________________________
        
        # Personal query :
        # elif 'question' in query:
        #     Auto_GPT()
            
        # _________________________________________________________________________________
        # Flight tracking :
        elif 'track the flight' in query:
            TrackFlight()
            
            
        # _________________________________________________________________________________
        # Track number :
        elif 'number' in query:
            speak("Please provide phone number which you want to track...")
            phone_number = input("Enter the phone number :")
            print(get_phone_details(phone_number))
            speak(get_phone_details(phone_number))
        # _________________________________________________________________________________
        
        #  Use to close all program.
        elif 'close' in query:
            speak("Which window would you like to close?")
            window_name = TakeCommand().lower()
            os.system(f'taskkill /im {window_name}.exe')
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
# @qmr4BVeW3TVNJw - Numverify API password...