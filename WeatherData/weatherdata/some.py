# import pandas as pd
# import requests
# from time import sleep
# import logging

# # Setup logging to track any failed requests
# logging.basicConfig(filename='weather_data_errors_2024.log', level=logging.INFO)

# # Your WeatherAPI key
# API_KEY = "1fe5a94ce82148a1986142957242510"

# # List of 64 districts with their coordinates
# districts = {
#     'Bagerhat': (22.6512, 89.7851), 'Bandarban': (22.1953, 92.2184), 
#     'Barguna': (22.1530, 90.1266), 'Barisal': (22.7010, 90.3535), 
#     'Bhola': (22.6859, 90.6482), 'Bogra': (24.8466, 89.3773),
#     'Brahmanbaria': (23.9571, 91.1115), 'Chandpur': (23.2513, 90.8512),
#     'Chittagong': (22.3569, 91.7832), 'Chuadanga': (23.6402, 88.8410),
#     'Comilla': (23.4607, 91.1809), 'Cox\'s Bazar': (21.4272, 92.0058),
#     'Dhaka': (23.8103, 90.4125), 'Dinajpur': (25.6270, 88.6377),
#     'Faridpur': (23.6070, 89.8420), 'Feni': (23.0101, 91.3976),
#     'Gaibandha': (25.3288, 89.5286), 'Gazipur': (23.9999, 90.4203),
#     'Gopalganj': (23.0050, 89.8266), 'Habiganj': (24.3745, 91.4155),
#     'Jamalpur': (24.9375, 89.9372), 'Jessore': (23.1667, 89.2167),
#     'Jhalokathi': (22.6400, 90.1987), 'Jhenaidah': (23.5440, 89.1539),
#     'Joypurhat': (25.1023, 89.0200), 'Khagrachhari': (23.1193, 91.9847),
#     'Khulna': (22.8456, 89.5403), 'Kishoreganj': (24.4449, 90.7766),
#     'Kurigram': (25.8074, 89.6362), 'Kushtia': (23.9013, 89.1206),
#     'Lakshmipur': (22.9440, 90.8304), 'Lalmonirhat': (25.9923, 89.2847),
#     'Madaripur': (23.1641, 90.1978), 'Magura': (23.5004, 89.4197),
#     'Manikganj': (23.8644, 90.0047), 'Meherpur': (23.7627, 88.6318),
#     'Moulvibazar': (24.4829, 91.7774), 'Munshiganj': (23.5422, 90.5305),
#     'Mymensingh': (24.7471, 90.4203), 'Naogaon': (24.7936, 88.9318),
#     'Narail': (23.1725, 89.4951), 'Narayanganj': (23.6238, 90.4993),
#     'Narsingdi': (23.9322, 90.7151), 'Natore': (24.4206, 89.0000),
#     'Netrokona': (24.8864, 90.7271), 'Nilphamari': (25.9310, 88.8560),
#     'Noakhali': (22.8696, 91.0995), 'Pabna': (24.0064, 89.2372),
#     'Panchagarh': (26.3411, 88.5542), 'Patuakhali': (22.3596, 90.3290),
#     'Pirojpur': (22.5790, 89.9750), 'Rajbari': (23.7570, 89.6440),
#     'Rajshahi': (24.3745, 88.6042), 'Rangamati': (22.6372, 92.2061),
#     'Rangpur': (25.7439, 89.2752), 'Satkhira': (22.7185, 89.0705),
#     'Shariatpur': (23.2423, 90.4348), 'Sherpur': (25.0180, 90.0171),
#     'Sirajganj': (24.4534, 89.7000), 'Sunamganj': (25.0657, 91.3950),
#     'Sylhet': (24.9045, 91.8611), 'Tangail': (24.3917, 89.9628),
#     'Thakurgaon': (26.0339, 88.4512), 'Chapainawabganj': (24.5965, 88.2777),
# }

# def fetch_weather_data(lat, lon, date):
#     """Fetch weather data from WeatherAPI."""
#     url = f"http://api.weatherapi.com/v1/history.json"
#     params = {"key": API_KEY, "q": f"{lat},{lon}", "dt": date}
#     try:
#         response = requests.get(url, params=params)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             logging.info(f"Failed request for {lat}, {lon} on {date}: {response.status_code}")
#     except Exception as e:
#         logging.info(f"Error fetching {lat}, {lon} on {date}: {e}")
#     return None

# def estimate_sunshine_hours(cloud_cover, daylight_hours):
#     """Estimate sunshine hours based on cloud cover."""
#     return daylight_hours * (1 - cloud_cover / 100)

# def process_daily_data(day_data):
#     """Process individual day's data."""
#     avg_temp = day_data['day']['avgtemp_c']
#     total_rain = day_data['day']['totalprecip_mm']
#     avg_humidity = day_data['day']['avghumidity']
#     cloud_cover = avg_humidity  # Assuming cloudiness approximates humidity
#     daylight_duration = 12  # Placeholder (in hours)

#     sunshine_hours = estimate_sunshine_hours(cloud_cover, daylight_duration)
#     return avg_temp, total_rain, sunshine_hours, avg_humidity

