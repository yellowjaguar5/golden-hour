# -*- coding: utf-8 -*-
from random import choice
from golden_hour.sunset import get_today_sunset_time
from golden_hour.location import get_location


def get_status_text(climacell_key, location, aq_sensor):
    from requests import request
    from json import loads
    sunset_time = get_today_sunset_time(location)
    forecast = loads(
        request("GET", "https://api.climacell.co/v3/weather/realtime",
                params={"lat": location.latitude,
                        "lon": location.longitude,
                        "unit_system": "us",
                        "fields": "weather_code,temp,feels_like,"
                                  "cloud_cover,precipitation_type,"
                                  "precipitation,wind_speed,"
                                  "wind_direction,visibility,"
                                  "epa_aqi,"  # "moon_phase,"
                                  "epa_primary_pollutant,"
                                  "epa_health_concern",
                        "apikey": climacell_key}).text)
    return '\n'.join(
        filter(None, [
            '🌅 sunset at {}\n'.format(sunset_time.strftime('%I:%M%p')),
            summary(forecast['weather_code'], forecast['cloud_cover'], forecast['temp']),
            temp(forecast['temp'], forecast['feels_like']),
            cloudiness(forecast['cloud_cover']),
            precipitation(forecast['cloud_cover'],
                          forecast['precipitation_type'], forecast['precipitation']),
            wind(forecast['wind_speed'], forecast['wind_direction']),
            visibility(forecast['visibility']),
            air_quality(forecast['epa_aqi'], forecast['epa_primary_pollutant']),
            get_aq_sensor(aq_sensor)
        ])
    )


def summary(weather_code_dict, cloud_cover_dict, temp_dict):
    weather_code = weather_code_dict['value']
    cloud_cover = cloud_cover_dict['value']
    temperature = temp_dict['value']

    return '{} {}'.format(
        get_emoji(weather_code, temperature, cloud_cover),
        weather_code.replace("_", " ").lower()
    )


def temp(temp_dict, feels_like_dict):
    temperature = temp_dict['value']
    apparent_temp = feels_like_dict['value']
    units = temp_dict['units']

    feels_like = (
        ''
        if round(temperature) == round(apparent_temp)
        else ' (feels like {})'.format(display_temp(apparent_temp, units))
    )

    return '🌡 {}{}'.format(
        display_temp(temperature, units),
        feels_like
    )


def cloudiness(cloud_cover_dict):
    cloud_cover = cloud_cover_dict['value']

    if cloud_cover > 0.01:
        return '{} {}% cloud cover'.format(
            get_cloud_cover_emoji(cloud_cover),
            round(cloud_cover)  # default units are percent
        )


def precipitation(cloud_cover_dict, precipitation_type_dict, precipitation_dict):
    cloud_cover = cloud_cover_dict['value']

    precipitation_amount = precipitation_dict['value']
    precipitation_type = precipitation_type_dict['value']

    if precipitation_type != "none":
        return '{} {} at {} {}'.format(
            get_precipitation_emoji(precipitation_type, cloud_cover),
            precipitation_type.replace("_", " ").lower(),
            round(precipitation_amount, 3),
            precipitation_dict['units']
        )


def wind(wind_speed_dict, wind_direction_dict):
    wind_speed = wind_speed_dict['value']
    wind_direction = wind_direction_dict['value']

    if wind_speed > 5:
        return '💨 winds about {} {} from the {}'.format(
            round(wind_speed),
            wind_speed_dict['units'],
            get_bearing(wind_direction)
        )


def visibility(visibility_dict):
    vis = visibility_dict['value']
    if vis < 5:
        return '🌁 {} {} of visibility'.format(vis, visibility_dict['units'])


def air_quality(epa_aqi_dict, epa_health_concern_dict):
    epa_aqi = epa_aqi_dict['value']
    # primary_pollutant = epa_primary_pollutant_dict['value']
    health_concern = epa_health_concern_dict['value']

    if epa_aqi > 10:
        return '{} aqi of {} ({})'.format(get_air_quality_emoji(epa_aqi),
                                          round(epa_aqi),
                                          health_concern.lower())


