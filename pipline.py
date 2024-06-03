#from mov2 import *
import socket
import sys
import time
import RPi.GPIO as GPIO
#IMPORTS DONE

GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 23
GPIO_ECHO = 24
ball_dir=""
GPIO.setup([M1_PWM_PIN, M1_DIR_PIN, M2_PWM_PIN, M2_DIR_PIN,
            M3_PWM_PIN, M3_DIR_PIN, M4_PWM_PIN, M4_DIR_PIN,
            M5_PWM_PIN, M5_DIR_PIN], GPIO.OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
ball_dropped = False
GPIO.setup(ENA_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(PUL_PIN, GPIO.OUT)
step_delay = 0.0005  # Adjust this value to control speed
duration = 2.5 # Duration for each rotation direction in seconds

zone2_flag = False
zone3_flag = False
bang_balls = False
response2 = "silo"
response1 = "pick"

OD_home = False
OD_silo = False
claw = "open"

HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 54322      # Choose a port number for control signals
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(1)
print("Raspberry Pi server is listening...")

global dir_list
global time_list
dir_list = []
time_list = []
num=1

def measure_distance():
    # Set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # Set Trigger after 0.01ms to LOW
    time.sleep(0.00000001)
    GPIO.output(GPIO_TRIGGER, False)

    start_time = time.time()
    stop_time = time.time()

    # Save start_time
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    # Save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    # Time difference between start and arrival
    time_elapsed = stop_time - start_time
    # Multiply with the speed of sound (34300 cm/s) and divide by 2
    distance = (time_elapsed * 34300) / 2

    return distance


def reverse_list(dir_list):
    rev_list = dir_list[::-1]
    return rev_list

def ret_home():
    print(dir_list)
    rev_dir_list = reverse_list(dir_list)
    rev_time_list = reverse_list(time_list)
    print(rev_time_list)
    for i in range(len(rev_dir_list)):
        if rev_dir_list[i] == 's':
            forward(for_speed = 10, seconds = rev_time_list[i])
            time.sleep(1)
            continue
        elif rev_dir_list[i] == 'r':
            right(seconds = rev_time_list[i])
            time.sleep(1)
            continue
        elif rev_dir_list[i] == 'l':
            left(seconds = rev_time_list[i])
            time.sleep(1)
            continue
        elif rev_dir_list[i] == 'dr':
            diagonal_right(seconds = rev_time_list[i])
            time.sleep(1)
        elif rev_dir_list[i] == 'dl':
            diagonal_left(seconds = rev_time_list[i])
            time.sleep(1)



try:
    zone_value = int(sys.argv[1])
    client_socket, address = server_socket.accept()
    print("Connected to:", address)
    while True:
        received_data = client_socket.recv(1024)
        print("Received from Jetson:", received_data.decode())
        command = received_data.decode()
        if not zone2_flag and zone_value == 1:
            zone2()
        if not zone3_flag and zone_value == 2:
            zone3()
        if zone3_flag and not bang_balls:
            ram()
        if zone3_flag and zone2_flag and bang_balls:
            if OD_silo == False:
                client_socket.sendall(response1.encode())
            if command != prev_command:
                if command != 'd':
                    dir_list.append(command)
                    time_list.append(0)

            if command == 's':

                if (ball_dir == "left"):
                    dir_list[-1] = 'r'
                    time_list[-1] += right(seconds=0.56)
                    right(seconds=0.1)
                elif (ball_dir == "right"):
                    dir_list[-1] = 'l'
                    time_list[-1] += left(seconds=0.56)

                print("Forward")
                straight()
                ball_detected = True
                # time.sleep(1)
                continue
            elif command == 'r':
                ball_dir = "right"
                print("Right")
                time_list[-1] = time_list[-1] + right()
                time.sleep(0.2)
                continue
            elif command == 'l':
                ball_dir = "left"
                print("Left")
                time_list[-1] = time_list[-1] + left()
                time.sleep(0.2)
                continue
            elif command == '0':
                print("Stopping motors")
                stop()
                time.sleep(1)
                continue
            elif command == 'd':
                if ball_dir == "right":
                    if dir_list[-1] != 'dl':
                        dir_list.append('dl')
                        time_list.append(0)
                    time_list[-1] += 2
                    diagonal_left(seconds=2)
                elif ball_dir == "left":
                    if dir_list[-1] != 'dr':
                        dir_list.append('dr')
                        time_list.append(0)
                    time_list[-1] += 2
                    diagonal_right(seconds=2)
                time.sleep(1)
                continue
            time.sleep(0.1)
            prev_command = command
            ball_pick()
            claw = "close"
            ret_home()
            OD_home = True
            OD_silo = True
            if claw == "close" and OD_home and OD_silo:
                client_socket.sendall(response2.encode())
                silo(command)
                claw = "open"
                for i in range(29):
                    rotate_right(rotation_speed=25)
                ret_home()
                OD_silo = False
                if num == 1:
                    silo2()
                    num*=-1
                elif num == -1:
                    silo4()
                    num*=-1



except KeyboardInterrupt:
    print("KeyboardInterrupt: Closing sockets...")
    # Close the connection
    client_socket.close()
    server_socket.close()

GPIO.cleanup()
