import requests
import csv
import time
from datetime import datetime

# Google Places API configuration
API_KEY = ''
BASE_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
DETAILS_URL = 'https://maps.googleapis.com/maps/api/place/details/json'
 
# Wayne County, Ohio geographic center and radius (in meters)
WAYNE_COUNTY_LOCATION = "40.8292,-81.8885"  # Approximate center of Wayne County
RADIUS = 20000  # About 12.4 miles radius to cover most of the county

# Categories to search for (using Google Places types)
CATEGORIES = [
    'restaurant',
    'atm',
    'gas_station',
    'farm',
    'store',
    'supermarket',
    'park',
    'hotel',
    'tourist_attraction',
    'shopping_mall',
    'museum',
    'movie_theater',
    'point_of_interest',
    'establishment'
]

def get_places_by_category(category):
    """Retrieve places for a specific category using paginated requests"""
    places = []
    next_page_token = None
    
    while True:
        params = {
            'query': f'{category} in Wayne County, Ohio',
            'key': API_KEY,
            'location': WAYNE_COUNTY_LOCATION,
            'radius': RADIUS
        }
        
        if next_page_token:
            params['pagetoken'] = next_page_token
            # Google requires a short delay between page token requests
            time.sleep(2)
        
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if data.get('results'):
            places.extend(data['results'])
        
        next_page_token = data.get('next_page_token')
        if not next_page_token:
            break
    
    return places

def get_place_details(place_id):
    """Get detailed information for a specific place"""
    params = {
        'place_id': place_id,
        'key': API_KEY,
        'fields': 'name,formatted_address,geometry,address_components,formatted_phone_number,website,url'
    }
    
    response = requests.get(DETAILS_URL, params=params)
    data = response.json()
    return data.get('result', {})

def parse_address_components(address_components):
    """Extract city, state, and ZIP from address components"""
    city = state = zip_code = ''
    
    for component in address_components:
        if 'locality' in component['types']:
            city = component['long_name']
        elif 'administrative_area_level_1' in component['types']:
            state = component['short_name']
        elif 'postal_code' in component['types']:
            zip_code = component['long_name']
    
    return city, state, zip_code

def main():
    all_places = []
    
    print("Starting data collection for Wayne County, OH...")
    
    # Collect places for all categories
    for category in CATEGORIES:
        print(f"Processing category: {category}")
        places = get_places_by_category(category)
        
        for place in places:
            place_id = place.get('place_id')
            if place_id:
                details = get_place_details(place_id)
                
                # Parse address components
                address_components = details.get('address_components', [])
                city, state, zip_code = parse_address_components(address_components)
                
                # Get coordinates
                location = details.get('geometry', {}).get('location', {})
                lat = location.get('lat')
                lng = location.get('lng')
                
                # Prepare place record
                place_record = {
                    'name': details.get('name'),
                    'category': category,
                    'full_address': details.get('formatted_address'),
                    'latitude': lat,
                    'longitude': lng,
                    'city': city,
                    'state': state,
                    'zip_code': zip_code,
                    'phone_number': details.get('formatted_phone_number'),
                    'website': details.get('website'),
                    'google_maps_url': details.get('url'),
                    'mailing_address': '',  # Google Places API doesn't provide this
                    'contact_person': '',  # Google Places API doesn't provide this
                    'email': ''  # Google Places API doesn't provide this
                }
                
                all_places.append(place_record)
                time.sleep(0.1)  # Add small delay to avoid rate limiting
    
    # Save to CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'wayne_county_poi_{timestamp}.csv'
    
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'name', 'category', 'full_address', 'latitude', 'longitude',
            'city', 'state', 'zip_code', 'phone_number', 'website',
            'google_maps_url', 'mailing_address', 'contact_person', 'email'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for place in all_places:
            writer.writerow(place)
    
    print(f"Data collection complete. Saved {len(all_places)} records to {filename}")

if __name__ == '__main__':
    main()
