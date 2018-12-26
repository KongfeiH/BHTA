#  gui_main.py
#  
#  ~~~~~~~~~~~~
#  
#  pyHand
#  
#  ~~~~~~~~~~~~
#  
#  ------------------------------------------------------------------
#  Authors : Chloe Eghtebas,
#            Brendan Ritter,
#            Pravina Samaratunga,
#            Jason Schwartz
#  
#  Last change: 08.08.2013
#
#  Language: Python 2.7
#  ------------------------------------------------------------------
# 
#  This version of pyHand is free software: you can 
#  redistribute it and/or modify it under the terms of the GNU General Public
#  License as published by the Free Software Foundation.
#

#########
#Imports#
#########

from Tkinter import *
import ttk as tk
import tkFont
import webbrowser
import tkMessageBox
from PIL import ImageTk
from PIL import Image
root=Tk()
from position_controls_tab import create_position_control_tab
from sensor_tab import create_sensor_tab
from maintenance_tab import create_maintenance_tab
from force_torque_tab import create_force_torque_tab, terminate
from pickles import *
from scrollable_frame import *
from pyHand_API.pyHand_api import *
from auto_resize import *

def center(window):
    '''
    Update the GUI window and center on the screen.

        @param window: The window to be centered.
        @type window: Tkinter.Frame
    '''
    #update the window. This is important!
    window.update()
    
    #get window size
    w=window.winfo_width()
    h=window.winfo_height()
    
    # get screen size ws, hs
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    
    # calculate position x, y with some arbitrary y offset
    x = (ws/2) - (w/2)    
    y = (hs/2) - (h/2) - 40

    # set the window's geometry
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
def correct_size(window,h=835, w=1400):
    '''
    Set the size of the window to the given height and width.

        @param window: The window to be resized.
        @type window: Tkinter.Frame
        @param h: Height of window in pixels.
        @type h: int
        @param w: Width of window in pixels.
        @type w: int
    '''
    window.geometry('%dx%d' % (w,h))

def support_site():
    '''
    Makes a popup window linking to the Barrett Support Site.
    '''
    if tkMessageBox.askokcancel("Barrett Support Site","This link will open your default browser to Barrett's Support Site.\n Click 'OK' to continue."):
        webbrowser.open("http://www.barrett.com/robot/support.htm")
        
def email_support():
    '''
    Makes a popup window to prompt the user to email company support.
    '''
    if tkMessageBox.askokcancel("Email Barrett Support","This link will open your default email application. \nClick 'OK' to continue."):
        webbrowser.open("mailto://support@barrett.com")
        
def about():
    '''
    Dummy function.
    '''
    pass

def wiki_site():
    '''
    Makes a popup window linking to the Barrett Support Wiki.
    '''
    if tkMessageBox.askokcancel("Barrett Support Site","This link will open your default browser to Barrett's Support Site.\n Click 'OK' to continue."):
        webbrowser.open("http://support.barrett.com/wiki/Hand")
    
def create_menu():
    '''
    Creates the file menu at the top of the screen.
    '''
    menubar = Menu(root)

    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Quit", command= windowClose)
    menubar.add_cascade(label="File",menu=filemenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Barrett Support Site", command=support_site)
    helpmenu.add_command(label="Barrett Technology Support Wiki", command= wiki_site)
    helpmenu.add_command(label="Email Barrett Support",command=email_support)
    menubar.add_cascade(label="Help", menu=helpmenu)
    root.config(menu=menubar)

def windowClose():
    '''
    Uninitialize the CAN connection and close the window.
    '''
    try:
        can_uninit()
    except:
        pass
    terminate()
    root.destroy()

def silence(event):
    set_property(0x405, MODE, MODE_IDLE)

def make_loud(event):
    set_property(0x405, MODE, MODE_VEL)          


###########
#MAIN CODE#
###########

#Display loading screen with a progressbar, two labels (one that is updated with the loading state), and the BarrettHand logo
load_bar=tk.Progressbar(root,mode='determinate',length=180, value = 0, maximum  = 7.01)
load_label_1 = Label(root, text = "pyHand is Loading")
load_label_2=Label(root,text="Please Wait")
load_label_1.grid(column = 0, row = 1)
load_bar.grid(column=0,row=2)
load_label_2.grid(column=0,row=3)
photo= ImageTk.PhotoImage(file= "Images/Icons/BTechLogoStacked_small.jpg")
photo_label = Label(root,image=photo, text="I am here")
photo_label.image = photo # keep a reference!
photo_label.grid(row=0, column=0, pady=(10,0))
center(root)
root.title("Loading")
root.update()

#Initialize hand (returns True if can is attached, false if not)
hand_attached = initialize()

#Increment loading screen progressbar and change progress text
load_bar.step()
load_label_2.configure(text = "Detecting/Initializing Hand")
root.update()

tactile = -1
strain = -1
thermistor = -1
handType = -1
if(hand_attached):
    hand_attached = hand_attached & init_hand()

if hand_attached:
    #Increment loading screen progressbar and change progress text
    load_bar.step()
    load_label_2.configure(text = "Parsing Role")
    root.update()

    #Parse the role
    role = get_property(FINGER1, ROLE)
    role_string = bin(role)[2:]
    for j in range(0, 16 - len(role_string)):
        role_string = "0" + role_string

    #Check if a hand has certain features based on role
    strain = int(role_string[4])
    tactile = int(role_string[3])
    thermistor = int(role_string[9])
    #The 2 options are 0 or 7, the division converts the 7 to a 1 to make it more intuitive
    handType = get_property(FINGER1, HALLS) / 7

    #Increment loading screen progressbar and change progress text
    load_bar.step()
    load_label_2.configure(text = "Creating Tabs")
    root.update()
else:
    #Increment loading screen progressbar twice and change progress text
    load_bar.step()
    load_bar.step()
    load_label_2.configure(text = "Loading")
    root.update()
    
    ans = tkMessageBox.askokcancel("Warning!", "There were problems connecting to a Barrett Hand. To continue (Note: most of the function of"
                                   + " the program will be disabled), press OK. Otherwise, press cancel and follow the troubleshooting instructions.", default = tkMessageBox.CANCEL)
    if(ans == False):
        root.destroy()
        sys.exit()

#Change progress text
load_label_2.configure(text = "Creating Tabs")
root.update()

hidden_top=scrollable_frame(root)
hidden_top_internal=hidden_top.internal_frame
tabs = Notebook(master=hidden_top_internal)

#Increment loading screen progressbar
load_bar.step()
root.update()

create_position_control_tab(tabs, handType)#,opengl)

#Increment loading screen progressbar
load_bar.step()
root.update()

#arguments passed to sensor tab tell the tab which sections to display
create_sensor_tab(tabs, tactile, strain, thermistor, handType)

#Increment loading screen progressbar
load_bar.step()
root.update()

create_maintenance_tab(tabs, handType)

load_bar.step()
root.update()
create_force_torque_tab(tabs, 8 in enum())

load_label_1.destroy()
load_label_2.destroy()
load_bar.destroy()
photo_label.destroy()
create_menu()

hidden_top.pack(fill=BOTH,expand=1)
tabs.pack(fill=BOTH,expand=1)
correct_size(root)
center(root)
root.title("pyHand")
root.wm_iconbitmap(bitmap = "Images/Icons/favicon2.ico")
root.update()

root.protocol('WM_DELETE_WINDOW', windowClose)
root.bind('<Control-s>', silence)
root.bind('<Control-v>', make_loud)

root.mainloop()
