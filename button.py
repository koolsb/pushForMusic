from gpiozero import Button
import RPi.GPIO as GPIO
from datetime import datetime
from time import sleep
from signal import pause
from flask import Flask
import os

timeout = 300 # time to play music for
button_pin = 17 # gpio of button
button_led_pin = 27 # gpio of button led
relay_pin = 4 # gpio of relay for amp
log = True # enable logging of button presses
log_file = 'log.txt' # log file for button presses

# initialize GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.output(relay_pin, GPIO.HIGH)
GPIO.setup(button_led_pin, GPIO.OUT)
GPIO.output(button_led_pin, GPIO.HIGH)

def pressed():
  print("Button Pressed")
  # log entry
  if log:
    now = datetime.now()

    f = open("/home/fpp/" + log_file, "a")
    f.write("\n" + now.strftime("%m/%d/%Y %H:%M"))
    f.close()

  # activate GPIO pin on HIGH for timeout if button led is on
  if GPIO.input(button_led_pin) == 0 and GPIO.input(relay_pin) == 1:
    print("Play Music")
    GPIO.output(relay_pin, GPIO.LOW)
    GPIO.output(button_led_pin, GPIO.HIGH)
    sleep(timeout)
    GPIO.output(relay_pin, GPIO.HIGH)
    GPIO.output(button_led_pin, GPIO.LOW)

button = Button(button_pin)

button.when_pressed = pressed

api = Flask('api')

@api.route('/music/on', methods=['GET'])
def music_on():
  GPIO.output(relay_pin, GPIO.LOW)
  return ('', 204)

@api.route('/music/off', methods=['GET'])
def music_off():
  GPIO.output(relay_pin, GPIO.HIGH)
  return ('', 204)

@api.route('/music/status', methods=["GET"])
def music_status():
  if GPIO.input(relay_pin) == 0:
    return str(1)
  else:
    return str(0)

@api.route('/led/on', methods=['GET'])
def light_on():
  GPIO.output(button_led_pin, GPIO.LOW)
  return ('', 204)

@api.route('/led/off', methods=['GET'])
def light_off():
  GPIO.output(button_led_pin, GPIO.HIGH)
  return ('', 204)

@api.route('/led/status', methods=["GET"])
def light_status():
  if GPIO.input(button_led_pin) == 0:
    return str(1)
  else:
    return str(0)

@api.route('/push', methods=['GET'])
def push():
  pressed()
  return ('', 204)

@api.route('/shutdown', methods=['GET'])
def shutdown_host():
  os.system("shutdown now -h")
  return ('',204)

api.run(host='0.0.0.0')

pause()
