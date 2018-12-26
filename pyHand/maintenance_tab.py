#  maintenance_tab.py
#  
#  ~~~~~~~~~~~~
#  
#  pyHand Maintenance Tab
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

##############################IMPORTS##########################################

import Tkinter as tk
from tkFileDialog import *
from ttk import *
import tkMessageBox
import tkFont
from IntegerEntry import *

import time
import math

import pyHand_API.pyHand_api as bt
import properties_tab as properties_tab

##############################GLOBAL_DECLARATIONS##############################

maintenance_frame = tk.Frame()
firmware = tk.Frame()
notebook = 0

##############################ENABLE_DISABLE_FUNCTIONS#########################

def disable_all():
    '''
    Disables all widgets in the window.
    '''
    properties_tab.disable(maintenance_frame)
    disable_tabs()

def enable_all():
    '''
    Enables all widgets in the window.
    '''
    properties_tab.enable(maintenance_frame)
    properties_tab.disable(firmware)
    enable_tabs()

def disable_tabs():
    '''
    Disable notebook tabs.
    '''
    nb = notebook
    tab_list = nb.tabs()
    for tab in tab_list:
        if nb.tab(tab,"text")!="Maintenance":
            nb.tab(tab,state="disabled")

def enable_tabs():
    '''
    Enable notebook tabs.
    '''
    nb = notebook
    tab_list = nb.tabs()
    for tab in tab_list:
        nb.tab(tab,state="normal")

##############################CYCLE_TEST#######################################

def cycle_test(parent_frame,x,y,output):
    '''
    Display the frame that interfaces with cycle_test.

        @param parent_frame: The tkinter frame in which the cycle_test frame is nested.
        @param x: The column of the parent frame that the cycle_test frame is nested in.
        @param y: The row of the parent frame that the cycle_test frame is nested in.
    '''
    cycle_frame=LabelFrame(parent_frame,text="Cycle Test")
    cycle_lbl=Label(cycle_frame,text="Cycles")
    cycle_input=IntegerEntry(cycle_frame,width=10)
    cycle_input.insert(0,10)

    #textframe = Frame(cycle_frame)
    #scroll = tk.Scrollbar(textframe)
    #output = tk.Text(textframe, wrap=tk.WORD, width = 52, height=10, yscrollcommand = scroll.set, state = tk.DISABLED)
    #scroll.config(command=output.yview)
    #scroll.pack(side="right", fill="y")
    #output.pack(side="left", expand = True)
    
    var=tk.BooleanVar()    
    var.set(0)
    start_btn=tk.Button(cycle_frame,text="Start Cycle Test",
                        command = lambda: start_stop_toggle(start_btn, output, cycle_input))
    start_btn.config(bg="#62CC68")
    start_btn.var=var
    
    # gridding for the cycle_test frame
    cycle_lbl.grid(row=0,column=0,padx=(5,0))
    cycle_input.grid(row=0,column=1,padx=(5,0))
    start_btn.grid(row=0, column=2, columnspan=3, sticky="ew", padx=(20,5),
                   ipadx=30, pady=(5,15))
    #textframe.grid(row=0,column=2, rowspan=3, padx=(10,5), sticky=tk.E+tk.W)

    cycle_frame.grid(row=y,column=x,sticky="ewn",padx=(0,0),pady=(0,0))

def start_stop_toggle(btn, textbox, entry):
    '''
    Toggle the cycle_test_command button on and off when pressed.

        @param btn: The tkinter button to be toggled.
        @param textbox: The tkinter textbox to output to.
        @param entry: The tkinter entry widget containing the number of cycles for a cycle test.
    '''
    if btn.var.get() == 0:
        btn.var.set(1)
        disable_all()
        btn.config(text='Stop Cycle Test', fg="black", relief= "raised",
                   bg="#B80000", state=tk.NORMAL)
        cycle_test_command(textbox, int(entry.get()), btn)
    elif btn.var.get()==1:
        btn.var.set(0)
        write_out(textbox, "\nEnding Cycle Test\n")
        enable_all()
        btn.config(text='Start Cycle Test', fg="black", relief=tk.RAISED, bg="#62CC68")
    else:
        print "Cycle Test Start/Stop button malfunctioning."

