import json

import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier

from opencage.geocoder import OpenCageGeocode

import folium

def main():
    # Get number to track
    number = input("Enter number to track: ")

    # Contruct phone number object
    parsed_number = phonenumbers.parse(number)

    # Get location(country)
    location = geocoder.description_for_number(parsed_number, "en")

    # Get carrier name
    provider = carrier.name_for_number(parsed_number, "en")

    # Open cage API key
    api_key = "0a4f8548cfc44676a7d0b8ad8d8b6ceb"

    # Construct open cage geocode object
    open_cage = OpenCageGeocode(api_key)

    # Query geocoder for details of the location tracked
    results = open_cage.geocode(str(location))
    
    # Get country flag
    flag = results[0]["annotations"]["flag"]

    # Access longitude and latitude from JSON file
    lat = results[0]["geometry"]["lat"]
    long = results[0]["geometry"]["lng"]

    # Generate map
    my_map = folium.Map(location=[lat, long], zoom_start=9)

    # Mark location on map
    folium.Marker([lat, long], popup=location).add_to(my_map)

    # Save map
    my_map.save("myLocation.html")
    print("Location map saved as 'myLocation.html")

if __name__ == "__main__":
    main()