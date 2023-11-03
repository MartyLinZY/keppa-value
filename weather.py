import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from pandas import read_excel
# Step 1: Load the data from the CSV file
# df = pd.read_csv('/Users/linzheyuan/PycharmProjects/keppa-value/filtered_location_id_01_with_cities_1.csv')

df = pd.read_csv('/Users/linzheyuan/PycharmProjects/keppa-value/filtered_location_id_01_with_cities.csv')


def fetch_weather_data(row):
    try:
        response = requests.get(
            "https://devapi.qweather.com/v7/warning/now",
            params={"key": "08cba729c5d1438cbd4f2561720783b0", "location": row['Location_ID']},
            timeout=10
        )
        print("request " + row['Location_Name_ZH'])

        data = response.json()
        #print(data)
        if 'warning' in data:
            for warning in data['warning']:
                if '台风' in warning.get('title', ''):
                    return row['Location_Name_ZH']
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

def extract_matching_entries(typhoon_warnings_path, gmair_path, output_path):
    # Step 1: Reading the data from the files
    typhoon_warnings = read_excel(typhoon_warnings_path)
    gmair = read_excel(gmair_path)

    # Step 2: Extracting the list of cities from the typhoon_warnings file
    city_list = typhoon_warnings['Location_Name_ZH'].tolist()
    print("start searching")
    # Step 3: Finding the entries in gmair where the address contains any of the cities from the city_list
    # Replacing NaN values with empty strings in the '地址' column
    gmair['地址'] = gmair['地址'].fillna('')
    matching_entries = gmair[gmair['地址'].str.contains('|'.join(city_list))]

    # Step 4: Saving the matching entries to the output file
    matching_entries.to_excel(output_path, index=False)

# Step 3: Use ThreadPoolExecutor to perform concurrent API calls
with ThreadPoolExecutor(max_workers=50) as executor:
    result = list(executor.map(fetch_weather_data, df.to_dict('records')))

# Step 4: Filter non-None results and save to Excel
result = [r for r in result if r is not None]
print(result)
pd.DataFrame({'Location_Name_ZH': result}).to_excel('typhoon_warnings.xlsx', index=False)

print("Script executed successfully. Data saved to typhoon_warnings.xlsx")

extract_matching_entries('typhoon_warnings.xlsx','gmair.xlsx','result.xlsx')

# Usage:
# extract_matching_entries('path/to/typhoon_warnings.xlsx', 'path/to/gmair.xls', 'path/to/output.xlsx')


# # Please replace with the actual path to your CSV file
# print("Reading csv")
# # Initialize an empty list to store the city names
# cities_with_typhoon_warning = []
# flag=0
# # Step 2: Loop through each Location_ID and make API requests
# for _, row in df.iterrows():
#     location_id = row['Location_ID']
#     location_name = row['Location_Name_ZH']
#     print("request "+location_name)
#     # Making API request
#     response = requests.get('https://devapi.qweather.com/v7/warning/now', params={'key': '08cba729c5d1438cbd4f2561720783b0',
#                                                                                   'location': location_id})
#     # Please replace 'YOUR_API_KEY' with your actual API key
#     flag+=1;
#     # Check if the response is valid
#     if response.status_code == 200:
#         data = response.json()
#
#         # Step 3: Check if the warning title contains the keyword "台风"
#         if 'warning' in data and 'title' in data['warning'] and "台风" in data['warning']['title']:
#             cities_with_typhoon_warning.append(location_name)
#     else:
#         print(f"Failed to fetch data for Location_ID: {location_id}")
#     if flag>10:
#         break
# # Step 4: Save the city names to an Excel file
# output_excel_file = './cities_with_typhoon_warning.xlsx'
# pd.DataFrame(cities_with_typhoon_warning, columns=['City_Name']).to_excel(output_excel_file, index=False)
