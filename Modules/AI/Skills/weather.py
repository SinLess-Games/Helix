# weather.py
# AI Weather Skill
# Timothy Pierce - 2021Nov23
# based off Kevin McAleer - July 2021

from pyowm import OWM
from geopy import Nominatim
from datetime import datetime


class Weather():

    # The location of where you want to be forecast
    __location = "Pablo, Montana"

    # API Key
    api_key = "5075797ddb7bc699058347fd8c080ef6"

    def __init__(self):
        self.ow = OWM(self.api_key)
        self.mngr = self.ow.weather_manager()
        locator = Nominatim(user_agent="myGeoCoder")
        city = "Pablo"
        state = "Montana"
        country = "United States"
        self.__location = city + ", " + state
        loc = locator.geocode(self.__location)
        self.lat = loc.latitude
        self.long = loc.longitude

    def uv_index(self, uvi: float):
        """ Returns a message depending on the UV Index provided """
        message = ""
        if uvi <= 2.0:
            message = "The Ultraviolet level is low, no protection is required."
        if uvi >= 3.0 and uvi < 6.0:
            message = "The Ultraviolet level is medium, skin protection is required."
        if uvi >= 6.0 and uvi < 8.0:
            message = "The Ultraviolet level is high, skin protection is required."
        if uvi >= 8.0 and uvi < 11.0:
            message = "The Ultraviolet level is very high, extra skin protection is required."
        if uvi >= 11.0:
            message = "The Ultraviolet level is extremely high, caution is advised and extra skin protection is required."
        return message

    @property
    def weather(self):
        forecast = self.mngr.one_call(lat=self.lat, lon=self.long)
        return forecast

    @property
    def forecast(self):
        '''
        Returns forecast at location
        '''

        forecast = self.mngr.one_call(lat=self.lat, lon=self.long)
        detail_status = forecast.forecast_daily[0].detailed_status
        pressure = str(forecast.forecast_daily[0].pressure.get('press'))
        humidity = str(forecast.forecast_daily[0].humidity)
        sunrise = datetime.utcfromtimestamp(forecast.forecast_daily[0].sunrise_time()).strftime("%I:%M:%S")
        sunset = datetime.utcfromtimestamp(forecast.forecast_daily[0].sunset_time()).strftime("%I:%M:%S")
        temperature = str(forecast.forecast_daily[0].temperature('fahrenheit').get('day'))
        uvi = forecast.forecast_daily[0].uvi

        # print('detailed status: ', detail_status)
        # print("humidity ", humidity)
        # print("pressure ", pressure)
        # print("sunrise: ", sunrise)
        # print("Sunset ", sunset)
        # print("temperature", temperature)
        # print("UVI ", uvi)

        message = "Here is the Weather: Today will be mostly " + detail_status \
                  + ", humidity of " + humidity + " percent" \
                  + " and a pressure of " + pressure + " millibars" \
                  + ". The temperature is " + temperature + " degrees " \
                  + ". Sunrise was at " + sunrise \
                  + " and sunset is at " + sunset \
                  + ". " + self.uv_index(uvi)

        # print(message)
        return message


# demo
# myweather = Weather()
# print(myweather.forecast)
