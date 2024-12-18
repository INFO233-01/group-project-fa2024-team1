# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 18:10:37 2024

@author: kevin
"""

import requests
import pyautogui
import time

# API Key and URL
API_KEY = '6ea5488623msh8c027bb0c9328bfp16451ejsnc5c92a2c5872'
BASE_URL = "https://travel-advisor.p.rapidapi.com/locations/search"
RESTAURANT_URL = "https://travel-advisor.p.rapidapi.com/restaurants/list"
ATTRACTION_URL = "https://travel-advisor.p.rapidapi.com/attractions/list"

# Headers
headers = {
    'x-rapidapi-host': 'travel-advisor.p.rapidapi.com',
    'x-rapidapi-key': API_KEY
}

# Function to fetch restaurants and attractions based on city or country
def get_location_data(location_name):
    # Parameters for the API request
    params = {
        'query': location_name,  # User input for city or country
        'limit': 3,  # Limit to top 3 results
        'lang': 'en_US',  # Language
        'currency': 'USD'  # Currency for pricing
    }

    try:
        # Send GET request to the API to search for the location
        response = requests.get(BASE_URL, headers=headers, params=params)

        # If the request was successful
        if response.status_code == 200:  # Error codes
            location_data = response.json()

            # Check if we found any locations
            if 'data' in location_data and len(location_data['data']) > 0:
                # Get the first location's details, including name and ID
                location = location_data['data'][0]['result_object']
                location_id = location['location_id']

                # Now fetch restaurants and attractions using this location's ID
                restaurants = fetch_restaurants(location_id)
                attractions = fetch_attractions(location_id)

                return restaurants, attractions
            else:
                return "No locations found matching your input. Please try again.", None
        else:
            return f"Error fetching location data: {response.status_code}", None
    except Exception as e:
        return f"Error: {e}", None

#Function to fetch restaurants based on the location_id
def fetch_restaurants(location_id): #defines a function to retrieve restaurant data for a specific location
    try:
        response = requests.get(RESTAURANT_URL, headers=headers, params={ #Sends a GET request to the API with required headers and parameters (asked chatgpt about parameters)
            'location_id': location_id, #dictionary that specifies the location to search restaurants for
            'lang': 'en_US',  #dictionary that sets the language for the API response
            'limit': 3, #dictionary that limits the results to 3 restaurants
            'currency': 'USD' #dictionary that specifies USD for any price information
        })
        return response.json().get('data', "No restaurants found.") #processes the API response and returns the data
    except:  #handles any errors that occur during the API request
        return "An error occurred while getting restaurants." #returns a simple error message

#function to fetch attractions based on the location_id
def fetch_attractions(location_id): #defines a function to retrieve attraction data for a specific location
    try:
        response = requests.get(ATTRACTION_URL, headers=headers, params={ #sends a GET request to the API with required headers and parameters
            'location_id': location_id, #specifies the location to search attractions for
            'lang': 'en_US', #sets the language for the API response
            'limit': 3, #limits the results to 5 attractions
            'currency': 'USD' #specifies USD for any price information
        })
        return response.json().get('data', "No attractions found.") #processes the API response and returns the data
    except:  #handles any errors that occur during the API request 
        return "An error occurred while fetching attractions."  #returns a simple error message


# ... [rest of the code]

def main():
    print("Welcome to the Travel Planner!") # Welcome message to user
    print("Here you will find restaurants and attractions in any city you are looking for!") # Informs user what program is looking for
    print("Let's get started!\n")

    while True:
        location_name = input("Enter a city to find restaurants and attractions: ")  # Asks user to input a city for searching restaurants and attractions
        restaurants, attractions = get_location_data(location_name)  # Calls the function to fetch restaurants and attractions
        if restaurants == "No locations found matching your input. Please try again.":
            print(restaurants)
            continue
        else:
            break

    #Display the restaurant information
    if type(restaurants) == list:  # Checks if the restaurants data is a list and display it
        print(f"\nFound {len(restaurants)} restaurants:")
        for restaurant in restaurants[:3]:  # Display top 3 restaurants
            restaurant_name = restaurant.get('name', 'No name available')
            restaurant_rating = restaurant.get('rating', 'No rating available')
            restaurant_price = restaurant.get('price', 'Price not available')
            print(f"- {restaurant_name} - Rating: {restaurant_rating} - Price: {restaurant_price} USD")
    else:
        print(restaurants)  # If the returned result is an error message, print it

    # Display the attraction information
    if type(attractions) == list:  # Checks if the attractions data is a list and display it
        print(f"\nFound {len(attractions)} attractions:")
        for attraction in attractions[:3]:  # Display top 3 attractions
            attraction_name = attraction.get('name', 'No name available')
            attraction_rating = attraction.get('rating', 'No rating available')
            attraction_description = attraction.get('description', 'No description available')
            print(f"- {attraction_name} - Rating: {attraction_rating} - Description: {attraction_description}")  # Prints attraction name and details
    else:
        print(attractions)  # If the returned result is an error message, print it

    #Wait for the results to appear on screen
    time.sleep(2)  #adds a 2-second delay to ensure the program output is visible

    #Take a screenshot after the results are printed
    screenshot = pyautogui.screenshot()
    screenshot.save("travel_planner_screenshot.png")
    print("\nScreenshot saved as 'travel_planner_screenshot.png'!")

#Uses main to run the program
if __name__ == "__main__":
    main()
