import requests
import datetime
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

api = 'ca1ae4256fbd6a8644510160cf40fb39'

def main():
    
    # creating starting page / UI
    layout_column = [
        [sg.Text('Search by city', justification = 'center', font = (30))],
        [sg.Input(key = '-INPUT-', size = (30, 30))],
        [sg.Button('Enter', bind_return_key = True, size = (10, 1))]
    ]
    
    title = [
        [sg.Text("WEATHER APP",justification = 'center', font = (60))]
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
                [sg.Text("Daily Weather Forcast", font = 30)],
            ]
                    
            # secondary portion of weather
            curr_dates = []
            temperatures = []
            for day in check_date.values():
                # removing unnecessary portion of time
                date = day['dt_txt'].split()[0]
                temp = day['main']['temp']
                info = day['weather'][0]['description']
                daily_weather.append([sg.Text(date), sg.Text(temp), sg.Text(info)])
                
                # for line graph
                curr_dates.append(date)
                temperatures.append(float(temp))
                
            print(curr_dates)
            print(temperatures)
            
            def create_graph(curr, temps):    
                plt.plot(curr, temps, color = 'blue', marker = 'o')
                plt.xlabel('Dates')
                plt.ylabel('Temperatures')
                plt.title('Forecast for the next couple days')
                plt.grid(True)
                return plt.gcf()
            
            def draw_fig(canvas, figure):
                fig = FigureCanvasTkAgg(figure, canvas)
                fig.draw()
                fig.get_tk_widget().pack(side= 'top', fill= 'both', expand= 1)
                return fig
            
            figure_layout = [
                [sg.Text('Weather Forecast')],
                [sg.Canvas(key= '-CANVAS-')],
            ]
            
            # UI
            title2 = [
                [sg.Text(location, justification = 'center', font = (60))],
                [sg.Text(datetime.datetime.now().date(), justification= 'center', font = (40))]
            ]

            layout_column2 = [
                [sg.Text(f'Temperature: {temp} F', font = (40))],
                [sg.Text(f'Feels like {like} F', font = (40))],
                [sg.Text(f'Humidity: {humidity}%', font = (40))],
                [sg.Text(f'Wind: {wind} mph', font = (40))],
                [sg.Text(f'Description: {description}', font = (40))],
            ]
            
            layout2 = [[sg.Push()],
                    [sg.Push(), sg.Column(title2, element_justification = 'center', pad = (20, 10)), sg.Push()],
                    [sg.Text('' * 40)],
                    [sg.Push(), sg.Column(layout_column2, element_justification = 'center'), sg.Push()],
                    [sg.Text('' * 40)],
                    [sg.Push(), sg.Column(daily_weather, element_justification= 'center'), sg.Push()],
                    [sg.Text('' * 40)],
                    [sg.Push(), sg.Column(figure_layout, element_justification='center'), sg.Push()],
                    [sg.VPush()]]
            
            window.close()

            window2 = sg.Window(title2, layout2, finalize= True, element_justification= 'center')
            draw_fig(window2['-CANVAS-'].TKCanvas, create_graph(curr_dates, temperatures))

            while True:
                
                event2, values2 = window2.read()
                
                if event2 == sg.WIN_CLOSED or event2 == 'Exit':
                    break

                
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
'''