# def process_monthly_data(data):
#     """Aggregate daily data into monthly averages and sums."""
#     temp_sum, rain_sum, sunshine_sum, humidity_sum, count = 0, 0, 0, 0, 0
#     for day in data.get('forecast', {}).get('forecastday', []):
#         avg_temp, total_rain, sunshine_hours, avg_humidity = process_daily_data(day)
#         temp_sum += avg_temp
#         rain_sum += total_rain
#         sunshine_sum += sunshine_hours
#         humidity_sum += avg_humidity
#         count += 1
#     if count > 0:
#         return temp_sum / count, rain_sum, sunshine_sum, humidity_sum / count
#     return None, None, None, None

# def main():
#     output_data = []

#     for district, (lat, lon) in districts.items():
#         year = 2024
#         temperatures, rainfalls, sunshines, humidities = [], [], [], []

#         for month in range(1, 13):
#             date = f"{year}-{month:02d}-01"
#             print(f"Fetching data for {district} ({year}-{month:02d})...")
#             data = fetch_weather_data(lat, lon, date)
#             if data:
#                 temp, rain, sunshine, humidity = process_monthly_data(data)
#                 temperatures.append(temp)
#                 rainfalls.append(rain)
#                 sunshines.append(sunshine)
#                 humidities.append(humidity)
#             else:
#                 temperatures.append(None)
#                 rainfalls.append(None)
#                 sunshines.append(None)
#                 humidities.append(None)
#             sleep(1)  # Avoid hitting rate limits

#         # Append the row for the current district
#         row = [district, year] + temperatures + rainfalls + sunshines + humidities
#         output_data.append(row)

#     # Define columns for the DataFrame
#     columns = (
#         ['District', 'Year'] +
#         [f'Temperature_{i}' for i in range(1, 13)] +
#         [f'Rainfall_{i}' for i in range(1, 13)] +
#         [f'Sunshine_{i}' for i in range(1, 13)] +
#         [f'Humidity_{i}' for i in range(1, 13)]
#     )

#     # Create a DataFrame and save it to Excel
#     df = pd.DataFrame(output_data, columns=columns)
#     df.to_excel("BangladeshClimateData2024.xlsx", index=False)
#     print("✅ Data extraction complete. Saved to ClimateData2024.xlsx.")

# if __name__ == "__main__":
#     main()


# version: 6.0

import pandas as pd
import requests
from time import sleep

# Full list of 64 districts with their coordinates
districts = {
    'Bagerhat': (22.6512, 89.7851), 'Bandarban': (22.1953, 92.2184), 
    'Barguna': (22.1530, 90.1266), 'Barisal': (22.7010, 90.3535), 
    'Bhola': (22.6859, 90.6482), 'Bogra': (24.8466, 89.3773),
    'Brahmanbaria': (23.9571, 91.1115), 'Chandpur': (23.2513, 90.8512),
    'Chittagong': (22.3569, 91.7832), 'Chuadanga': (23.6402, 88.8410),
    'Comilla': (23.4607, 91.1809), 'Cox\'s Bazar': (21.4272, 92.0058),
    'Dhaka': (23.8103, 90.4125), 'Dinajpur': (25.6270, 88.6377),
    'Faridpur': (23.6070, 89.8420), 'Feni': (23.0101, 91.3976),
    'Gaibandha': (25.3288, 89.5286), 'Gazipur': (23.9999, 90.4203),
    'Gopalganj': (23.0050, 89.8266), 'Habiganj': (24.3745, 91.4155),
    'Jamalpur': (24.9375, 89.9372), 'Jessore': (23.1667, 89.2167),
    'Jhalokathi': (22.6400, 90.1987), 'Jhenaidah': (23.5440, 89.1539),
    'Joypurhat': (25.1023, 89.0200), 'Khagrachhari': (23.1193, 91.9847),
    'Khulna': (22.8456, 89.5403), 'Kishoreganj': (24.4449, 90.7766),
    'Kurigram': (25.8074, 89.6362), 'Kushtia': (23.9013, 89.1206),
    'Lakshmipur': (22.9440, 90.8304), 'Lalmonirhat': (25.9923, 89.2847),
    'Madaripur': (23.1641, 90.1978), 'Magura': (23.5004, 89.4197),
    'Manikganj': (23.8644, 90.0047), 'Meherpur': (23.7627, 88.6318),
    'Moulvibazar': (24.4829, 91.7774), 'Munshiganj': (23.5422, 90.5305),
    'Mymensingh': (24.7471, 90.4203), 'Naogaon': (24.7936, 88.9318),
    'Narail': (23.1725, 89.4951), 'Narayanganj': (23.6238, 90.4993),
    'Narsingdi': (23.9322, 90.7151), 'Natore': (24.4206, 89.0000),
    'Netrokona': (24.8864, 90.7271), 'Nilphamari': (25.9310, 88.8560),
    'Noakhali': (22.8696, 91.0995), 'Pabna': (24.0064, 89.2372),
    'Panchagarh': (26.3411, 88.5542), 'Patuakhali': (22.3596, 90.3290),
    'Pirojpur': (22.5790, 89.9750), 'Rajbari': (23.7570, 89.6440),
    'Rajshahi': (24.3745, 88.6042), 'Rangamati': (22.6372, 92.2061),
    'Rangpur': (25.7439, 89.2752), 'Satkhira': (22.7185, 89.0705),
    'Shariatpur': (23.2423, 90.4348), 'Sherpur': (25.0180, 90.0171),
    'Sirajganj': (24.4534, 89.7000), 'Sunamganj': (25.0657, 91.3950),
    'Sylhet': (24.9045, 91.8611), 'Tangail': (24.3917, 89.9628),
    'Thakurgaon': (26.0339, 88.4512), 'Chapainawabganj': (24.5965, 88.2777),
}

