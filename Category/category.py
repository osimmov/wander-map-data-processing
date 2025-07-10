import pandas as pd
import re
from collections import defaultdict

# Define the target categories (same as before)
TARGET_CATEGORIES = [
    'Self care', 'Museums', 'Campgrounds', 'Lodging', 'Attractions', 
    'Food/Drinks', 'Government', 'Furniture', 'Farm', 'Brews', 
    'Nonprofit', 'Fitness/Health', 'Nature', 'Transportation', 'Antiques'
]

# Enhanced keyword mapping with weights (more specific terms have higher weights)
CATEGORY_KEYWORDS = {
    'Self care': {'beauty': 2, 'spa': 3, 'salon': 2, 'wax': 1, 'massage': 2, 'skin care': 2, 'barber': 2, 'nails': 2},
    'Museums': {'museum': 3, 'historical society': 2, 'art museum': 3, 'gallery': 2, 'exhibit': 1},
    'Campgrounds': {'campground': 3, 'rv park': 2, 'rv resort': 2, 'campsite': 2},
    'Lodging': {'hotel': 3, 'motel': 3, 'inn': 3, 'bed and breakfast': 3, 'b&b': 3, 'guest house': 2, 'suites': 1},
    'Attractions': {'attraction': 2, 'amusement': 2, 'entertainment': 1, 'arena': 2, 'ice arena': 3, 'racquet club': 3, 'zoo': 3, 'aquarium': 3},
    'Food/Drinks': {'restaurant': 3, 'cafe': 3, 'diner': 3, 'bistro': 3, 'grill': 3, 'pizza': 3, 'bar': 3, 'pub': 3, 'tavern': 3, 
                   'eatery': 2, 'food': 1, 'dining': 1, 'bakery': 3, 'coffee': 3, 'ice cream': 3, 'cupcake': 3, 'burger': 3, 
                   'steak': 3, 'bbq': 3, 'chicken': 2, 'pasta': 2, 'sushi': 3, 'mexican': 2, 'chinese': 2, 'italian': 2, 'deli': 2, 'buffet': 2},
    'Government': {'city hall': 3, 'government': 2, 'public works': 3, 'administration': 2, 'township': 2},
    'Furniture': {'furniture': 3, 'cabinets': 2, 'woodworking': 2, 'home decor': 1},
    'Farm': {'farm': 3, 'orchard': 3, 'dairy': 2, 'produce': 1, 'ranch': 2, 'agriculture': 2, 'crops': 2},
    'Brews': {'brewery': 3, 'winery': 3, 'distillery': 3, 'vineyard': 3, 'beer': 2, 'wine': 2, 'cider': 2},
    'Nonprofit': {'nonprofit': 3, 'non-profit': 3, 'charity': 3, 'foundation': 2, 'historical society': 1},
    'Fitness/Health': {'fitness': 3, 'gym': 3, 'yoga': 3, 'crossfit': 3, 'wellness': 2, 'health': 2, 
                      'hospital': 3, 'clinic': 3, 'medical': 2, 'doctor': 2, 'dental': 2, 'pharmacy': 2},
    'Nature': {'park': 2, 'trail': 2, 'preserve': 3, 'garden': 2, 'nature': 1, 'conservancy': 3, 'wildlife': 2, 'forest': 2},
    'Transportation': {'transportation': 2, 'railroad': 2, 'trucking': 2, 'logistics': 1, 'auto': 1, 'car wash': 2},
    'Antiques': {'antique': 3, 'vintage': 2, 'collectible': 2, 'retro': 1}
}

def categorize_location(name, description):
    """
    Improved categorization using weighted keyword scoring and priority matching
    """
    if not isinstance(description, str):
        description = ''
    
    combined_text = (name + ' ' + description).lower()
    scores = defaultdict(int)
    
    # Score each category based on keyword matches
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword, weight in keywords.items():
            if re.search(r'\b' + re.escape(keyword) + r'\b', combined_text):
                scores[category] += weight
    
    # If we have matches, return the highest scoring category
    if scores:
        return max(scores.items(), key=lambda x: x[1])[0]
    
    # Special cases based on name patterns (unchanged from original)
    name_lower = name.lower()
    if 'hotel' in name_lower or 'inn' in name_lower:
        return 'Lodging'
    if 'park' in name_lower and 'national' not in name_lower and 'state' not in name_lower:
        return 'Nature'
    if 'farm' in name_lower or 'orchard' in name_lower:
        return 'Farm'
    if 'museum' in name_lower:
        return 'Museums'
    if 'gallery' in name_lower:
        return 'Museums'
    if 'clinic' in name_lower or 'hospital' in name_lower:
        return 'Fitness/Health'
    if 'gym' in name_lower or 'fitness' in name_lower:
        return 'Fitness/Health'
    if 'winery' in name_lower or 'brewery' in name_lower:
        return 'Brews'
    
    return 'Attractions'  # Default category

# Rest of the code remains the same...

def main():
    # Read the CSV file
    df = pd.read_csv('cleaned_unique_locations_v1(in).csv')
    
    # Add a new column for the categorized data
    df['category'] = df.apply(lambda row: categorize_location(row['name'], row['summary']), axis=1)
    
    # Save to a new CSV file
    df.to_csv('categorized_locations.csv', index=False)
    print("Categorization complete. Saved to 'categorized_locations.csv'")

if __name__ == '__main__':
    main()