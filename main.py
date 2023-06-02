# @custom:dev-run-script SensorContract

import serial  # Seri iletişim için serial kütüphanesini dahil edin
import time  # Zaman fonksiyonları için time kütüphanesini dahil edin
from web3 import Web3  # Ethereum iletişimi için Web3 kütüphanesini dahil edin
from web3.auto import w3

# w3 nesnesi otomatik olarak yerel Remix Web3 sağlayıcısıyla oluşturulur.


# Seri port yapılandırması
# Arduino'nun bağlı olduğu seri portu ve baud hızını ayarlar
# arduino_port = "/dev/ttyACM0"  # Linux
arduino_port = "COM3"  # Windows
baud_rate = 9600

# Seri bağlantıyı başlat
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # Arduino'nun bağlantıya hazır olması için bekle


# Ethereum node bağlantısı
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

# Akıllı sözleşme adresi ve ABI
contract_address = ''
#contract_address = Web3.toChecksumAddress('')
contract_abi = [
	{
		"inputs": [
			{
				"internalType": "address payable",
				"name": "_transporter",
				"type": "address"
			},
			{
				"internalType": "address payable",
				"name": "_owner",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [],
		"name": "humidity",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "isContractActive",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "isPaymentMade",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "lastVibrationTime",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address payable",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "paymentAmount",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "pressure",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_temperature",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_humidity",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_pressure",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_vibration",
				"type": "uint256"
			}
		],
		"name": "setSensorValues",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "temperature",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "transporter",
		"outputs": [
			{
				"internalType": "address payable",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "vibration",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
# Akıllı sözleşme nesnesi
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

while True:
    # Seri porttan gelen veriyi okuyup ve ayrıştırır
    data = ser.readline().decode().strip()
    print("Arduino'dan gelen veri:", data)

    values = data.split('\n')
    temperature = None
    humidity = None
    pressure = None
    vibration = None
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

    # Sensör verilerini akıllı sözleşmeye gönder
    if temperature is not None and humidity is not None and pressure is not None and vibration is not None:
        print(temperature, humidity, pressure, vibration)
        tx_hash = contract.functions.setSensorValues(
            int(temperature),
            int(humidity),
            int(pressure),
            int(vibration)
        ).transact({'from': w3.eth.accounts[0]})
        print("İşlem hash'i:", tx_hash.hex())

    time.sleep(2)
   # print(
    #    f"Data sent to the smart contract: {temperature} *C, {humidity} %, {pressure} hPa, {vibration}"
    #)  # Veri gönderildiğinde bilgi yazdır