def get_aq_sensor(use_sensor):
    if use_sensor:
        try:
            from golden_hour import pm_sensor
            sensor_data = pm_sensor.read()
            pm25 = sensor_data[0]
            pm10 = sensor_data[1]
        except RuntimeError as error:
            print("Exception reading air quality sensor:", error.args)
        except Exception as error:
            print("Unknown exception reading air quality sensor", error.args)
        else:
            print("Data received from air quality sensor:", sensor_data)
            if pm10 + pm25 >= 4:
                return "hyper-local air quality: pm2.5: {} ({}), pm10: {} ({})".format(
                    pm25, get_pm_25_category(pm25),
                    pm10, get_pm_10_category(pm10))
    else:
        print("Air Quality Sensor not requested.")


def get_pm_10_category(pm10):
    if pm10 < 55:
        return "Good"
    elif pm10 < 155:
        return "Moderate"
    elif pm10 < 255:
        return "Unhealthy for Sensitive Groups"
    elif pm10 < 355:
        return "Unhealthy"
    else:
        return "Very Unhealthy"


def get_pm_25_category(pm25):
    if pm25 < 15.5:
        return "Good"
    elif pm25 < 40.5:
        return "Moderate"
    elif pm25 < 65.5:
        return "Unhealthy for Sensitive Groups"
    elif pm25 < 150.5:
        return "Unhealthy"
    else:
        return "Very Unhealthy"


def display_temp(temperature, units):
    degrees = '℉' if units == 'F' else '℃'

    return str(round(temperature)) + degrees


def get_emoji(weather_code, temperature, cloud_cover):
    if 'clear' in weather_code:
        if temperature > 75:
            return choice(['☀️', '☀️', '😎'])

        if temperature < 32:
            return choice(['☀️', '☀️', '⛄️'])

        return '☀️'

    if ('rain' in weather_code) or ('freezing' in weather_code):
        if cloud_cover < 0.5:
            return choice(['🌧', '☔️', '🌦'])

        return choice(['🌧', '☔️'])

    if weather_code == 'drizzle':
        return '🌦'

    if ('ice_pellets' in weather_code) or ('snow' in weather_code):
        return choice(['❄️', '🌨', '☃️'])

    if 'fog' in weather_code:
        return '🌁'

    return {
        'flurries': '🌨',
        'tstorm': '⛈',
        'cloudy': '☁️',
        'partly_cloudy': '⛅',
    }.get(weather_code, '')


def get_cloud_cover_emoji(cloud_cover):
    if cloud_cover < 0.2:
        return '☀️'

    if cloud_cover < 0.5:
        return '🌤'

    if cloud_cover < 0.9:
        return '🌥'

    return '☁️'


def get_precipitation_emoji(precip_type, cloud_cover):
    if precip_type == 'rain':
        if cloud_cover < 0.5:
            return choice(['🌧', '☔️', '🌦'])

        return choice(['🌧', '☔️'])

    if (precip_type == 'snow') or ('ice' in precip_type):
        return choice(['❄️', '🌨', '☃️'])

    if 'freezing' in precip_type:
        return '🌨'

    return ''


def get_bearing(degrees, short=False):
    directions = (
        'N,NNE,NE,ENE,E,ESE,SE,SSE,S,SSW,SW,WSW,W,WNW,NW,NNW'
        if short
        else 'north,northeast,east,southeast,south,southwest,'
             'west,northwest'
    ).split(',')

    count = len(directions)

    # Distance between each direction
    span = 360.0 / count

    # Use modulo to "round" `16` to `0`
    index = round(degrees / span) % count

    return directions[index]


def get_air_quality_emoji(aqi):
    if aqi < 50:
        return "🏞"
    elif aqi < 100:
        return '⚠️'
    elif aqi < 150:
        return '🌆'
    elif aqi < 200:
        return '🚩'
    elif aqi < 250:
        return '👾'
    else:
        return '🌫'


if __name__ == '__main__':
    from os.path import isfile, expanduser
    from golden_hour import configuration

    if isfile(expanduser('~/.config/golden-hour.yaml')):
        config = configuration.load_configuration(
            expanduser('~/.config/golden-hour.yaml'))
    else:
        config = configuration.load_configuration(expanduser(
            str(input("Enter path from user home to yaml config file "
                      "(starting with ~/): "))))

    print(get_status_text(
        config['climacell_key'],
        get_location(config['location']),
        config['use_air_quality_sensor']))
