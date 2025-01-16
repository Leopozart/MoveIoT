from flask import Flask, request, jsonify
from flask_cors import CORS
import serial
import time

arduino = serial.Serial(port='/dev/cu.usbmodem11301', baudrate=9600, timeout=.1)

app = Flask(__name__)
CORS(app)

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

def bmi_calculator(weight, height):
    height_meter = height / 100
    return round(weight / (height_meter ** 2), 2)

def calculate_bmr(weight, height, age, gender):
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == 'female':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    return bmr

def send_to_arduino(value):
    """Send data to Arduino over the serial port."""
    if arduino.is_open:
        arduino.write(f"{value}\n".encode())  # Send the value followed by a newline
        time.sleep(0.1) 

@app.route('/calculate-steps', methods=['POST'])
def calculate_steps():
    data = request.get_json()
    input_number = int(data['age'])
    weight_number = int(data['weight'])
    height_number = int(data['height'])
    gender = data['gender']
    steps = step_calculator(input_number)
    bmi = bmi_calculator(weight_number, height_number)
    bmr = calculate_bmr(weight_number, height_number, input_number, gender)
    send_to_arduino(steps)  # Send steps value to Arduino
    return jsonify({'steps': steps, 'bmi': bmi, 'bmr': bmr })

if __name__ == '__main__':
    app.run(debug=True)