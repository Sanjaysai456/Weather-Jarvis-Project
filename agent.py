import requests
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Function to get weather data from Yahoo Weather API
def get_weather_data(city):
    url = "https://yahoo-weather5.p.rapidapi.com/weather"
    querystring = {"location": city, "format": "json", "u": "f"}
    headers = {
        "x-rapidapi-key": "6629c83885mshb9efdddf4879e22p14823fjsn4f13b6889da8",
        "x-rapidapi-host": "yahoo-weather5.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# Function to get family information


# Function to get room temperature
def temp_room(room):
    return "Temp = 20, Humidity = 70"

# Function to get city temperature
def temp_city(city):
    weather_data = get_weather_data(city)
    if "current_observation" in weather_data:
        obs = weather_data["current_observation"]
        hum = obs["atmosphere"]["humidity"]
        temp_f = obs["condition"]["temperature"]
        temp_c = round((temp_f - 32) * 5.0/9.0, 2)
        return f"Humidity: {hum}%, Temp in C: {temp_c}°"
    else:
        return "Weather data not available."

# Available functions dictionary
available_functions = {
    "temp_city": temp_city,
    "temp_room": temp_room,
    
}

# Function definitions for the Gemini API
definitions = [
    {
        "name": "temp_city",
        "description": "Find the weather, temperature of a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City to find the weather"
                }
            },
            "required": ["city"]
        }
    }
   
]

# Gemini API key
key = "AIzaSyCXin2833P6siZ9f0w_Yg8xnFNpzhmWe-A"

# Function to parse function response from Gemini API
def parse_function_response(message):
    function_call = message[0].get("functionCall")
    function_name = function_call["name"]
    print("Gemini: call function", function_name)
    
    try:
        arguments = function_call.get("args")
        print("Gemini: arguments are", arguments)
        
        if arguments:
            function = available_functions.get(function_name)
            print("function is", function)
            if function:
                function_response = function(**arguments)
            else:
                function_response = "Function not found"
        else:
            function_response = "No arguments are present"
    
    except Exception as e:
        print(e)
        function_response = "Invalid function"
    
    return function_response

# Function to run conversation with Gemini API
def run_conversation(user_message):
    messages = []  # list which holds all messages
    print(user_message)
    
    system_message = """You are an AI bot that can do everything using function call.
    When you are asked to do something, use the function call you have available and then respond with message"""
    
    # first instruction
    message = {
        "role": "user",
        "parts": [{"text": system_message + "\n" + user_message}]
    }
    
    messages.append(message)
    
    data = {
        "contents": [messages],
        "tools": [{"function_declarations": definitions}]
    }
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={key}"
    
    try:
        response = requests.post(url, json=data, verify=False)
    except requests.exceptions.SSLError as e:
        print(f"SSL Error: {e}")
        return
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return
    
    if response.status_code != 200:
        print(response.text)
        return
    
    t1 = response.json()
    
    if "content" not in t1.get("candidates")[0]:
        print("Error: No content in response")
        return
    
    message = t1.get("candidates")[0].get("content").get("parts")
    
    if "functionCall" in message[0]:
        resp1 = parse_function_response(message)
        return resp1

if __name__ == "_main_":
    user_message = "find the temperature of Hyderabad"
    print(run_conversation(user_message))