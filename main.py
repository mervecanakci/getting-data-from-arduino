import serial
import time
from web3 import Web3

arduino_port = "COM3"  # Arduino'nun bağlı olduğu seri port
baud_rate = 9600

ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)

w3 = Web3(Web3.HTTPProvider('http://localhost:7545')) #ganache de aynı portta

contract_address = '0x5B38Da6a701c568545dCfcB03FcB875f56beddC4'
contract_abi = [
    # Akıllı sözleşme ABI buraya gelecek
]

contract = w3.eth.contract(address=contract_address, abi=contract_abi)


def send_sensor_data(temperature, humidity, pressure, vibration):
    tx_hash = contract.functions.setSensorValues(
        int(temperature),
        int(humidity),
        int(pressure),
        int(vibration)
    ).transact({'from': w3.eth.accounts[0]})
    print("İşlem hash'i:", tx_hash.hex())


while True:
    data = ser.readline().decode().strip()
    print(data)
    values = data.split('\n')
    temperature, humidity, pressure, vibration = None, None, None, None
    for value in values:
        if ':' in value:
            sensor, val = value.split(':')
            sensor = sensor.strip()
            val = val.strip()
            if sensor == 'temperature':
                temperature = float(val)
            elif sensor == 'humidity':
                humidity = float(val)
            elif sensor == 'pressure':
                pressure = float(val)
            elif sensor == 'vibration':
                vibration = float(val)

    if temperature is not None and humidity is not None and pressure is not None and vibration is not None:
        print("Ölçüm Değerleri:")
        print(f"Sıcaklık: {temperature} derece")
        print(f"Nem: {humidity}%")
        print(f"Basınç: {pressure} Pascal")
        print(f"Titreşim: {vibration} birim")

        send_sensor_data(temperature, humidity, pressure, vibration)

    time.sleep(2)
