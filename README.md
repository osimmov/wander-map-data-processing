# Wander Map: Wayne County Location Dataset

This repository contains the data processing scripts used to gather, clean, and organize location-based information for Wayne County, Ohio. The data is used in conjunction with an interactive mapping platform to help visualize local points of interest such as restaurants, parks, museums, and more.

## 📍 Project Overview

Using the Google Places API, we collected over **1,000+ locations** in Wayne County across various categories including:
- Restaurants
- Museums
- Parks
- Campgrounds
- Historical sites
- Local businesses

After collecting raw data, we processed it using Python, `pandas`, and Excel to:
- Clean and sort the data
- Categorize locations into meaningful groups
- Gather Pictures for all the locations
- Prepare structured data for integration into the Wander Map platform

## 🧰 Technologies Used
- Python 3
- Google Places API
- pandas
- requests
- Microsoft Excel (manual sorting & review)

### Key Scripts

- `wayne_county_places.py`: Gathers locations from the Google Places API.
- `category.py`: Categorizes the locations into specific types (restaurants, parks, museums, etc.).
- `status.py`: Checks the status of each location (e.g., open/closed).
- `code_1.py`: To get pictures for the given Excel File


