import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(14,GPIO.LOW)
GPIO.setwarnings(False)
def btn_pressed():
    while True: 
        if GPIO.input(17) == GPIO.LOW:
            return True
        else:
            return False
        time.sleep(1)

""" while True:
    try:
        if btn_pressed():
            GPIO.output(14,GPIO.HIGH)
        else:
            GPIO.output(14,GPIO.LOW)
    except KeyboardInterrupt:
        GPIO.cleanup() """