# Open-Meteo API setup
API_ENDPOINT = "https://archive-api.open-meteo.com/v1/era5"
PARAMS_TEMPLATE = {
    "hourly": "temperature_2m,precipitation,sunshine_duration,relative_humidity_2m",
    "timezone": "Asia/Dhaka"
}

def fetch_data(lat, lon, year):
    """Fetch weather data for a district and year."""
    params = PARAMS_TEMPLATE.copy()
    params.update({
        "latitude": lat, "longitude": lon,
        "start_date": f"{year}-01-01", "end_date": f"{year}-12-31"
    })
    response = requests.get(API_ENDPOINT, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"⚠️ Data for {year} not available at {lat}, {lon}.")
        return None

def process_data(data, year):
    """Process the data into monthly aggregates."""
    monthly_data = {
        'Temperature': [None]*12, 'Rainfall': [None]*12, 
        'Sunshine': [None]*12, 'Humidity': [None]*12
    }
    df = pd.DataFrame(data['hourly'])

    for month in range(1, 13):
        month_str = f"{year}-{month:02d}"
        month_data = df[df['time'].str.startswith(month_str)]
        if not month_data.empty:
            monthly_data['Temperature'][month-1] = month_data['temperature_2m'].mean()
            monthly_data['Rainfall'][month-1] = month_data['precipitation'].sum()
            monthly_data['Sunshine'][month-1] = month_data['sunshine_duration'].sum() / 3600  # Convert to hours
            monthly_data['Humidity'][month-1] = month_data['relative_humidity_2m'].mean()
    return monthly_data

def main():
    output_data = []

    for district, (lat, lon) in districts.items():
        for year in range(2022, 2024):
            print(f"Fetching data for {district} ({year})...")
            data = fetch_data(lat, lon, year)
            if data:
                monthly_data = process_data(data, year)
                row = [district, year] + monthly_data['Temperature'] + \
                      monthly_data['Rainfall'] + monthly_data['Sunshine'] + \
                      monthly_data['Humidity']
                output_data.append(row)
            sleep(1)  # To avoid rate limits

    columns = ['District', 'Year'] + \
              [f'Temperature_{month}' for month in range(1, 13)] + \
              [f'Rainfall_{month}' for month in range(1, 13)] + \
              [f'Sunshine_{month}' for month in range(1, 13)] + \
              [f'Humidity_{month}' for month in range(1, 13)]

    df = pd.DataFrame(output_data, columns=columns)
    df.to_excel("BangladeshClimateData2022_2023.xlsx", index=False)
    print("✅ Data extraction complete. Saved to Bangladesh_Climate_Data_2022_2023.xlsx.")

if __name__ == "__main__":
    main()

# version: 5.0

# import pandas as pd
# import requests
# from time import sleep
# import logging

# # Setup logging to track any failed requests
# logging.basicConfig(filename='weather_data_errors_2024.log', level=logging.INFO)

# # Your WeatherAPI key
# API_KEY = "1fe5a94ce82148a1986142957242510"

# # List of 64 districts with their coordinates
# districts = {
#     'Bagerhat': (22.6512, 89.7851), 'Bandarban': (22.1953, 92.2184), 
#     'Barguna': (22.1530, 90.1266), 'Barisal': (22.7010, 90.3535), 
#     'Bhola': (22.6859, 90.6482), 'Bogra': (24.8466, 89.3773),
#     'Brahmanbaria': (23.9571, 91.1115), 'Chandpur': (23.2513, 90.8512),
#     'Chittagong': (22.3569, 91.7832), 'Chuadanga': (23.6402, 88.8410),
#     'Comilla': (23.4607, 91.1809), 'Cox\'s Bazar': (21.4272, 92.0058),
#     'Dhaka': (23.8103, 90.4125), 'Dinajpur': (25.6270, 88.6377),
#     'Faridpur': (23.6070, 89.8420), 'Feni': (23.0101, 91.3976),
#     'Gaibandha': (25.3288, 89.5286), 'Gazipur': (23.9999, 90.4203),
#     'Gopalganj': (23.0050, 89.8266), 'Habiganj': (24.3745, 91.4155),
#     'Jamalpur': (24.9375, 89.9372), 'Jessore': (23.1667, 89.2167),
#     'Jhalokathi': (22.6400, 90.1987), 'Jhenaidah': (23.5440, 89.1539),
#     'Joypurhat': (25.1023, 89.0200), 'Khagrachhari': (23.1193, 91.9847),
#     'Khulna': (22.8456, 89.5403), 'Kishoreganj': (24.4449, 90.7766),
#     'Kurigram': (25.8074, 89.6362), 'Kushtia': (23.9013, 89.1206),
#     'Lakshmipur': (22.9440, 90.8304), 'Lalmonirhat': (25.9923, 89.2847),
#     'Madaripur': (23.1641, 90.1978), 'Magura': (23.5004, 89.4197),
#     'Manikganj': (23.8644, 90.0047), 'Meherpur': (23.7627, 88.6318),
#     'Moulvibazar': (24.4829, 91.7774), 'Munshiganj': (23.5422, 90.5305),
#     'Mymensingh': (24.7471, 90.4203), 'Naogaon': (24.7936, 88.9318),
#     'Narail': (23.1725, 89.4951), 'Narayanganj': (23.6238, 90.4993),
#     'Narsingdi': (23.9322, 90.7151), 'Natore': (24.4206, 89.0000),
#     'Netrokona': (24.8864, 90.7271), 'Nilphamari': (25.9310, 88.8560),
#     'Noakhali': (22.8696, 91.0995), 'Pabna': (24.0064, 89.2372),
#     'Panchagarh': (26.3411, 88.5542), 'Patuakhali': (22.3596, 90.3290),
#     'Pirojpur': (22.5790, 89.9750), 'Rajbari': (23.7570, 89.6440),
#     'Rajshahi': (24.3745, 88.6042), 'Rangamati': (22.6372, 92.2061),
#     'Rangpur': (25.7439, 89.2752), 'Satkhira': (22.7185, 89.0705),
#     'Shariatpur': (23.2423, 90.4348), 'Sherpur': (25.0180, 90.0171),
#     'Sirajganj': (24.4534, 89.7000), 'Sunamganj': (25.0657, 91.3950),
#     'Sylhet': (24.9045, 91.8611), 'Tangail': (24.3917, 89.9628),
#     'Thakurgaon': (26.0339, 88.4512)
# }

