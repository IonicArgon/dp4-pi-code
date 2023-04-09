from gps import GPS
from api import API
from gui import MainWindow
import time

# creating GPS object
gps = GPS('/dev/ttyS0', # serial port 
          115200,       # baudrate
          (43.2617, -79.9228)   # default lat/long
)

# creating API object
api = API(
    'https://api.openweathermap.org/data/2.5/weather?', # API URL
    'a09d563977b5ea798f5af4b95f48231f', # API key
    [
        [-10, 0, 10, 20, 25], # temp for each time
        [60, 55, 45, 30, 20]  # time for each temp
    ]
)

# creating GUI object
app = MainWindow()

# main
if __name__ == '__main__':
    # configure GPS
    print("configure gps")
    status = gps.send_AT('AT+CGPS=0', 'OK', 1) # turn off GPS
    status = gps.send_AT('AT+CGPS=1,1', 'OK', 1) # turn on GPS
    status = gps.send_AT('AT+CGPS?', 'OK', 1) # check GPS status
    time.sleep(2)

    # get location
    status = gps.send_AT('AT+CGPSINFO', '+CGPSINFO: ', 1) # get GPS data
    location = gps.get_lat_long() # get lat/long
    print(location) 
    
    # get temp
    api.set_lat_long(location) # set lat/long
    api.scrape() # scrape data from weather api
    temp, _time = api.get_temp_time() # get temp and time
    print(temp, _time) 
    app.set_timer(_time) # set timer
    app.mainloop() # start GUI
