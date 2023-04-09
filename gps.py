import serial
import time

# this class is used to get the lat/long from the GPS
# logic written by Mani Nabovati Khormazard
class GPS:
    def __init__(self, p_port, p_baudrate, p_default_lat_long):
        self.__m_port = p_port
        self.__m_baudrate = p_baudrate
        self.__m_serial = serial.Serial(self.__m_port, self.__m_baudrate) # serial object
        self.__m_rx_buffer = ''
        self.__m_lat_long = (0, 0)
        self.__m_default_lat_long = p_default_lat_long

        # clear the serial buffer
        self.__m_serial.flushInput()

    # send an AT command to the GPS
    # function takes in 3 arguments: the AT command, the acknowledgement string, and the timeout
    # the function returns -1 if there is an error or 1 if there is no error
    # it processes GPS data from the SiM7600G-H 4G GSM/GPS hat
    # documentation for the module was found here: https://www.waveshare.com/w/upload/6/6d/SIM7600E-H-4G-HAT-Manual-EN.pdf
    def send_AT(self, p_command, p_ack, p_timeout):
        # clear the data buffer
        self.__m_rx_buffer = ''

        # send the command
        self.__m_serial.write((p_command + '\r\n').encode())
        time.sleep(p_timeout)

        # read the response
        if self.__m_serial.inWaiting():
            time.sleep(0.01)
            self.__m_rx_buffer = self.__m_serial.read(self.__m_serial.inWaiting())
        
        # if the response is not empty
        if self.__m_rx_buffer != '':
            # if the response does not include our acknowledgement string
            if p_ack not in self.__m_rx_buffer.decode():
                print(f'An error occured executing command {p_command}')
                return -1
            # otherwise decode the response
            elif '+CGPSINFO: ' in self.__m_rx_buffer.decode():
                gps_data = str(self.__m_rx_buffer.decode())[13:]
                
                # if the response returns a bunch of commas, then there is no GPS lock or the antenna is not connected
                if ",,,,,,,," in self.__m_rx_buffer.decode():
                    print('No GPS lock or antenna is not connected.')
                    print('Using default lat/long.')
                    self.__m_lat_long = self.__m_default_lat_long
                    return -1
                
                # otherwise, calculate the lat/long (GPS returns the data in degrees and minutes)
                lat_deg = gps_data[:2]
                lat_min = gps_data[2:11]
                lat_dir = gps_data[12]
                
                long_deg = gps_data[14:17]
                long_min = gps_data[17:26]
                long_dir = gps_data[27]

                lat = float(lat_deg) + (float(lat_min) / 60)
                lon = float(long_deg) + (float(long_min) / 60)

                if lat_dir == 'S':
                    lat = -lat
                if long_dir == 'W':
                    lon = -lon

                self.__m_lat_long = (lat, lon)
                return 1
            else:
                return 1
        else:
            return -1
        
    def get_lat_long(self):
        return self.__m_lat_long
    


