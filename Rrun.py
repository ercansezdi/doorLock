import RPi.GPIO as GPIO
from time import strftime
import os
from datetime import datetime
class raspi:
    def __init__(self):
        self.klasor_olustur()
        self.pin_tanimla()



    def klasor_olustur(self):
        self.address = os.getcwd()
        self.address = self.address.split('/')
        self.address = self.address[0] + '/' + self.address[1] + '/' + self.address[2] + '/Desktop'
        if not(os.path.exists(self.address + '/doorLock')):
            os.mkdir(self.address + '/doorLock')
        self.address = self.address  + "/doorLock/"
        if not(os.path.exists(self.address + 'database/')):
            os.mkdir(self.address  + 'database/')
        if not(os.path.exists(self.address + 'data/')):
            os.mkdir(self.address + 'data/')
    def pin_tanimla(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.manyetik_port = 3
        GPIO.setup(self.manyetik_port,GPIO.OUT) #3. pin manyetik kapı kilidi +si


    def kilitle(self):
        GPIO.output(self.manyetik_port,GPIO.HIGH)
    def kilit_ac(self):
        GPIO.output(self.manyetik_port,GPIO.LOW)




if __name__ == "__main__":

    giris = raspi()
    giris.pin_tanimla()
