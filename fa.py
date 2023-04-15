import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711
import speech_recognition as sr

referenceUnit = 1
hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(-747)
hx.reset()
hx.tare()

GPIO.setup(18, GPIO.OUT)
servoPIN1 = GPIO.PWM(18, 50)
servoPIN1.start(10)
GPIO.setup(25, GPIO.OUT)
servoPIN2 = GPIO.PWM(25, 50)
servoPIN2.start(10)

r = sr.Recognizer()
mic = sr.Microphone()

while True:
    try:
        with mic as source:
                try:
                    servoPIN1.ChangeDutyCycle(0)
                    servoPIN2.ChangeDutyCycle(0)
                    audio = r.listen(source, 10)
                    words = r.recognize_google(audio)
                    if words == "please give some treats":
                            print(words)
                            servoPIN2.ChangeDutyCycle(5)
                            time.sleep(0.2)
                            servoPIN2.ChangeDutyCycle(10)
                            time.sleep(0.2)
                            servoPIN2.ChangeDutyCycle(0)
                    else:
                          print("I did not understand...You said: " + words)
                except:
                       print("Nothing was said...")
                       servoPIN1.ChangeDutyCycle(0)
        weight = max(0.0, hx.get_weight(5))
        print(round(weight, 1), "g")
        hx.power_down()
        hx.power_up()
        if weight <= 70 and weight >= 40:
                servoPIN1.ChangeDutyCycle(5)
                time.sleep(0.5)
                servoPIN1.ChangeDutyCycle(10)
                time.sleep(0.5)
                servoPIN1.ChangeDutyCycle(0)
        if weight < 40:
                servoPIN1.ChangeDutyCycle(5)
                time.sleep(1.0)
                servoPIN1.ChangeDutyCycle(10)
                time.sleep(0.5)
                servoPIN1.ChangeDutyCycle(0)
        if weight > 70:
                servoPIN1.ChangeDutyCycle(0)
        time.sleep(1.5)

    except (KeyboardInterrupt, SystemExit):
        sys.exit()  
