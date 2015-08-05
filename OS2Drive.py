#!/usr/bin/env python3

from threading import Thread
import subprocess
from tkinter import *
import tkinter.ttk as ttk
from queue import Queue
import time
import os
import signal
import shlex


ABOUT_TEXT = "(c) Copyright 2015. Al Poole <netstar@gmail.com>. All Rights Reserved \n" + \
                "    Visit http://haxlab.org for more information!\n\n" + \
                "    Thanks to Sam Watkins, Chris Rahm and Jason Pierce as always!\n\n"

class Application(Frame):
        def __init__(self, master):
                self.myParent = master;
                super(Application, self).__init__(master)
                self.active = False;
                self.process = None
                self.grid()
                self.create_widgets()
                
        # The work engine (seperate thread)
        def work(self):
                if self.process:
                    self.process.terminate() 
                    self.active = False;
                    return
                distro = self.list_distro.get()
                drive = self.list_drives.get() #DANGER!!
                
                cmd = "OS2Drive.exe " + distro + " " + drive # DANGEROUS!!!!!!
                print(cmd)
                self.process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
                self.start_button.configure(state='disabled')

                while True: #self.process.poll() is None:
                    output = self.process.stdout.readline()

                    output = output.decode("utf-8")
                    output = output.rstrip()
                    
                    if output == '':
                        break

                    count = 0
                    count = int(output)
                    
                    if count != 0:
                      self.progress.step(1)

                self.start_button.configure(state='normal')	
                self.process = None

        # Thread for doing the work
        def worker(self):
                self.active = True;
                t = Thread(target=self.work) #, args=(,))
                t.start()

        # Beging process code
        def start(self, *args):
                if self.process:
                    print("nooooooo")
                else:
                    self.worker()

        # Terminate process code
        def stop(self):
                #os.kill(self.process.pid, signal.SIGKILL)
                if self.process:
                        self.process.terminate()
                        self.process = None
                        self.active = False;
                        self.start_button.configure(state='disabled')
        def center(self):
                screen_width = self.myParent.w_info.screenwidth()
                screen_height = self.myParent.w_info.screenheight()

        # Some about program stuff
        def about(self, *args):
                #self.insert_text(ABOUT_TEXT)
                return

                about = Toplevel(width=100,height=100)
                about.title("About")
                label = Label(about, text= "http://haxlab.org")
                label.grid(row=0, sticky=W+N+S+E)
                about.resizable(0, 0)
                about.wm_geometry("300x300")
                about.focus_set()

        # Clear the textbox...
        def clear(self, *args):
                return
                #self.textbox.configure(state='normal')
                #self.textbox.delete(0.0, END)
                #self.textbox.configure(state='disabled')
             
        def create_widgets(self):   
                # This stuff gives me nightmares...nevermind!
                self.frame = Frame(self)
                self.frame.pack(expand=1, fill='both')
      
                  
                # menu configuration
                self.menu = Menu(self.myParent)
                self.filemenu = Menu(self.menu, tearoff = 0)
                self.filemenu.add_command(label="About", command = self.about)
                self.filemenu.add_command(label="Quit", command = quit)
                
                self.label = Label(self.frame, text="OS:")
                self.label.grid(row=0, column=0, sticky=W)
                self.list_distro = Spinbox(self.frame, values=("FreeBSD","NetBSD", "OpenBSD", "Debian", "Fedora", "OpenSUSE", "Ubuntu"))
                self.list_distro.grid(row=0, column=1, sticky=W)
                
                self.label_disk = Label(self.frame, text="Drive to install to:")
                self.label_disk.grid(row=1, column = 0, sticky = W)
                
                self.list_drives = Spinbox(self.frame, values=("E:", "F:"))
                self.list_drives.index(0)
                self.list_drives.grid(row=1, column=1, sticky=W)
                                
                self.progress = ttk.Progressbar(self.frame,max=100, length=100 * 4)
                self.progress.grid(row=2, column=0, columnspan=2,sticky=W)
                # Terminate process if it is active (button)
                self.start_button = Button(self.frame, text = "Write Image", command = self.start)
                self.start_button.grid(row=3, column=0, sticky=W)
                        
                # Set the menu!
                self.myParent.config(menu=self.filemenu)

def main():
        root = Tk()
        root.title("OS2Drive (ALPHA)")
        app = Application(root)
        root.resizable(0, 0)
        root.mainloop()

if __name__ == "__main__":
        main()