def cycle_test_command(textbox, cycle_in, btn):
    '''
    Begins cycle test and establish whether or not the hand has strain gauges.
    Executing the appropriate function accordingly.

        @param textbox: The tkinter textbox to output to.
        @param cycle_in: An integer representing the number of cycles to make.
        @param button: A tkinter button controlling the continued execution of this function.
    '''
    textbox.update()
    if btn.var.get()==0:
        write_out(textbox, "\nCycle Test Complete\n")
        btn.config(text='Start', fg="black", relief=tk.RAISED, bg="#62CC68")
        return
    write_out(textbox, "\nInitializing...\n")
    bt.init_hand()

    textbox.update()
    if btn.var.get()==0:
        write_out(textbox, "\nCycle Test Complete\n")
        btn.config(text='Start', fg="black", relief=tk.RAISED, bg="#62CC68")
        return
    
    # Disable self-preservation for this test.
    for p in bt.GRASP:
        bt.set_property(p, bt.STAT, 2) #Wake the puck
        bt.set_property(p, bt.HSG, 10000)
        bt.set_property(p, bt.TSTOP, 50)
    bt.set_property(bt.SPREAD, bt.TSTOP, 150)

    textbox.update()
    if btn.var.get()==0:
        write_out(textbox, "\nCycle Test Complete\n")
        btn.config(text='Start', fg="black", relief=tk.RAISED, bg="#62CC68")
        return
    write_out(textbox, "Program will now run hand for "+str(cycle_in)+" cycles.\n")
    #Check if the hand has strain gauges. Specifically, puck 11.
    has_strain_gauge = bt.get_role(11)[6]
    
    if btn.var.get()==0:
        write_out(textbox, "\nCycle Test Complete\n")
        btn.config(text='Start', fg="black", relief=tk.RAISED, bg="#62CC68")
        return 
    if has_strain_gauge:
        cycle_test_with_sg(textbox, cycle_in, btn)
    else:
        cycle_test_without_sg(textbox, cycle_in, btn)

    btn.var.set(0)
    enable_all()
    btn.config(text='Start Cycle Test', fg="black", relief=tk.RAISED, bg="#62CC68")

def cycle_test_with_sg(textbox, cycle_in, btn):
    '''
    Performs the cycle test loop with the assumption that the hand has strain gauges.

        @param textbox: The tkinter textbox to output to.
        @param cycle_in: An integer representing the number of cycles to make.
        @param button: A tkinter button controlling the continued execution of this function.
    '''
    cycle = 0
    while cycle < cycle_in:
        bt.close_grasp()
        textbox.update()
        if btn.var.get()==0:
            write_out(textbox, "\nHand has now completed "+str(cycle)+" cycles.\n")
            btn.config(text='Start', fg="black", relief=tk.RAISED, bg="#62CC68")
            return
        bt.open_grasp()
        textbox.update()
        if btn.var.get()==0:
            write_out(textbox, "\nHand has now completed "+str(cycle)+" cycles.\n")
            btn.config(text='Start', fg="black", relief=tk.RAISED, bg="#62CC68")
            return
        bt.close_spread()
        textbox.update()
        if btn.var.get()==0:
            write_out(textbox, "\nHand has now completed "+str(cycle)+" cycles.\n")
            btn.config(text='Start', fg="black", relief=tk.RAISED, bg="#62CC68")
            return
        bt.open_spread()
        textbox.update()
        if btn.var.get()==0:
            write_out(textbox, "\nHand has now completed "+str(cycle)+" cycles.\n")
            btn.config(text='Start', fg="black", relief=tk.RAISED, bg="#62CC68")
            return
        bt.can_reset()
        temp1 = bt.get_property(bt.FINGER1, bt.TEMP)
        temp2 = bt.get_property(bt.FINGER2, bt.TEMP)
        temp3 = bt.get_property(bt.FINGER3, bt.TEMP)
        temp4 = bt.get_property(bt.SPREAD, bt.TEMP)
        therm1 = bt.get_property(bt.FINGER1, bt.THERM)
        therm2 = bt.get_property(bt.FINGER2, bt.THERM)
        therm3 = bt.get_property(bt.FINGER3, bt.THERM)
        therm4 = bt.get_property(bt.SPREAD, bt.THERM)
        sg1 = bt.get_property(bt.FINGER1, bt.SG)
        sg2 = bt.get_property(bt.FINGER2, bt.SG)
        sg3 = bt.get_property(bt.FINGER3, bt.SG)

        textbox.update()
        if btn.var.get()==0:
            write_out(textbox, "\nHand has now completed "+str(cycle)+" cycles.\n")
            btn.config(text='Start', fg="black", relief=tk.RAISED, bg="#62CC68")
            return
        cycle += 1
        spaces = " "*(6-len(str(cycle)))
        write_out(textbox, "\n\nCycle: "+str(cycle)+spaces+" TEMP | THERM | STRAIN GAUGE |")
        write_out(textbox, "\n -- Finger 1:   "+str(temp1)+" |    "+str(therm1)+" |         "+str(sg1)+" |")
        write_out(textbox, "\n -- Finger 2:   "+str(temp2)+" |    "+str(therm2)+" |         "+str(sg2)+" |")
        write_out(textbox, "\n -- Finger 3:   "+str(temp3)+" |    "+str(therm3)+" |         "+str(sg3)+" |")
        write_out(textbox, "\n --   Spread:   "+str(temp4)+" |    "+str(therm4)+" |         N/A  |")
    write_out(textbox, "\nHand has now completed "+str(cycle_in)+" cycles.\n")

