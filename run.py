#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
from tkinter import *

################ globals #####################
global verbose

verbose = True


############### classes ######################
class configure_class:
    def __init__(self):
        self.create_folder()


    def create_folder(self):
        if verbose:
            print('>>>door_lock.create_folder() fonksiyonuna giris yapılıyor...')
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
            print('<<<door_lock.create_folder() fonksiyonundan cikis yapılıyor...')



    def create_database(self):
        if verbose:
            print('>>>door_lock.create_database() fonksiyonuna giris yapılıyor...')
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
            print('<<<door_lock.create_folder() fonksiyonundan cikis yapılıyor...')
class user_interface(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.frame_one = Frame(self.parent)
        self.frame_one.grid(row=0,column=0)
        self.frame_one.grid_remove()

        self.frame_two = Frame(self.parent)
        self.frame_two.grid(row=0,column=0)
        self.frame_two.grid_remove()
        #self.parent.attributes("-fullscreen", True)
        self.parent.geometry('330x200')
        self.parent.title('Kuluçka Merkezi doorLock')
        self.parent.bind('<Escape>',quit)

        ################# variables ###################

        self.backup = None
        self.variable = StringVar()

        self.address = os.getcwd()

        if str(os.name) == 'posix': #Linux
            self.address = self.address.split('/')
            self.address = self.address[0] + '/' + self.address[1] + '/' + self.address[2] + '/Desktop'
            self.address = self.address + '/doorLock'
        if str(os.name) == 'nt': #Windows
            self.address = str(self.address).split('\\')
            self.address = self.address[0] + '\\' + self.address[1] + '\\' + self.address[2] + '\\Desktop'
            self.address = self.address + '\\doorLock'


        ################ functions ####################
        self.configure_interface()
        self.start_interface()
    def configure_interface(self):
        if verbose:
            print('>>>user_interface.start_gui() fonksiyonuna giris yapılıyor...')
        #################################### Frames ###########################################
        self.frame_text_1 = Frame(self.frame_two)
        self.frame_text_1.grid(row = 0,column = 0,pady = 10,rowspan=1,columnspan =1)
        self.frame_text_2 = Frame(self.frame_two)
        self.frame_text_2.grid(row = 1,column = 0,pady = 10,rowspan=1,columnspan =1)
        self.frame_text_3 = Frame(self.frame_two)
        self.frame_text_3.grid(row = 2,column = 0,pady = 10,rowspan=1,columnspan =1)


        #################################### Buttons ##########################################
        self.exitButton    = Button(self.frame_one,text = 'Exit',wraplength=750,anchor="center",height=1,width=3,highlightbackground="#000000",font ="Helvetica 15 bold italic",fg='#FFFFFF',command=self.parent.destroy)
        self.exitButton.grid(row=3,column=1, sticky=W,padx= 150, pady = 0,columnspan=1,rowspan=2)
        #################################### Labels ###########################################
        self.text_1        = Label(self.frame_one,text="Kart Bilgisi Bekleniyor...",borderwidth=0,bg="#008000")
        self.text_1.grid(row=2,column=1,padx=0,rowspan=1,columnspan=1)
        #self.text_variable = Label(self.frame_one,textvariable=self.variable,borderwidth=0,bg="#008000")
        self.text_2        = Label(self.frame_text_1 ,text="İsim Giriniz                       :",bg="#008000",justify = LEFT)
        self.text_2.grid(row=0,column=0,padx=5,pady = 0)
        self.text_3        = Label(self.frame_text_2,text="Soyisim Giriniz                  :",borderwidth=0,bg="#008000")
        self.text_3.grid(row=1,column=0,padx=5,pady = 0,rowspan=1,columnspan=1)
        self.text_4        = Label(self.frame_text_3,text="Öğrenci Numarası Giriniz :",borderwidth=0,bg="#008000") #23
        self.text_4.grid(row=2,column=0,padx=5,pady = 0,rowspan=1,columnspan=1)
        #################################### Enty ############################################

        self.name          = Entry(self.frame_text_1)
        self.name.grid(row=0,column=1,padx=0,pady = 0)
        self.surname       = Entry(self.frame_text_2)
        self.surname.grid(row=1,column=1,padx=0,pady = 0,rowspan=1,columnspan=1)
        self.studentNumber = Entry(self.frame_text_3)
        self.studentNumber.grid(row=2,column=1,padx=0,pady = 0,rowspan=1,columnspan=1)





        if verbose:
            print('<<<user_interface.start_gui() fonksiyonundan cikis yapılıyor...')
    def data_waiting(self):

        try:
            self.uuid = None
            if str(os.name) == 'posix': #Linux
                self.read_data = open(self.address  + "/data/read_uuid.txt",'r')
            if str(os.name) == 'nt': #windwos
                self.read_data = open(self.address + "\\data\\read_uuid.txt",'r')
            self.uuid = self.read_data.read()
        except:
            if verbose:
                print('Veri Bekleniyor..')

        if self.backup != self.uuid:
            self.backup = self.uuid
            self.data_read()
        else:
            root.after(1000,run.data_waiting)
    def data_read(self):
        print('Veri Okundu.')
        self.read_data_interface()

    def read_data_interface(self):
        if verbose:
            print('>>>user_interface.read_data_interface() fonksiyonuna giris yapılıyor...')
            self.frame_one.grid_remove()
            self.frame_two.grid(row = 0 ,column = 0)


        if verbose:
            print('<<<user_interface.read_data_interface() fonksiyonundan cikis yapılıyor...')
    def start_interface(self):
        if verbose:
            print('>>>user_interface.start_interface() fonksiyonuna giris yapılıyor...')
            self.frame_two.grid_remove()
            self.frame_one.grid(row = 0 ,column =0)
            #self.text_variable.grid(row=0,column=1,padx=0,pady = 0,rowspan=1,columnspan=1)
        if verbose:
            print('<<<user_interface.start_interface() fonksiyonundan cikis yapılıyor...')
if __name__ == "__main__":
    connect = configure_class()
    root = Tk()
    root.call('tk', 'scaling', 1.0)
    run = user_interface(root)
    root.after(1000,run.data_waiting)
    root.mainloop()
