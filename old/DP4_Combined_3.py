import numpy as np
import requests, json


## conventions used:
##      temperature in degrees C, time in minutes
##      dataset = [[temperature data], [time data]]
##      points/walks = [temperature, time]



## function takes 1 input:
##      the current dataset, a list of two lists, [[temperature data], [time data]]
## returns a two item list:
##      [current temperature, calculated time]
##      can be used as the point for the updateData function

def calcTempTime(dataset):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

    ## GPS DATA HERE
    LAT = str(43.2557) 
    LON = str(79.8711)
    
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
        time = round(model(temp))
        return [temp, time]
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




