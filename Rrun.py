import RPi.GPIO as GPIO
from time import strftime
import os
from datetime import datetime
import sqlite3
import configparser
from threading import Thread
import signal
import MFRC522
import socket

global verbose
global rfid_yes
global config


config = configparser.ConfigParser()
rfid_yes = False
verbose = True
class raspi:
    def __init__(self):
        self.klasor_olustur()
        config.read(self.address + "conf/configuration.cfg")
        self.manyetik_kapi_port = 3
        self.kirmizi=29
        self.yesil=31
        self.mavi =33
        self.gonderme_onay = False
        if rfid_yes:
            signal.signal(signal.SIGINT, self.end_read)
            self.MIFAREReader = MFRC522.MFRC522()
    def redOn(self):
        GPIO.output(self.kirmizi,GPIO.LOW)
        GPIO.output(self.yesil  ,GPIO.HIGH)
        GPIO.output(self.mavi   ,GPIO.HIGH)
        sleep(int(config['veri']['lamba_suresi']))
        GPIO.output(self.kirmizi,GPIO.HIGH)
        GPIO.output(self.yesil  ,GPIO.HIGH)
        GPIO.output(self.mavi  ,GPIO.HIGH)
    def greenOn(self):
        GPIO.output(self.kirmizi,GPIO.HIGH)
        GPIO.output(self.yesil,GPIO.LOW)
        GPIO.output(self.mavi ,GPIO.HIGH)
        sleep(int(config['veri']['lamba_suresi']))
        GPIO.output(self.kirmizi,GPIO.HIGH)
        GPIO.output(self.yesil,GPIO.HIGH)
        GPIO.output(self.mavi,GPIO.HIGH)
    def blueOn(self):
        GPIO.output(self.kirmizi,GPIO.HIGH)
        GPIO.output(self.yesil,GPIO.HIGH)
        GPIO.output(self.mavi ,GPIO.LOW)
        sleep(int(config['veri']['lamba_suresi']))
        GPIO.output(self.kirmizi,GPIO.HIGH)
        GPIO.output(self.yesil,GPIO.HIGH)
        GPIO.output(self.mavi,GPIO.HIGH)
    def klasor_olustur(self):
        if verbose:
            print('>>>raspi.klasor_olustur() fonksiyonuna giris yapiliyor...')
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

        if verbose:
            print('<<<raspi.klasor_olustur() fonksiyonundan cikis yapiliyor...')
        self.database_tanimla()
    def database_tanimla(self):
        if verbose:
            print('>>>raspi.database_tanimla() fonksiyonuna giris yapiliyor...')
        self.data = sqlite3.connect(self.address + "database/members.db")
        self.veri = self.data.cursor()
        if self.veri.execute("SELECT name FROM sqlite_master").fetchone() == None:
            self.veri.execute("""CREATE TABLE {} (
            'ad_soyad'	TEXT,
            'numara'   TEXT,
            'kart_id'  TEXT,
            PRIMARY KEY(kart_id));""".format('people'))
            self.data.commit()
        else:
            pass
        if verbose:
            print('<<<raspi.database_tanimla() fonksiyonundan cikis yapiliyor...')
    def pin_tanimla(self):
        if verbose:
            print('>>>raspi.pin_tanimla() fonksiyonuna giris yapiliyor...')
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.manyetik_kapi_port,GPIO.OUT) #3. pin manyetik kapi kilidi +
        GPIO.setup(self.kirmizi,GPIO.OUT)
        GPIO.setup(self.yesil  ,GPIO.OUT)
        GPIO.setup(self.mavi  ,GPIO.OUT)
        if verbose:
            print('<<<raspi.pin_tanimla() fonksiyonundan cikis yapiliyor...')
        GPIO.output(self.manyetik_kapi_port,GPIO.HIGH)
        commit = Thread(target=self.commit_data)
        basla = Thread(target=self.loop)
        commit.start()
        basla.start()
    def kilitle(self):
        if verbose:
            print('>>>raspi.kilitle() fonksiyonuna giris yapiliyor...')
        GPIO.output(self.manyetik_kapi_port,GPIO.HIGH)
        if verbose:
            print('<<<raspi.kilitle() fonksiyonundan cikis yapiliyor...')
    def kilit_ac(self):
        if verbose:
            print('>>>raspi.kilit_ac() fonksiyonuna giris yapiliyor...')
        GPIO.output(self.manyetik_kapi_port,GPIO.LOW)
        zaman = (int(datatime.today().strftime('%S')) + int(config['veri']['kapi_ac_izin'])) % 60
        while int(datatime.today().strftime('%S')) < zaman:
            pass
        self.kilitle()

        if verbose:
            print('<<<raspi.kilit_ac() fonksiyonundan cikis yapiliyor...')
    def toHex(self,dec):
        x = (dec %16)
        digits = "0123456789ABCDEF"
        rest = dec /16
        return digits[int(rest)] + digits[int(x)]
    def end_read(self,signal,frame):
        global continue_reading
        continue_reading = False
        GPIO.cleanup()
    def commit_data(self):
        self.gonderme_onay = True
        while self.gonderme_onay:
            #try:
            if True:
                mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                mysocket.bind((config['veri']['raspberry_ip'], int(config['veri']['raspberry_port'])))
                mysocket.listen(5)
                (client, (ip,port)) = mysocket.accept()
                data = client.recv(int(config['veri']['raspberry_buffer_size']))
                self.okunanVeri = data.decode()
                self.gonderme_onay = False
                mysocket.close()

            #except:
            #    if verbose:
            #        print('Hata Veri bekleniyor')

    def loop(self):
        if verbose:
            print("Waiting data . . .")
        continue_reading = True
        while continue_reading:
            hata = True
            try:

                if not(self.gonderme_onay):
                    averi  = Thread(target=self.commit_data)
                    averi.start()

                self.okunanVeri = self.okunanVeri.split(",")
                ad_soyad  = self.okunanVeri[0]
                numara = self.okunanVeri[1]
                uuid = self.okunanVeri[2]
            except:
                hata = False
            if hata: # yeni veri gelmis
                self.data = sqlite3.connect(self.address + "database/members.db")
                self.veri = self.data.cursor()
                buKisiEklimi = self.veri.execute("select exists(select * from people where kart_id = '"+  str(uuid) + "')").fetchone()[0]

                if buKisiEklimi == 0:#bu kişi ekli değil ekle
                    self.veri.execute("INSERT INTO people (ad_soyad,numara,kart_id) VALUES (?,?,?)",(ad_soyad,numara,uuid))
                    self.data.commit()
                else:
                    pass
            else: # yeni veri gelmemis kart okumayı kontrol et
                pass
                if rfid_yes:
                    (status,TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
                    (status,uid) = self.MIFAREReader.MFRC522_Anticoll()
                    if status == self.MIFAREReader.MI_OK:
                        okunanKart = self.toHex(uid[int(0)]) + " " +self.toHex(uid[int(1)])+ " " +self.toHex(uid[int(2)]) + " " +self.toHex(uid[int(3)])

                    ###
                    ##
                    #
                    buKisiEklimi = self.veri.execute("select exists(select * from people where kart_id = '"+  str(okunanKart) + "')").fetchone()[0]
                    if buKisiEklimi == 0:#bu kişi ekli değil ekle
                        izin = Thread(target=self.kilitle)
                        rgb = Thread(target=self.redOn)
                    else:
                        izin = Thread(target=self.kilit_ac)
                        rgb = Thread(target=self.greenOn                                                                                  )

                    izin.start()
                    rgb.start()


if __name__ == "__main__":

    giris = raspi()
    giris.pin_tanimla()
