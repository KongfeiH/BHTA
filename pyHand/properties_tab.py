#  properties_tab.py
#  
#  ~~~~~~~~~~~~
#  
#  Property Management
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
#IMPORTS#
#########
from Tkinter import *
import ttk
from pickles import load_puck_units as property_list
from IntegerEntry import *
from tkFont import *

from pyHand_API.pyHand_api import *


##################
#GLOBAL VARIABLES#
##################
properties = property_list()
keys=["Property"]
if properties!=None:
    keys = list(properties.keys())
alphaKeys = sorted(keys)
alphaKeys.remove("Property")
activePucks = [False, False, False, False]
selectedButton = None
output = None

#creates and returns a frame whose master is given as an argument
#this frame allows a client to get, set, and save properties of one of the four pucks in the hand
def create_property_frame(master):
    '''
    Populates the property management section of maintenance tab with its contents

    @param master: the frame on which widgets are placed
    @type master: any variation of Frame (such as labelFrame) tkinter widget
    '''
    frame = Frame(master)

    #this frame holds the four buttons which allow a user to select an active puck
    puckFrame = Frame(frame)
    f1 = Button(puckFrame, text = "Finger 1",
                command = lambda: setActivePuck([f1, f2, f3, f4], 11))
    f2 = Button(puckFrame, text = "Finger 2",
                command = lambda: setActivePuck([f1, f2, f3, f4], 12))
    f3 = Button(puckFrame, text = "Finger 3",
                command = lambda: setActivePuck([f1, f2, f3, f4], 13))
    f4 = Button(puckFrame, text = "Spread",
                command = lambda: setActivePuck([f1, f2, f3, f4], 14))

    f1.grid(column = 0, row = 0, sticky = 'ew')
    f2.grid(column = 1, row = 0, sticky = 'ew')
    f3.grid(column = 2, row = 0, sticky = 'ew')
    f4.grid(column = 3, row = 0, sticky = 'ew')
    
    puckFrame.grid(column = 0, row = 0, columnspan = 4, pady = 5, padx = 3, sticky = 'ew')
    
    value = StringVar()
    propSelection = StringVar()
    vl = Label(frame, text = "Value")
    e = IntegerEntry(frame, textvariable = value)
    vl.grid(column = 0, row = 1, sticky = 'ew')
    e.grid(column = 1, row = 1, sticky = 'nesw', pady = 3, padx = 3)

    options = OptionMenu(frame, propSelection, command = lambda x: check_property(propSelection.get(), getb, setb, saveb), *alphaKeys)
    propSelection.set("Select A Property")
    options.grid(column = 0, columnspan = 3, sticky = 'ew', row = 2, padx = 3, pady = 2)

    propDescription = Button(frame, text = "Get Property Description", command = lambda: getPropDescription(propSelection))
    propDescription.grid(column = 0, columnspan = 3, sticky = 'ew', row = 3, padx = 5, pady = 2)
    
    getb = Button(frame, text = "Get", bg = "#62CC68", state = DISABLED, command = lambda: getProperty(propSelection, value))
    setb = Button(frame, text = "Set", bg = "#62CC68", state = DISABLED, command = lambda: setProperty(propSelection, value))
    saveb = Button(frame, text = "Save", bg = "#62CC68", state = DISABLED, command = lambda: saveProperty(propSelection))
    getb.grid(column = 3, row = 1, sticky = 'ew', padx = 3, pady = 2)
    setb.grid(column = 3, row = 2, sticky = 'ew', padx = 3, pady = 2)
    saveb.grid(column = 3, row = 3, sticky = 'ew', padx = 3, pady = 2)

##    frame.rowconfigure(1, weight = 1)
##    frame.rowconfigure(2, weight = 1)
##    frame.rowconfigure(3, weight = 1)
    
    return frame

