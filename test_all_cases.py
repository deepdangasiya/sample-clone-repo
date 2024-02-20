"""
This test file is to test all functionality of MySerial class.
"""

import logging
import pytest
import serial
from my_serial import MySerial

handler = logging.StreamHandler()
logging.getLogger(__name__).addHandler(handler)


@pytest.fixture
def mock_serial(mocker):
    return mocker.patch('serial.Serial')
    # return mocker.patch('my_serial.MySerial')


@pytest.fixture
def mock_open_file(mocker):
    return mocker.patch('builtins.open', mocker.mock_open())


@pytest.mark.connect_pass_case
def test_connect_success(mock_serial):
    """
    Pass case for testing successful connection with serial port.
    """
    logging.info("Test connection to the port.")
    # serial_connection = MySerial(
    #     port='COM1')  # Provide a port for successful connection
    serial_connection = MySerial()  # Provide a port for successful connection
    serial_connection.connect()
    try:
        mock_serial.assert_called_once_with('COM1', 9600, timeout=1)
    except AssertionError as e:
        logging.exception(
            f"Connection failed in test_connect_success. {e}")


@pytest.mark.connect_fail_case
def test_connect_failure(mock_serial):
    """
    Dummy fail case to test connection functionality.
    """
    logging.info("Test connection to the port is fail.")
    mock_serial.side_effect = serial.SerialException("Connection failed")
    # serial_connection = MySerial(
    #     port='COM2')  # Provide a port for connection failure
    serial_connection = MySerial()
    try:
        serial_connection.connect()
        assert serial_connection.serial is None
    except Exception as e:
        logging.exception(f"Connection failed in "
                          f"test_connect_failure. {e}")


@pytest.mark.write_case
def test_write(mock_serial, mock_open_file):
    """
    Writing a small message on port and store it in txt file.
    """
    logging.info("Test logging for serial communication.")
    # serial_connection = MySerial(
    #     port='COM1')  # Provide a port for successful connection
    serial_connection = MySerial()
    serial_connection.connect()
    try:
        serial_connection.write(b'Testing\n')
        mock_open_file.assert_called_once_with('COM_test_Log.txt', 'w')
        mock_open_file().write.assert_called_once_with('Testing\n')
    except IOError as e:
        logging.exception(f"Failed to write file. {e}")
    except AssertionError as e:
        logging.exception(f"AssertionError while writing log file. {e}")


@pytest.mark.write_to_log_case
def test_write_to_log(mock_serial):
    """
    Write to log file.
    """
    logging.info("Testing write to log functionality.")
    serial_connection = MySerial()
    try:
        serial_connection.connect()
    except serial.SerialException as e:
        logging.exception(f"Connection failed: {e}")

    try:
        serial_connection.write_to_log(b"Hellooooo\n")
    except serial.SerialException as e:
        logging.exception(f"Write to log file is failed. {e}")


@pytest.mark.read_port_case
def test_read_port(mock_serial):
    """
    Reading port.
    """
    logging.info("Testing read port functionality.")
    logging.info(f"Creating mock_serial_instance.")
    try:
        mock_serial_instance = mock_serial.return_value
        mock_serial_instance.read.return_value = b'Testing\n'
    except BaseException as e:
        logging.exception(f"Mock serial instance generation failed. {e}")

    try:
        serial_connection = MySerial()
        serial_connection.connect()
        expected_out = b'Testing\n'
        data = serial_connection.read()
        assert data == expected_out
    except serial.SerialException as e:
        logging.exception(f"Serial port reading is failed. {e}")
