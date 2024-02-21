import logging
import serial
import serial.tools.list_ports as pl


class MySerial:
    logging.info("Testing functionality of MySerial class...!!!")

    def __init__(self, baudrate=115200, timeout=1):
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None
        self.log_file = None
        self.log_file_path = "COM_test_Log.txt"

    def find_available_ports(self):
        logging.info("Finding available ports to connect.")
        ser = pl.comports()
        port_list = []
        try:
            for port in ser:
                port_list.append(port.name)
            logging.info(f"Available port list: {port_list}")
        except serial.SerialException:
            pass
        return port_list

    def connect(self, port=None):
        logging.info("Trying to connect to available ports.")
        available_ports = self.find_available_ports()
        if port:
            try:
                self.serial = serial.Serial(port, self.baudrate,
                                            timeout=self.timeout)
                print(f"Connected to port: {port}")
                logging.info(f"Connection successful with port {port}")
            except serial.SerialException as e:
                print(f"Failed to connect to port {port}: {e}")
                logging.exception(f"Failed to connect to port {port}: {e}")
        elif available_ports:
            for port in available_ports:
                try:
                    self.serial = serial.Serial(port, self.baudrate,
                                                timeout=self.timeout)
                    print(f"Connected to port: {port}")
                    logging.info(f"Connection successful with port {port}")
                    break
                except serial.SerialException as e:
                    print(f"Failed to connect to port {port}: {e}")
                    logging.exception(f"Failed to connect to port {port}: {e}")
        else:
            print("No available ports found.")
            logging.warning("No available ports found.")

    def read(self, size=1):
        logging.info("Start Reading on port.")
        if self.serial:
            logging.info("Port read successfully.")
            return self.serial.read(size)
        else:
            print("No connection established.")
            logging.warning("No connection established.")

    def write(self, data):
        logging.info("Start writing on port.")
        if self.serial:
            logging.info("Writing on port.")
            self.serial.write(data)
            logging.info("flush the port after writing.")
            self.serial.flush()
            logging.info("Writing to log file.")
            self.write_to_log(data)
        else:
            print("No connection established.")
            logging.warning("No connection established.")

    def flush(self):
        logging.info("Flush the port.")
        if self.serial:
            logging.info("Flushing the port.")
            self.serial.flush()
        else:
            print("No connection established.")
            logging.warning("No connection established.")

    def write_to_log(self, data):
        logging.info("Writing into log file.")
        try:
            logging.info(f"Writing logs to {self.log_file_path}")
            with open(self.log_file_path, "w") as f:
                logging.info("write file with utf-8 decoding.")
                f.write(data.decode('utf-8'))
        except Exception as e:
            print(f"Error writing to log file: {e}")
            logging.exception(f"Error writing to log file: {e}")

    def close(self):
        logging.info("Closing the COM port connection.")
        if self.serial:
            logging.info("Closing the serial COM connection.")
            self.serial.close()
        if self.log_file:
            logging.info("Closing the file.")
            self.log_file.close()