# def fetch_weather_data(lat, lon, date):
#     """Fetch weather data from WeatherAPI."""
#     url = f"http://api.weatherapi.com/v1/history.json"
#     params = {"key": API_KEY, "q": f"{lat},{lon}", "dt": date}
#     try:
#         response = requests.get(url, params=params)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             logging.info(f"Failed request for {lat}, {lon} on {date}: {response.status_code}")
#     except Exception as e:
#         logging.info(f"Error fetching {lat}, {lon} on {date}: {e}")
#     return None

# def estimate_sunshine_hours(cloud_cover, daylight_hours):
#     """Estimate sunshine hours based on cloud cover."""
#     return daylight_hours * (1 - cloud_cover / 100)

# def process_daily_data(day_data):
#     """Process individual day's data."""
#     avg_temp = day_data['day']['avgtemp_c']
#     total_rain = day_data['day']['totalprecip_mm']
#     cloud_cover = day_data['day']['avghumidity']  # Assuming cloudiness approximates humidity
#     daylight_duration = 12  # Placeholder (in hours) for simplicity; ideally calculate from sunrise & sunset
    
#     sunshine_hours = estimate_sunshine_hours(cloud_cover, daylight_duration)
#     return avg_temp, total_rain, sunshine_hours

# def process_monthly_data(data):
#     """Aggregate daily data into monthly averages and sums."""
#     temp_sum, rain_sum, sunshine_sum, count = 0, 0, 0, 0
#     for day in data.get('forecast', {}).get('forecastday', []):
#         avg_temp, total_rain, sunshine_hours = process_daily_data(day)
#         temp_sum += avg_temp
#         rain_sum += total_rain
#         sunshine_sum += sunshine_hours
#         count += 1
#     if count > 0:
#         return temp_sum / count, rain_sum, sunshine_sum
#     return None, None, None

# def main():
#     output_data = []

#     for district, (lat, lon) in districts.items():
#         year = 2024
#         temperatures, rainfalls, sunshines = [], [], []
        
#         for month in range(1, 13):
#             date = f"{year}-{month:02d}-01"
#             print(f"Fetching data for {district} ({year}-{month:02d})...")
#             data = fetch_weather_data(lat, lon, date)
#             if data:
#                 temp, rain, sunshine = process_monthly_data(data)
#                 temperatures.append(temp)
#                 rainfalls.append(rain)
#                 sunshines.append(sunshine)
#             else:
#                 temperatures.append(None)
#                 rainfalls.append(None)
#                 sunshines.append(None)
#             sleep(1)  # Avoid hitting rate limits

#         # Append the row for the current district
#         row = [district, year] + temperatures + rainfalls + sunshines
#         output_data.append(row)

#     # Define columns as per the existing file's format
#     columns = (
#         ['District', 'Year'] +
#         [f'Temperature_{i}' for i in range(1, 13)] +
#         [f'Rainfall_{i}' for i in range(1, 13)] +
#         [f'Sunshine_{i}' for i in range(1, 13)]
#     )

#     # Create a DataFrame and save it to Excel
#     df = pd.DataFrame(output_data, columns=columns)
#     df.to_excel("ClimateData2023.xlsx", index=False)
#     print("✅ Data extraction complete. Saved to Bangladesh_Climate_Data_2024.xlsx.")

# if __name__ == "__main__":
#     main()


# version: 4.0

# import pandas as pd
# import requests
# from time import sleep
# import logging

# # Setup logging to track any failed requests
# logging.basicConfig(filename='weather_data_errors_2024.log', level=logging.INFO)

# # Your WeatherAPI key
# API_KEY = "1fe5a94ce82148a1986142957242510"

