import time
import RPi.GPIO as GPIO
import socket
import inputs

GPIO.setmode(GPIO.BCM)

M1_PWM_PIN = 19
M1_DIR_PIN = 26
M2_PWM_PIN = 6
M2_DIR_PIN = 13

# Define GPIO pins for Motor Driver 2
M3_PWM_PIN = 16
M3_DIR_PIN = 20
M4_PWM_PIN = 1
M4_DIR_PIN = 12
M5_PWM_PIN = 8  # Example pin for the 6th motor
M5_DIR_PIN = 25  # Example pin for the 6th motor


GPIO.setup([M1_PWM_PIN, M1_DIR_PIN, M2_PWM_PIN, M2_DIR_PIN,
            M3_PWM_PIN, M3_DIR_PIN, M4_PWM_PIN, M4_DIR_PIN,
            M5_PWM_PIN, M5_DIR_PIN], GPIO.OUT)
ENA_PIN = 4  # Enable pin
DIR_PIN = 15  # Direction pin
PUL_PIN = 3  # Pulse pin
step_delay = 0.0005  # Adjust this value to control speed
duration = 5  # Duration for each rotation direction in seconds


# Function to set motor speed and direction
GPIO.setwarnings(False)
GPIO.setup(ENA_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(PUL_PIN, GPIO.OUT)

def set_motor_speed(motor, speed):
    if speed >= 0:
        GPIO.output(motor["dir_pin"], GPIO.HIGH)
    else:
        GPIO.output(motor["dir_pin"], GPIO.LOW)
    motor["pwm"].start(abs(speed))

# Function to stop all motors
def stop_motors():
    for motor in motors:
        motor["pwm"].stop()

# Define motors
motor1 = {"pwm": GPIO.PWM(M1_PWM_PIN, 100), "dir_pin": M1_DIR_PIN}
motor2 = {"pwm": GPIO.PWM(M2_PWM_PIN, 100), "dir_pin": M2_DIR_PIN}
motor3 = {"pwm": GPIO.PWM(M3_PWM_PIN, 100), "dir_pin": M3_DIR_PIN}
motor4 = {"pwm": GPIO.PWM(M4_PWM_PIN, 100), "dir_pin": M4_DIR_PIN}
motor5 = {"pwm": GPIO.PWM(M5_PWM_PIN, 100), "dir_pin": M5_DIR_PIN}
motors = [motor1, motor2, motor3, motor4,motor5]
for motor in motors:
    motor["pwm"].start(0)

speed = 10
rotspeed0 = 25
backward_speed = 50
forward_speed = 50
rot_speed = 3

'''
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 54322      # Choose a port number for control signals

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(1)
print("Raspberry Pi server is listening...")
'''
'''
def forward():
    set_motor_speed(motor1, forward_speed)
    set_motor_speed(motor2, forward_speed)
    set_motor_speed(motor3, forward_speed)
    set_motor_speed(motor4, forward_speed)
    time.sleep(0.05)
'''# FORWARD AND BACKWARD REQUIRED FUNCS
def forward(for_speed=forward_speed, seconds=-1):
    start_time = time.time()
    if seconds == -1:
        set_motor_speed(motor1, for_speed)
        set_motor_speed(motor2, for_speed)
        set_motor_speed(motor3, for_speed)
        set_motor_speed(motor4, for_speed)
        time.sleep(0.05)
    else:
        while time.time() - start_time < seconds:
            set_motor_speed(motor1, for_speed)
            set_motor_speed(motor2, for_speed)
            set_motor_speed(motor3, for_speed)
            set_motor_speed(motor4, for_speed)
            time.sleep(0.05)
    return time.time() - start_time

def backward(back_speed=backward_speed, seconds=-1):
    start_time = time.time()
    if seconds == -1:
        start_time = time.time()
        set_motor_speed(motor1, -back_speed)
        set_motor_speed(motor2, -back_speed)
        set_motor_speed(motor3, -back_speed)
        set_motor_speed(motor4, -back_speed)
        time.sleep(0.05)
    else:
        while time.time() - start_time < seconds:
            set_motor_speed(motor1, -backward_speed)
            set_motor_speed(motor2, -backward_speed)
            set_motor_speed(motor3, -backward_speed)
            set_motor_speed(motor4, -backward_speed)
            time.sleep(0.05)
    return time.time() - start_time

# RIGHT AND LEFT REQUIRED FUNCS
def left(seconds=-1):
    start_time = time.time()
    if seconds == -1:
        set_motor_speed(motor1, -speed)
        set_motor_speed(motor2, speed)
        set_motor_speed(motor3, speed)
        set_motor_speed(motor4, -speed)
        time.sleep(0.05)
    else:
        while time.time() - start_time < seconds:
            set_motor_speed(motor1, -speed)
            set_motor_speed(motor2, speed)
            set_motor_speed(motor3, speed)
            set_motor_speed(motor4, -speed)
            time.sleep(0.05)
    return time.time() - start_time

def right(seconds=-1):
    start_time = time.time()
    if seconds == -1:
        set_motor_speed(motor1, speed)
        set_motor_speed(motor2, -speed)
        set_motor_speed(motor3, -speed)
        set_motor_speed(motor4, speed)
        time.sleep(0.05)
    else:
        while time.time() - start_time < seconds:
            set_motor_speed(motor1, speed)
            set_motor_speed(motor2, -speed)
            set_motor_speed(motor3, -speed)
            set_motor_speed(motor4, speed)
            time.sleep(0.05)
    return time.time() - start_time

# DIAGONAL LEFT AND DIAGONAL RIGHT REQUIRED FUNCTIONS
def diagonal_left(seconds=-1):
    start_time = time.time()
    if seconds == -1:
        set_motor_speed(motor1, 0)
        set_motor_speed(motor2, speed)
        set_motor_speed(motor3, speed)
        set_motor_speed(motor4, 0)
        time.sleep(0.05)
    else:
        while time.time() - start_time < seconds:
            set_motor_speed(motor1, 0)
            set_motor_speed(motor2, speed)
            set_motor_speed(motor3, speed)
            set_motor_speed(motor4, 0)
            time.sleep(0.05)
    return time.time()-start_time

def diagonal_right(seconds=-1):
    start_time = time.time()
    if seconds == -1:
        set_motor_speed(motor1, speed)
        set_motor_speed(motor2, 0)
        set_motor_speed(motor3, 0)
        set_motor_speed(motor4, speed)
        time.sleep(0.05)
    else:
        while time.time() - start_time < seconds:
            set_motor_speed(motor1, speed)
            set_motor_speed(motor2, 0)
            set_motor_speed(motor3, 0)
            set_motor_speed(motor4, speed)
            time.sleep(0.05)
    return time.time() - start_time

# ROTATION LEFT AND RIGHT FUNCTIONS
def rotate_left(rotation_speed=rot_speed, seconds=-1):
    start_time = time.time()
    if seconds == -1:
        set_motor_speed(motor1, -rotation_speed)
        set_motor_speed(motor2, rotation_speed)
        set_motor_speed(motor3, -rotation_speed)
        set_motor_speed(motor4, rotation_speed)
        time.sleep(0.05)
    else:
        start_time = time.time()
        while time.time() - start_time < seconds:
            set_motor_speed(motor1, -rotation_speed)
            set_motor_speed(motor2, rotation_speed)
            set_motor_speed(motor3, -rotation_speed)
            set_motor_speed(motor4, rotation_speed)
            time.sleep(0.05)
    return time.time() - start_time

def rotate_right(rotation_speed=rot_speed, seconds=-1):
    start_time = time.time()
    if seconds == -1:
        set_motor_speed(motor1, rotation_speed)
        set_motor_speed(motor2, -rotation_speed)
        set_motor_speed(motor3, rotation_speed)
        set_motor_speed(motor4, -rotation_speed)
        time.sleep(0.05)
    else:
        while time.time() - start_time < seconds:
            set_motor_speed(motor1, rotation_speed)
            set_motor_speed(motor2, -rotation_speed)
            set_motor_speed(motor3, rotation_speed)
            set_motor_speed(motor4, -rotation_speed)
            time.sleep(0.05)
    return time.time() - start_time

# OTHER FUNCTIONS
def stop():
    for i in range(5,-1,-1):
        set_motor_speed(motor1, i)
        set_motor_speed(motor2, i)
        set_motor_speed(motor3, i)
        set_motor_speed(motor4, i)
    time.sleep(0.05)

def pneumat_on():
    set_motor_speed(motor5, 100)
      

def pneumat_off():
    set_motor_speed(motor5, 0)
     
    
def rotate_motor(direction):
    GPIO.output(DIR_PIN, direction)
    print(f"Set direction to {'HIGH (Clockwise)' if direction == GPIO.HIGH else 'LOW (Counter-Clockwise)'}")
    start_time = time.time()
    while time.time() - start_time < duration:
        GPIO.output(PUL_PIN, GPIO.HIGH)
        time.sleep(step_delay)
        GPIO.output(PUL_PIN, GPIO.LOW)
        time.sleep(step_delay)       

GPIO.cleanup()