def cycle_test_without_sg(textbox, cycle_in, btn):
    '''
    Performs the cycle test loop with the assumption that the hand has no strain gauges.

        @param textbox: The tkinter textbox to output to.
        @param cycle_in: An integer representing the number of cycles to make.
        @param button: A tkinter button controlling the continued execution of this function.
    '''
    cycle = 0
    while cycle < cycle_in:
        bt.close_grasp()
        textbox.update()
        if btn.var.get()==0:
            write_out(textbox, "\nHand has now completed "+str(cycle)+" cycles.\n")
            btn.config(text='Start', fg="black", relief=tk.RAISED, bg="#62CC68")
            return
        bt.open_grasp()
        textbox.update()
        if btn.var.get()==0:
            write_out(textbox, "\nHand has now completed "+str(cycle)+" cycles.\n")
            btn.config(text='Start', fg="black", relief=tk.RAISED, bg="#62CC68")
            return
        bt.close_spread()
        textbox.update()
        if btn.var.get()==0:
            write_out(textbox, "\nHand has now completed "+str(cycle)+" cycles.\n")
            btn.config(text='Start', fg="black", relief=tk.RAISED, bg="#62CC68")
            return
        bt.open_spread()
        textbox.update()
        if btn.var.get()==0:
            write_out(textbox, "\nHand has now completed "+str(cycle)+" cycles.\n")
            btn.config(text='Start', fg="black", relief=tk.RAISED, bg="#62CC68")
            return
        bt.can_reset()
        temp1 = bt.get_property(bt.FINGER1, bt.TEMP)
        temp2 = bt.get_property(bt.FINGER2, bt.TEMP)
        temp3 = bt.get_property(bt.FINGER3, bt.TEMP)
        temp4 = bt.get_property(bt.SPREAD, bt.TEMP)
        therm1 = bt.get_property(bt.FINGER1, bt.THERM)
        therm2 = bt.get_property(bt.FINGER2, bt.THERM)
        therm3 = bt.get_property(bt.FINGER3, bt.THERM)
        therm4 = bt.get_property(bt.SPREAD, bt.THERM)
        textbox.update()
        if btn.var.get()==0:
            write_out(textbox, "\nHand has now completed "+str(cycle)+" cycles.\n")
            btn.config(text='Start', fg="black", relief=tk.RAISED, bg="#62CC68")
            return
        cycle += 1
        spaces = " "*(6-len(str(cycle)))
        write_out(textbox, "\n\nCycle: "+str(cycle)+spaces+" TEMP | THERM |")
        write_out(textbox, "\n -- Finger 1:   "+str(temp1)+" |    "+str(therm1)+" |")
        write_out(textbox, "\n -- Finger 2:   "+str(temp2)+" |    "+str(therm2)+" |")
        write_out(textbox, "\n -- Finger 3:   "+str(temp3)+" |    "+str(therm3)+" |")
        write_out(textbox, "\n --   Spread:   "+str(temp4)+" |    "+str(therm4)+" |")
    write_out(textbox, "\nHand has now completed "+str(cycle_in)+" cycles.\n")

##############################SET_DEFAULTS#####################################

def default_properties(parent_frame,x,y,text):
    '''
    Display the frame to interface with the function to reset each puck to its default properties.

        @param parent_frame: The tkinter frame in which the frame containing these buttons resides.
        @param x: The column of the parent frame that this frame is nested in.
        @param y: The row of the parent frame that this frame is nested in.
        @param text: The textbox to which default_properties outputs.
    '''
    def_frame=LabelFrame(parent_frame,text="Set to Default Properties")

    motor_1=tk.Button(def_frame,text="Finger 1",command=lambda:reset_to_def(11, text,motor_1))
    motor_2=tk.Button(def_frame,text="Finger 2",command=lambda:reset_to_def(12, text,motor_2))
    motor_3=tk.Button(def_frame,text="Finger 3",command=lambda:reset_to_def(13, text,motor_3))
    motor_4=tk.Button(def_frame,text="Spread",command=lambda:reset_to_def(14, text,motor_4))

    easy_pack(def_frame,motor_1,motor_2, motor_3,motor_4)
    
    def_frame.grid(row=y,column=x,sticky=tk.E+tk.W, pady=(0, 10))