def check_property(propKey, getb, setb, saveb):
    '''
    Gets the property ID and sees if the property can be read, set, or saved, disableing/enabling the buttons

    @param propKey: a string representing a property from the drop down menu
    @type propKey: string

    @param getb: a button that is disabled/enabled based on the property
    @type getb: tkinter button widget
    
    @param setb: a button that is disabled/enabled based on the property
    @type setb: tkinter button widget
    
    @param saveb: a button that is disabled/enabled based on the property
    @type saveb: tkinter button widget
    '''
    prop = getID(propKey)
    if prop in NO_WRITE_PROPERTIES:
        setb.configure(state = DISABLED)
    else:
        setb.configure(state = NORMAL)

    if prop in NO_READ_PROPERTIES:
        getb.configure(state = DISABLED)
    else:
        getb.configure(state = NORMAL)

    if properties[propKey][4] == "No":
        saveb.configure(state = DISABLED)
    else:
        saveb.configure(state = NORMAL)

    if prop in LOCKED_PROPERTIES:
        setb.configure(state = DISABLED)
        saveb.configure(state = DISABLED)

def create_output_frame(master):
    '''
    Takes in a parent frame and returns a frame with a master frame equal to the parent frame. The returned frame has a textbox that is used as an output window

    @param master: the frame on which widgets are placed
    @type master: any variation of Frame (such as labelFrame) tkinter widget
    '''
    global output
    textframe = Frame(master)
    scroll = Scrollbar(textframe)
    output = Text(textframe, wrap = WORD, height = 10, yscrollcommand = scroll.set)
    scroll.config(command=output.yview)
    scroll.pack(side="right", fill="y")
    output.pack(side="left", fill = "x", expand = True)
    output.configure(state = DISABLED)
    textframe.grid(column = 0, row = 0)
    
    return textframe

def disable_list(widget_list):
    '''
    Takes a list of widgets and recursively calls the disable function of each of the widgets in the list

    @param widget_list: the list of widgets to be disabled
    @type widget_list: a list of tkinter widgets
    '''
    for widget in widget_list:
        disable(widget)

def disable(widget):
    '''
    Takes a widget and disables all of the sub-widgets of this widget

    @param widget: the widget of which the subwidgets will be disabled
    @type widget: any tkinter widget
    '''
    if widget == None:
        return
    else:
        if widget.winfo_class()=="TLabelframe" or widget.winfo_class()=="TFrame" or widget.winfo_class()=="Frame" or widget.winfo_class()=="Labelframe":
            disable_list(widget.grid_slaves())
            disable_list(widget.pack_slaves())
        else:
            if widget.winfo_class()!="Scrollbar":
                widget.configure(state = DISABLED)

def enable_list(widget_list):
    '''
    Takes a list of widgets and recursively calls the enable function of each of the widgets in the list

    @param widget_list: the list of widgets to be enable
    @type widget_list: a list of tkinter widgets
    '''
    for widget in widget_list:
        enable(widget)

def enable(widget):
    '''
    Takes a widget and enabled all of the sub-widgets of this widget

    @param widget: the widget of which the subwidgets will be enabled
    @type widget: any tkinter widget
    '''
    if widget == None:
        return
    else:
        if widget.winfo_class()=="TLabelframe" or widget.winfo_class()=="TFrame" or widget.winfo_class()=="Frame" or widget.winfo_class()=="Labelframe":
            enable_list(widget.grid_slaves())
            enable_list(widget.pack_slaves())
        else:
            if widget.winfo_class()!="Scrollbar":
                widget.configure(state = NORMAL)

#Processing Functions
def write_to_output(text):
    '''
    Write the line to the specified textbox.

    @param text: The line to be written.
    @type text: str
    '''
    global output
    output.configure(state = NORMAL)
    output.insert(END, text)
    output.yview(END)
    output.configure(state = DISABLED)

def getPropDescription(propVar):
    try:
        key = propVar.get()
        description = properties[key][1]
        write_to_output(key + ": " + str(description) + ".\n")
    except:
        write_to_output("Selected property description not found.\n")

