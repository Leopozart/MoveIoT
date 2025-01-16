from flask import Flask, request, jsonify
from flask_cors import CORS
import serial
import time

arduino = serial.Serial(port='/dev/cu.usbmodem11301', baudrate=9600, timeout=.1)

app = Flask(__name__)
CORS(app)

def step_calculator(bmi, bmr):
    steps = round((bmr / bmi) * 78) #Detta är alltså enligt en hemsida som räknar ut steg, bmr/ bmi * steg längd, fast deras formel använde steg längd i ft vilket inte gav realistiska resultat så detta är i cm :) kommentaren tar slut här.
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
    age_number = int(data['age'])
    weight_number = int(data['weight'])
    height_number = int(data['height'])
    gender = data['gender']
    bmi = bmi_calculator(weight_number, height_number)
    bmr = calculate_bmr(weight_number, height_number, age_number, gender)
    steps = step_calculator(bmi, bmr)
    send_to_arduino(steps)  # Send steps value to Arduino
    return jsonify({'steps': steps, 'bmi': bmi, 'bmr': bmr })

if __name__ == '__main__':
    app.run(debug=True)