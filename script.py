from flask import Flask, request, jsonify
from flask_cors import CORS
import serial
import time

#-arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

app = Flask(__name__)
CORS(app)

def step_calculator(input_number):
    if input_number < 25:
        steps = "8000"
    elif 25 <= input_number < 50:
        steps = "7000"
    elif 50 <= input_number < 60:
        steps = "6000"
    else:
        steps = "5000"
    return steps

def send_to_arduino(value):
    """Send data to Arduino over the serial port."""
    if arduino.is_open:
        arduino.write(f"{value}\n".encode())  # Send the value followed by a newline
        time.sleep(0.1) 


@app.route('/calculate-steps', methods=['POST'])
def calculate_steps():
    data = request.get_json()
    input_number = int(data['age'])
    steps = step_calculator(input_number)
    #send_to_arduino(steps)  # Send steps value to Arduino
    return jsonify({'steps': steps})

if __name__ == '__main__':
    app.run(debug=True)