def reset_to_def(puck,t,btn):
    '''
    Internal wrapper for the bt.set_puck_like(int, int) function.

        @param puck: The integer ID for the motor being communicated with on the CAN bus.
        @param t: A textbox that this function outputs to.
    '''
    disable_all()
    #btn.config(fg="black", relief= "raised", bg="#B80000", state=tk.NORMAL)
    if puck in [11,12,13]:
        write_out(t, "\nSetting finger "+str(puck-10)+" properties to default. Please wait...\n")
    else:
        write_out(t, "\nSetting spread properties to default. Please wait...\n")
    bt.set_puck_like(puck,puck)
    write_out(t, "Properties set to default.\n")
    enable_all()
    btn.config(fg="black", relief="raised", bg="SystemButtonFace")

##############################MOTOR_OFFSET_TEST################################

def motor_offsets(parent_frame,x,y,text):
    '''
    Displays the frame to interface with find_motor_offsets

        @param parent_frame: The tkinter frame in which the frame containing these buttons resides.
        @param x: The column of the parent frame that this frame is nested in.
        @param y: The row of the parent frame that this frame is nested in.
        @param text: The textbox to which find_motor_offsets outputs.
    '''
    motor_frame=LabelFrame(parent_frame,text="Find Motor Offset")

    motor_1=tk.Button(motor_frame,text="Finger 1",
                      command=lambda:mofst_btn_press(11,text,motor_1))
    motor_1.var=tk.IntVar()
    motor_1.var.set(0)
    motor_2=tk.Button(motor_frame,text="Finger 2",
                      command=lambda:mofst_btn_press(12,text,motor_2))
    motor_2.var=tk.IntVar()
    motor_2.var.set(0)
    motor_3=tk.Button(motor_frame,text="Finger 3",
                      command=lambda:mofst_btn_press(13,text,motor_3))
    motor_3.var=tk.IntVar()
    motor_3.var.set(0)
    motor_4=tk.Button(motor_frame,text="Spread",
                      command=lambda:mofst_btn_press(14,text,motor_4))
    motor_4.var=tk.IntVar()
    motor_4.var.set(0)

    easy_pack(motor_frame,motor_1,motor_2, motor_3,motor_4)

    motor_frame.grid(row=y, column=x,sticky=tk.E+tk.W, pady=(10,10))

def mofst_btn_press(puck, text, btn):
    '''
    The middleman function to process the button press and call find_motor_offset.

        @param puck: The motor on which the mofst test is being run.
        @param text: The textbox to which find_motor_offsets outputs.
        @param btn: The tkinter button pressed that activates this function.
    '''
    if btn.var.get() == 0: #Offset test not running.
        are_you_sure_offset_test(btn)
        find_motor_offset(puck, text, btn)
    elif btn.var.get()==1: #Offset Test running
        btn.var.set(0)
    else:
        print "MOFST button malfunctioning."

def are_you_sure_offset_test(btn):
    '''
    Prompts user if they want to continue executing the offset test.
    '''
    if tkMessageBox.askokcancel("Motor Offset Test","WARNING: You are about to execute the Motor Offset Test, "
                                +"which can cause serious damage to your BarrettHand.\n\n"
                                +"If a member of Barrett Technology Inc. has instructed you to test motor "
                                +"offsets, click \"OK\". Otherwise, please excercise utmost caution, and take "
                                +"care not to touch the hand while the test is running."):
        btn.var.set(1)
    else:
        btn.var.set(0)

def hex_wrench_prompt(btn):
    '''
    Prompts user to continue to the Motor Offset portion of the test.
    '''
    if tkMessageBox.askokcancel("Motor Offset Test","To continue, please get a 2mm hex wrench, and loosen the "
                                +"finger. When you are done, press \"OK\". For optimal results, remove the "
                                +"finger of the motor you are testing from the hand completely. If you want "
                                +"to end the Offset Test here, press \"Cancel\"."):
        pass
    else:
        btn.var.set(0)

