import csv
import requests
import time
from datetime import datetime



# Configuration
INPUT_CSV = 'categorized_locations.csv'  # Input CSV file with location data
OUTPUT_CSV = 'location_status_checked.csv'
GOOGLE_API_KEY = ''  # Replace with your actual API key

def check_location_status(name, address):
    """Check if a business is permanently closed using Google Maps API"""
    base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    
    # Build the query - using both name and address for better accuracy
    query = f"{name} {address}".strip()
    
    params = {
        'input': query,
        'inputtype': 'textquery',
        'fields': 'business_status',
        'key': GOOGLE_API_KEY
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if data['status'] == 'OK' and 'candidates' in data:
            if data['candidates']:
                return data['candidates'][0].get('business_status', 'UNKNOWN')
        return 'UNKNOWN'
    except Exception as e:
        print(f"Error checking {name}: {str(e)}")
        return 'ERROR'

def process_csv():
    """Process the CSV file and check location status"""
    with open(INPUT_CSV, mode='r', encoding='utf-8') as infile, \
         open(OUTPUT_CSV, mode='w', encoding='utf-8', newline='') as outfile:
        
        reader = csv.DictReader(infile)
        
        # Add new columns while preserving existing ones
        fieldnames = reader.fieldnames + ['business_status', 'last_checked', 'notes']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            # Get location details from your specific CSV structure
            name = row.get('name', '').strip('"')  # Remove potential quotes
            address = row.get('full_address', '')
            
            if name and address:
                print(f"Checking: {name} at {address}")
                status = check_location_status(name, address)
                row['business_status'] = status
                row['last_checked'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Add notes based on status
                if status == 'CLOSED_PERMANENTLY':
                    row['notes'] = 'Verified as permanently closed via Google API'
                elif status == 'OPERATIONAL':
                    row['notes'] = 'Verified as operational via Google API'
                else:
                    row['notes'] = 'Status could not be determined'
                
                # API rate limiting (100 requests per second is Google's limit)
                time.sleep(0.1)  # Conservative delay to avoid hitting limits
            else:
                row['business_status'] = 'INSUFFICIENT_DATA'
                row['last_checked'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                row['notes'] = 'Missing name or address data'
                
            writer.writerow(row)

if __name__ == '__main__':
    print("Starting location status check...")
    print(f"Reading from: {INPUT_CSV}")
    print(f"Will output to: {OUTPUT_CSV}")
    process_csv()
    print(f"Processing complete. Results saved to {OUTPUT_CSV}")
