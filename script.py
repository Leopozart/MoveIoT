from flask import Flask, request, jsonify
from flask_cors import CORS
import serial
import threading
import time

arduino = serial.Serial(port='/dev/cu.usbmodem1301', baudrate=9600, timeout=.1)

app = Flask(__name__)
CORS(app)

def read_serial():
    """Continuously read data from Arduino and print it."""
    while True:
        if arduino.is_open:
            data = arduino.readline().decode().strip()
            if data:  # Print only if there's valid data
                print(f"Arduino: {data}")
        time.sleep(0.1)  # Prevent busy-waiting

# Start the serial reader in a background thread
serial_thread = threading.Thread(target=read_serial, daemon=True)
serial_thread.start()

def step_calculator(input_number):
    if input_number < 25:
        steps = "100"
    elif 25 <= input_number < 50:
        steps = "7000"
    elif 50 <= input_number < 60:
        steps = "6000"
    else:
        steps = "5000"
    return steps

def select_gender(input_gender):
    if input_gender.lower() == 'female':
        gender = 'female'
    else:
        gender = 'male'
    return gender

def calculate_bmi(weight, height):
    height_meters = height / 100
    return round(weight / (height_meters ** 2), 2)

def calculate_bmr(weight, height, age, gender):
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender.lower() == 'female':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    return bmr

def send_to_arduino(value):
    """Send data to Arduino over the serial port."""
    if arduino.is_open:
        arduino.write(f"{value}\n".encode())  # Send the value followed by a newline
        time.sleep(0.2)

@app.route('/calculate-steps', methods=['POST'])
def calculate_steps():
    print("POST request received")  # Debugging line
    data = request.get_json()
    print(f"Received data: {data}")  # Print out the received data
    input_number = int(data['age'])
    input_gender = data['gender']
    input_weight = float(data['weight'])
    input_height = float(data['height'])
    bmi = calculate_bmi(input_weight, input_height)
    bmr = calculate_bmr(input_weight, input_height, input_number, input_gender)
    steps = step_calculator(input_number)
    send_to_arduino(steps)  # Send steps value to Arduino
    results = [steps, bmi, bmr]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)