def find_motor_offset(puck, text, btn):
    '''
    This function performs the motor offset test as specified in /btclient/src/btutils/main.c

        @param puck: The motor on which the mofst test is being run.
        @param text: The textbox to which find_motor_offsets outputs.
        @param btn: The tkinter button pressed that activates this function.
    '''
    btn.update()
    if int(btn.var.get()) ==0:
        return
    disable_all()
    btn.config(fg="black", relief= "raised", bg="#B80000", state=tk.NORMAL)
    text.config(state='normal')
    text.delete((0.0), tk.END)
    text.config(state='disabled')
    samples = 256
    err = 0
    vers= bt.get_property(puck, bt.VERS)
    dat = bt.get_property(puck, bt.IOFST)
    write_out(text, "\nThe old offset (IOFST) was: "+str(dat))
    
    # Get a valid IOFST.
    IOFST_MIN = 1800
    IOFST_MAX = 2230
    IOFST_STDEV = 15.0
    
    # Collect Stats
    sumX = 0
    sumX2= 0
    max_ = -2e9
    min_ = +2e9
    write_out(text, "\nThis may take a while. Please hold.")
    i=0
    while i < samples:
        i+=1
        text.config(state = tk.NORMAL)
        text.delete("4.0", tk.END)
        text.config(state = tk.DISABLED)
        if int(btn.var.get()) ==0:
            enable_all()
            btn.config(fg="black", relief= "raised", bg='SystemButtonFace')
            write_out(text, "\nOffset Test Aborted\n")
            return
        write_out(text, "\nCollecting sample "+str(i)+" of "+str(samples)+".")
        bt.set_property(puck, bt.FIND, bt.IOFST) #Calibrate IOFST
        dat = bt.get_property(puck, bt.IOFST)
        if dat > max_:
            max_ = dat
        if dat < min_:
            min_ = dat
        sumX += dat
        sumX2 += dat*dat

    # Do the math and output it.
    mean = 1.0 * sumX/samples
    stdev = math.sqrt((1.0 * samples * sumX2 - sumX * sumX) / (samples * samples - samples))
    write_out(text, "\nMIN IOFST = "+str(min_))
    if min_ < IOFST_MIN:
        write_out(text, " -- FAIL: Please contact Barrett Technology for assistance.")
        err += 1
    write_out(text, "\nMAX IOFST = "+str(max_))
    if max_ > IOFST_MAX:
        write_out(text, " -- FAIL: Please contact Barrett Technology for assistance.")
        err += 1
    write_out(text, "\nMEAN IOFST = "+str(mean))
    write_out(text, "\nSTDEV IOFST = "+str(round(stdev,3)))
    if stdev > IOFST_STDEV:
        write_out(text, " -- FAIL: Please contact Barrett Technology for assistance.")
        err += 1
    
    # If IOFST is fine, check out MOFST.
    if err == 0: 
        bt.set_property(puck, bt.IOFST, int(mean))
        write_out(text, "\nThe new offset (IOFST) is: "+str(int(mean))+"\n")
        hex_wrench_prompt(btn)
        btn.update()
        if btn.var.get() == 0:    
            enable_all()
            btn.config(fg="black", relief= "raised", bg='SystemButtonFace')
            write_out(text, "\nOffset Test Aborted\n")
            return        
        bt.set_property(puck, bt.TSTOP, 0)
        bt.set_property(puck, bt.MODE, bt.MODE_TORQUE)
        dat = bt.get_property(puck, bt.MOFST)
        write_out(text, "\nThe old mechanical offset (MOFST) was: "+str(dat))
        if vers <= 39:
            bt.set_property(puck, bt.ADDR, 32971) #I'm not sure what's going on here, exactly? I'm just copying the code...
            bt.set_property(puck, bt.VALUE, 1)
        else:
            bt.set_property(puck, bt.FIND, bt.MOFST)
        
        write_out(text, "\nPlease wait (10 sec)...\n")
        sleep(10, btn, value = 0)
        if btn.var.get() == 0:    
            enable_all()
            btn.config(fg="black", relief= "raised", bg='SystemButtonFace')
            write_out(text, "\nOffset Test Aborted\n")
            return
        
        if vers <= 39:
            bt.set_property(puck, bt.ADDR, 32970)
            dat = bt.get_property(puck, bt.VALUE)
        else:
            dat = bt.get_property(puck, bt.MOFST)
            write_out(text, "\nThe new mechanical offset (MOFST) is: "+str(dat))
            bt.set_property(puck, bt.MODE, bt.MODE_IDLE)
        if vers <= 39:
            bt.set_property(puck, bt.MOFST, dat)
            bt.set_property(puck, bt.SAVE, bt.MOFST)
    write_out(text, "\nDone. \n")

    btn.var.set(0)
    enable_all()
    btn.config(fg="black", relief= "raised", bg='SystemButtonFace')

