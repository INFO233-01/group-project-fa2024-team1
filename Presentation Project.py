# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 19:34:16 2024

@author: kevin
"""

import requests
from datetime import datetime
import pyautogui



# API Key and URL
API_KEY = '6ea5488623msh8c027bb0c9328bfp16451ejsnc5c92a2c5872'
BASE_URL = "https://travel-advisor.p.rapidapi.com/locations/search"
HOTEL_URL = "https://travel-advisor.p.rapidapi.com/hotels/list"
RESTAURANT_URL = "https://travel-advisor.p.rapidapi.com/restaurants/list"
ATTRACTION_URL = "https://travel-advisor.p.rapidapi.com/attractions/list"

# Headers
headers = {
    'x-rapidapi-host': 'travel-advisor.p.rapidapi.com',
    'x-rapidapi-key': API_KEY
}

#Function to fetch hotels based on city or country
def get_hotels_by_location(location_name, checkin_date, checkout_date):
    # Parameters for the API request
    params = {
        'query': location_name,  #User input for city or country
        'limit': 3,  #Limit to top 3 results
        'lang': 'en_US',  # Language
        'currency': 'USD'  #Currency for pricing
    }

    try:
        # send GET request to the API to search for the location
        response = requests.get(BASE_URL, headers=headers, params=params)

        # if the request was successful
        if response.status_code == 200: #error codes
            location_data = response.json()

            # Check if we found any locations
            if 'data' in location_data and len(location_data['data']) > 0:
                # Get the first location's details, including name and ID
                location = location_data['data'][0]['result_object']
                location_id = location['location_id']

                # Now fetch hotels, restaurants, and attractions using this location's ID
                hotels = fetch_hotels(location_id, checkin_date, checkout_date)
                restaurants = fetch_restaurants(location_id)
                attractions = fetch_attractions(location_id)

                return hotels, restaurants, attractions
            else:
                return "No locations found matching your input.", None, None
        else:
            return f"Error fetching location data: {response.status_code}", None, None
    except Exception as e:
        return f"Error: {e}", None, None

# Function to fetch hotels based on the location_id
def fetch_hotels(location_id, checkin_date, checkout_date): # finds hotels based on location id
    hotel_params = {'location_id': location_id,  'lang': 'en_US','limit': 5,  'currency': 'USD','checkin': checkin_date,  'checkout': checkout_date, 'nights': 3 } # sets parameters based on time staying

    try:
        response = requests.get(HOTEL_URL, headers=headers, params=hotel_params) # accesses API to search for location

        if response.status_code == 200: # checks for request success
            hotel_data = response.json()

            if 'data' in hotel_data and len(hotel_data['data']) > 0: # if there are hotels in the data list they are output
                return hotel_data['data']
            else:
                return "No hotels found for the specified location." # if no hotels displays as so
        else:
            return f"Error fetching hotel data: {response.status_code}" # prints error for wrong status code
    except Exception as e:
        return f"Error: {e}"

# Function to fetch restaurants based on the location_id
def fetch_restaurants(location_id):  # Defines a function to retrieve restaurant data for a specific location
    try:
        response = requests.get(RESTAURANT_URL, headers=headers, params={ # Sends a GET request to the API with required headers and parameters (asked chatgpt about parameters)
            'location_id': location_id,  #dictionary that specifies the location to search restaurants for
            'lang': 'en_US',            # dictionary that sets the language for the API response
            'limit': 3,                 # dictionary that limits the results to 3 restaurants
            'currency': 'USD'           # dictionary that specifies USD for any price information
        })
        return response.json().get('data', "No restaurants found.") # Processes the API response and returns the data
    except:  # Handles any errors that occur during the API request
        return "An error occurred while getting restaurants."  # Returns a simple error message
def fetch_attractions(location_id):  # Defines a function to retrieve attraction data for a specific location
    try:
       
        response = requests.get(ATTRACTION_URL, headers=headers, params={  # Sends a GET request to the API with required headers and parameters
            'location_id': location_id,  # Specifies the location to search attractions for
            'lang': 'en_US',            # Sets the language for the API response
            'limit': 3,                 # Limits the results to 5 attractions
            'currency': 'USD'           # Specifies USD for any price information
        })
        return response.json().get('data', "No attractions found.") # Processes the API response and returns the data
    except:  # Handles any errors that occur during the API request
        return "An error occurred while fetching attractions."  # Returns a simple error message

# Main function to run the program
def main():
    print("Welcome to the Travel Planner!")
    print("Here you will find hotels, restaurants, and attractions in any city you are looking for!")
    print("Let's get started!\n")
    while True:
        location_name = input("Enter a city to find hotels, restaurants, and attractions: ")
        hotels,restaurants, attractions=get_hotels_by_location(location_name, None, None)
        if hotels =="Invalid city. Please enter a valid city.":
            print(hotels)
            continue
        else:
            break


    #ask for check-in and check-out dates, ensuring they are in the correct format
    while True:
        try:
            checkin_date = input("Enter your check-in date (YYYY-MM-DD): ")
            datetime.strptime(checkin_date, '%Y-%m-%d') # Ensures correct date format
            break
        except ValueError:
            print("Invalid date format. Please enter the date in the format YYYY-MM-DD.")

    while True:
        try:
            checkout_date = input("Enter your check-out date (YYYY-MM-DD): ")
            datetime.strptime(checkout_date, '%Y-%m-%d')
            break
        except ValueError:
            print("Date format is invalid. Please enter the date in the format YYYY-MM-DD.")

    #fetch the data for hotels, restaurants, attractions
    hotels, restaurants, attractions = get_hotels_by_location(location_name, checkin_date, checkout_date)

    #display the hotel information 
    if type(hotels) == list:  # Check if the hotels data is a list and display as list
        print(f"\nFound {len(hotels)} hotels:")
        for hotel in hotels[:3]:  # Display top 3 hotels
            hotel_name = hotel.get('name', 'No name available')
            hotel_rating = hotel.get('rating', 'No rating available')
            hotel_price = hotel.get('price', 'Price not available')
            print(f"- {hotel_name} - Rating: {hotel_rating} - Price: {hotel_price} USD")
    else:
        print(hotels)  #if the returned result is an error message print error message

    # display the restaurant information 
    if type(restaurants) == list:  #check if the restaurants data is a list and display as a list 
        print(f"\nFound {len(restaurants)} restaurants:")
        for restaurant in restaurants[:3]:  # Display top restaurants
            restaurant_name = restaurant.get('name', 'No name available')
            restaurant_rating = restaurant.get('rating', 'No rating available')
            restaurant_price = restaurant.get('price', 'Price not available')
            print(f"- {restaurant_name} - Rating: {restaurant_rating} - Price: {restaurant_price} USD")
    else:
        print(restaurants)  #if the returned result is an error message print error message 

    #display the attraction information
    if type(attractions) == list:  #check if the attractions data is a list and display as a list 
        print(f"\nFound {len(attractions)} attractions:")
        for attraction in attractions[:3]:  # Display top attractions
            attraction_name = attraction.get('name', 'No name available')
            attraction_rating = attraction.get('rating', 'No rating available')
            attraction_description = attraction.get('description', 'No description available')
            print(f"- {attraction_name} - Rating: {attraction_rating} - Description: {attraction_description}")
    else:
        print(attractions)  #if the returned result is an error message print error message
        
        
        # Take a screenshot at the end
        screenshot = pyautogui.screenshot()
        screenshot.save("travel_planner_screenshot.png")
        print("\nScreenshot saved as 'travel_planner_screenshot.png'!")
        
        


# use main to run the program 
if __name__ == "__main__":
    main()



