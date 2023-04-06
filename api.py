import numpy as np
import requests, json

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

    def scrape(self):
        url = self.__m_endpoint + "lat=" + str(self.__m_lat) + "&lon=" + str(self.__m_long) + "&appid=" + self.__m_api_key + "&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            main = data['main']
            self.__m_temperature = main['feels_like']

            model = np.poly1d(np.polyfit(self.__m_dataset[0], self.__m_dataset[1], 2))
            self.__m_time = round(model(self.__m_temperature))
            return 1
        else:
            print("Error in the HTTP request")
            return -1
        
    def get_temp_time(self):
        return (self.__m_temperature, self.__m_time)

    def update_data(self, p_point):
        self.__m_dataset[0].append(p_point[0])
        self.__m_dataset[1].append(p_point[1])
    