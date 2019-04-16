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

        self.frame_one = Frame(self.parent)
        self.frame_one.grid(row=0,column=0)
        self.frame_one.grid_remove()



        self.frame_two = Frame(self.parent)
        self.frame_two.grid(row=0,column=0)
        self.frame_two.grid_remove()

        #self.parent.attributes("-fullscreen", True)
        self.parent.geometry('380x200')
        self.parent.bind('<Escape>',quit)
        self.parent.title('Kuluçka Merkezi doorLock')

        ################# colors ######################
        self.bg = "#1e0000"
        self.fg = "#ffffff"

        self.parent.configure(background=self.bg )
        self.frame_one.configure(background=self.bg )
        self.frame_two.configure(background=self.bg )



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
        self.text_1        = Label(self.frame_one,text="Kart Bilgisi Bekleniyor...",borderwidth=0,bg=self.bg,fg=self.fg,font ="Helvetica 25 bold italic")
        self.text_1.grid(row=0,column=1,padx=25,pady=80,rowspan=3,columnspan=2)
        #self.text_variable = Label(self.frame_one,textvariable=self.variable,borderwidth=0,bg="#008000")
        self.text_2        = Label(self.frame_text_1 ,text=" İsim Giriniz                            :",bg=self.bg,fg=self.fg,justify = LEFT,font ="Helvetica 15 bold italic")
        self.text_2.grid(row=0,column=0,padx=5,pady = 0)
        self.text_3        = Label(self.frame_text_2,text=" Soyisim Giriniz                     : ",borderwidth=0,bg=self.bg,fg=self.fg,font ="Helvetica 15 bold italic")
        self.text_3.grid(row=1,column=0,padx=5,pady = 0,rowspan=1,columnspan=1)
        self.text_4        = Label(self.frame_text_3,text="Öğrenci Numarasi Giriniz    : ",borderwidth=0,bg=self.bg,fg=self.fg,font ="Helvetica 15 bold italic")
        self.text_4.grid(row=2,column=0,padx=5,pady = 0,rowspan=1,columnspan=1)
        #################################### Enty ############################################

        self.name          = Entry(self.frame_text_1,font ="Helvetica 12 bold italic")
        self.name.grid(row=0,column=1,padx=0,pady = 0,rowspan=1,columnspan=1)
        self.surname       = Entry(self.frame_text_2,font ="Helvetica 12 bold italic")
        self.surname.grid(row=1,column=1,padx=0,pady = 0,rowspan=1,columnspan=1)
        self.studentNumber = Entry(self.frame_text_3,font ="Helvetica 12 bold italic")
        self.studentNumber.grid(row=2,column=1,padx=0,pady = 0,rowspan=1,columnspan=1)


        if verbose:
            print('<<<user_interface.start_gui() fonksiyonundan cikis yapiliyor...')
    def send_data(self):
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
                    print("""
                    Gönderilecek Veriler:
                    Name          : {}
                    Surname       : {}
                    Numarasi      : {}
                    Kart Numarasi : {}
                    """.format(self.name.get(),self.surname.get(),self.studentNumber.get(),self.uuid))


                    self.name.delete(0, "end")
                    self.surname.delete(0, "end")
                    self.studentNumber.delete(0, "end")
                    self.start_interface()
                    root.after(3000,run.data_waiting)

                else:
                    pass
            else:
                pass
        else:
            pass





    def data_waiting(self):
        self.uuid = None
        try:
            if str(os.name) == 'posix': #Linux
                self.read_data = open(self.address  + "/data/read_uuid.txt",'r')
            if str(os.name) == 'nt': #windwos
                self.read_data = open(self.address + "\\data\\read_uuid.txt",'r')
            self.uuid = self.read_data.read()
            self.read_data.close()
            if str(os.name) == 'posix': #Linux
                os.remove(self.address  + "/data/read_uuid.txt")
            if str(os.name) == 'nt': #Windows
                os.remove(self.address  + "\\data\\read_uuid.txt")
        except:
            if verbose:
                print('Veri Bekleniyor..')

        if self.backup != self.uuid and self.uuid != "" and self.uuid != None:
            self.backup = self.uuid
            self.data_read()
        else:
            root.after(1000,run.data_waiting)
    def data_read(self):
        if verbose:
            print('Veri Okundu.')
        self.read_data_interface()

    def read_data_interface(self):
        if verbose:
            print('>>>user_interface.read_data_interface() fonksiyonuna giris yapiliyor...')
            self.frame_one.grid_remove()
            self.frame_two.grid(row = 0 ,column = 0)



        if verbose:
            print('<<<user_interface.read_data_interface() fonksiyonundan cikis yapiliyor...')
    def start_interface(self):
        if verbose:
            print('>>>user_interface.start_interface() fonksiyonuna giris yapiliyor...')
            self.frame_two.grid_remove()
            self.frame_one.grid(row = 0 ,column =0)

            #self.text_variable.grid(row=0,column=1,padx=0,pady = 0,rowspan=1,columnspan=1)
        if verbose:
            print('<<<user_interface.start_interface() fonksiyonundan cikis yapiliyor...')
if __name__ == "__main__":
    connect = configure_class()
    root = Tk()
    root.call('tk', 'scaling', 1.0)
    run = user_interface(root)
    root.after(1000,run.data_waiting)
    root.mainloop()