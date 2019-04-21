#!/usr/bin/env python
import RPi.GPIO as GPIO
from time import strftime,sleep,strptime
import os
from datetime import datetime,timedelta
import sqlite3
import configparser
from threading import Thread
import signal
import socket
from RC522 import RFID
import sys


global verbose
global rfid_yes
global config


config = configparser.ConfigParser()
rfid_yes = True
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
        self.yedek_kart = True
        self.ara_zaman = -5
        if rfid_yes:
            self.rdr = RFID()
            self.util = self.rdr.util()
            self.util.debug = True
            signal.signal(signal.SIGINT, self.end_read)
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
        kapanmaZamani = datetime.strptime(datetime.today().strftime('%H:%M:%S'),'%H:%M:%S')
        sure = timedelta(seconds = int(config['veri']['kapi_ac_izin']))
        kapanmaZamani = kapanmaZamani + sure
        guncelSure = datetime.strptime(datetime.today().strftime('%H:%M:%S'),'%H:%M:%S')
        while  guncelSure < kapanmaZamani:
            guncelSure = datetime.strptime(datetime.today().strftime('%H:%M:%S'),'%H:%M:%S')
        self.kilitle()

        if verbose:
            print('<<<raspi.kilit_ac() fonksiyonundan cikis yapiliyor...')
    def toHex(self,dec):
        x = (dec %16)
        digits = "0123456789ABCDEF"
        rest = dec /16
        return digits[int(rest)] + digits[int(x)]
    def end_read(self,signal,frame):
        print("\nCtrl+C captured, ending read.")
        self.rdr.cleanup()
        sys.exit()
    def commit_data(self):
        self.gonderme_onay = True
        while self.gonderme_onay:
            try:

                mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                mysocket.bind((config['veri']['raspberry_ip'], int(config['veri']['raspberry_port'])))
                mysocket.listen(5)
                (client, (ip,port)) = mysocket.accept()
                data = client.recv(int(config['veri']['raspberry_buffer_size']))
                self.okunanVeri = data.decode()
                client.send(b"knock knock knock, I'm the server")
                mysocket.close()

                sart = self.okunanVeri.split(",")

                if sart[0] == "True":
                    self.ip_address = sart[1]
                    self.okunanVeri = ","
                    print("a")
                    self.veri_yolla_bilgisayar()
                    print('V')
                else:
                    self.gonderme_onay = False
                #data = s.recv(1024) #alinan veri


                    #client.send(b"""1mysocket.bind((config['veri']['raspberry_ip'], int(config['veri']['raspberry_port'])))"""

            except Exception as error_name:

                if verbose:
                    print(2," ",error_name)
                else:
                    pass
    def veri_yolla_bilgisayar(self):
        print('KKKKKKKKKKKKKKKKK')
        self.data = sqlite3.connect(self.address + "database/register.db")
        print('a')
        self.veri = self.data.cursor()
        print('b')
        oku = self.veri.execute("select * from people").fetchall()
        print('c')
        bos = " "
        print('d')
        for i in oku:
            for j in i:
                bos= bos + "," + str(j)
        print('e')
        self.data.commit()
        text = bos
        print('1')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('2')
        s.connect((self.ip_address, int(config['veri']['raspberry_port'])))
        print('3')
        text = text.encode('utf-8')
        print('4')
        s.send(text)
        print('5')
        data = s.recv(int(config['veri']['raspberry_buffer_size'])) #alinan veri
        print('6')
        s.close()
        print('YYYYYYYYYYYYYYYYY')
        self.gonderme_onay = False








    def loop(self):
        if verbose:
            print("Waiting data . . .")

        while True:
            if not(self.gonderme_onay):
                averi  = Thread(target=self.commit_data)
                averi.start()
            hata = True
            try:
                self.okunanVeri = self.okunanVeri.split(",")
                ad_soyad  = self.okunanVeri[0]
                numara = self.okunanVeri[1]
                uuid = self.okunanVeri[2]
            except Exception as error_name:
                hata = False
            if hata: # yeni veri gelmis
                if verbose:
                    print('>>> New People')
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
                    self.rdr.wait_for_tag()
                    (error, data) = self.rdr.request()
                    (error, uid) = self.rdr.anticoll()
                    if not(error):
                        self.okunanKart= str(self.toHex(int(uid[0]))) + " " +str(self.toHex(uid[1]))+ " " +str(self.toHex(uid[2])) + " " +str(self.toHex(uid[3]))
                        sleep(0.1)
                    else:
                        self.okunanKart =False
                    ###
                    ##
                    #
                    if self.okunanKart != False:
                        self.data = sqlite3.connect(self.address + "database/register.db")
                        self.veri = self.data.cursor()
                        if self.veri.execute("SELECT name FROM sqlite_master").fetchone() == None:
                            self.veri.execute("""CREATE TABLE {} (
                            'ad_soyad'	TEXT,
                            'numara'   TEXT,
                            'giris_saat'   TEXT,
                            'cikis_saat'   TEXT,
                            PRIMARY KEY(numara));""".format('people'))
                            self.data.commit()
                        else:
                            pass
                        self.data = sqlite3.connect(self.address + "database/members.db")
                        self.veri = self.data.cursor()
                        buKisiEklimi = self.veri.execute("select exists(select * from people where kart_id = '"+  str(self.okunanKart) + "')").fetchone()[0]
                        if buKisiEklimi == 0:#bu kişi ekli değil ekle
                            izin = Thread(target=self.kilitle)
                            rgb = Thread(target=self.redOn)
                        else:
                            alinan = self.veri.execute("select * from people").fetchall()
                            for i in alinan:
                                if bool(i[2] == self.okunanKart):
                                    ad_soyad = i[0]
                                    numara = i[1]
                                    giris_saat = datetime.today().strftime("%d/%m/%y %H:%M:%S")
                                    cikis_saat = None
                                    break
                            self.data = sqlite3.connect(self.address + "database/register.db")
                            self.veri = self.data.cursor()
                            self.veri.execute("INSERT INTO people (ad_soyad,numara,giris_saat,cikis_saat) VALUES (?,?,?,?)",(ad_soyad,numara,giris_saat,cikis_saat))
                            self.data.commit()
                            izin = Thread(target=self.kilit_ac)
                            rgb = Thread(target=self.greenOn                                                                                  )

                        izin.start()
                        rgb.start()
                        sleep(int(config['veri']['lamba_suresi']))


if __name__ == "__main__":

    giris = raspi()
    giris.pin_tanimla()
