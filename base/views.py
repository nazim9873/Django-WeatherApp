from django.shortcuts import render
import requests
from datetime import datetime
from django.templatetags.static import static

# Create your views here.
def WeatherDetails(request):
    details = []

    if request.method == "POST":
        tags = request.POST.get('tags')
        tags = tags.strip('][').split(',')
        for tag in tags:
            tag = eval(tag)
            city = tag['value']
            latitude , longitude, country = findCoordinates(city)
            if latitude:
                current_weather = findWeatherInfo(latitude, longitude)
                interpretation = findWeatherInterpretation(current_weather)
                current_weather['time'] =  updateTimeFormat(current_weather)
                current_weather['image_url'] = getImageUrl(current_weather)
                current_weather['interpretation'] = interpretation
                current_weather['city'] = city
                current_weather['country'] = country
                details.append(current_weather)               

    context = {"details": details}
    return render(request, 'main.html', context)

def updateTimeFormat(current_weather):
    date_time = datetime.strptime(current_weather['time'], "%Y-%m-%dT%H:%M")
    return date_time.strftime("%d %B, %Y %I%p")

def findCoordinates(city):
    response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}")
    response = response.json()
    if response and response.get('results') and response.get('results'):
        res = response['results'][0]
        x , y, z = res['latitude'], res['longitude'], res.get('country', "")
    else:
        x, y, z = False, False, False
    return x, y, z

    
def findWeatherInfo(latitude, longitude):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=True")
    response = response.json()
    if response and response.get('current_weather'):
        return response['current_weather']

def findWeatherInterpretation(current_weather):
    interpretation_dict = {
        0 : "Clear sky",
        1 : "Mainly clear, partly cloudy, and overcast",
        2 : "Mainly clear, partly cloudy, and overcast",
        3 : "Mainly clear, partly cloudy, and overcast",
        45 : "Fog and depositing rime fog",
        48 : "Fog and depositing rime fog",
        51 : "Drizzle: Light, moderate, and dense intensity",
        53 : "Drizzle: Light, moderate, and dense intensity",
        55 : "Drizzle: Light, moderate, and dense intensity",
        56: "Freezing Drizzle: Light and dense intensity",
        57 : "Freezing Drizzle: Light and dense intensity",
        61 : "Rain: Slight, moderate and heavy intensity",
        63 : "Rain: Slight, moderate and heavy intensity",
        65 : "Rain: Slight, moderate and heavy intensity",
        66 : "Freezing Rain: Light and heavy intensity",
        67 : "Freezing Rain: Light and heavy intensity" ,
        71 : "Snow fall: Slight, moderate, and heavy intensity",
        73 : "Snow fall: Slight, moderate, and heavy intensity",
        75 : "Snow fall: Slight, moderate, and heavy intensity",
        77 : "Snow grains",
        80 : "Rain showers: Slight, moderate, and violent",
        81 : "Rain showers: Slight, moderate, and violent",
        82 : "Rain showers: Slight, moderate, and violent",
        85 : "Snow showers slight and heavy",
        86 : "Snow showers slight and heavy",
        95 : "Thunderstorm: Slight or moderate",
        96 : "Thunderstorm with slight and heavy hail",
        99 : "Thunderstorm with slight and heavy hail"
    }

    weathercode = current_weather['weathercode']
    interpretation = interpretation_dict.get(weathercode, None)
    return interpretation
    
def getImageUrl(current_weather):
    return {
        0 : static('images/clear_sky.jpg'),
        1 : static('images/partly_cloudy.jpg'),
        2 : static('images/partly_cloudy.jpg'),
        3 : static('images/partly_cloudy.jpg'),
        45 : static('images/fog.jpg'),
        48 : static('images/fog.jpg'),
        51 : static('images/light_rain.jpg'),
        53 : static('images/light_rain.jpg'),
        55 : static('images/light_rain.jpg'),
        56: static('images/freezing_drizzle.jpg'),
        57 : static('images/freezing_drizzle.jpg'),
        61 : static('images/rain.jpg'),
        63 : static('images/rain.jpg'),
        65 : static('images/rain.jpg'),
        66 : static('images/freezing_rain.jpg'),
        67 : static('images/freezing_rain.jpg'),
        71 : static('images/snowfall.jpg'),
        73 : static('images/snowfall.jpg'),
        75 : static('images/snowfall.jpg'),
        77 : static('images/snow_grains.jpg'),
        80 : static('images/rain_shower.jpg'),
        81 : static('images/rain_shower.jpg'),
        82 : static('images/rain_shower.jpg'),
        85 : static('images/snow_shower.jpg'),
        86 : static('images/snow_shower.jpg'),
        95 : static('images/thunderstorm.jpg'),
        96 : static('images/heavy_hail.jpg'),
        99 : static('images/heavy_hail.jpg'),
    }.get(current_weather['weathercode'], None)
