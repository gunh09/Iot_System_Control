#door.py
import RPi.GPIO as GPIO
import time
import socket

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)    # motor
p = GPIO.PWM(18, 50)
p.start(0)

GPIO.setup(23, GPIO.IN)    # pir

cnt = 0
cnt_data = 0
cnt_permit = 0

PERMIT_COUNT = 2
CLOSE_DELAY = 3

open_flag = True

HOST = '59.26.44.137'
PORT = 8003

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    while True:
        data = s.recv(1024)
        data = str(data).split("b'", 1)[1].rsplit("'",1)[0]
        print('CLOSE_DELAY: ' + str(cnt))

        try:    
            if data == '1':                                               
                if cnt_permit >= PERMIT_COUNT and open_flag is True:                
                    print('--- Open the door ---')
                    
                    p.ChangeDutyCycle(6.2)
                    
                    cnt_permit = 0       
                    open_flag = False
                    
                elif cnt_permit < PERMIT_COUNT:
                    cnt_permit += 1
            else:                          
                print('--- Not-permitted ---')
                
            if open_flag is False:
                if cnt > CLOSE_DELAY:
                    print('--- Close the door ---')
                    
                    p.ChangeDutyCycle(3.5)
                    
                    open_flag = True
                    cnt = 0
                else:
                    cnt += 1
                    
            if GPIO.input(23) == 0:                
                cnt = 0                
                
        except KeybordInterrupt:    
            GPIO.cleanup()