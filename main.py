import os
import configparser
from datetime import datetime, timedelta
from PIL import Image, ImageFont, ImageDraw
import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_ILI9341 as TFT
from pyowm import OWM

# Config file
configObj = configparser.ConfigParser()
configObj.read("/home/pi/weather-report/configfile.ini")
OWMAPI = configObj["OWM_API"]
UserLoc = configObj["Location"]

api = OWMAPI["api"]
lat = float(UserLoc["latitude"])
lon = float(UserLoc["longitude"])
city = str(UserLoc["city"])
country = str(UserLoc["country"])

# Initialize the TFT display
DC = 24
RST = 25
SPI_PORT = 0
SPI_DEVICE = 0

display = TFT.ILI9341(dc=DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Clear the display
display.begin()
display.clear()

# Load fonts
RESOURCES = "/home/pi/weather-report/resources/"
PIXEL_FONT = ImageFont.truetype(RESOURCES + "fonts/Pixel12x10.ttf", 12)
Terminal_FONT = ImageFont.truetype(RESOURCES + "fonts/terminal-grotesque.ttf", 16)
Mister_Pixel_FONT = ImageFont.truetype(RESOURCES + "fonts/Mister_Pixel_Regular.otf", 18)
B_FONT = ImageFont.truetype(RESOURCES + "fonts/04B_03.ttf", 16)
VG5000_FONT = ImageFont.truetype(RESOURCES + "fonts/VG5000-Regular.otf", 24)
FT88Reg_FONT = ImageFont.truetype(RESOURCES + "fonts/FT88-Regular.otf", 20)

# Create image and drawing object
img = Image.new('RGB', (480, 320), color=(0, 0, 0))
draw = ImageDraw.Draw(img)

# OpenWeatherMap Integration
owm = OWM(api)
mgr = owm.weather_manager()
weather = mgr.weather_at_place(city+","+country).weather
one_call = mgr.one_call(lat, lon)

# Weather data
curTemp = int(weather.temperature("fahrenheit")["temp"])
feelsLike = int(weather.temperature("fahrenheit")["feels_like"])
maxTemp = int(weather.temperature("fahrenheit")["temp_max"])
minTemp = int(weather.temperature("fahrenheit")["temp_min"])
curWind = int(weather.wind(unit="miles_hour")["speed"])

# Forecast data
TwoHrTemp = str(int(one_call.forecast_hourly[2].temperature("fahrenheit").get("temp", 0)))
TwoHrCond = str(one_call.forecast_hourly[2].status)
FourHrTemp = str(int(one_call.forecast_hourly[4].temperature("fahrenheit").get("temp", 0)))
FourHrCond = str(one_call.forecast_hourly[4].status)
SixHrTemp = str(int(one_call.forecast_hourly[6].temperature("fahrenheit").get("temp", 0)))
SixHrCond = str(one_call.forecast_hourly[6].status)
EightHrTemp = str(int(one_call.forecast_hourly[8].temperature("fahrenheit").get("temp", 0)))
EightHrCond = str(one_call.forecast_hourly[8].status)

# Draw text and data on image
draw.text((10, 10), "WEATHER REPORT", font=VG5000_FONT, fill=(255, 255, 255))

# Current temperature
draw.text((10, 50), f"Current Temp: {curTemp}°F", font=VG5000_FONT, fill=(255, 255, 255))
draw.text((10, 90), f"Feels Like: {feelsLike}°F", font=VG5000_FONT, fill=(255, 255, 255))
draw.text((10, 130), f"Max Temp: {maxTemp}°F", font=VG5000_FONT, fill=(255, 255, 255))
draw.text((10, 170), f"Min Temp: {minTemp}°F", font=VG5000_FONT, fill=(255, 255, 255))
draw.text((10, 210), f"Wind Speed: {curWind} MPH", font=VG5000_FONT, fill=(255, 255, 255))

# Hourly forecast
draw.text((10, 250), f"2h: {TwoHrTemp}°F, {TwoHrCond}", font=FT88Reg_FONT, fill=(255, 255, 255))
draw.text((10, 270), f"4h: {FourHrTemp}°F, {FourHrCond}", font=FT88Reg_FONT, fill=(255, 255, 255))
draw.text((10, 290), f"6h: {SixHrTemp}°F, {SixHrCond}", font=FT88Reg_FONT, fill=(255, 255, 255))
draw.text((10, 310), f"8h: {EightHrTemp}°F, {EightHrCond}", font=FT88Reg_FONT, fill=(255, 255, 255))

# Display the image
display.display(img)
