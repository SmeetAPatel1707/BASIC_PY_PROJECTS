# JARVIS – Voice-Based Intelligent Assistant

## 📌 Project Overview
JARVIS (Just A Rather Virtual Intelligent System) is a Python-based intelligent voice assistant designed to perform a wide range of automated tasks through **voice commands and GUI interaction**. The system integrates speech recognition, text-to-speech, web automation, third-party APIs, and a graphical interface to simulate a real-world virtual assistant.

This project demonstrates practical implementation of **AI automation, NLP, API integration, and system-level operations** in a single application.

---

## 🎯 Project Objectives
- Build a functional voice-controlled intelligent assistant  
- Integrate speech recognition and text-to-speech systems  
- Automate daily tasks such as web search, email, weather, news, and music  
- Use external APIs for real-time data retrieval  
- Provide both **voice-based** and **GUI-based** interaction  

---

## 🧠 Problem Statement
Manual execution of repetitive digital tasks can be time-consuming. This project aims to reduce manual effort by enabling users to interact with their system using natural voice commands and a simple graphical interface, simulating a real-world AI assistant.

---

## 🛠️ Technologies & Libraries Used
- **Programming Language:** Python  
- **Speech Recognition:** SpeechRecognition (Google Speech API)  
- **Text-to-Speech:** pyttsx3  
- **Natural Language Processing:** Wikipedia API  
- **Web Automation:** webbrowser, OS  
- **Email Automation:** smtplib  
- **Music Control:** pygame  
- **Web Scraping:** BeautifulSoup  
- **API Integration:** Requests  
- **GUI Framework:** Gradio  
- **Computer Vision (Optional):** pyzbar  
- **Development Environment:** Python Script  

---

## ⚙️ Core Features

### 🎙️ Voice Interaction
- Voice command recognition using microphone  
- Text-to-speech responses for all outputs  
- Authentication-based startup using password verification  

### 🌐 Web & Information Services
- Wikipedia-based information search  
- Google search via voice commands  
- Real-time weather updates using OpenWeatherMap API  
- Latest news headlines using NewsAPI  
- Motivational quotes via ZenQuotes API  
- Joke generation using JokeAPI  

### ✉️ Email Automation
- Send emails using voice or GUI input  
- Gmail SMTP server integration  

### 🎵 Media Control
- Play music from local system  
- Pause and resume music playback  
- Song selection using voice commands  

### ✈️ Utility Services
- Flight tracking using AviationStack API  
- Phone number validation and carrier lookup using NumVerify API  
- System automation (open VS Code, GitHub, close applications)  

### 🖥️ Graphical User Interface
- GUI built using **Gradio**
- Dedicated sections for:
  - Email sending  
  - Music playback  
  - Weather updates  
  - News headlines  
  - Motivational quotes  
  - Jokes  
  - Flight tracking  
  - Phone number tracking  

---

## 🔄 System Workflow
1. Initialize text-to-speech engine  
2. Authenticate user via password  
3. Continuously listen for voice commands  
4. Process user intent  
5. Trigger corresponding function  
6. Fetch real-time data via APIs if required  
7. Respond using speech output and/or GUI  

---

## 📂 Project Structure
