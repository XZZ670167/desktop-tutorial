import json
import os
from datetime import datetime

import requests


def get_today_datetime():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def call_sg_api_weather_api_2hr(dtestr):
    api_url = "https://api.data.gov.sg/v1/environment/2-hour-weather-forecast?date_time=" + dtestr
    response = requests.get(api_url)
    json_object = json.loads(response.content.decode("utf-8"))
    return json_object


def telegram_bot_sendtext(message):
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    chat_id = os.environ['TELEGRAM_WEATHER_CHAT_ID']
    url = 'https://api.telegram.org/bot' + str(bot_token) + '/sendMessage'
    response = requests.get(url, params={'chat_id': str(chat_id), 'text': str(message)})
    return response.json()


if __name__ == '__main__':
    weather_data = call_sg_api_weather_api_2hr(get_today_datetime())
    forecasts = weather_data['items'][0]['forecasts']
    area_of_interest = "Jurong East"
    for forecast in forecasts:
        if forecast['area'].lower() == area_of_interest.lower():
            message = "Current weather forecast for " + area_of_interest + " is " + forecast['forecast']
            print(message)
            telegram_bot_sendtext(message)
