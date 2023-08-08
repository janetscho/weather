import io
import requests
import datetime
import pytz
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import calendar
from collections import defaultdict
import numpy as np

api = 'ca1ae4256fbd6a8644510160cf40fb39'

def main():
    
    # creating starting page / UI
    layout_column = [
        [sg.Text('Search by city', justification = 'center', font = ('Helvetica', 14))],
        [sg.Input(key = '-INPUT-', size = (30, 30))],
        [sg.Button('Enter', bind_return_key = True, size = (10, 1))]
    ]
    
    title = [
        [sg.Text("WEATHER APP",justification = 'center', font = ('Helvetica', 20))]
        ]
    
    layout = [[sg.Push()],
              [sg.Push(), sg.Column(title, element_justification = 'center', pad = (20, 10)), sg.Push()],
              [sg.Text('' * 40)],
              [sg.Push(), sg.Column(layout_column, element_justification = 'center'), sg.Push()],
              [sg.VPush()]]
    
    window = sg.Window('Weather App', layout)
    
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        
        # if location is provided
        if event == 'Enter':
            location = values['-INPUT-']
            window['-INPUT-'].update('')
            
            # calling API request
            url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api}&units=imperial'

            res = requests.get(url)
            data = res.json()
            
            # main weather information
            humidity = data['main']['humidity']
            wind = data['wind']['speed']
            description = data['weather'][0]['description']
            temp = data['main']['temp']
            like = data['main']['feels_like']
            # icon_code1 = data['weather'][0]['icon']
            # icon_url1 = f'https://openweathermap.org/img/wn/{icon_code1}@2x.png'
            
            forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api}&units=imperial'
            res = requests.get(forecast_url)
            data = res.json()
            
            # checks if date is already in the dictionary since forecast returns the weather every 3 hours
            check_date = {}
            for day in data['list']:
                # first time the date appears
                date = day['dt_txt'].split()[0]
                
                if date not in check_date:
                    check_date[date] = day
                    
            daily_weather = [
                [sg.Text("Daily Weather Forcast", font = ('Helvetica', 16))],
            ]
                    
            # Daily weather
            curr_dates = []
            temperatures = []
            day_of_week_counts = defaultdict(int)
            for day in check_date.values():
                # Extracting date and time
                dt_txt = day['dt_txt']
                date_obj = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
                
                # Getting day of the week (Monday, Tuesday, etc.)
                day_of_week = date_obj.strftime("%A")
                
                # Update day of the week count
                day_of_week_counts[day_of_week] += 1

                # Extracting the date without the year
                date = dt_txt.split()[0]
                date = '-'.join(date.split('-')[1:])

                temp = day['main']['temp']
                info = day['weather'][0]['description']
                # icon_code2 = day['weather'][0]['icon']
                # icon_url2 = f'https://openweathermap.org/img/wn/{icon_code2}@2x.png'
                

                daily_weather.append([
                    sg.Text(day_of_week, font=("Helvetica", 14), size=(11, 1), justification='left'),
                    sg.Text(f"{calendar.month_abbr[int(date.split('-')[0])]} {date.split('-')[1]}", font=("Helvetica", 14), size=(8, 1), justification='left'),
                    sg.Text(temp, font=("Helvetica", 14), size=(6, 1), justification='left'),
                    sg.Text(info.title(), font=("Helvetica", 14), size=(15, 1), justification='left'), 
                ])

                
                # for line graph
                curr_dates.append(date)
                temperatures.append(float(temp))

            def create_graph(curr, temps):    
                plt.figure(figsize=(4, 3))  # Set a larger figure size for better visibility
                
                # Plot the data with blue line and red dots
                plt.plot(curr, temps, color='red', marker='o', linestyle='-', linewidth=2, markersize=8, label='Temperature')
                
                # Add temperature values above each data point
                for date, temp in zip(curr, temps):
                    plt.text(date, temp + 1, f'{temp:.1f}', ha='center', va='bottom', fontsize=10)

                # Fill the area under the curve with light blue
                plt.fill_between(curr, temps, color='lightblue', alpha=0.5)
                
                plt.xlabel('Dates')
                plt.ylabel('Temperatures (F)')
                
                # Add faint dashed gridlines for x-axis
                plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7, axis='x')
                
                y_min = min(temps) - 10 
                y_max = max(temps) + 10
                
                # Set y-axis limits
                plt.ylim(y_min, y_max)
                
                # Create custom y-axis ticks every ten degrees
                y_ticks = np.arange(np.floor(y_min / 5) * 5, np.ceil(y_max / 5) * 5 + 1, 5)                
                plt.yticks(y_ticks)

                plt.tight_layout()
                
                return plt.gcf()

            def draw_fig(canvas, figure):
                fig = FigureCanvasTkAgg(figure, canvas)
                fig.draw()
                fig.get_tk_widget().pack(side='top', fill='both', expand=1)
                return fig

            
            figure_layout = [
                [sg.Canvas(key= '-CANVAS-')],
            ]
            
            # to do a new location
            restart_layout = [
                [sg.Button('New location', size = (10, 1))]
            ]
            
            # finds actual timezone for the location
            geolocator = Nominatim(user_agent='yessir')
            geo_location = geolocator.geocode(location)
            time_obj = TimezoneFinder()
            location_result = time_obj.timezone_at(lng = geo_location.longitude, lat = geo_location.latitude)
            IST = pytz.timezone(location_result)
            location_time = datetime.now(IST)
            
            # UI
            title2 = [
                [sg.Text(location, justification = 'center', font = ('Helvetica', 20))],
                [sg.Text(location_time.strftime('%Y-%m-%d %H:%M:%S'), justification= 'center', font = ('Helvetica', 12))]
            ]

            layout_column2 = [
                [sg.Text(f'Temperature: {temp} F', font = ('Helvetica', 20))],
                [sg.Text(f'Feels like {like} F', font = ('Helvetica', 20))],
                [sg.Text(f'Humidity: {humidity}%', font = ('Helvetica', 12))],
                [sg.Text(f'Wind: {wind} mph', font = ('Helvetica', 12))],
                [sg.Text(f'Description: {description.title()}', font = ('Helvetica', 12))],
            ]
            
            layout2 = [[sg.Push()],
                    [sg.Push(), sg.Column(title2, element_justification = 'center', pad = (20, 10)), sg.Push()],
                    #[sg.Text('' * 40)],
                    [sg.Push(), sg.Column(layout_column2, element_justification = 'center'), sg.Push()],
                    [sg.Text('' * 40)],
                    [sg.Push(), sg.Column(daily_weather, element_justification= 'center'), sg.Push(), sg.Column(figure_layout, element_justification='center'), sg.Push()],
                    [sg.Text('' * 40)],
                    #[sg.Push(), sg.Column(figure_layout, element_justification='center'), sg.Push()],
                    [sg.Push(), sg.Column(restart_layout, element_justification='center'), sg.Push()],
                    [sg.VPush()]]
            
            window.close()

            window2 = sg.Window(title2, layout2, finalize= True, element_justification= 'center')
            draw_fig(window2['-CANVAS-'].TKCanvas, create_graph(curr_dates, temperatures))
            window2.refresh()
            window2.move_to_center()

            while True:
                
                event2, values2 = window2.read()
                
                if event2 == sg.WIN_CLOSED or event2 == 'Exit':
                    break
                
                if event2 == 'New location':
                    window2.close()
                    main()

                
            window2.close()
    
if __name__ == '__main__':
    main()    
    
'''
REFERENCE:
https://stackoverflow.com/questions/61852225/align-button-to-the-center-of-the-window-using-pysimplegui
https://www.instructables.com/Get-Weather-Data-Using-Python-and-Openweather-API/
https://openweathermap.org/current#data
https://openweathermap.org/forecast5#list
https://github.com/jsubroto/5-day-weather-forecast/blob/master/five_day_weather_forecast.py
https://www.youtube.com/watch?v=XpKtgNasiBw
https://github.com/PySimpleGUI/PySimpleGUI/issues/5802
https://www.geeksforgeeks.org/get-current-time-in-different-timezone-using-python/
'''