##############################OPEN_CLOSE_TEST##################################

def test_open_close(parent_frame,x,y,text):
    '''
    Display the frame to interface with perform_open_close_test.

        @param parent_frame: The tkinter frame in which the frame containing these buttons resides.
        @param x: The column of the parent frame that this frame is nested in.
        @param y: The row of the parent frame that this frame is nested in.
        @param text: The textbox to which find_motor_offsets outputs.
    '''
    opn_cls_frame=tk.LabelFrame(parent_frame,text="Open Close Test")

    v1 = tk.IntVar()
    motor_1=tk.Button(opn_cls_frame,text="Finger 1",
                      command=lambda:open_close_btn(11,text, motor_1))
    motor_1.var = v1
    motor_1.var.set(0)
    
    v2 = tk.IntVar()
    motor_2=tk.Button(opn_cls_frame,text="Finger 2",
                      command=lambda:open_close_btn(12,text, motor_2))
    motor_2.var = v2
    motor_2.var.set(0)

    v3 = tk.IntVar()
    motor_3=tk.Button(opn_cls_frame,text="Finger 3",
                      command=lambda:open_close_btn(13,text, motor_3))
    motor_3.var = v3
    motor_3.var.set(0)

    v4 = tk.IntVar()
    motor_4=tk.Button(opn_cls_frame,text="Spread",
                      command=lambda:open_close_btn(14,text, motor_4))
    motor_4.var = v4
    motor_4.var.set(0)

    easy_pack(opn_cls_frame,motor_1,motor_2, motor_3,motor_4)
    opn_cls_frame.grid(row=y, column=x,sticky=tk.E+tk.W, pady=(10, 10))

def open_close_btn(puck, textbox, btn):
    '''
    Middleman method to moderate button presses.

        @param puck: The motor being controlled.
        @param text: The textbox to output to.
        @param btn: The button being pressed.
    '''
    if btn.var.get() == 0:
        btn.var.set(1)
        disable_all()
        btn.config(fg="black", relief= "raised", bg="#B80000", state=tk.NORMAL)
        perform_open_close_test(puck, textbox, btn)
    elif btn.var.get()==1:
        btn.var.set(0)
        enable_all()
        btn.config(fg="black", relief=tk.RAISED, bg="SystemButtonFace")
        write_out(textbox, "\nEnding Open/Close Test\n")
    else:
        print "Cycle Test Start/Stop button malfunctioning."

def perform_open_close_test(motor, text, btn):
    '''
    Open and close the hand 3 times.

        @param motor: The integer corresponding to the motor to be tested.
        @param text: The textbox to output to.
        @param btn: The button being pressed.
    '''
    write_out(text, "\nTesting...")
    bt.open_finger(motor)
    i = 0
    while i < 3:
        i += 1
        write_out(text, "\nCycle "+str(i))
        if (btn.var.get()==0):
            return
        sleep(0.5, btn, value=0)
        text.update()
        if (btn.var.get()==0):
            return
        bt.close_finger(motor)
        text.update()
        if (btn.var.get()==0):
            return
        sleep(0.5, btn, value=0)
        bt.open_finger(motor)

    btn.var.set(0)
    enable_all()
    btn.config(fg="black", relief=tk.RAISED, bg="SystemButtonFace")
    write_out(text, "\nEnding Open/Close Test\n")

##############################FIRMWARE_DOWNLOADING#############################

# NOTICE: ABSOLUTELY NONE OF THIS IS FUNCTIONAL. ENABLE THINGS AT YOUR OWN RISK

def popup():
    if tkMessageBox.askyesno("Firmware Download","You are about to download Firmware vers ___. \n Would you like to proceed?"):
        pass

def on_firm_click(*all_inputs):
    print "beep"
    for check_var in all_inputs:
        check_var.set(0)

