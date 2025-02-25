from machine import Pin
from utime import sleep
import dht
import network
import urequests as req

# Sensor Setup
dht_sensor = dht.DHT11(Pin(18))
pir_sensor = Pin(22, Pin.IN)

# Wi-Fi Connection
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect('Aliyyano', '12345678')

print("Menghubungkan ke Wi-Fi", end="")
while not wifi.isconnected():
    print(".", end="")
    sleep(0.5)
print("\nWi-Fi Terhubung!")
print("IP Address:", wifi.ifconfig()[0])

# Ubidots Setup
TOKEN = "BBUS-mMCX79SBkESTigYWtLpbgTQ64OAWio"
DEVICE_ID = "sensor"
UBIDOTS_URL = f"http://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_ID}"
HEADERS = {
    "X-Auth-Token": TOKEN,
    "Content-Type": "application/json"
}

# Flask Server IP (Ganti dengan IP PC Anda)
FLASK_IP = "192.168.1.100"  # Ubah sesuai dengan IP PC Flask
ENDPOINT_URL = f"http://{FLASK_IP}:5001/data"

# Send Data to Ubidots
def send_data_ubidots(temperature, humidity, motion):
    if not wifi.isconnected():
        print("Wi-Fi tidak terhubung! Data tidak dikirim.")
        return

    try:
        payload = {
            "temperature": temperature,
            "humidity": humidity,
            "motion": motion
        }
        response = req.post(UBIDOTS_URL, json=payload, headers=HEADERS)
        print("Ubidots Response:", response.text)
        response.close()
    except Exception as e:
        print("Error saat mengirim data ke Ubidots:", e)

# Send Data to Flask
def send_data_flask(temperature, humidity, motion):
    try:
        payload = {
            "temperature": temperature,
            "humidity": humidity,
            "motion": motion
        }
        response = req.post(ENDPOINT_URL, json=payload, headers={"Content-Type": "application/json"})
        print("Flask Response:", response.text)
        response.close()
    except Exception as e:
        print("Error saat mengirim data ke Flask:", e)

# Main Loop
while True:
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        motion_detected = 1 if pir_sensor.value() else 0

        print(f"Temperature: {temperature}°C | Humidity: {humidity}% | Motion: {motion_detected}")
        send_data_ubidots(temperature, humidity, motion_detected)
        send_data_flask(temperature, humidity, motion_detected)

    except OSError as e:
        print("Error membaca sensor:", e)

    sleep(5)
