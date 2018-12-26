#  force_torque_tab.py
#  
#  ~~~~~~~~~~~~
#  
#  pyHand Force Toque Tab
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
#  This version of pyHand is free software: you can redistribute it and/or 
#  modify it under the terms of the GNU General Public License as published
#  by the Free Software Foundation.
#

#============================IMPORT=STATEMENTS================================#
import time
from Tkinter import Frame, Label, Entry, Button     #Tkinter Widgets
from Tkinter import BooleanVar, StringVar           #Tkinter Variables
from ftsstr import ftsstr

#============================GLOBAL=DECLARATIONS==============================#
toggle_var = BooleanVar()   #Global Variable controlling processes.


#============================TKINTER=CLASSES===================================#

class FTSFrame:
    '''
    Acts as a Tkinter Label without too much trouble.
    '''

    def update(self):
        '''
        Updates Tkinter labels with FTS data.
        '''
        #print "Updating "+self.prop+" in Tkinter boxes"
        self.configure_data()
        self.data_out.set(self.data)

    def __init__(self,parent_frame,row,column,fts,prop):
        '''
        Creates a box with a label that references the force-torque sensor.

            @param parent_frame: The frame with this widget.
            @type parent_frame: Frame
            @param row: The row to grid this.
            @type row: int
            @param column: The column to grid this.
            @type column: int
            @param fts: The object holding the fts data to use.
            @type fts: ftsstr
            @param prop: The specific force or torque for this widget.
            @type prop: str
        '''
        self.fts = fts
        self.data = float()
        self.prop = prop
        self.configure_data()
        self.configure_box(parent_frame, row, column)
        self.configure_output()
        #class variables not declared here:
        #   self.output = Entry()
        #   self.data_out = StringVar()

    def configure_data(self):
        '''
        Gets fts data from the sensor.
        '''
        if self.prop == "Force X: ":
            self.data = self.fts.forceX
        elif self.prop == "Force Y: ":
            self.data = self.fts.forceY
        elif self.prop == "Force Z: ":
            self.data = self.fts.forceZ
        elif self.prop == "Torque X: ":
            self.data = self.fts.torqueX
        elif self.prop == "Torque Y: ":
            self.data = self.fts.torqueY
        elif self.prop == "Torque Z: ":
            self.data = self.fts.torqueZ
        else:
            raise Exception("Invalid \'prop\' value: \""+prop+": "+"\"\n")

    def configure_box(self, parent_frame, row, column):
        '''
        Creates the frame for the FTS data to be displayed in.
        '''
        box = Frame(parent_frame)
        Label(box, text=self.prop).grid(row=0,column=0)
        #self.output = Text(master=box, width=5, height=0)
        self.output = Label(master=box)
        self.output.grid(row=0,column=1)
        box.grid(row=row, column=column, pady=10, padx=10)

    def configure_output(self):
        '''
        Sets up a StringVar inside which the data will reside.
        '''
        self.data_out = StringVar()
        self.data_out.set(self.data)
        self.output.config(textvariable=self.data_out)

class ErrorLabel(Label):
    def update(self):
        '''
        Repeatedly shows if the error_byte is nonzero.
        '''
        if self.fts.error_byte & 0x80:
            self.config(text="Re-Tare Suggested.\nError: "+hex(self.fts.error_byte))
        else:
            self.config(text="")
    
    def __init__(self, master, sensor):
        Label.__init__(self, master, text="")
        self.fts = sensor

class ToggleButton(Button):
    def __init__(self, master, var, **kw):
        '''
        Toggle data collection on and off.

            @param var: The cariable controlling data collection.
        '''
        Button.__init__(self, master)
        self.config(kw) #There must be a better way to pass this through the constructor itself.
        self.var = var
        self.config(command=self.toggle)

    def toggle(self):
        '''
        Toggles the button on and off.
        '''
        if self.var.get() == 0:
            self.var.set(1)
            self.toggle_on()
        if self.var.get() == 1:
            self.var.set(0)
            self.toggle_off()

    def toggle_on(self):
        '''
        The button's action when on.
        '''
        raise NotImplementedError("Toggle On Command not specified.")

    def toggle_off(self):
        '''
        The button's action when off.
        '''
        raise NotImplementedError("Toggle Off Command not specified.")

class Updater(ToggleButton):
    def update_list(self):
        '''
        Update a list of widgets.
        '''
        for updateable in self.list:
            try:
                updateable.update()
            except Exception as ex:
                print "\n\nFailure to update: ",ex

    def __init__(self, master, to_update, **kw):
        '''
        Makes a button controlling a toggle.

            @param parent_frame: The frame to grid the button to.
            @param to_update: The list of widgets to update.
        '''
        ToggleButton.__init__(self, master, toggle_var)
        self.config(kw)
        self.list = to_update

    def toggle_on(self):
        self.config(text="Stop Force/Torque Data Reading",bg="#B80000")
        while self.var.get() == 1:
            self.update_list()
            time.sleep(.1)

    def toggle_off(self):
        self.config(text="Start Force-Torque Data Reading",bg="#62CC68")

