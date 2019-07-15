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
import tkinter.ttk
import  sqlite3

################ globals #####################
global verbose
global config


verbose = True
config = configparser.ConfigParser()

############### classes ######################
class configure_class:
    def __init__(self):
        self.create_folder()
    def create_database_1(self):
        self.data = sqlite3.connect("database/register.db")
        self.veri = self.data.cursor()
        if self.veri.execute("SELECT name FROM sqlite_master").fetchone() == None:
            self.veri.execute("""CREATE TABLE {} (
            'ad_soyad'	TEXT,
            'TC_Kimlik_No'   TEXT,
            'giris_saat'   TEXT,
            'cikis_saat'   TEXT
            );""".format('people'))
        else:
            pass
        self.data.commit()
        self.data.close()
    def create_database_2(self):
        self.data = sqlite3.connect("database/members.db")
        self.veri = self.data.cursor()
        if self.veri.execute("SELECT name FROM sqlite_master").fetchone() == None:
            self.veri.execute("""CREATE TABLE {} (
            'ad_soyad'	TEXT,
            'TC_no'    TEXT,
            'kart_id'  TEXT,
            'kayit_tarihi' TEXT
            );""".format('people'))
        else:
            pass
        self.data.commit()
        self.data.close()
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
        self.frame_two.config(bg="#ffffff")
        self.frame_two.grid(row=0,column=0)
        self.frame_two.grid_remove()

        self.frame_three = Frame(self.parent)
        self.frame_three.grid(row=0,column=0)
        self.frame_three.grid_remove()

        #self.parent.attributes("-fullscreen", True)
        self.parent.geometry('572x615')
        self.parent.bind('<Escape>',quit)
        self.parent.title('Kuluçka Merkezi doorLock')
        self.database = configure_class()
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
        self.serial_port = 'X'
        self.backup = "loop_end"
        self.variable = StringVar()
        self.address = os.getcwd()
        self.hata = True
        self.dot = "."
        self.message = ""
        self.serial_durdur = "loop_end"

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
        ################ functions ####################
        self.configure_interface()
        self.start_interface()
        self.ip_adres_ogren()
        if self.hata:
            self.serial_ogren()
        if self.hata:
            self.raspbery_durum_ogren()
    def serial_ogren(self):
        if verbose:
            print('>>>user_interface.serial_ogren() fonksiyonuna giris yapiliyor...')
        self.port_counter = 0
        hata = True
        port_x = "COM"
        while hata:
            try:
                port = port_x + str(self.port_counter)
                ard = serial.Serial(port ,9600,timeout=2)
                hata = False
                self.serial_port = "COM3" #port

            except Exception as error_name:
                if verbose:
                    print('3__' + str(error_name))
                else:
                    pass
                self.port_counter = self.port_counter + 1
                if self.port_counter == 11:
                    self.hata = False
                    self.variable1.set("Ardiuno bağlanmamış.")
                    break
        if verbose:
            print('<<<user_interface.serial_ogren() fonksiyonundan cikis yapiliyor...')
    def raspbery_durum_ogren(self):
        if verbose:
            print('>>>user_interface.raspbery_durum_ogren() fonksiyonuna giris yapiliyor...')
        try:
            ip = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ip.connect((config['veri']['raspberry_ip'], int(config['veri']['raspberry_port'])))
            ip.close()
        except Exception as error_name:
            print('4__' + str(error_name))
            self.hata = False
            self.variable1.set("Kapı Çalışmıyor.")
            if verbose:
                print(error_name)
            else:
                pass
        if verbose:
            print('<<<user_interface.raspbery_durum_ogren() fonksiyonundan cikis yapiliyor...')
    def ip_adres_ogren(self):
        if verbose:
            print('>>>user_interface.ip_adres_ogren() fonksiyonuna giris yapiliyor...')
        try:
            ip = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ip.connect(("8.8.8.8", 80))
            self.ip_adres = (ip.getsockname()[0])
            ip.close()
        except Exception as error_name:
            print('5__'+ str(error_name))
            self.hata = False
            self.variable1.set("İnternet Bağlantınız yok.")
            if verbose:
                print(error_name)
            else:
                pass
        if verbose:
            print('<<<user_interface.ip_adres_ogren() fonksiyonundan cikis yapiliyor...')
    def configure_interface(self):
        if verbose:
            print('>>>user_interface.start_gui() fonksiyonuna giris yapiliyor...')

        self.frame_buttons = Frame(self.frame_two)
        #################################### Buttons ##########################################
        self.ekle    = Button(self.frame_buttons,text = ' + ',wraplength=750,anchor="center",height=2,width=20,highlightbackground=self.bg,font ="Helvetica 15 bold italic",fg=self.bg,command=self.ekle_members)
        self.ekle.grid(row=0,column=0, sticky=W,padx= 0, pady = 0)
        self.cikar    = Button(self.frame_buttons,text = ' - ',wraplength=750,anchor="center",height=2,width=20,highlightbackground=self.fg,font ="Helvetica 15 bold italic",fg=self.bg,command=self.sil_members)
        self.cikar.grid(row=0,column=1, sticky=W,padx= 0, pady = 0)
        self.durdur    = Button(self.frame_buttons,text =  "Kart Okuma Kapalı",wraplength=750,anchor="center",height=2,width=20,highlightbackground=self.fg,font ="Helvetica 15 bold italic",fg=self.bg,command=self.serial_degistir)
        self.durdur.grid(row=0,column=2, sticky=W,padx= 0, pady = 0)

        #################################### Menu #####################################33
        #self.exit.add_command(label="Exit", command=self.parent.destroy)
        self.menu.add_cascade(label="Giriş - Çıkış Kayıtları", command=self.requeset_data)
        self.menu.add_cascade(label=" | ")
        self.menu.add_cascade(label="Üye İşlemleri", command=self.requeset_data_2)


        if verbose:
            print('<<<user_interface.start_gui() fonksiyonundan cikis yapiliyor...')
    def sil_members(self):
        selected_item = self.tree_2.selection()[0] ## get selected item
        self.tree_2.delete(selected_item)
        sira = 0;
        #
        if selected_item[-1] != 0:
            if selected_item[-2] != 0:
                if selected_item[-3] != 0:
                    sira = int(str(selected_item[-3]) + str(selected_item[-2]) + str(selected_item[-1]))
                else:
                    sira = int(str(selected_item[-2]) + str(selected_item[-1]))
            else:
                sira = int(selected_item[-1])
        else:
            sira = 0

        #
        print(self.members_list[sira-1])
        self.send_data_ = "delete" + "," + str(self.members_list[sira-1][0]) + "," + str(self.members_list[sira-1][2])
        self.send_raspberry()

    def ekle_members(self):

        self.popup = Toplevel()
        self.popup.geometry('370x155')
        self.popup.configure(background=self.bg)
        self.grid(sticky=(N, S, W, E))
        self.popup.grid_rowconfigure(0, weight=0)
        self.popup.grid_columnconfigure(0, weight=0)

        self.popup_frame_one = Frame(self.popup)
        self.popup_frame_one.configure(background=self.bg)
        self.frame_one.grid(row=0,column=0)
        self.popup_frame_two = Frame(self.popup)
        self.popup_frame_two.configure(background=self.bg)
        self.popup_frame_two.grid(row=0,column=0)

        self.text_1        = Label(self.popup_frame_two,textvariable=self.variable1,borderwidth=0,bg=self.bg,fg=self.fg,font ="Helvetica 25 bold italic")
        self.text_1.grid(row=0,column=1,padx=50,pady=55,rowspan=3,columnspan = 2)
        self.variable1.set("Kart Bilgisi Bekleniyor")

        self.name          = Entry(self.popup_frame_one ,font ="Helvetica 12 bold italic")
        self.name.grid(row=0,column=1,padx=0,pady = 5)
        self.studentNumber       = Entry(self.popup_frame_one ,font ="Helvetica 12 bold italic")
        self.studentNumber.grid(row=1,column=1,padx=0,pady = 5)
        self.TC_NO = Entry(self.popup_frame_one ,font ="Helvetica 12 bold italic")
        self.TC_NO.grid(row=2,column=1,padx=0,pady = 5)

        self.text_2        = Label(self.popup_frame_one ,text=" Ad-Soyad Giriniz :            ",bg=self.bg,fg=self.fg,justify = LEFT,font ="Helvetica 15 bold italic")
        self.text_2.grid(row=0,column=0,padx=0,pady = 5)
        self.text_3        = Label(self.popup_frame_one,text=" Öğrenci Numarasi Giriniz :",borderwidth=0,bg=self.bg,justify = LEFT,fg=self.fg,font ="Helvetica 15 bold italic")
        self.text_3.grid(row=1,column=0,padx=0,pady = 5)
        self.text_4        = Label(self.popup_frame_one,text=" TC. Kimlik No Giriniz  :      ",borderwidth=0,bg=self.bg,justify = LEFT,fg=self.fg,font ="Helvetica 15 bold italic")
        self.text_4.grid(row=2,column=0,padx=0,pady = 5)

        self.sendButton    = Button(self.popup_frame_one,text = 'Bilgiyi Gönder',wraplength=750,anchor="center",height=1,width=13,highlightbackground=self.fg,font ="Helvetica 15 bold italic",fg=self.bg,command=self.send_data)
        self.sendButton.grid(row=3,column=0, sticky=W,padx= 120, pady = 25,columnspan=2,rowspan=1)
        self.serial_degistir()
    def serial_degistir(self):
        if verbose:
            print('>>>user_interface.serial_degistir() fonksiyonuna giris yapiliyor...')
        if self.serial_durdur ==  "loop_end":
            self.serial_durdur = None
            self.durdur["text"] = "Kart Okuma Açık"
        else:
            self.serial_durdur =  "loop_end"
            self.durdur["text"] = "Kart Okuma Kapalı"
        if verbose:
            print('<<<user_interface.serial_degistir() fonksiyonundan cikis yapiliyor...')
    def read_serial(self):

        if self.serial_durdur != "loop_end" :
            if verbose:
                print('>>>user_interface.read_serial() fonksiyonuna giris yapiliyor...')
            ard = serial.Serial(self.serial_port ,9600,timeout=2)
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
                self.popup_frame_two.grid_remove()
                self.popup_frame_one.grid(row=0,column=0)
            else:
                self.message = ""
            if verbose:
                print('<<<user_interface.read_serial() fonksiyonundan cikis yapiliyor...')
        root.after(300,run.read_serial)
    def treeview_login_exit(self):
        self.frame_two.grid_remove()
        self.frame_one.grid(row=0,column=0)
        self.tree_1 = tkinter.ttk.Treeview(self.frame_one, height=30)
        self.tree_1.place(x=55, y=95)
        # self.tree_1.configure(bg = self.bg)
        vsb = tkinter.ttk.Scrollbar(self.frame_one, orient="vertical", command=self.tree_1.yview)
        vsb.place(x = 552, y=5, height=605)
        self.tree_1.configure(yscrollcommand=vsb.set)

        self.tree_1['columns'] = ('starttime', 'endtime', 'status','status_1')
        # -------------------------------------------------------
        self.tree_1.heading("#0", text='Numara', anchor='center')
        self.tree_1.column("#0", anchor="center", width=50, minwidth=35)  # W,N,S,
        # -------------------------------------------------------
        self.tree_1.heading('starttime', text='TC Kimlik No', anchor='center')
        self.tree_1.column('starttime', anchor='center', width=100, minwidth=130)
        # -------------------------------------------------------
        self.tree_1.heading('endtime', text='Adı - Soyadı', anchor='center')
        self.tree_1.column('endtime', anchor='center', width=150, minwidth=125)
        # -------------------------------------------------------
        self.tree_1.heading('status', text='Giriş Tarih', anchor='center')
        self.tree_1.column('status', anchor='center', width=130, minwidth=0)
        # -------------------------------------------------------
        self.tree_1.heading('status_1', text='Giriş Saati', anchor='center')
        self.tree_1.column('status_1', anchor='center', width=138, minwidth=0)
        # -------------------------------------------------------
        self.tree_1.grid(sticky=(N, S, W, E), row=0, column=0, padx=0, pady=0, columnspan=12, rowspan=4)
        self.canvas = Canvas(self.tree_1, relief=SUNKEN, borderwidth=2)  # ,
        self.vscroll = Scrollbar(self.tree_1, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vscroll.set)
        self.tree_1.grid_rowconfigure(0, weight=1)
        self.tree_1.grid_columnconfigure(0, weight=1)
        self.data = sqlite3.connect("database/register.db")
        self.veri = self.data.cursor()
        sira = 1
        okunan = self.veri.execute("select * from people").fetchall()
        for i in okunan:
            veri = i[2].split(' ')
            self.tree_1.insert('', 'end', text= sira, values=(i[1],i[0],veri[0],veri[1]))
            sira = sira + 1
        self.data.commit()
        self.data.close()
    def treeview_users(self):
        self.frame_one.grid_remove()
        self.frame_two.grid(row=0,column=0)

        self.tree_2 = tkinter.ttk.Treeview(self.frame_two, height=27)
        self.tree_2.grid(row=0,column=0,rowspan=9)

        # self.tree_2.configure(bg = self.bg)
        vsb = tkinter.ttk.Scrollbar(self.frame_two, orient="vertical", command=self.tree_2.yview)
        vsb.place(x = 553, y=0, height=564)
        self.tree_2.configure(yscrollcommand=vsb.set)

        self.tree_2['columns'] = ('starttime', 'endtime', 'status')
        # -------------------------------------------------------
        self.tree_2.heading("#0", text='Numara', anchor='center')
        self.tree_2.column("#0", anchor="center", width=40, minwidth=35)  # W,N,S,
        # -------------------------------------------------------
        self.tree_2.heading('starttime', text='TC Kimlik No', anchor='center')
        self.tree_2.column('starttime', anchor='center', width=145, minwidth=130)
        # -------------------------------------------------------
        self.tree_2.heading('endtime', text='Adı - Soyadı', anchor='center')
        self.tree_2.column('endtime', anchor='center', width=195, minwidth=125)
        # -------------------------------------------------------
        self.tree_2.heading('status', text='Kayıt Tarihi', anchor='center')
        self.tree_2.column('status', anchor='center', width=185, minwidth=0)
        # -------------------------------------------------------
        self.tree_2.grid(sticky=(N, S, W, E), row=0, column=0, padx=0, pady=0, columnspan=12, rowspan=4)
        self.canvas = Canvas(self.tree_2, relief=SUNKEN, borderwidth=2)  # ,
        self.vscroll = Scrollbar(self.tree_2, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vscroll.set)
        self.tree_2.grid_rowconfigure(0, weight=1)
        self.tree_2.grid_columnconfigure(0, weight=1)
        self.data = sqlite3.connect("database/members.db")
        self.veri = self.data.cursor()
        sira = 1
        okunan = self.veri.execute("select * from people").fetchall()
        self.members_list = []
        for i in okunan:
            veri = i[2].split(' ')
            self.members_list.append([i[0],i[1],i[2],i[3]])
            self.tree_2.insert('', 'end', text= sira, values=(i[1],i[0],i[3]))
            sira = sira + 1
        self.data.commit()
        self.data.close()

        self.frame_buttons.grid(row=10,column=0,pady=0)
    def send_data(self):
        if verbose:
            print('>>>user_interface.send_data() fonksiyonuna giris yapiliyor...')
        if self.name.get() == "" or self.name.get() == " " or self.name.get() == " " or self.name.get() == "   ":
            self.name.insert(0, '')
            self.name.insert(0, 'Boş Birakilamaz.')
        if self.studentNumber.get() == "" or self.studentNumber.get() == " " or self.studentNumber.get() == "  " or self.studentNumber.get() == "   ":
            self.studentNumber.insert(0, 'Boş Birakilamaz.')
        if self.TC_NO.get() == ""  or self.TC_NO.get() == " " or self.TC_NO.get() == "  " or self.TC_NO.get() == "   ":
            self.TC_NO.insert(0, 'Boş Birakilamaz.')

        if self.name.get() != "" and self.name.get() != "Boş Birakilamaz." and self.name.get() != " " and self.name.get() != " " and self.name.get() != "   ":
            if self.studentNumber.get() != "" and self.studentNumber.get() != "Boş Birakilamaz." and self.studentNumber.get() != " " and self.studentNumber.get() != "  " and self.studentNumber.get() != "   ":
                if self.TC_NO.get() != "" and self.TC_NO.get() != "Boş Birakilamaz." and self.TC_NO.get() != " " and self.TC_NO.get() != "  " and self.TC_NO.get() != "   ":
                    self.backup = "loop_end"
                    if verbose:
                        print("""
                        Gönderilecek Veriler:
                        Name           : {}
                        Numarası       : {}
                        TC No.         : {}
                        Kart Numarasi  : {}
                        """.format(self.name.get(),self.studentNumber.get(),self.TC_NO.get(),self.message))

                    self.send_data_ = str(self.name.get()) + "," + str(self.TC_NO.get()) + "," + str(self.message)+ ","+str(datetime.today().strftime("%d / %m / %y | %H:%M:%S"))
                    self.message = ""
                    self.name.delete(0, "end")
                    self.studentNumber.delete(0, "end")
                    self.TC_NO.delete(0, "end")
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
        self.popup.destroy()
        self.frame_two.grid_remove()
        self.frame_one.grid(row = 0, column = 0)
    def send_raspberry(self):
        if verbose:
            print('>>>user_interface.send_raspberry() fonksiyonuna giris yapiliyor...')
        self.hata = False
        while not(self.hata):
            self.dot = self.dot + '.'
            if self.dot == '....':
                self.dot = ""
            self.variable2.set("Bilgiler Gönderiliyor" + self.dot)
            try:
                veri = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                veri.connect((config['veri']['raspberry_ip'], int(config['veri']['raspberry_port'])))
                print('-----',self.send_data_)
                self.send_data_ = self.send_data_.encode('utf-8')
                veri.send(self.send_data_)
                #data = s.recv(1024) #alinan veri
                veri.close()
                self.hata = True
            except Exception as error_name:
                self.hata = False
                if verbose:
                    print('1__' + str(error_name))
                else:
                    pass

        self.backup = 'loop_end'
        if verbose:
            print('<<<user_interface.send_raspberry() fonksiyonundan cikis yapiliyor...')
        self.start_interface()
    def data_waiting(self):

        if self.backup != 'loop_end' and self.hata:
            self.dot = self.dot + '.'
            if self.dot == '....':
                self.dot = ""
            if self.message == "":
                text = "Kart Bilgisi Bekleniyor" + self.dot
                if text == "Kart Bilgisi Bekleniyor....":
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
        self.frame_two.grid_remove()
        self.frame_one.grid(row = 0 ,column = 0)

        if verbose:
            print('<<<user_interface.read_data_interface() fonksiyonundan cikis yapiliyor...')
    def start_interface(self):
        if verbose:
            print('>>>user_interface.start_interface() fonksiyonuna giris yapiliyor...')
        self.frame_one.grid_remove()
        self.frame_two.grid(row = 0 ,column =0)
        self.treeview_login_exit()

        self.backup = None
            #self.text_variable.grid(row=0,column=1,padx=0,pady = 0,rowspan=1,columnspan=1)
        if verbose:
            print('<<<user_interface.start_interface() fonksiyonundan cikis yapiliyor...')
    def requeset_data(self):
        if verbose:
            print('>>>user_interface.requeset_data() fonksiyonuna giris yapiliyor...')
        hata = True
        self.backup = 'loop_end'
        while hata:
            try:
                veri = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                veri.connect((config['veri']['raspberry_ip'], int(config['veri']['raspberry_port'])))
                text = str(True)  + "," + self.ip_adres
                text = text.encode('utf-8')
                veri.send(text)
                veri.recv(int(config['veri']['raspberry_buffer_size'])) #alinan veri
                veri.close()

                mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                mysocket.bind((self.ip_adres, int(config['veri']['raspberry_port'])))
                mysocket.listen(5)
                (client, (ip,port)) = mysocket.accept()
                client.send(b"knock knock knock, I'm the server")
                data = client.recv(int(config['veri']['raspberry_buffer_size']))
                alinan = data.decode()
                mysocket.close()
                self.alinan_veri = alinan
                hata = False
            except Exception as error_name:
                if verbose:
                    print('2__' +str(error_name))
                else:
                    pass
                hata = True
        self.giris_cikis_goster()
        self.backup = None
        if verbose:
            print('<<<user_interface.requeset_data() fonksiyonundan cikis yapiliyor...')
    def requeset_data_2(self):
        if verbose:
            print('>>>user_interface.requeset_data_2() fonksiyonuna giris yapiliyor...')
        hata = True
        self.backup = 'loop_end'
        while hata:
            try:
                veri = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                veri.connect((config['veri']['raspberry_ip'], int(config['veri']['raspberry_port'])))
                text = str(False)  + "," + self.ip_adres
                print('---',text)
                text = text.encode('utf-8')
                veri.send(text)
                veri.recv(int(config['veri']['raspberry_buffer_size'])) #alinan veri
                veri.close()

                mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                mysocket.bind((self.ip_adres, int(config['veri']['raspberry_port'])))
                mysocket.listen(5)
                (client, (ip,port)) = mysocket.accept()
                client.send(b"knock knock knock, I'm the server")
                data = client.recv(int(config['veri']['raspberry_buffer_size']))
                alinan = data.decode()
                mysocket.close()
                self.alinan_veri = alinan
                hata = False
            except Exception as error_name:
                if verbose:
                    print('2__' +str(error_name))
                else:
                    pass
                hata = True
        self.user_goster()
        self.backup = None
        if verbose:
            print('<<<user_interface.requeset_data_2() fonksiyonundan cikis yapiliyor...')
    def giris_cikis_goster(self):
        if not(os.path.isfile("database/register.db")):
            pass
        else:
            os.remove("database/register.db")
            self.database.create_database_1()

        self.data = sqlite3.connect("database/register.db")
        self.veri = self.data.cursor()
        sayac= 0
        self.alinan_veri = self.alinan_veri.split(',')
        for i in range(0,(len(self.alinan_veri) -1 )//4):
            self.veri.execute("INSERT INTO people (ad_soyad,TC_Kimlik_No,giris_saat,cikis_saat) VALUES (?,?,?,?)",(self.alinan_veri[1+sayac],self.alinan_veri[2+sayac],self.alinan_veri[3+sayac],self.alinan_veri[4+sayac]))
            self.data.commit()
            sayac = sayac + 4

        self.alinan_veri = ","
        self.data.close()
        self.treeview_login_exit()
    def user_goster(self):
        if not(os.path.isfile("database/members.db")):
            pass
        else:
            os.remove("database/members.db")
            self.database.create_database_2()

        self.data = sqlite3.connect("database/members.db")
        self.veri = self.data.cursor()
        sayac= 0
        self.alinan_veri = self.alinan_veri.split(',')
        print(self.alinan_veri)
        for i in range(0,(len(self.alinan_veri) -1 )//4):
            self.veri.execute("INSERT INTO people (ad_soyad,TC_no,kart_id,kayit_tarihi) VALUES (?,?,?,?)",(self.alinan_veri[1+sayac],self.alinan_veri[2+sayac],self.alinan_veri[3+sayac],self.alinan_veri[4+sayac]))
            self.data.commit()
            sayac = sayac + 4

        self.alinan_veri = ","
        self.data.close()
        self.treeview_users()


if __name__ == "__main__":
    connect = configure_class()
    root = Tk()
    root.call('tk', 'scaling', 1.0)
    run = user_interface(root)
    root.after(1000,run.data_waiting)
    root.after(1000,run.read_serial)
    root.mainloop()
