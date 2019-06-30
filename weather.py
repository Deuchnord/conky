#!/usr/bin/env python

import argparse
import json
from datetime import datetime
import requests
import time


OWM_API_ENDPOINT = 'https://api.openweathermap.org/data/2.5/weather?id=%1&APPID=%2'


def weather_icon(weather) -> str:
    sunrise = weather['sys']['sunrise']
    sunset = weather['sys']['sunset']
    timestamp = time.time()
    night = False

    if timestamp < sunrise or timestamp >= sunset:
        night = True

    condition = weather['weather'][0]['id']

    if 200 <= condition < 300:
        # Thunderstorm
        if condition <= 201:
            return '\uf01d'
        return '\uf01e'
    elif 300 <= condition < 400:
        # Drizzle
        if not night:
            return '\uf0b2'
        return '\uf0b3'

    # Rain
    elif 500 <= condition < 510:
        if condition == 500:
            return '\uf0b5'
        if condition == 501:
            return '\uf015'
        return '\uf019'
    elif condition == 511:
        return '\uf017'
    elif 520 <= condition < 600:
        return '\uf01a'

    # Snow
    elif 600 <= condition < 700:
        return '\uf01b'

    # Mist
    elif condition == 701:
        return '\uf014'

    # Clear
    elif condition == 800:
        return '\uf00d' if not night else '\uf02e'

    # Cloudy
    elif condition > 800:
        if condition < 803:
            return '\uf002' if not night else '\uf086'
        else:
            return '\uf013'

    return '\uf07b'


def print_weather(weather, units):
    temp_unit = ' K'

    if units == 'metric':
        temp_unit = '°C'
    elif units == 'imperial':
        temp_unit = '°F'

    sunrise = datetime.fromtimestamp(weather['sys']['sunrise'])
    sunset = datetime.fromtimestamp(weather['sys']['sunset'])

    sunrise = '%sh%s' % (sunrise.hour, sunrise.minute if sunrise.minute > 9 else '0%d' % sunset.minute)
    sunset = '%sh%s' % (sunset.hour, sunset.minute if sunset.minute > 9 else '0%d' % sunset.minute)

    description = str(weather['weather'][0]['description'])
    description = description[0].upper() + description[1:]

    print('${color orange}' + font_weather_icon(weather_icon(weather), size=80) + '$color')
    print('${voffset -80}${offset 170}%s' % description)
    print('${offset 170}Temp. : %d%s' % (weather['main']['temp'], temp_unit))
    print('${offset 170}Hum. : %d%%' % weather['main']['humidity'])
    print('${offset 170}%s${font CantarellRegular:size=10} %s$font' % (font_weather_icon('\uf051', size=10), sunrise), end='')
    print('${offset 50}%s${font CantarellRegular:size=10} %s$font' % (font_weather_icon('\uf052', size=10), sunset), end='\n\n')

    now = time.strftime('%Hh%M')
    print('$alignr${font CantarellRegular:size=8}Dernière mise à jour à %s$font' % now)


def font_weather_icon(text, size=12):
    return '${font WeatherIcons:size=%d}%s$font' % (size, text)


def get_arguments():
    example_config = {'key': '<your API key>', 'language': 'en', 'city': 2643743, 'units': 'metrics'}

    argparser = argparse.ArgumentParser(description='Get the weather from OpenWeatherMap and write it in the Conky format on the standard output', epilog='Example of JSON configuration: ' + json.dumps(example_config))
    argparser.add_argument('--config', type=str, required=True, help='Configuration file of the script')

    return argparser.parse_args()


def main():
    args = get_arguments()
    config = None

    with open(args.config, 'r') as f:
        config = json.loads(f.read())
        if 'token' not in config or 'city' not in config:
            print('The configuration file must contain at least the "token" and "city" parameter.')
            exit(1)

    city_id = config['city']
    token = config['token']
    units = config['units'] if 'units' in config else None
    lang = config['language'] if 'language' in config else None

    endpoint = OWM_API_ENDPOINT.replace('%1', city_id).replace('%2', token)

    if units is not None:
        endpoint += '&units=' + units
    if lang is not None:
        endpoint += '&lang=' + lang

    response = requests.get(endpoint)

    if response.status_code != 200:
        print("Could not fetch the weather details.")
        print("OpenWeatherMap said: " + response.text)
        exit(3)

    try:
        weather = response.json()
        print_weather(weather, units)
    except ValueError:
        print("Something went wrong :(")
        exit(3)

    exit(0)


if __name__ == '__main__':
    main()