# # List of 64 districts with their coordinates
# districts = {
#     'Bagerhat': (22.6512, 89.7851), 'Bandarban': (22.1953, 92.2184), 
#     'Barguna': (22.1530, 90.1266), 'Barisal': (22.7010, 90.3535), 
#     'Bhola': (22.6859, 90.6482), 'Bogra': (24.8466, 89.3773),
#     'Brahmanbaria': (23.9571, 91.1115), 'Chandpur': (23.2513, 90.8512),
#     'Chittagong': (22.3569, 91.7832), 'Chuadanga': (23.6402, 88.8410),
#     'Comilla': (23.4607, 91.1809), 'Cox\'s Bazar': (21.4272, 92.0058),
#     'Dhaka': (23.8103, 90.4125), 'Dinajpur': (25.6270, 88.6377),
#     'Faridpur': (23.6070, 89.8420), 'Feni': (23.0101, 91.3976),
#     'Gaibandha': (25.3288, 89.5286), 'Gazipur': (23.9999, 90.4203),
#     'Gopalganj': (23.0050, 89.8266), 'Habiganj': (24.3745, 91.4155),
#     'Jamalpur': (24.9375, 89.9372), 'Jessore': (23.1667, 89.2167),
#     'Jhalokathi': (22.6400, 90.1987), 'Jhenaidah': (23.5440, 89.1539),
#     'Joypurhat': (25.1023, 89.0200), 'Khagrachhari': (23.1193, 91.9847),
#     'Khulna': (22.8456, 89.5403), 'Kishoreganj': (24.4449, 90.7766),
#     'Kurigram': (25.8074, 89.6362), 'Kushtia': (23.9013, 89.1206),
#     'Lakshmipur': (22.9440, 90.8304), 'Lalmonirhat': (25.9923, 89.2847),
#     'Madaripur': (23.1641, 90.1978), 'Magura': (23.5004, 89.4197),
#     'Manikganj': (23.8644, 90.0047), 'Meherpur': (23.7627, 88.6318),
#     'Moulvibazar': (24.4829, 91.7774), 'Munshiganj': (23.5422, 90.5305),
#     'Mymensingh': (24.7471, 90.4203), 'Naogaon': (24.7936, 88.9318),
#     'Narail': (23.1725, 89.4951), 'Narayanganj': (23.6238, 90.4993),
#     'Narsingdi': (23.9322, 90.7151), 'Natore': (24.4206, 89.0000),
#     'Netrokona': (24.8864, 90.7271), 'Nilphamari': (25.9310, 88.8560),
#     'Noakhali': (22.8696, 91.0995), 'Pabna': (24.0064, 89.2372),
#     'Panchagarh': (26.3411, 88.5542), 'Patuakhali': (22.3596, 90.3290),
#     'Pirojpur': (22.5790, 89.9750), 'Rajbari': (23.7570, 89.6440),
#     'Rajshahi': (24.3745, 88.6042), 'Rangamati': (22.6372, 92.2061),
#     'Rangpur': (25.7439, 89.2752), 'Satkhira': (22.7185, 89.0705),
#     'Shariatpur': (23.2423, 90.4348), 'Sherpur': (25.0180, 90.0171),
#     'Sirajganj': (24.4534, 89.7000), 'Sunamganj': (25.0657, 91.3950),
#     'Sylhet': (24.9045, 91.8611), 'Tangail': (24.3917, 89.9628),
#     'Thakurgaon': (26.0339, 88.4512)
# }

# def fetch_weather_data(lat, lon, date):
#     """Fetch weather data from WeatherAPI."""
#     url = f"http://api.weatherapi.com/v1/history.json"
#     params = {"key": API_KEY, "q": f"{lat},{lon}", "dt": date}
#     try:
#         response = requests.get(url, params=params)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             logging.info(f"Failed request for {lat}, {lon} on {date}: {response.status_code}")
#     except Exception as e:
#         logging.info(f"Error fetching {lat}, {lon} on {date}: {e}")
#     return None

# def process_monthly_data(data):
#     """Aggregate daily data into monthly averages and sums."""
#     temp_sum, rain_sum, sunshine_sum, count = 0, 0, 0, 0
#     for day in data.get('forecast', {}).get('forecastday', []):
#         temp_sum += day['day']['avgtemp_c']
#         rain_sum += day['day']['totalprecip_mm']
#         sunshine_sum += day['day'].get('daily_will_it_sun', 0)
#         count += 1
#     if count > 0:
#         return temp_sum / count, rain_sum, sunshine_sum
#     return None, None, None

# def main():
#     output_data = []

#     for district, (lat, lon) in districts.items():
#         year = 2024
#         temperatures, rainfalls, sunshines = [], [], []
        
#         for month in range(1, 13):
#             date = f"{year}-{month:02d}-01"
#             print(f"Fetching data for {district} ({year}-{month:02d})...")
#             data = fetch_weather_data(lat, lon, date)
#             if data:
#                 temp, rain, sunshine = process_monthly_data(data)
#                 temperatures.append(temp)
#                 rainfalls.append(rain)
#                 sunshines.append(sunshine)
#             else:
#                 temperatures.append(None)
#                 rainfalls.append(None)
#                 sunshines.append(None)
#             sleep(1)  # Avoid hitting rate limits

#         # Append the row for the current district
#         row = [district, year] + temperatures + rainfalls + sunshines
#         output_data.append(row)

#     # Define columns as per the existing file's format
#     columns = (
#         ['District', 'Year'] +
#         [f'Temperature_{i}' for i in range(1, 13)] +
#         [f'Rainfall_{i}' for i in range(1, 13)] +
#         [f'Sunshine_{i}' for i in range(1, 13)]
#     )