class Tarer(ToggleButton):
    def __init__(self, master, sensor, **kw):
        '''
        Makes a button which will tare the sensor.

            @param master: The frame to grid the button to.
            @param sensor: The ftsstr object to be tared.
        '''
        ToggleButton.__init__(self, master, var=BooleanVar())
        self.config(kw)
        self.fts = sensor

    def toggle_on(self):
        self.config(bg="#B80000")
        self.fts.tare()
        self.config(bg="#63CC68")
        self.var.set(0)

    def toggle_off(self):
        self.config(bg="#B80000")
        self.fts.tare()
        self.config(bg="#63CC68")
        self.var.set(0)

#============================ENABLE/DISABLE=FUNCTIONS=========================#
def disable(widget):
    '''
    Disables all subwidgets of these widgets.

        @param widget: Subwidgets will be disabled.

    '''
    if widget == None:
        return
    else:
        frame_names = ["TLabelframe", "TFrame", "Frame", "Labelframe"]
        if widget.winfo_class() in frame_names:
            disable_list(widget.grid_slaves())
            disable_list(widget.pack_slaves())
        else:
            if widget.winfo_class()!="Scrollbar":
                widget.configure(state='disabled')

def disable_list(widget_list):
    '''
    Disables a list of widgets.

        @param widget_list: List of widgets to be enabled.

    '''
    for widget in widget_list:
        disable(widget)

def enable(widget):
    '''
    Enables all subwidgets of the widget.

        @param widget: Subwidgets will be enabled.
    '''
    if widget == None:
        return
    else:
        frame_names = ["TLabelframe", "TFrame", "Frame", "Labelframe"]
        if widget.winfo_class() in frame_names:
            enable_list(widget.grid_slaves())
            enable_list(widget.pack_slaves())
        else:
            if widget.winfo_class()!="Scrollbar":
                widget.configure(state='normal')

def enable_list(widget_list):
    '''
    Enables a list of widgets.

        @param widget_list: List of widgets to be enabled.
    '''
    for widget in widget_list:
        enable(widget)

#============================MISCELLANIA======================================#

def tab_changed(nb, master_frame, boolvar, sensor_btn, has_fts):
    '''
    Respond to the tab changing.
    '''
    if nb.select() != "" and has_fts:
        current_tab = nb.tab(nb.select(),'text')
        if current_tab == "Force/Torque":
            enable(master_frame)
            sensor_btn.config(text="Start Force/Torque Data Reading",
                              bg='#62CC68')
        if current_tab != "Force/Torque":
            boolvar.set(0)
            disable(master_frame)

def terminate():
    '''
    This function is meant for files outside of this one to end the processes
    with no more imported than minimally needed.
    '''
    global toggle_var
    toggle_var.set(0)

def create_force_torque_tab(nb, has_fts):

    '''
    Display the tab to the root window (nb).

        @param nb: The notebook to display the tab to.
        @param has_fts: Boolean representing whether or not an FTS is attached.
    '''
    force_torque_frame = Frame(nb, name='fts')
    fts = ftsstr()
    global toggle_var
    toggle_var = BooleanVar()
    toggle_var.set(0)

    layout_frame = Frame(force_torque_frame)
    fx = FTSFrame(layout_frame, row=0, column=0, fts=fts, prop="Force X: ")
    fy = FTSFrame(layout_frame, row=1, column=0, fts=fts, prop="Force Y: ")
    fz = FTSFrame(layout_frame, row=2, column=0, fts=fts, prop="Force Z: ")
    tx = FTSFrame(layout_frame, row=0, column=1, fts=fts, prop="Torque X: ")
    ty = FTSFrame(layout_frame, row=1, column=1, fts=fts, prop="Torque Y: ")
    tz = FTSFrame(layout_frame, row=2, column=1, fts=fts, prop="Torque Z: ")
    layout_frame.grid(row=3, column=0)

    error = ErrorLabel(force_torque_frame, sensor=fts)
    error.grid(row=0,column=0, pady=(0,10))
    
    fts_button = Updater(force_torque_frame,
                to_update=[fts,error,fx,fy,fz,tx,ty,tz,force_torque_frame],
                text="Stop Force/Torque Data Reading",
                bg="#62CC68")
    fts_button.grid(row=1, column=0, sticky='nsew',
                pady=(50,15), padx=80)
    
    tare_button = Tarer(force_torque_frame, sensor=fts,
                        text="Tare Force/Torque Sensor",
                        relief='raised', bg="#63CC68")
    tare_button.grid(row=2, column=0, sticky='nsew', pady=(0,15), padx=80)
    
    watchout = lambda x:tab_changed(nb, force_torque_frame,
                                    toggle_var, fts_button, has_fts)
    nb.bind('<<NotebookTabChanged>>', watchout)

    if has_fts==False:
        disable(force_torque_frame)
    
    force_torque_frame.grid(row=0, column=0)
    nb.add(force_torque_frame, text = "Force/Torque")
