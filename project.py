import PySimpleGUI as sg
import requests

api = 'ca1ae4256fbd6a8644510160cf40fb39'

def main():
    
    layout_column = [
        [sg.Text('Search by city', justification = 'center', font = (30))],
        [sg.Input(key = '-INPUT-', size = (30, 30))],
        [sg.Button('Enter', size = (10, 1))]
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
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        
        if event == 'Enter':
            location = values['-INPUT-']
            window['-INPUT-'].update('')
            
            url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api}&units=imperial'
            
            print(url)

            res = requests.get(url)
            data = res.json()
            
            print(data)
            
            humidity = data['main']['humidity']
            wind = data['wind']['speed']
            description = data['weather'][0]['description']
            temp = data['main']['temp']
            like = data['main']['feels_like']
            
            print(temp)
            
            title2 = [
                [sg.Text(location, justification = 'center', font = (60))]
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
                    [sg.VPush()]]
            
            window.close()

            window2 = sg.Window(title2, layout2)

            while True:
                event2, values2 = window2.read()
                print(event2, values2)
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
'''