def firmware_download(parent_frame,x,y):
    def onBrowse(entry):
        entry.delete(0, END)
        entry.insert(0, askopenfilename())
        
    v1 = tk.IntVar()
    v2 = tk.IntVar()
    v3 = tk.IntVar()
    v4 = tk.IntVar()
    
    download_frame=tk.LabelFrame(parent_frame,text="Firmware Download")
    global firmware
    firmware = download_frame
    firmware_path=tk.Entry(download_frame,state=tk.DISABLED)
    firmware_path.insert(0,"File")
    browse_btn=tk.Button(download_frame,text="Browse",command=lambda:onBrowse(firmware_path),state=tk.DISABLED)

    
    finger_1=tk.Checkbutton(download_frame,text="Finger 1",variable=v1,command=lambda:on_firm_click(v2,v3,v4),state=tk.DISABLED)
    finger_2=tk.Checkbutton(download_frame,text="Finger 2",variable=v2,command=lambda:on_firm_click(v1,v3,v4),state=tk.DISABLED)
    finger_3=tk.Checkbutton(download_frame,text="Finger 3",variable=v3,command=lambda:on_firm_click(v1,v2,v4),state=tk.DISABLED)
    spread=tk.Checkbutton(download_frame,text="Spread",variable=v4,command=lambda:on_firm_click(v1,v2,v3),state=tk.DISABLED)

    download_btn=tk.Button(download_frame,text="Download", command= popup,state=tk.DISABLED)
    download_btn.config(bg="#62CC68" )

    firmware_path.grid(row=0, column=0,padx=5,sticky=tk.E+tk.W)
    browse_btn.grid(row=0,column=1,padx=(0,5),sticky="ew")

    finger_1.grid(row=1,column=0,sticky=tk.W)
    finger_2.grid(row=2,column=0,sticky=tk.W)
    finger_3.grid(row=3,column=0,sticky=tk.W)
    spread.grid(row=4, column=0,sticky=tk.W)

    download_btn.grid(row=5,column=0,columnspan=2, sticky=tk.E+tk.W,padx=5, pady=5)

    download_frame.grid(row=y,column=x,padx=5, pady=5,sticky=tk.E+tk.W)
    download_frame.grid_columnconfigure(0,weight=1)
    download_frame.grid_columnconfigure(1,weight=1)

def firmware(parent_frame,x,y):
    firm_frame=tk.LabelFrame(parent_frame,text="Firmware")
    firmware_download(firm_frame,1,0)
    firmware_version(firm_frame,0,0)
    
    firm_frame.grid(row=y,column=x,sticky=tk.E+tk.W)
    firm_frame.grid_columnconfigure(0,weight=1)
    firm_frame.grid_columnconfigure(1,weight=1)

def firmware_version(parent_frame,x,y):
    version_frame=LabelFrame(parent_frame,text="Firmware Version")

    finger_1_lbl=Label(version_frame,text="Finger 1")
    finger_2_lbl=Label(version_frame,text="Finger 2")
    finger_3_lbl=Label(version_frame,text="Finger 3")
    spread_lbl=Label(version_frame,text="Spread")

    vers1 = ""
    vers2 = ""
    vers3 = ""
    vers4 = ""

    try:
        vers1 = str(bt.get_property(bt.FINGER1, bt.VERS))
    except:
        vers1 = "Unknown"
    try:
        vers2 = str(bt.get_property(bt.FINGER1, bt.VERS))
    except:
        vers2 = "Unknown"
    try:
        vers3 = str(bt.get_property(bt.FINGER1, bt.VERS))
    except:
        vers3 = "Unknown"
    try:
        vers4 = str(bt.get_property(bt.FINGER1, bt.VERS))
    except:
        vers4 = "Unknown"

    f_1_ver_lbl=Label(version_frame,text=vers1)
    f_2_ver_lbl=Label(version_frame,text=vers2)
    f_3_ver_lbl=Label(version_frame,text=vers3)
    spread_ver_lbl=Label(version_frame,text=vers4)

    finger_1_lbl.grid(row=0,column=0,sticky=tk.W,padx=(5,0))
    finger_2_lbl.grid(row=1,column=0,sticky=tk.W,padx=(5,0))
    finger_3_lbl.grid(row=2,column=0,sticky=tk.W,padx=(5,0))
    spread_lbl.grid(row=3,column=0,sticky=tk.W,padx=(5,0))

    f_1_ver_lbl.grid(row=0,column=1,sticky=tk.E,padx=(0,5))
    f_2_ver_lbl.grid(row=1,column=1,sticky=tk.E,padx=(0,5))
    f_3_ver_lbl.grid(row=2,column=1,sticky=tk.E,padx=(0,5))
    spread_ver_lbl.grid(row=3,column=1,sticky=tk.E,padx=(0,5))

    version_frame.grid(row=y,column=x,sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)
    version_frame.grid_columnconfigure(0,weight=1)
    version_frame.grid_columnconfigure(1,weight=1)
    version_frame.grid_rowconfigure(0,weight=1)
    version_frame.grid_rowconfigure(1,weight=2)
    version_frame.grid_rowconfigure(2,weight=1)
    version_frame.grid_rowconfigure(3,weight=2)

##############################MISCELLANEOUS####################################

