import sqlite3
import os
from tkinter import *



################ globals #####################
global verbose

verbose = True



class configure_class:
    def __init__(self):
        self.create_folder()


    def create_folder(self):
        if verbose:
            print('>>>door_lock.create_folder() fonksiyonuna giris yapılıyor...')
        if not(os.path.exists('database/')):
            os.mkdir('database/')
        if not(os.path.exists('conf/')):
            os.mkdir('conf/')

        if verbose:
            print('<<<door_lock.create_folder() fonksiyonundan cikis yapılıyor...')
        self.create_database()


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
        self.frame_two = Frame(self.parent)
        self.frame_two.grid(row=0,column=0)
        self.frame_two.grid_remove()
        self.parent.attributes("-fullscreen", True)
        self.parent.bind('<Escape>',quit)

        self.configure_interface()
        self.start_interface()

    def configure_interface(self):
        if verbose:
            print('>>>user_interface.start_gui() fonksiyonuna giris yapılıyor...')
        #################################### Buttons ##########################################
        self.exitButton = Button(self.frame_one,text = 'Exit',wraplength=750,anchor="center",height=1,width=3,highlightbackground="#000000",font ="Helvetica 15 bold italic",fg='#FFFFFF',command=self.parent.destroy)
        self.exitButton.grid(row=0,column=1, sticky=W,padx= 150, pady = 0,columnspan=1,rowspan=2)
        #################################### Labels ###########################################
        self.text_1 = Label(self.frame_one,text="Kart Bilgisi Bekleniyor...",borderwidth=0,bg="#008000")
        self.text_1.grid(row=2,column=1,padx=85,pady = 60,rowspan=1,columnspan=1)


        if verbose:
            print('<<<user_interface.start_gui() fonksiyonundan cikis yapılıyor...')
    def data_read(self):
        data = False
        if data:
            pass
        else:
            print("False")
            root.after(1000,run.data_read)

    def start_interface(self):
        if verbose:
            print('>>>user_interface.start_gui() fonksiyonuna giris yapılıyor...')


        if verbose:
            print('<<<user_interface.start_gui() fonksiyonundan cikis yapılıyor...')
if __name__ == "__main__":
    connect = configure_class()

    root = Tk()
    root.call('tk', 'scaling', 1.0)
    run = user_interface(root)
    root.after(1000,run.data_read)
    root.mainloop()
