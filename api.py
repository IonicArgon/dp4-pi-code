import numpy as np
import requests, json

# this class is used to scrape weather data from the openweathermap API
# logic written by Jennifer Francis
class API:
    def __init__(self, p_endpoint, p_api_key, p_initial_dataset):
        self.__m_endpoint = p_endpoint
        self.__m_api_key = p_api_key
        self.__m_lat = 0
        self.__m_long = 0
        self.__m_dataset = p_initial_dataset
        self.__m_temperature = 0
        self.__m_time = 0

    def set_lat_long(self, p_lat_long):
        self.__m_lat = p_lat_long[0]
        self.__m_long = p_lat_long[1]

    # scrape data from the API
    def scrape(self):
        # determine the url based on the lat/long
        url = self.__m_endpoint + "lat=" + str(self.__m_lat) + "&lon=" + str(self.__m_long) + "&appid=" + self.__m_api_key + "&units=metric"
        
        # get the data from the API using the url and the requests library
        response = requests.get(url)
        if response.status_code == 200: # if the request was successful (HTTP status 200 = OK)
            data = response.json()  # get the data from the response (convert it from JSON to a dictionary)
            main = data['main']    # get the main data from the data (its stored as a dictionary)
            self.__m_temperature = main['feels_like'] # get the temperature from the main data

            # get the time from the temperature using the dataset and a quadratic regression
            model = np.poly1d(np.polyfit(self.__m_dataset[0], self.__m_dataset[1], 2))
            self.__m_time = round(model(self.__m_temperature))
            return 1
        else:
            # if the request was not successful, print an error message
            print("Error in the HTTP request")
            return -1
        
    def get_temp_time(self):
        return (self.__m_temperature, self.__m_time)

    # update the dataset with the new temperature and time
    def update_data(self, p_point):
        self.__m_dataset[0].append(p_point[0])
        self.__m_dataset[1].append(p_point[1])
    