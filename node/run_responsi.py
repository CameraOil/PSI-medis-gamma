import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711
import minimalmodbus
import serial, csv
import os

# node import
# from dotenv import load_dotenv
import core as node
import json


referenceUnit = -411
RELAY_PIN = 17  # GPIO17 (Pin 11)
json_filename = 'config.json'
cal_urine = 203
t1_urine = (1023 - cal_urine)//3
t2_urine = (1023 - cal_urine) * 2 // 3
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

# PHOTODIODE & TGS (modbus)
instrument = minimalmodbus.Instrument('/dev/rs485_adapter', 1)  # Adj>instrument.serial.baudrate = 9600
instrument.serial.timeout = 1
instrument.serial.bytesize = 8
instrument.serial.parity = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.mode = minimalmodbus.MODE_RTU
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True

# Good practice to clean up before and after each execution
#instrument.clear_buffers_before_each_transaction = True
#instrument.close_port_after_each_call = True

# DISTANCE
TRIG = 13
ECHO = 19

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def read_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    duration = pulse_end - pulse_start
    distance_cm = duration * 17150
    return round(distance_cm, 2)

# TEMPERATURE
base_dir = '/sys/bus/w1/devices/'
device_folder = [d for d in os.listdir(base_dir) if d.startswith('28-')][0]
device_file = base_dir + device_folder + '/w1_slave'

def read_temp():
    with open(device_file, 'r') as f:
        lines = f.readlines()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        with open(device_file, 'r') as f:
            lines = f.readlines()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return round(temp_c, 2)

# LOAD CELL
hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()

def read_weight():
    return round(hx.get_weight(5), 2)

# Json setup
def write_json(json_filename, kvp: dict):
        with open(json_filename, mode='w+', newline='') as file:
                json.dump(kvp, file, indent=4)

# Node setup
# load_dotenv()
# SERVER = os.getenv('BASE_URL')  # no trailing slash
# EMAIL = os.getenv('EMAIL')
# PASSWORD = os.getenv('PASSWORD')
NODE_ID = 1  # <-- ID of this node in the database
token = node.get_token()

try:
    data = {"temperature": None,
            "alcohol": 1,
            "urine" : 1,
            "berat": None,
            "tinggi": None
            }

    success = [0,0,0,0,0]
    GPIO.output(RELAY_PIN, GPIO.HIGH)

    while token:
        write_json(json_filename, data)

        node_info = node.get_node_info(token)


        if not node_info:
            break

        status = node_info.get("status")
        patient_id = node_info.get("assigned_patient")

        if status == "assigned" and patient_id:
            node.busy_node_status(token)
            print(f"[INFO] Assigned patient {patient_id}. Starting reading...")

            GPIO.output(RELAY_PIN, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(RELAY_PIN, GPIO.LOW)
            time.sleep(3)
            GPIO.output(RELAY_PIN, GPIO.HIGH)

            #success[0] = node.send_reading(token, NODE_ID)
            #success[1] = node.send_reading(token, NODE_ID)

            # Urine
            light = instrument.read_register(0, 0)
            if light >= t2_urine:
                urine = 0
            elif  light >= t1_urine and light < t2_urine:
                urine = 1
            else:
                urine = 2
            data["urine"] = urine
            write_json(json_filename,data)
            success[0] = node.send_reading(token, NODE_ID)
            #time.sleep(2)

            #Alcohol
            if success[0] == True:
                gas = instrument.read_register(1, 0)
                data["alcohol"] = gas
                write_json(json_filename,data)
                success[1] = node.send_reading(token, NODE_ID)
            #time.sleep(2)

            # temperature
            if success[1] == True:
                temp = read_temp()
                data["temperature"] = temp
                write_json(json_filename,data)
                success[2] = node.send_reading(token, NODE_ID)
            #time.sleep(2)

            # berat
            if success[2] == True:
                berat = read_weight()
                data["berat"] = berat
                write_json(json_filename,data)
                success[3] = node.send_reading(token, NODE_ID)
            #time.sleep(2)

            # tinggi
            if success[3] == True:
                tinggi = read_distance()
                data["tinggi"] = tinggi
                write_json(json_filename,data)
                success[4] = node.send_reading(token, NODE_ID)
            #time.sleep(2)

            if success[4] == True:
                #time.sleep(5)
                node.set_node_status(token, "available")
            # reset data to None
                data = {"temperature": None,
                "alcohol": 1,
                "urine" : 1,
                "berat": None,
                "tinggi": None
                }
                sensor = [0,0,0,0,0]

            #GPIO.output(RELAY_PIN, GPIO.HIGH)
            #time.sleep(1)
            #GPIO.output(RELAY_PIN, GPIO.LOW)
            #time.sleep(1)
            #time.sleep(2)
        else:
            print("[INFO] Waiting for job...")

except Exception as e:
    node.set_node_status(token, "error")
    print(f"Logging stopped by user: {e}")
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    GPIO.cleanup()

finally:
    instrument.serial.close()
# try:
#     while True:
#         light = instrument.read_register(0, 0)  # Register 0
#         gas = instrument.read_register(1, 0)    # Register 1
#         temp = read_temp()
#         weight = read_weight()
#         distance = read_distance()
#         print(f"Temp: {temp}°C | Weight: {weight} g | Distance: {distance} cm | Light>#         time.sleep(2)

# except KeyboardInterrupt:
#     GPIO.cleanup()