#     # Create a DataFrame and save it to Excel
#     df = pd.DataFrame(output_data, columns=columns)
#     df.to_excel("Bangladesh_Climate_Data_2024.xlsx", index=False)
#     print("✅ Data extraction complete. Saved to Bangladesh_Climate_Data_2024.xlsx.")

# if __name__ == "__main__":
#     main()


# version: 3.0

# import pandas as pd
# import requests
# from time import sleep

# # Your WeatherAPI key
# API_KEY = "1fe5a94ce82148a1986142957242510"

# # List of 64 districts in Bangladesh with their coordinates
# districts = {
#     'Bagerhat': (22.6512, 89.7851), 'Bandarban': (22.1953, 92.2184), 
#     'Barguna': (22.1530, 90.1266), 'Barisal': (22.7010, 90.3535), 
#     'Bhola': (22.6859, 90.6482), 'Bogra': (24.8466, 89.3773),
#     'Brahmanbaria': (23.9571, 91.1115), 'Chandpur': (23.2513, 90.8512),
#     'Chittagong': (22.3569, 91.7832), 'Chuadanga': (23.6402, 88.8410),
#     'Comilla': (23.4607, 91.1809), 'Cox\'s Bazar': (21.4272, 92.0058),
#     'Dhaka': (23.8103, 90.4125), 'Dinajpur': (25.6270, 88.6377),
#     'Faridpur': (23.6070, 89.8420), 'Feni': (23.0101, 91.3976),
#     'Gaibandha': (25.3288, 89.5286), 'Gazipur': (23.9999, 90.4203),
#     'Gopalganj': (23.0050, 89.8266), 'Habiganj': (24.3745, 91.4155),
#     'Jamalpur': (24.9375, 89.9372), 'Jessore': (23.1667, 89.2167),
#     'Jhalokathi': (22.6400, 90.1987), 'Jhenaidah': (23.5440, 89.1539),
#     'Joypurhat': (25.1023, 89.0200), 'Khagrachhari': (23.1193, 91.9847),
#     'Khulna': (22.8456, 89.5403), 'Kishoreganj': (24.4449, 90.7766),
#     'Kurigram': (25.8074, 89.6362), 'Kushtia': (23.9013, 89.1206),
#     'Lakshmipur': (22.9440, 90.8304), 'Lalmonirhat': (25.9923, 89.2847),
#     'Madaripur': (23.1641, 90.1978), 'Magura': (23.5004, 89.4197),
#     'Manikganj': (23.8644, 90.0047), 'Meherpur': (23.7627, 88.6318),
#     'Moulvibazar': (24.4829, 91.7774), 'Munshiganj': (23.5422, 90.5305),
#     'Mymensingh': (24.7471, 90.4203), 'Naogaon': (24.7936, 88.9318),
#     'Narail': (23.1725, 89.4951), 'Narayanganj': (23.6238, 90.4993),
#     'Narsingdi': (23.9322, 90.7151), 'Natore': (24.4206, 89.0000),
#     'Netrokona': (24.8864, 90.7271), 'Nilphamari': (25.9310, 88.8560),
#     'Noakhali': (22.8696, 91.0995), 'Pabna': (24.0064, 89.2372),
#     'Panchagarh': (26.3411, 88.5542), 'Patuakhali': (22.3596, 90.3290),
#     'Pirojpur': (22.5790, 89.9750), 'Rajbari': (23.7570, 89.6440),
#     'Rajshahi': (24.3745, 88.6042), 'Rangamati': (22.6372, 92.2061),
#     'Rangpur': (25.7439, 89.2752), 'Satkhira': (22.7185, 89.0705),
#     'Shariatpur': (23.2423, 90.4348), 'Sherpur': (25.0180, 90.0171),
#     'Sirajganj': (24.4534, 89.7000), 'Sunamganj': (25.0657, 91.3950),
#     'Sylhet': (24.9045, 91.8611), 'Tangail': (24.3917, 89.9628),
#     'Thakurgaon': (26.0339, 88.4512)
# }

# def fetch_weather_data(lat, lon, date):
#     """Fetch weather data from WeatherAPI."""
#     url = f"http://api.weatherapi.com/v1/history.json"
#     params = {
#         "key": API_KEY,
#         "q": f"{lat},{lon}",
#         "dt": date
#     }
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"⚠️ Failed to fetch data for {lat}, {lon} on {date}.")
#         return None

# def process_monthly_data(data):
#     """Process daily data into monthly aggregates."""
#     temp_sum, rain_sum, sunshine_sum, count = 0, 0, 0, 0
#     for day in data['forecast']['forecastday']:
#         temp_sum += day['day']['avgtemp_c']
#         rain_sum += day['day']['totalprecip_mm']
#         sunshine_sum += day['day'].get('daily_will_it_sun', 0)
#         count += 1
#     return temp_sum / count, rain_sum, sunshine_sum

# def main():
#     output_data = []

#     for district, (lat, lon) in districts.items():
#         for year in range(2022, 2024):
#             for month in range(1, 13):
#                 date = f"{year}-{month:02d}-01"
#                 print(f"Fetching data for {district} ({year}-{month:02d})...")
#                 data = fetch_weather_data(lat, lon, date)
#                 if data:
#                     temp, rain, sunshine = process_monthly_data(data)
#                     row = [district, year, month, temp, rain, sunshine]
#                     output_data.append(row)
#                 sleep(1)  # Avoid hitting rate limits

