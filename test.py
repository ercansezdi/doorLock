#!/usr/bin/env python
import RPi.GPIO as GPIO
from time import sleep
class buzzerClass():
    def __init__(self):

        GPIO.setmode(GPIO.BOARD)
        self.buzzer_pin = 37
        #GPIO.setup(self.buzzer_pin, GPIO.IN)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)
    def buzz(self,pitch, duration):   #create the function “buzz” and feed it the pitch and duration)

        if(pitch==0):
            sleep(duration)
            return
        period = 1.0 / pitch     #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
        delay = period / 2     #calcuate the time for half of the wave
        cycles = int(duration * pitch)   #the number of waves to produce is the duration times the frequency

        for i in range(cycles):    #start a loop from 0 to the variable “cycles” calculated above
            GPIO.output(self.buzzer_pin, True)   #set pin 18 to high
            sleep(delay)    #wait with pin 18 high
            GPIO.output(self.buzzer_pin, False)    #set pin 18 to low
            sleep(delay)    #wait with pin 18 low
    def play(self,tune):
        x=0
        if(tune==1): #giriş
            pitches=[10, 20]
            duration=[0.2,0.2]
            for p in pitches:
                self.buzz(p, duration[x])  #feed the pitch and duration to the func$
                sleep(duration[x] *0.5)
                x+=1

        elif(tune==2):#çikiş
            pitches=[90]
            duration=[0.4]
            for p in pitches:
                self.buzz(p, duration[x])  #feed the pitch and duration to the func$
                sleep(duration[x] *0.5)
                x+=1

    def run(self):
        self.play(1)
        sleep(1)
        self.play(2)
if __name__ == "__main__":
    test = buzzerClass( )
    test.run()
