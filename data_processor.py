import pandas as pd
import geocoder
import os

HERE_APP_ID = os.getenv('HERE_APP_ID')
HERE_APP_CODE = os.getenv('HERE_APP_CODE')
MAPQUEST_KEY = os.getenv('MAPQUEST_API_KEY')

def lat(row):
    return geocoder.here(row['Address'] + ', New York', app_id=HERE_APP_ID, app_code=HERE_APP_CODE).lat

def lng(row):
    return geocoder.here(row['Address'] + ', New York', app_id=HERE_APP_ID, app_code=HERE_APP_CODE).lng

def init():
    print(HERE_APP_ID, HERE_APP_CODE)
    df = pd.read_csv('csv_files/clothing.csv')
    df['lat'] = df.apply(lat, axis=1)
    df['lng'] = df.apply(lng, axis=1)

    print(df.isnull().values.any())

    df.to_json('clothing_charities.json', orient='records')

def reverse_geocode(row):
    return geocoder.mapquest([row['lat'], row['lng']], method='reverse', key=MAPQUEST_KEY).json['address']

def map_quest():
    print(MAPQUEST_KEY)
    df = pd.read_json('service.json')
    df['Address'] = df.apply(reverse_geocode, axis=1)
    print(df.isnull().values.any())
    df.to_json('new_service.json', orient='records')

def zip_code(row):
    return geocoder.here(row['Address'] + ', New York', app_id=HERE_APP_ID, app_code=HERE_APP_CODE).postal

def func():
    df = pd.read_json('service.json')
    df['Zip Code'] = df.apply(zip_code, axis=1)
    df.to_json('new_service.json', orient='records')

func()
