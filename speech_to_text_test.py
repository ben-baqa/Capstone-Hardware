import RPi.GPIO as GPIO
import time
import subprocess
import os
import signal
import speech_recognition as sr
import requests
import json
# Print Start of test
print("ReSpeaker 2-Mic Pi Button test")

# User button pin
P2T_BUTTON = 25
redPin = 6
greenPin = 5
bluePin = 26
C_BUTTON = 27
transmitled = 24
# User button setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(P2T_BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(greenPin,GPIO.OUT)
GPIO.setup(bluePin,GPIO.OUT)
GPIO.setup(transmitled,GPIO.OUT)
GPIO.setup(C_BUTTON,GPIO.IN, pull_up_down = GPIO.PUD_UP)

previous = GPIO.input(C_BUTTON)
GPIO.output(bluePin, GPIO.LOW)
GPIO.output(greenPin, GPIO.LOW)
GPIO.output(redPin, GPIO.HIGH)
channel = 1

r = sr.Recognizer()
# Save previous state
previousState = GPIO.input(P2T_BUTTON)

global proc_args
global rec_proc

# Unending Loop (main)
while True:
    time.sleep(0.01)
    
    button_state = GPIO.input(C_BUTTON)
    if button_state != previous:
        previous = button_state
        if button_state == GPIO.HIGH:
            channel += 1
            if channel == 2:
                GPIO.output(redPin, GPIO.LOW)
                GPIO.output(bluePin, GPIO.LOW)
                GPIO.output(greenPin, GPIO.HIGH)
            if channel == 3:
                GPIO.output(redPin, GPIO.LOW)
                GPIO.output(greenPin, GPIO.LOW)
                GPIO.output(bluePin, GPIO.HIGH)
            if channel > 3:
                channel = 1
                GPIO.output(greenPin, GPIO.LOW)
                GPIO.output(bluePin, GPIO.LOW)
                GPIO.output(redPin, GPIO.HIGH)
                
    if GPIO.input(P2T_BUTTON) == 0 and previousState == 1:
        # Get button state
        currentState = GPIO.input(P2T_BUTTON)
        # Check if any difference
        proc_args = ['arecord', '-f', 'cd', '-Dplug:myTest', '/home/pi/test.wav'] 
        rec_proc = subprocess.Popen(proc_args, shell=False, preexec_fn=os.setsid)
        print("startRecordingArecord()> recording started")
        # Store current state as previous
        previousState = currentState
        # Check the current state of the button
    elif GPIO.input(P2T_BUTTON) == 1 and previousState == 0:
        os.killpg(rec_proc.pid, signal.SIGTERM)
        rec_proc.terminate()
        rec_proc = None
        print("stopRecordingArecord()> Recording stopped")
        previousState = 1
        filename = "/home/pi/test.wav"
        
        with sr.AudioFile(filename) as source:
            r.adjust_for_ambient_noise(source)
            audio_data = r.record(source)
            try:
                text = r.recognize_google(audio_data)
                if text == ("talk-box turn off"):
                    time.sleep(1)
                    GPIO.output(redPin, GPIO.LOW)
                    GPIO.output(bluePin, GPIO.LOW)
                    GPIO.output(greenPin, GPIO.LOW)
                    GPIO.output(transmitled, GPIO.HIGH)
                    time.sleep(0.5)
                    GPIO.output(transmitled, GPIO.LOW)
                    time.sleep(0.5)
                    GPIO.output(transmitled, GPIO.HIGH)
                    time.sleep(0.5)
                    GPIO.output(transmitled, GPIO.LOW)
                    time.sleep(0.5)
                    GPIO.output(transmitled, GPIO.HIGH)
                    time.sleep(0.5)
                    GPIO.output(transmitled, GPIO.LOW)
                    time.sleep(0.1)
                    os.system("sudo shutdown now")
            except sr.UnknownValueError:
                print("Speech was inaudible")
                text = ("Speech was inaudible")
            except sr.RequestError:
                print("Internet connection issues...")
                text = ("Internet connection issues...")
        url = "https://talk-box-server.herokuapp.com/"
        data = {'sender': 'talkbox_essa', 'text': text, 'channel': channel}
        headers = {'Content-type': 'application/json'}
        #send the requests and print the result
        print(requests.post(url, data = json.dumps(data), headers=headers))
                
            


 


            