#     # Save data to Excel
#     columns = ['District', 'Year', 'Month', 'Avg_Temperature_C', 'Total_Rainfall_mm', 'Sunshine_Hours']
#     df = pd.DataFrame(output_data, columns=columns)
#     df.to_excel("Bangladesh_Climate_Data_WeatherAPI.xlsx", index=False)
#     print("✅ Data extraction complete. Saved to Bangladesh_Climate_Data_WeatherAPI.xlsx.")

# if __name__ == "__main__":
#     main()

# version: 2.0

# import pandas as pd
# import requests
# from time import sleep

# # Full list of 64 districts with their coordinates
# districts = {
#     'Bagerhat': (22.6512, 89.7851), 'Bandarban': (22.1953, 92.2184), 'Barguna': (22.1530, 90.1266),
#     'Barisal': (22.7010, 90.3535), 'Bhola': (22.6859, 90.6482), 'Bogra': (24.8466, 89.3773),
#     'Brahmanbaria': (23.9571, 91.1115), 'Chandpur': (23.2513, 90.8512), 'Chittagong': (22.3569, 91.7832),
#     'Chuadanga': (23.6402, 88.8410), 'Comilla': (23.4607, 91.1809), 'Cox\'s Bazar': (21.4272, 92.0058),
#     'Dhaka': (23.8103, 90.4125), 'Dinajpur': (25.6270, 88.6377), 'Faridpur': (23.6070, 89.8420),
#     'Feni': (23.0101, 91.3976), 'Gaibandha': (25.3288, 89.5286), 'Gazipur': (23.9999, 90.4203),
#     'Gopalganj': (23.0050, 89.8266), 'Habiganj': (24.3745, 91.4155), 'Jamalpur': (24.9375, 89.9372),
#     'Jessore': (23.1667, 89.2167), 'Jhalokathi': (22.6400, 90.1987), 'Jhenaidah': (23.5440, 89.1539),
#     'Joypurhat': (25.1023, 89.0200), 'Khagrachhari': (23.1193, 91.9847), 'Khulna': (22.8456, 89.5403),
#     'Kishoreganj': (24.4449, 90.7766), 'Kurigram': (25.8074, 89.6362), 'Kushtia': (23.9013, 89.1206),
#     'Lakshmipur': (22.9440, 90.8304), 'Lalmonirhat': (25.9923, 89.2847), 'Madaripur': (23.1641, 90.1978),
#     'Magura': (23.5004, 89.4197), 'Manikganj': (23.8644, 90.0047), 'Meherpur': (23.7627, 88.6318),
#     'Moulvibazar': (24.4829, 91.7774), 'Munshiganj': (23.5422, 90.5305), 'Mymensingh': (24.7471, 90.4203),
#     'Naogaon': (24.7936, 88.9318), 'Narail': (23.1725, 89.4951), 'Narayanganj': (23.6238, 90.4993),
#     'Narsingdi': (23.9322, 90.7151), 'Natore': (24.4206, 89.0000), 'Netrokona': (24.8864, 90.7271),
#     'Nilphamari': (25.9310, 88.8560), 'Noakhali': (22.8696, 91.0995), 'Pabna': (24.0064, 89.2372),
#     'Panchagarh': (26.3411, 88.5542), 'Patuakhali': (22.3596, 90.3290), 'Pirojpur': (22.5790, 89.9750),
#     'Rajbari': (23.7570, 89.6440), 'Rajshahi': (24.3745, 88.6042), 'Rangamati': (22.6372, 92.2061),
#     'Rangpur': (25.7439, 89.2752), 'Satkhira': (22.7185, 89.0705), 'Shariatpur': (23.2423, 90.4348),
#     'Sherpur': (25.0180, 90.0171), 'Sirajganj': (24.4534, 89.7000), 'Sunamganj': (25.0657, 91.3950),
#     'Sylhet': (24.9045, 91.8611), 'Tangail': (24.3917, 89.9628), 'Thakurgaon': (26.0339, 88.4512)
# }

# # Open-Meteo API setup
# API_ENDPOINT = "https://archive-api.open-meteo.com/v1/era5"
# PARAMS_TEMPLATE = {
#     "hourly": "temperature_2m,precipitation,sunshine_duration",
#     "timezone": "Asia/Dhaka"
# }

# def fetch_data(lat, lon, year):
#     """Fetch weather data for a district and year."""
#     params = PARAMS_TEMPLATE.copy()
#     params.update({
#         "latitude": lat, "longitude": lon,
#         "start_date": f"{year}-01-01", "end_date": f"{year}-12-31"
#     })
#     response = requests.get(API_ENDPOINT, params=params)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"⚠️ Data for {year} not available at {lat}, {lon}.")
#         return None

# def process_data(data, year):
#     """Process the data into monthly aggregates."""
#     monthly_data = {'Temperature': [None]*12, 'Rainfall': [None]*12, 'Sunshine': [None]*12}
#     df = pd.DataFrame(data['hourly'])

#     for month in range(1, 13):
#         month_str = f"{year}-{month:02d}"
#         month_data = df[df['time'].str.startswith(month_str)]
#         if not month_data.empty:
#             monthly_data['Temperature'][month-1] = month_data['temperature_2m'].mean()
#             monthly_data['Rainfall'][month-1] = month_data['precipitation'].sum()
#             monthly_data['Sunshine'][month-1] = month_data['sunshine_duration'].sum() / 3600  # Convert to hours
#     return monthly_data