def setActivePuck(buttons, num):
    '''
    Sets the active puck to a new one.

    @param buttons: The toggle buttons that set a finger active/inactive
    @type buttons: list of tkinter buttons
    
    @param num: the number of the puck to toggle
    @type num: C{int}
    '''
    global activePucks
    global selectedButton
    activePucks[num - 11] = not activePucks[num - 11]
    for j in range(0, 4):
        if(activePucks[j]):
            buttons[j].configure(bg = 'yellow')
        else:
            buttons[j].configure(bg = 'SystemButtonFace')

    name = getPuckName(num)
    
    if(activePucks[num - 11]):
        write_to_output(name + " is now active.\n")
    else:
        write_to_output(name + " is no longer active.\n")

def getProperty(propVar, entryVar):
    '''
    Gets a property from the active puck.

    @param propVar: The variable holding the property.
    @type propVar: Tkinter.StringVar

    @param entryVar: The entry to hold the E{"}GET E{"}value.
    @type entryVar: IntegerEntry.IntegerEntry
    '''
    if(True in activePucks):
        for j in range(0, len(activePucks)):
            if(activePucks[j]):
                try:
                    val = get_property(j + 11, getID(propVar.get()))
                    write_to_output(getPuckName(j + 11) + ", Property: " + propVar.get() + " is " + str(val) + ".\n")
                except:
                    write_to_output("Failure to get property.\n")
        entryVar.set("")
    else:
        write_to_output("Select hand spread or a finger to continue.\n")

def setProperty(propVar, entryVar):
    '''
    Sets a property to the value in the entry.

    @param propVar: The variable holding the property.
    @type propVar: Tkinter.StringVar
    
    @param entryVar: The entry holding the value to set to.
    @type entryVar: IntegerEntry.IntegerEntry
    '''
    if(True in activePucks):
        for j in range(0, len(activePucks)):
            if(activePucks[j]):
                try:
                    val = int(entryVar.get())
                except:
                    write_to_output("The value in the box is not valid. Please make sure the value is valid and try again.\n")
                    break
                try:
                    set_property(j + 11, getID(propVar.get()), val)
                    write_to_output(getPuckName(j + 11) + ", Property: " + str(propVar.get()) + " has been set to " + str(entryVar.get()) + ".\n")
                except:
                    write_to_output("Failure to set property.\n")
        entryVar.set("")
    else:
        write_to_output("Select hand spread or a finger to continue.\n")

def saveProperty(propVar):
    '''
    Saves a selected property.

    @param propVar: The variable holding the property.
    @type propVar: Tkinter.StringVar
    '''
    if(True in activePucks):
        for j in range(0, len(activePucks)):
            if(activePucks[j]):
                try:
                    save_property(j + 11, getID(propVar.get()))
                    write_to_output(getPuckName(j + 11) + ", Property: " + propVar.get() + " has been saved.\n")
                except:
                    write_to_output("Failure to save property.\n")
    else:
        write_to_output("Select hand spread or a finger to continue.\n")

def getID(string):
    '''
    Uses a pickle dictionary to find the ID of a given property.

    @param string: The string referring to the property. For example, MV for Max Velocity.
    @type string: str
    '''
    return int(properties[string][0])

def getPuckName(num):
    '''
    Returns a name for a puck #

    @param num: the number of the puck to be turned into a name
    @type num: c{int}
    '''
    name = "Finger " + str(int(num - 10))
    if(num == 14):
        name = "Hand Spread"
    return name

def create_properties_tab(master, x, y, handType):
    '''
    Display the properties tab to a master frame.

    @param master: The frame of which the properties widget is a child.
    @type master: Tkinter.Frame
    
    @param x: The column which the properties frame will be gridded to.
    @type x: int

    @param y: The row which the properties frame will be gridded to.
    @type y: int
    
    @param handType: Specifies whether the hand is a 280, 282, or unknown type by returning 1, 0, or -1 respectively.
    @type handType: int
    '''
    wholeFrame = LabelFrame(master, text = "Property Management")
    pframe = create_property_frame(wholeFrame)
    oframe = create_output_frame(wholeFrame)
    pframe.grid(column = 0, row = 0, padx = (0, 5))
    oframe.grid(column = 1, row = 0, padx = 5, pady = (0, 5), sticky = 'ew')
    wholeFrame.grid(column = x, row = y, padx = (25,0), pady=(25,0),sticky = 'new')
    if handType == -1:
        disable(wholeFrame)