def write_out(textbox, line):
    '''
    Write the line to the specified textbox.

        @param textbox: The textbox to write to.
        @param line: The line to be written.
    '''
    textbox.config(state=tk.NORMAL)
    textbox.insert(tk.END, line)
    textbox.yview(tk.END)
    textbox.config(state=tk.DISABLED)
    textbox.update()

def easy_pack(parent_frame,a,b,c,d):
    '''
    Pack four buttons together into a frame.

        @param parent_frame: The frame in which to pack the buttons.
        @param a: The first button in the frame.
        @param b: The second button in the frame.
        @param c: The third button in the frame.
        @param d: The fourth button in the frame.
    '''
    left_padding=0
    right_padding=10
    x_pad=(left_padding,right_padding)
    up_padding=0
    down_padding=5
    y_pad=(up_padding,down_padding)
    a.pack(side="left", padx=(5,right_padding),pady=y_pad, fill="both",expand=True)
    b.pack(side="left", padx=x_pad, pady=y_pad, fill="both",expand=True)
    c.pack(side="left", padx=x_pad, pady=y_pad, fill="both",expand=True)
    d.pack(side="left", padx=(0,5),pady=y_pad, fill="both",expand=True)
    # a.grid(row=0, column=0, padx=(5,right_padding),pady=y_pad, sticky='ew')
    # b.grid(row=0, column=1, padx=x_pad, pady=y_pad, sticky='ew')
    # c.grid(row=0, column=2, padx=x_pad, pady=y_pad, sticky='ew')
    # d.grid(row=0, column=3, padx=x_pad, pady=y_pad, sticky='ew')

def sleep(seconds, widget, value = 0):
    '''
    Sleep for the specified amount of time, and allow for a break in the middle.

        @param seconds: Max time to sleep.
        @type seconds: float
        @param variable: The widget holding the variable holding whether or not to break. Break if variable == value.
        @type variable: Tkinter widget
        @param value: Break when variable == value.
    '''
    i = 0.0
    while i < seconds:
        widget.update()
        time.sleep(.1)
        i += .1
        if widget.var.get() == value:
            return

# This class represents the big initialize button on the top of the frame.
class initialize_btn():
    def do_something(self):
        disable_all()
        bt.initialize()
        bt.init_hand()
        enable_all()

    def format(self):
        self.init_btn.grid(row=self.y, column=self.x, sticky=tk.N+tk.S+tk.E+tk.W,pady=(25,25),padx=(50, 50), columnspan=2)

    def __init__(self,parent_frame,x,y):
        self.parent_frame=parent_frame
        self.x=x
        self.y=y
        self.init_btn=tk.Button(parent_frame,text="Initialize Hand",command= self.do_something)
        self.init_btn.config(bg="#62CC68")
        self.format()
        self.font = tkFont.Font(size=14, weight="bold")

def create_maintenance_tab(nb, handType):
    '''
    Display the tab to the root window (nb).

        @param nb: The notebook to display the tab to.
        @param handType: Specifies whether the hand is a 280, 282, or unknown type by returning 1, 0, or -1 respectively.
    '''
    global maintenance_frame
    global notebook
    notebook = nb
    maintenance_frame=Frame(nb,name='maintenance')
    #left_half = Frame(maintenance_frame)
    #right_half= Frame(maintenance_frame)
    
    herp=initialize_btn(maintenance_frame,0,0)
    nb.herp=herp
    
    textframe = Frame(maintenance_frame)
    scroll = tk.Scrollbar(textframe)
    text = tk.Text(textframe,height=20, width=90,yscrollcommand = scroll.set, wrap=tk.WORD, state = tk.DISABLED)
    scroll.config(command=text.yview)
    scroll.pack(side="right", fill="y")
    text.pack(side="left", fill="x", expand=True)
    textframe.grid(row=1,column=1,rowspan=4,padx=(25,0),sticky=tk.E+tk.W)
    
    default_properties(maintenance_frame,0,2,text)
    motor_offsets(maintenance_frame,0,3,text)
    test_open_close(maintenance_frame,0,4,text)
    cycle_test(maintenance_frame,0,1,text)
    firmware(maintenance_frame,0,5)
    properties_tab.create_properties_tab(maintenance_frame, 1,5, handType)
    
    #left_half.grid( row=1, column=0)
    #right_half.grid(row=1, column=1, sticky = tk.N)
    if handType < 0:
        properties_tab.disable(maintenance_frame)
    maintenance_frame.grid(row=0, column=0)
    nb.add(maintenance_frame, text='Maintenance', underline=0, padding=2)
