import os
import pandas as pd
from openpyxl import Workbook

# Configuration
CSV_FILE = 'short.csv'  # Your input CSV file
PICS_FOLDER = 'pics'    # Folder containing the pictures
OUTPUT_EXCEL = 'location_pictures.xlsx'  # Output Excel file

# Supported image extensions (add more if needed)
SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.avif', '.bmp', '.gif', '.tiff')

def find_matching_pictures(location_name):
    """Find all pictures matching the location name pattern"""
    matching_files = []
    base_name = location_name.replace('_', '_')  # Replace spaces with underscores
    
    # Check for pictures with pattern "LocationName_X_Y.ext"
    pattern1 = f"{base_name}_"
    
    # Also check for patterns with different number placements
    for filename in os.listdir(PICS_FOLDER):
        if filename.startswith(pattern1):
            # Check if the file has a supported image extension (case-insensitive)
            if any(filename.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                matching_files.append(filename)
    
    return sorted(matching_files)

def main():
    # Read the CSV file
    df = pd.read_csv(CSV_FILE)
    
    # Prepare the output data with three columns
    output_data = []
    
    # Process each location
    for location in df['name']:
        if pd.isna(location):  # Skip empty entries
            continue
            
        # Find matching pictures
        pictures = find_matching_pictures(location)
        
        # Prepare the row with three columns
        row = {
            'Location': location,
            'First Picture': pictures[0] if len(pictures) > 0 else 'No picture found',
            'Second Picture': pictures[1] if len(pictures) > 1 else ''
        }
        
        output_data.append(row)
    
    # Create DataFrame from collected data
    output_df = pd.DataFrame(output_data, columns=['Location', 'First Picture', 'Second Picture'])
    
    # Save to Excel
    output_df.to_excel(OUTPUT_EXCEL, index=False)
    print(f"Successfully created {OUTPUT_EXCEL} with {len(output_df)} entries.")

if __name__ == '__main__':
    # Verify the pictures folder exists
    if not os.path.exists(PICS_FOLDER):
        print(f"Error: Pictures folder '{PICS_FOLDER}' not found.")
    else:
        main()