#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
from tkinter import *
import socket
from threading import Thread
from time import sleep
import configparser
from datetime import datetime
from time import strftime
import serial
################ globals #####################
global verbose
global config


verbose = True
config = configparser.ConfigParser()

############### classes ######################
class configure_class:
    def __init__(self):
        self.create_folder()


    def create_folder(self):
        if verbose:
            print('>>>door_lock.create_folder() fonksiyonuna giris yapiliyor...')
        address = os.getcwd()
        if str(os.name) == 'posix': #Linux
            address = address.split('/')
            address = address[0] + '/' + address[1] + '/' + address[2] + '/Desktop'
            if not(os.path.exists(address + '/doorLock')):
                os.mkdir(address + '/doorLock')
            address = address  + "/doorLock/"
            if not(os.path.exists(address + 'database/')):
                os.mkdir(address  + 'database/')
            if not(os.path.exists(address + 'data/')):
                os.mkdir(address + 'data/')

        if str(os.name) == 'nt': # Windows
            address = str(address).split('\\')
            address = address[0] + '\\' + address[1] + '\\' + address[2] + '\\Desktop'
            if not(os.path.exists(address + '\\doorLock')):
                os.mkdir(address + '\\doorLock')
            address = address  + "\\doorLock"
            if not(os.path.exists(address + '\\database')):
                os.mkdir(address + '\\database')
            if not(os.path.exists(address +  '\\data')):
                os.mkdir(address + '\\data')

        if verbose:
            print('<<<door_lock.create_folder() fonksiyonundan cikis yapiliyor...')



    def create_database(self):
        if verbose:
            print('>>>door_lock.create_database() fonksiyonuna giris yapiliyor...')
        data = sqlite3.connect("database/members.db").cursor()
        if data.execute("SELECT name FROM sqlite_master").fetchone() == None:
            data.execute("""CREATE TABLE {} (
            'ad_soyad'	TEXT,
            'kart_id'  TEXT,
            PRIMARY KEY(kart_id));""".format('data'))
            data.commit()
        else:
            pass



        if verbose:
            print('<<<door_lock.create_folder() fonksiyonundan cikis yapiliyor...')
