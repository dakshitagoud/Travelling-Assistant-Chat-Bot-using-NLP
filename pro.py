from flask import Flask, render_template, request
import geopy
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob


app = Flask(__name__)

def get_location_coordinates(location):
    geolocator = geopy.Nominatim(user_agent="travel-assistant")
    location_data = geolocator.geocode(location)
    if location_data:
        latitude = location_data.latitude
        longitude = location_data.longitude
        return latitude, longitude
    else:
        return None, None

def get_place_suggestions(location):
    latitude, longitude = get_location_coordinates(location)

    if latitude is None or longitude is None:
        return []

    # Use OpenStreetMap Overpass API to retrieve nearby points of interest
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    node(around:5000,{latitude},{longitude})[tourism];
    out center;
    """
    response = requests.get(overpass_url, params={"data": overpass_query})
    data = response.json()

    places = []
    # Process the place suggestions from OpenStreetMap
    if "elements" in data:
        places = data["elements"]


    return places

def get_additional_information(location):
    wikipedia_url = f"https://en.wikipedia.org/wiki/{location.replace(' ', '_')}"
    response = requests.get(wikipedia_url)
    soup = BeautifulSoup(response.content, "html.parser")
    paragraphs = soup.select("#mw-content-text p")
    additional_info = ""
    if paragraphs:
        for i in range(min(3, len(paragraphs))):
            additional_info += paragraphs[i].text.strip() + "\n\n"

    return additional_info

def get_bot_response(user_input):
    user_input = user_input.lower().strip()

    if user_input == "hello":
        return "Hello! How can I assist you today?"
    
    if user_input == "hi":
        return "Hello! How can I assist you today?"
    
    if user_input == "hii":
        return "Hello! How can I assist you today?"
    
    if user_input == "how are you":
        return "I'm a bot, so I don't have feelings, but thanks for asking!"
    if user_input == "how are you ?":
        return "I'm a bot, so I don't have feelings, but thanks for asking!"
    
    if user_input == "i need travelling suggestion":
        return "Sure enter your location that you wanted to find"
    
    if user_input == "location":
        return "Sure enter your location that you wanted to find"
    
    if user_input == "need location":
        return "Sure enter your location that you wanted to find"
    
    if user_input == "bye":
        return "It's been pleasure!"
    
    if user_input == "goodbye":
        return "It's been pleasure!"
    
    if user_input == "nothing":
        return "It's fine, pleasure helping you"
    
    sentiment = TextBlob(user_input).sentiment.polarity

    if user_input.startswith("i"):
        if sentiment >= 0:
            return "I'm glad to hear that you're feeling positive and liked this"
        else:
            return "I'm sorry to hear that you're feeling negative. How can I help?"
    else :
        location = user_input
        places = get_place_suggestions(location)

        additional_info = get_additional_information(location)

        if not places:
            return "Sorry, I couldn't find answer to your response"
        response = f"Here are some places of interest in {location}:\n\n"
        for place in places:
            place_name = place.get('tags', {}).get('name')
            if place_name:
                response += f"- {place_name}\n"
        if additional_info:
                response += f"\nAdditional Information:\n{additional_info}"


        return response


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['location']
        bot_response = get_bot_response(user_input)
        return render_template('index.html', user_input=user_input, bot_response=bot_response)
    return render_template('index.html', user_input='', bot_response='')


if __name__ == '__main__':
    app.run(debug=True)
