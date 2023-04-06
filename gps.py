import serial
import time

class GPS:
    def __init__(self, p_port, p_baudrate):
        # setup variables
        self.__m_port = p_port
        self.__m_baudrate = p_baudrate
        self.__m_serial = serial.Serial(self.__m_port, self.__m_baudrate)
        self.__m_rx_buffer = ''
        self.__m_lat_long = (0, 0)

        # setup serial
        self.__m_serial.flushInput()

    def send_AT(self, p_command, p_ack, p_timeout):
        self.__m_rx_buffer = ''
        self.__m_serial.write((p_command + '\r\n').encode())
        time.sleep(p_timeout)

        if self.__m_serial.inWaiting():
            time.sleep(0.01)
            self.__m_rx_buffer = self.__m_serial.read(self.__m_serial.inWaiting())
        
        if self.__m_rx_buffer != '':
            if p_ack not in self.__m_rx_buffer.decode():
                return -1
            else:
                gps_data = str(self.__m_rx_buffer.decode())[13:]
                lat_deg = gps_data[:2]
                lat_min = gps_data[2:11]
                lat_dir = gps_data[12]

                long_deg = gps_data[14:17]
                long_min = gps_data[17:26]
                long_dir = gps_data[27]

                lat = float(lat_deg) + (float(lat_min) / 60)
                long = float(long_deg) + (float(long_min) / 60)

                if lat_dir == 'S':
                    lat = -lat
                if long_dir == 'W':
                    long = -long

                self.__m_lat_long = (lat, long)
                return 1
        else:
            return -1
        
    def get_lat_long(self):
        return self.__m_lat_long
    