class user_interface(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.menu = Menu(self.parent)
        self.parent.config(menu=self.menu)
        self.parent.config(bg='#2A2C2B', menu=self.menu)
        self.frame_one = Frame(self.parent)
        self.frame_one.grid(row=0,column=0)
        self.frame_one.grid_remove()

        self.frame_two = Frame(self.parent)
        self.frame_two.grid(row=0,column=0)
        self.frame_two.grid_remove()

        self.frame_three = Frame(self.parent)
        self.frame_three.grid(row=0,column=0)
        self.frame_three.grid_remove()

        #self.parent.attributes("-fullscreen", True)
        self.parent.geometry('390x200')
        self.parent.bind('<Escape>',quit)
        self.parent.title('Kuluçka Merkezi doorLock')

        ################# colors ######################
        self.bg = "#1e0000"
        self.fg = "#ffffff"

        self.parent.configure(background=self.bg )
        self.frame_one.configure(background=self.bg )
        self.frame_two.configure(background=self.bg )
        self.frame_three.configure(background=self.bg )




        ################# variables ###################
        self.variable1 = StringVar()
        self.variable2 = StringVar()
        self.variable3 = StringVar()
        self.backup = "loop_end"
        self.variable = StringVar()
        self.address = os.getcwd()
        self.dot = "."
        self.message = ""
        self.serial_durdur = None

        if str(os.name) == 'posix': #Linux
            self.address = self.address.split('/')
            self.address = self.address[0] + '/' + self.address[1] + '/' + self.address[2] + '/Desktop'
            self.address = self.address + '/doorLock'
            config.read(self.address + "/conf/configuration.cfg")
        if str(os.name) == 'nt': #Windows
            self.address = str(self.address).split('\\')
            self.address = self.address[0] + '\\' + self.address[1] + '\\' + self.address[2] + '\\Desktop'
            self.address = self.address + '\\doorLock'
            config.read(self.address + "\\conf\\configuration.cfg")
            print(self.address + "\\conf\\configuration.cfg")
        ################ functions ####################
        self.configure_interface()
        self.start_interface()
    def configure_interface(self):
        if verbose:
            print('>>>user_interface.start_gui() fonksiyonuna giris yapiliyor...')
        #################################### Frames ###########################################
        self.frame_text_1 = Frame(self.frame_two)
        self.frame_text_1.grid(row = 0,column = 0,pady = 10,rowspan=1,columnspan =1)
        self.frame_text_1.configure(background=self.bg )
        self.frame_text_2 = Frame(self.frame_two)
        self.frame_text_2.grid(row = 1,column = 0,pady = 10,rowspan=1,columnspan =1)
        self.frame_text_2.configure(background=self.bg )
        self.frame_text_3 = Frame(self.frame_two)
        self.frame_text_3.grid(row = 2,column = 0,pady = 10,rowspan=1,columnspan =1)
        self.frame_text_3.configure(background=self.bg )


        #################################### Buttons ##########################################
        self.exitButton    = Button(self.frame_one,text = 'Exit',wraplength=750,anchor="center",height=1,width=3,highlightbackground=self.bg,font ="Helvetica 15 bold italic",fg=self.fg,command=self.parent.destroy)
        #self.exitButton.grid(row=3,column=1, sticky=W,padx= 150, pady = 0,columnspan=1,rowspan=2)
        self.sendButton    = Button(self.frame_two,text = 'Bilgiyi Gönder',wraplength=750,anchor="center",height=1,width=13,highlightbackground=self.fg,font ="Helvetica 15 bold italic",fg=self.bg,command=self.send_data)
        self.sendButton.grid(row=3,column=0, sticky=W,padx= 120, pady = 25,columnspan=2,rowspan=1)



        #################################### Labels ###########################################
        self.text_1        = Label(self.frame_one,textvariable=self.variable1,borderwidth=0,bg=self.bg,fg=self.fg,font ="Helvetica 25 bold italic")
        self.text_1.grid(row=0,column=1,padx=25,pady=80,rowspan=3,columnspan=2)
        self.variable1.set("Kart Bilgisi Bekleniyor")
        #self.text_variable = Label(self.frame_one,textvariable=self.variable,borderwidth=0,bg="#008000")
        self.text_2        = Label(self.frame_text_1 ,text=" İsim Giriniz                            :",bg=self.bg,fg=self.fg,justify = LEFT,font ="Helvetica 15 bold italic")
        self.text_2.grid(row=0,column=0,padx=5,pady = 0)
        self.text_3        = Label(self.frame_text_2,text=" Soyisim Giriniz                     : ",borderwidth=0,bg=self.bg,fg=self.fg,font ="Helvetica 15 bold italic")
        self.text_3.grid(row=1,column=0,padx=5,pady = 0,rowspan=1,columnspan=1)
        self.text_4        = Label(self.frame_text_3,text="Öğrenci Numarasi Giriniz    : ",borderwidth=0,bg=self.bg,fg=self.fg,font ="Helvetica 15 bold italic")
        self.text_4.grid(row=2,column=0,padx=5,pady = 0,rowspan=1,columnspan=1)
        self.text_5        = Label(self.frame_three,textvariable=self.variable2,borderwidth=0,bg=self.bg,fg=self.fg,font ="Helvetica 25 bold italic")
        self.text_5.grid(row=0,column=1,padx=25,pady=80,rowspan=3,columnspan=2)
        self.variable2.set("Bilgiler Gönderiliyor")
        #################################### Enty ############################################

        self.name          = Entry(self.frame_text_1,font ="Helvetica 12 bold italic")
        self.name.grid(row=0,column=1,padx=0,pady = 0,rowspan=1,columnspan=1)
        self.surname       = Entry(self.frame_text_2,font ="Helvetica 12 bold italic")
        self.surname.grid(row=1,column=1,padx=0,pady = 0,rowspan=1,columnspan=1)
        self.studentNumber = Entry(self.frame_text_3,font ="Helvetica 12 bold italic")
        self.studentNumber.grid(row=2,column=1,padx=0,pady = 0,rowspan=1,columnspan=1)

        #################################### Menu #####################################33
        #self.exit.add_command(label="Exit", command=self.parent.destroy)
        self.menu.add_cascade(label="Giriş - Çıkış Kayıtları", command=self.requeset_data_beginning)
        self.menu.add_cascade(label=" | ")
        self.menu.add_cascade(label="Yeni Kişi Ekleme", command=self.start_interface)
        self.menu.add_cascade(label=" | ")
        self.menu.add_cascade(label= "Kart Okuma Aktif", command=self.serial_degistir)

        if verbose:
            print('<<<user_interface.start_gui() fonksiyonundan cikis yapiliyor...')
    def serial_degistir(self):
        a = "Kart Okuma Aktif"
        b = "Kart Okuma Kapalı"
        if self.serial_durdur ==  "loop_end":
            self.serial_durdur = None
            self.menu.delete(b)
            self.menu.add_cascade(label=a, command=self.serial_degistir)
        else:
            self.serial_durdur =  "loop_end"
            self.menu.delete(a)
            self.menu.add_cascade(label=b, command=self.serial_degistir)
    def read_serial(self):
        if self.serial_durdur != "loop_end":
            port_counter = 0
            hata = True
            port_x = "COM"
            while hata:
                try:
                    port = port_x + str(port_counter)
                    ard = serial.Serial(port ,9600,timeout=2)
                    hata = False
                except:
                    port_counter = port_counter + 1

            # Serial read section
            msg = ard.readline()
            if str(msg) != "b''":
                self.message = ""
                for i in str(msg):
                    if i != "'" and i != 'b':
                        self.message = self.message + i

                self.message = str(self.message).split(" ")
                self.message = self.message[1] + " " + self.message[2] + " " + self.message[3] + " " + self.message[4]
                if verbose:
                    print("Read card : ",self.message)
            else:
                self.message = ""
        root.after(300,run.read_serial)
    def send_data(self):
        if verbose:
            print('>>>user_interface.send_data() fonksiyonuna giris yapiliyor...')
        if self.name.get() == "" or self.name.get() == " " or self.name.get() == " " or self.name.get() == "   ":
            self.name.insert(0, '')
            self.name.insert(0, 'Boş Birakilamaz.')
        if self.surname.get() == "" or self.surname.get() == " " or self.surname.get() == "  " or self.surname.get() == "   ":
            self.surname.insert(0, 'Boş Birakilamaz.')
        if self.studentNumber.get() == ""  or self.studentNumber.get() == " " or self.studentNumber.get() == "  " or self.studentNumber.get() == "   ":
            self.studentNumber.insert(0, 'Boş Birakilamaz.')

        if self.name.get() != "" and self.name.get() != "Boş Birakilamaz." and self.name.get() != " " and self.name.get() != " " and self.name.get() != "   ":
            if self.surname.get() != "" and self.surname.get() != "Boş Birakilamaz." and self.surname.get() != " " and self.surname.get() != "  " and self.surname.get() != "   ":
                if self.studentNumber.get() != "" and self.studentNumber.get() != "Boş Birakilamaz." and self.studentNumber.get() != " " and self.studentNumber.get() != "  " and self.studentNumber.get() != "   ":
                    self.backup = "loop_end"
                    if verbose:
                        print("""
                        Gönderilecek Veriler:
                        Name          : {}
                        Surname       : {}
                        Numarasi      : {}
                        Kart Numarasi : {}
                        """.format(self.name.get(),self.surname.get(),self.studentNumber.get(),self.message))
                    self.send_data_ = str(self.name.get()) + " " + str(self.surname.get()) + "," + str(self.studentNumber.get()) + "," + str(self.message)

                    self.name.delete(0, "end")
                    self.surname.delete(0, "end")
                    self.studentNumber.delete(0, "end")
                    if verbose:
                        print('<<<user_interface.send_data() fonksiyonundan cikis yapiliyor...')

                    restart_data = Thread(target=self.waiting)
                    send = Thread(target=self.send_raspberry)
                    restart_data.start()
                    send.start()


                else:
                    pass
            else:
                pass
        else:
            pass

    def waiting(self):
        self.frame_two.grid_remove()
        self.frame_three.grid(row = 0, column = 0)
    def send_raspberry(self):
        if verbose:
            print('>>>user_interface.send_raspberry() fonksiyonuna giris yapiliyor...')
        self.hata = False
        while not(self.hata):
            self.dot = self.dot + '.'
            if self.dot == '....':
                self.dot = ""
            self.variable2.set("Bilgiler Gönderiliyor" + self.dot)
            #try:
            if True:
                veri = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                veri.connect((config['veri']['raspberry_ip'], int(config['veri']['raspberry_port'])))
                print(self.send_data_)
                self.send_data_ = self.send_data_.encode('utf-8')
                veri.send(self.send_data_)
                #data = s.recv(1024) #alinan veri
                veri.close()
                self.hata = True
            #except:
            #    self.hata = False
        self.backup = None
        if verbose:
            print('<<<user_interface.send_raspberry() fonksiyonundan cikis yapiliyor...')
        self.serial_degistir()
        self.start_interface()

    def data_waiting(self):
        if self.backup != 'loop_end':
            self.dot = self.dot + '.'
            if self.dot == '....':
                self.dot = ""
            if self.message == "":
                text = "Kart Bilgisi Bekleniyor" + self.dot
                if text == "Kart Bilgisi Bekleniyor...":
                    text = "Kart Bilgisi Bekleniyor"
                self.variable1.set(text)
            else:
                self.backup = "loop_end"
                self.serial_degistir()
                self.read_data_interface()
        else:
            pass
        root.after(1000,run.data_waiting)
    def read_data_interface(self):
        if verbose:
            print('>>>user_interface.read_data_interface() fonksiyonuna giris yapiliyor...')
            self.frame_one.grid_remove()
            self.frame_two.grid_remove()
            self.frame_two.grid(row = 0 ,column = 0)
            self.frame_three.grid_remove()

        if verbose:
            print('<<<user_interface.read_data_interface() fonksiyonundan cikis yapiliyor...')
    def start_interface(self):
        if verbose:
            print('>>>user_interface.start_interface() fonksiyonuna giris yapiliyor...')
            self.frame_one.grid_remove()
            self.frame_one.grid(row = 0 ,column =0)
            self.frame_two.grid_remove()
            self.frame_three.grid_remove()
            self.backup = None
            #self.text_variable.grid(row=0,column=1,padx=0,pady = 0,rowspan=1,columnspan=1)
        if verbose:
            print('<<<user_interface.start_interface() fonksiyonundan cikis yapiliyor...')
    def requeset_data_beginning(self):
        if verbose:
            print('>>>user_interface.requeset_data_beginning() fonksiyonuna giris yapiliyor...')
        self.backup = 'loop_end'
        self.serial_degistir()
        #burada popup açılacak
        self.requeset_data()
        if verbose:
            print('<<<user_interface.requeset_data_beginning() fonksiyonundan cikis yapiliyor...')

    def requeset_data(self):
        if verbose:
            print('>>>user_interface.requeset_data() fonksiyonuna giris yapiliyor...')
        hata = True
        #while hata:
            #try:
        if True:
            if True:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((config['veri']['raspberry_ip'], int(config['veri']['raspberry_port'])))

                text ="databse_send_me"

                text = text.encode('utf-8')
                s.send(text)
                self.requeset_data_answer = s.recv(int(config['veri']["raspberry_buffer_size"]))
                print(self.requeset_data_answer)
                s.close()
            #except:
            #    hata = True
        self.serial_degistir()
        self.backup = None
        if verbose:
            print('<<<user_interface.requeset_data() fonksiyonundan cikis yapiliyor...')
if __name__ == "__main__":
    connect = configure_class()
    root = Tk()
    root.call('tk', 'scaling', 1.0)
    run = user_interface(root)
    root.after(1000,run.data_waiting)
    root.after(1000,run.read_serial)
    root.mainloop()
