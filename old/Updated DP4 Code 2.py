import numpy as np
import requests, json
import RPi.GPIO as GPIO
import serial
import time

## conventions used:
##      temperature in degrees C, time in minutes
##      dataset = [[temperature data], [time data]]
##      points/walks = [temperature, time]



ser = serial.Serial('/dev/ttyS0',115200)
ser.flushInput()

rec_buff = ''

## Function takes 3 arguments the AT command, acknowledgment (back) and timeout value.
## The function processes the GPS data from the Waveshare SiM7600G-H 4G HAT GSM/GPS module
## The function returns latitude and longitude as well as a binary confirmation code of 0 or 1.
## The code was adapted and modified from: https://core-electronics.com.au/guides/raspberry-pi/raspberry-pi-4g-gps-hat/
def send_at(command,back,timeout):
	rec_buff = ''
	ser.write((command+'\r\n').encode())
	time.sleep(timeout)
	if ser.inWaiting():
		time.sleep(0.01 )
		rec_buff = ser.read(ser.inWaiting())
	if rec_buff != '':
		if back not in rec_buff.decode():
			return 0,0,0
		else:
			
			global GPS
			GPS = str(rec_buff.decode())[13:]
				
			Lat_Deg = GPS[:2]
			Lat_Min = GPS[2:11]
			N_S = GPS[12]
						
			Long_Deg = GPS[14:17]
			Long_Min = GPS[17:26]
			E_W = GPS[27]
			
			Latitude = float(Lat_Deg) + (float(Lat_Min)/60)
			Longitude = float(Long_Deg) + (float(Long_Min)/60)
			
			if  N_S == 'S': Latitude = -Latitude
			if  E_W == 'W': Longitude = -Longitude
						
						
			return Latitude,Longitude,1
	else:
		print('GPS is not ready')
		return 0,0,0




## function takes 1 input:
##      the current dataset, a list of two lists, [[temperature data], [time data]]
## returns a two item list:
##      [current temperature, calculated time]
##      can be used as the point for the updateData function

def calcTempTime(dataset):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

    ## GPS DATA HERE
    send_at('AT+CGPS=1,1','OK',1)
    time.sleep(2)
    answer = send_at('AT+CGPSINFO','+CGPSINFO: ',1)
    
    LAT = str(answer[0])
    print(LAT)
    LON = str(answer[1])
    print(LON)
    
    API_KEY = "a09d563977b5ea798f5af4b95f48231f"
    URL = BASE_URL + "lat=" + LAT + "&lon=" + LON + "&appid=" + API_KEY + "&units=metric"

    ## get current temperature
    response = requests.get(URL) 
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        temp = main['feels_like']

        ## quadratic regression algorithm to predict time
        model = np.poly1d(np.polyfit(dataset[0], dataset[1], 2))
        t = round(model(temp))
        return [temp, t]
    else:
        print("Error in the HTTP request")
        return [0, 0]


## function takes 2 inputs:
##      the current dataset, a list of two lists [[temperature data], [time data]]
##      a new data point, a two item list [temperature, time]
## returns a new dataset:
##      [[updated temperature data], [updated time data]]
##      can be used as the new dataset for the calcTempTime() function

def updateData(dataset, point):
    tempList = dataset[0]
    tempList.append(point[0])
    timeList = dataset[1]
    timeList.append(point[1])
    return [tempList, timeList]

## data stored in a two item list [[temperature list], [time list]]
data = [[-10, 0, 10, 20, 25], [60, 55, 45, 30, 20]]
## new data points in format [temperature, time]
walk1 = [-5, 55]

data = updateData(data, walk1)
print(calcTempTime(data))

walk2 = [15, 30] ## adding a new point not on current prediction

data = updateData(data, walk2)
print(calcTempTime(data))