# def main():
#     output_data = []

#     for district, (lat, lon) in districts.items():
#         for year in range(2022, 2024):
#             print(f"Fetching data for {district} ({year})...")
#             data = fetch_data(lat, lon, year)
#             if data:
#                 monthly_data = process_data(data, year)
#                 row = [district, year] + monthly_data['Temperature'] + \
#                       monthly_data['Rainfall'] + monthly_data['Sunshine']
#                 output_data.append(row)
#             sleep(1)  # To avoid rate limits

#     columns = ['District', 'Year'] + \
#               [f'Temperature_{month}' for month in range(1, 13)] + \
#               [f'Rainfall_{month}' for month in range(1, 13)] + \
#               [f'Sunshine_{month}' for month in range(1, 13)]

#     df = pd.DataFrame(output_data, columns=columns)
#     df.to_excel("BangladeshClimateData2022_2023.xlsx", index=False)
#     print("✅ Data extraction complete. Saved to Bangladesh_Climate_Data_2022_2024.xlsx.")

# if __name__ == "__main__":
#     main()

# version: 1.0

# import pandas as pd
# import requests
# from time import sleep

# # List of 64 districts in Bangladesh with their coordinates
# districts = {
#     'Dhaka': (23.8103, 90.4125), 'Chittagong': (22.3569, 91.7832), 
#     'Sylhet': (24.9045, 91.8611), 'Rajshahi': (24.3745, 88.6042),
#     'Barisal': (22.7010, 90.3535), 'Khulna': (22.8456, 89.5403),
#     'Rangpur': (25.7439, 89.2752), 'Mymensingh': (24.7471, 90.4203),
#     'Comilla': (23.4607, 91.1809), 'Gazipur': (23.9999, 90.4203),
#     'Narayanganj': (23.6238, 90.4993), 'Tangail': (24.2513, 89.9165),
#     'Kushtia': (23.9013, 89.1206), 'Jessore': (23.1667, 89.2167),
#     'Patuakhali': (22.3596, 90.3290), 'Bagerhat': (22.6512, 89.7851),
#     'Faridpur': (23.6070, 89.8420), 'Noakhali': (22.8696, 91.0995),
#     'Bogra': (24.8466, 89.3773), 'Dinajpur': (25.6270, 88.6377),
#     'Cox\'s Bazar': (21.4272, 92.0058), 'Pabna': (24.0064, 89.2372),
#     'Feni': (23.0101, 91.3976), 'Sirajganj': (24.4534, 89.7000),
#     'Nawabganj': (24.5965, 88.2776), 'Tangail': (24.3917, 89.9628),
#     # Add more districts as needed...
# }

# API_ENDPOINT = "https://archive-api.open-meteo.com/v1/era5"
# PARAMS_TEMPLATE = {
#     "hourly": "temperature_2m,precipitation,sunshine_duration",
#     "timezone": "Asia/Dhaka"
# }

# def fetch_data(lat, lon, year):
#     """Fetch weather data from the Open-Meteo API."""
#     params = PARAMS_TEMPLATE.copy()
#     params.update({
#         "latitude": lat, "longitude": lon,
#         "start_date": f"{year}-01-01", "end_date": f"{year}-12-31"
#     })
#     response = requests.get(API_ENDPOINT, params=params)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Failed to fetch data for {lat}, {lon} ({year})")
#         return None

# def process_data(data, year):
#     """Process the API response into monthly averages and sums."""
#     monthly_data = {'Temperature': [None]*12, 'Rainfall': [None]*12, 'Sunshine': [None]*12}
#     df = pd.DataFrame(data['hourly'])

#     for month in range(1, 13):
#         month_str = f"{year}-{month:02d}"
#         month_data = df[df['time'].str.startswith(month_str)]
#         monthly_data['Temperature'][month-1] = month_data['temperature_2m'].mean()
#         monthly_data['Rainfall'][month-1] = month_data['precipitation'].sum()
#         monthly_data['Sunshine'][month-1] = month_data['sunshine_duration'].sum() / 3600  # Convert to hours

#     return monthly_data

# def main():
#     output_data = []

#     for district, (lat, lon) in districts.items():
#         for year in range(2022, 2025):
#             print(f"Fetching data for {district} ({year})...")
#             data = fetch_data(lat, lon, year)
#             if data:
#                 monthly_data = process_data(data, year)
#                 row = [district, year] + monthly_data['Temperature'] + \
#                       monthly_data['Rainfall'] + monthly_data['Sunshine']
#                 output_data.append(row)
#             sleep(1)  # To avoid hitting rate limits

#     columns = ['District', 'Year'] + \
#               [f'Temperature_{month}' for month in range(1, 13)] + \
#               [f'Rainfall_{month}' for month in range(1, 13)] + \
#               [f'Sunshine_{month}' for month in range(1, 13)]

#     df = pd.DataFrame(output_data, columns=columns)
#     df.to_excel("Bangladesh_Climate_Data_2022_2024.xlsx", index=False)
#     print("Data extraction complete. Saved to Bangladesh_Climate_Data_2022_2024.xlsx.")

# if __name__ == "__main__":
#     main()
