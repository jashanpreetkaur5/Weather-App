# -------------------------------
# ---Jashanpreet Kaur C0873872----
# -------------------------------
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime, timezone, timedelta
import requests
from PIL import ImageTk, Image
import configparser
import time

# Set up GUI layout
# -----------------------------------------------
root = Tk()
root.title("Weather App")
root.geometry('670x350+250+150')
root.configure(bg="#0E71DA")
root.resizable(False, False)

# icon-------------------------------------------
image_icon = PhotoImage(file="images/clouds.png")
root.iconphoto(False, image_icon)
# ------------------------------------------------
# Load configuration from file---------------
config = configparser.ConfigParser()
config.read('config.yaml')
apiKey = config.get('config', 'apiKey')
city = config.get('config', 'city')
timezone_offset = 0
first = True
load = False
time_counter = 0
previous_time = datetime.now(timezone.utc)
total_seconds = 0
# ------------------------------------------------------------------
# clock function-------------------------------------------------


def getTime():
    global timezone_offset, previous_time, load, total_seconds
    root.after(10, getTime)
    current_time = datetime.now(timezone.utc) + \
        timedelta(seconds=timezone_offset)
    if (load):
        previous_time = current_time
        load = False
    clock.config(text=current_time.strftime("%I:%M:%S"))

    total_seconds = (current_time-previous_time).total_seconds()
    ref.config(text=f"Refresh Time: {round(total_seconds)} seconds")
    if (int(total_seconds) >= int(config.get('config', 'interval'))):
        previous_time = current_time
        getWeather()
# -----------------------------------------------------------------------
# Function for fetching weather data-----------------------------------


def getWeather():
    try:
        print('Fetching weather data')
        global timezone_offset, load
        city = textfield.get()

        obj = TimezoneFinder()
        name.config()
        # weather

        api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}&units=metric"
        json_data = requests.get(api).json()
        condition = json_data['weather'][0]['main']
        # Access the 'coord' data
        coord_data = json_data["coord"]
        lon = coord_data["lon"]
        lati = coord_data["lat"]
        result = obj.timezone_at(lng=lon, lat=lati)

        timeZone.config(text=result)
        long_lat.config(text=f"{round(lati,4)}°N,{round(lon,4)}°E")
        # Get the current time in the specified city
        timezone_offset = json_data['timezone']
        description = json_data['weather'][0]['description']
        temp = json_data['main']['temp']
        Fehrenheit = (temp * 1.8) + 32
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']
        temp_lable.config(
            text=(round(temp), "°C", "|", round(Fehrenheit), "°F"))
        feelslable.config(
            text=(condition, "|", "Feels", "Like", round(temp), "°"))
        windlable.config(text=(wind, "m/s"))
        humidityLable.config(text=(humidity, "%"))
        descriplable.config(text=description)
        pressure_lable.config(text=(pressure, "hPa"))

        icon_url = 'http://openweathermap.org/img/wn/{}.png'.format(
            json_data['weather'][0]['icon'])

        # display the weather icon------------------------
        icon_image = Image.open(requests.get(icon_url, stream=True).raw)
        icon_image = icon_image.resize((100, 100), Image.ANTIALIAS)
        icon_photo = ImageTk.PhotoImage(icon_image)
        weather_icon_label.configure(image=icon_photo)
        weather_icon_label.image = icon_photo
    except Exception as e:
        messagebox.showerror("Weather App", "Please Type Correct City Name!")
    finally:
        load = True
        ref.config(text="Refreshed...")
# -------------------------------------------------------------------------


# Weather Data labels-------------------------------------
label1 = Label(root, text="Pressure", font=(
    'Helvetica', 12), fg="white", bg="#0E71DA")
label1.place(x=50, y=247)
label2 = Label(root, text="Humidity", font=(
    'Helvetica', 12), fg="white", bg="#0E71DA")
label2.place(x=50, y=225)
label4 = Label(root, text="Wind Speed", font=(
    'Helvetica', 12), fg="white", bg="#0E71DA")
label4.place(x=50, y=180)
label5 = Label(root, text="Description", font=(
    'Helvetica', 12), fg="white", bg="#0E71DA")
label5.place(x=50, y=203)
windlable = Label(root, font=("Helvetica", 12),
                  fg="white", bg="#0E71DA")
windlable.place(x=160, y=180)
descriplable = Label(root, font=("Helvetica", 12),
                     fg="white", bg="#0E71DA")
descriplable.place(x=160, y=203)

humidityLable = Label(root, font=("Helvetica", 12),
                      fg="white", bg="#0E71DA")
humidityLable.place(x=160, y=225)

pressure_lable = Label(root, font=(
    "Helvetica", 12), fg="white", bg="#0E71DA")
pressure_lable.place(x=160, y=250)


# search box elements------------------------------------------------------
Search_image = PhotoImage(file="images/button.png")
myimage = Label(image=Search_image, bg="#0E71DA")
myimage.place(x=70, y=10)

textfield = tk.Entry(root, justify="center", width=15, font=(
    "poppins", 25), bg="#203243", border=0, fg="white", insertbackground="white")
textfield.insert(END, city)
textfield.place(x=140, y=20)
textfield.focus()

Search_icon = PhotoImage(file="images/search.png")
myimage_icon = Button(image=Search_icon, borderwidth=0,
                      cursor="hand2", bg="#203243", command=getWeather)
myimage_icon.place(x=490, y=18)

# timezone gui elements----------------------------------------------------------
name = Label(root, font=("Helvetica", 15), bg="#0E71DA")
name.place(x=150, y=200)

timeZone = Label(root, font=("Helvetica", 20), fg="white", bg="#0E71DA")
timeZone.place(x=200, y=100)

temp_lable = Label(root, font=("Helvetica", 20),
                   fg="white", bg="#0E71DA")
temp_lable.place(x=415, y=100)

long_lat = Label(root, font=("Helvetica", 10), fg="white", bg="#0E71DA")
long_lat.place(x=270, y=130)

weather_icon_label = tk.Label(root, bg="#0E71DA", width=50)
weather_icon_label.place(x=300, y=150)

feelslable = Label(font=("arial", 14), bg="#0E71DA", fg="white")
feelslable.place(x=450, y=175)

clock = Label(root, font=("Helvetica", 30), fg="white", bg="#0E71DA")
clock.place(x=270, y=250)

ref = Label(root, font=("Helvetica", 10), fg="white", bg="#0E71DA")
ref.place(x=270, y=300)

t1 = Label(font=("arial", 70), fg="#ee666d", bg="#0E71DA")
t1.place(x=650, y=150)

frame = Frame(root, width=900, height=10, bg="white")
frame.pack(side=BOTTOM)
getWeather()
root.after(100, getTime)
root.mainloop()
# -------------------------------------------------------------------------------
