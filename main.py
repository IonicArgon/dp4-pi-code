from gps import GPS
from api import API
import time

gps = GPS('/dev/ttyS0', 
          115200,
          (43.2617, -79.9228)
)
api = API(
    'https://api.openweathermap.org/data/2.5/weather?',
    'a09d563977b5ea798f5af4b95f48231f',
    [
        [-10, 0, 10, 20, 25],
        [60, 55, 45, 30, 20]
    ]
)

if __name__ == '__main__':
    print("configure gps")
    status = gps.send_AT('AT+CGPS=0', 'OK', 1)
    status = gps.send_AT('AT+CGPS=1,1', 'OK', 1)
    status = gps.send_AT('AT+CGPS?', 'OK', 1)
    time.sleep(2)
    
    while True:
        status = gps.send_AT('AT+CGPSINFO', '+CGPSINFO: ', 1)
        location = gps.get_lat_long()
        print(location)
        
        api.set_lat_long(location)
        api.scrape()
        print(api.get_temp_time())
        time.sleep(1)
