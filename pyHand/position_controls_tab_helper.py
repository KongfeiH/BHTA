#  position_controls_tab_helper.py
#  
#  ~~~~~~~~~~~~
#  
#  pyHand Position Controls Tab Helper File
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

from Tkinter import *
import ttk as tk
import tkFont
from PIL import ImageTk
import time
import demo
import threading
import tkMessageBox
from pyHand_API.pyHand_api import *



demoRunning = False
hand_control_thread=""

def reset_finger(finger, rootWindow, demo_btn, chart, 
                 scale1, scale2, scale3, scale_spread):
    """
    Resets a given finger

    @param finger: which finger to reset
    @type finger: C{int}

    @param rootWindow: the root Tk()
    @type rootWindow C{Tk_Widget}
    
    @param demo_btn: The button that runs the demo.
    @type demo_btn: C{Button_Widget}
    
    @param chart: A dictionary of dictionaries that keeps track of where all sliders are in relation to each other.
    @type chart: C{ [Scale_Widget: [Scale_Widget : Double] , [Scale_Widget :  Double]...(1) ]...(3) }
    
    @param slider1: The Finger 1 Scale
    @type slider1: C{Scale_Widget}
    
    @param slider2: The Finger 2 Scale
    @type slider2: C{Scale_Widget}
    
    @param slider3: The Finger 3 Scale
    @type slider3: C{Scale_Widget}
    
    @param slider_spread: The Spread Scale
    @type slider_spread: C{Scale_Widget}
    """
    
    disable_list(None, rootWindow.grid_slaves())
    disable(None, demo_btn)
    disable_tabs(rootWindow.master, rootWindow.master.tabs())
    rootWindow.update()
    toSet = get_property(finger, MODE)
    init_finger(finger)
    time.sleep(4)
    set_puck_like(finger, finger)
    undisable_list(None, rootWindow.grid_slaves())
    undisable(None, demo_btn)
    enable_tabs(rootWindow.master, rootWindow.master.tabs())
    set_modes_tstop()
    set_sliders_to_hand(chart, scale1, scale2, scale3, scale_spread)

def check_name_for_commas(name):
    """
    Takes in a name string and checks whether that string contains a comma. 

    @param name: A string that is the new position name
    @type name: C{String}
        
    @return: True if there is NOT a comma, False if there is.
    @rtype: C{Boolean}
    """
    contains_commas=("," in name)
    if contains_commas:
        tkMessageBox.showerror("Invalid Position Name", "Error: Names cannot contain commas.")
        return not contains_commas
    else:
        return not contains_commas


def set_hand_pos(chart,scale_list,selected,pos_chart,top_frame):
    """
    Sets all sliders and entries to the positions dictated by a preconfigured position.

    @param chart: A dictionary of dictionaries that keeps track of where all sliders are in relation to each other.
    @type chart: C{ [Scale_Widget: [Scale_Widget : Double] , [Scale_Widget :  Double]...(1) ]...(3) }

    @param scale_list: A list of all scale objects
    @type scale_list: C{[Scale_widget,Scale_widget...(2)]}

    @param selected: The currently selected position from the optionmenu. The same as optionMenu.select()
    @type selected: C{String}

    @param pos_chart: A dictionary that maps position names to a list of values associated with all fingers.
        The last value (4) keeps track of whether or no the position is a default position.
    @type pos_chart: C{[String:[int,int,int,int,int]...(x)]}
    """
    if selected not in pos_chart:
        tkMessageBox.showerror("Invalid Position Name","Error: Cannot load from a name that has not been saved")
    else:
        new_pos=pos_chart[selected]
        dummy_btn=Button(None)
        open_grasp()
        time.sleep(.5)

        new_pos_1=(int(new_pos[0])*1950)
        new_pos_2=(int(new_pos[1])*1950)
        new_pos_3=(int(new_pos[2])*1950)
        new_pos_spread=(int(new_pos[3])*362)

        move_to(SPREAD,new_pos_spread)
        move_to(FINGER1,new_pos_1,True)
        move_to(FINGER2,new_pos_2,True)
        move_to(FINGER3,new_pos_3)
        #Will wait for last finger to finish moving
        time.sleep(1)

##        undisable(dummy_btn,top_frame)

        set_sliders_to_hand(chart,scale_list[0],scale_list[1],scale_list[2],scale_list[3])
        set_modes_tstop()

def del_pos(option, options,pos_chart,selected,var,frame,load_btn):
    """
    Deletes a precofigured set of positions

    @param option: A optionMenu widget that holds all of the options
    @type option: C{OptionMenu_Widget}

    @param options: A list of preconfigured position names. The same as pos_chart.keys()
    @type options: C{[String...(x)]}

    @param pos_chart: A dictionary that maps position names to a list of values associated with all fingers.
        The last value (4) keeps track of whether or no the position is a default position.
    @type pos_chart: C{[String:[int,int,int,int,int]...(x)]}
    
    @param selected: The currently selected position from the optionmenu.
        The same as optionMenu.select()
    @type selected: C{String}

    @param var: The TK variable that keeps track of all of option's options (I am so sorry)
    @type var: C{StringVar()}

    @param frame: The parent_frame of option so that the widget can be recreated afters options updates.
    @type frame: C{Frame_Widget}
    """
    txt_file=open("Memory/Hand_Positions/hand_positions.txt")
    pos_name=selected.strip()
    if pos_name in pos_chart:
        if pos_chart[pos_name][4]=="1":
            tkMessageBox.showerror("Invalid Position Name","This position is protected. Position not deleted")

        else:
            del pos_chart[pos_name]
            tkMessageBox.showinfo("Position Deleted","Position "+pos_name+" deleted")
            actually_save_pos(pos_chart)
            
            option.grid_forget()    
            options=load_hand_positions(pos_chart)
            option=OptionMenu(frame,var,*options,command=lambda x:flash_button(load_btn))#,command=lambda x:set_hand_pos(chart,scale_list,x,pos_chart))
            var.set(options[0])
            option.grid(row= 1, column= 0,sticky="ew")
    else:
        tkMessageBox.showerror("Invalid Position Name","Position not found. Position not deleted")

def load_hand_positions(pos_chart):
    """
    Looks into memory for saved positions

    @param pos_chart: A dictionary that maps position names to a list of values associated with all fingers.
        The last value (4) keeps track of whether or no the position is a default position.
    @type pos_chart: C{[String:[int,int,int,int,int]...(x)]}

    @return: A list of all saved positions
    """
    txt_file=open("Memory/Hand_Positions/hand_positions.txt")
    for line in txt_file:
        line=line.replace("\n","")
        line=line.split(",")
        #print line
        name=line[0].replace("\n","")
        if name!="":
            pos_chart[name]=line[1:len(line)]
    txt_file.close()
    protected_list=[]
    regular_list=[]
    for key in pos_chart.keys():
        if pos_chart[key][4]=="1":
            protected_list.append(key)
        else:
            regular_list.append(key)
    full_list=sorted(protected_list)+sorted(regular_list)
##    print pos_chart
    return full_list

def actually_save_pos(pos_chart):
    """
    Saves all info (keys and vals) in pos_chart to file (txt_file, see source for filepath)

    @param pos_chart: A dictionary that maps position names to a list of values associated with all fingers.
        The last value (4) keeps track of whether or no the position is a default position.
    @type pos_chart: C{[String:[int,int,int,int,int]...(x)]}
    """
    txt_file=open("Memory/Hand_Positions/hand_positions.txt",'w')
    for key,value in pos_chart.iteritems():
        txt_file.write("\n"+key)
        txt_file.write(","+str(value[0])+","+str(value[1])+","+str(value[2])+","+str(value[3])+","+str(value[4]))                
    txt_file.close()
    
def save_hand_positions(chart,pos_chart,entry,option,options,frame,var,entry_list,scale_list,load_btn):
    """
    Does error checking for the saving of positions. Warns the user for a variety of reasons. Some parameters are redundant.
    
    @param chart: A dictionary of dictionaries that keeps track of where all sliders are in relation to each other.
    @type chart: C{ [Scale_Widget: [Scale_Widget : Double] , [Scale_Widget :  Double]...(1) ]...(3) }
    
    @param pos_chart: A dictionary that maps position names to a list of values associated with all fingers.
        The last value (4) keeps track of whether or no the position is a default position.
    @type pos_chart: C{[String:[int,int,int,int,int],...(x)]}
        
    @param entry: The entry connected to 'option'. Probably unnessessary.
    @type entry: C{Entry_Widget}
    
    @param option: A optionMenu widget that holds all of the options
    @type option: C{OptionMenu_Widget}
    
    @param options: A list of preconfigured position names. The same as pos_chart.keys()
    @type options: C{[String,...(x)]}
    
    @param frame: The parent frame for option so it can be reconstructed
    @type frame: C{Frame_Widget}
    
    @param var: The TK variable that keeps track of all of option's options.
    @type var: C{StringVar()}
    
    @param entry_list: A list of all entries (connected to sliders and checkboxes)
    @type entry_list: C{[Entry_Widget,...(3)]}
    
    @param scale_list: A list of all scales (connected to entries and checkboxes)
    @type scale_list: C{[Scale_Widget,...(3)]}
    """
    new_pos_name=entry.get().strip()
    
    if (new_pos_name not in pos_chart) and new_pos_name!="":
        if check_name_for_commas(new_pos_name):
            pos_chart[new_pos_name]=[entry_list[0].get(),entry_list[1].get(),entry_list[2].get(),entry_list[3].get(),"0"]
            actually_save_pos(pos_chart)
            tkMessageBox.showinfo("Position Saved","Position "+entry.get()+" saved")
        else:
            print "huh?"
    elif new_pos_name in pos_chart:
        if tkMessageBox.askyesno("Overwrite Position", "Position "+entry.get()+" already exists.\n Would you like to overwite position "+entry.get()+" ?"):
            if pos_chart[new_pos_name][4]=="1":
                tkMessageBox.showerror("Invalid Position Name","This position is protected. Position not saved")
            else:
                pos_chart[new_pos_name]=[entry_list[0].get(),entry_list[1].get(),entry_list[2].get(),entry_list[3].get(),"0"]
                actually_save_pos(pos_chart)
                tkMessageBox.showinfo("Position Saved","Position "+entry.get()+" saved")

    elif new_pos_name=="":
        tkMessageBox.showerror("Invalid Position Name","Error: The position name consists of only whitespace.")
    option.grid_forget()    
    options=load_hand_positions(pos_chart)
    option=OptionMenu(frame,var,*options,command=lambda x:flash_button(load_btn))#,command=lambda x:set_hand_pos(chart,scale_list,x,pos_chart))
    option.grid(row= 1, column= 0,sticky="ew")
    
def enable_tabs(nb,tab_list):
    '''
    Enables all tabs previously disabled.

    @param nb: notebook to enable tabs from.
    @type nb: C{Notebook_Widget}
    
    @param tab_list: list of tabs to be enabled.
    @type tab_list: C{[tab_id...(x)]}
    '''
    for tab in tab_list:
        nb.tab(tab,state="normal")

def disable_tabs(nb,tab_list):
    '''
    Disables all tabs but the one user is on.

    @param nb: notebook to disable tabs from.
    @type nb: C{Notebook_Widget}
    
    @param tab_list: list of tabs to be disabled.
    @type tab_list: C{[tab_id...(x)]}
    '''
    for tab in tab_list:
        if nb.tab(tab,"text")!="Control":
            nb.tab(tab,state="disabled")
        
def run_stop_toggle(btn, top_frame,chart,slider1,slider2,slider3,slider_spread):
    """
    Starts and stops the Barrett Hand demo. The gui is non-functional while the demo is running.
    
    @param btn: The demo button
    @type btn: C{Button_Widget}
    
    @param top_frame: The parent frame of btn so that everything can be disabled when the demo is running.
    @type top_frame: C{Frame_Widget}
    """
    global demoRunning
    if btn.var.get() == 0:
        demoRunning = True
        btn.config(text='Stop Demo', bg="#B80000", fg="black", relief= "raised")
        disable_list(btn,top_frame.grid_slaves())
        btn.var.set(1)
        
        nb=top_frame.master
        tab_list=nb.tabs()
        disable_tabs(nb,tab_list)
        
        t = threading.Thread(target=lambda: demo.start_demo(btn.var))
        t.start()
        
    elif btn.var.get()==1:
        btn.var.set(0)
        time.sleep(2)
        
        btn.config(text='Barrett Hand Demo', bg="#62CC68", fg="black")
        undisable_list(btn,top_frame.grid_slaves())
        btn.config(relief=RAISED)

        nb=top_frame.master
        tab_list=nb.tabs()
        enable_tabs(nb,tab_list)

        set_sliders_to_hand(chart,slider1,slider2,slider3,slider_spread)
        set_modes_tstop()

        demoRunning = False
        
    else:
        print "being stupid"

def disable_list(btn,widget_list):
    """
    Recursively disables all widgets in the given list except for the given button

    @param btn: The Demo button.
    @type btn: C{Button_Widget}

    @param widget_list: A list of widgets to disable.
    @type widget_list: C{Widget...(x)}
    """
    for widget in widget_list:
        disable(btn,widget)

def disable(btn,widget):
    """
    Recursively disables this widget and all child widgets except for the given button

    @param btn: The Demo button.
    @type btn: C{Button_Widget}

    @param widget: A list of widgets to disable.
    @type widget: C{Widget}
    """
    if widget==None:
        return
    elif widget!=btn:
        if widget.winfo_class()=="TLabelframe" or widget.winfo_class()=="TFrame" or widget.winfo_class()=="Frame" or widget.winfo_class()=="Labelframe":
            disable_list(btn,widget.grid_slaves())
            disable_list(btn, widget.pack_slaves())
        elif widget.winfo_class()=="Canvas":
            pass
        else:
            widget.config(state=DISABLED)
    else:
        pass
def undisable_list(btn,widget_list):
    """
    Recursively activates all widgets in the given list except for the given button

    @param btn: The Demo button.
    @type btn: C{Button_Widget}

    @param widget_list: A list of widgets to activate.
    @type widget_list: C{Widget...(x)}
    """
    for widget in widget_list:
        undisable(btn,widget)
def undisable(btn,widget):
    """
    Recursively activates this widget and all child widgets except for the given button

    @param btn: The Demo button.
    @type btn: C{Button_Widget}

    @param widget: A list of widgets to activate.
    @type widget: C{Widget}
    """
    if widget==None:
        return
    elif widget!=btn:
        if widget.winfo_class()=="TLabelframe" or widget.winfo_class()=="TFrame" or widget.winfo_class()=="Frame" or widget.winfo_class()=="Labelframe":
            undisable_list(btn,widget.grid_slaves())
            undisable_list(btn,widget.pack_slaves())
        elif widget.winfo_class()=="Canvas":
            pass
        else:
            widget.config(state=NORMAL)
    else:
        pass

    
def check(set_mem,n,chart,active_c, other1_c,other2_c,other3_c,canvas):
    """
    Checks all position control check buttons and figures out which sliders to connect

    @param set_mem: Whether or not to set the memory of the active checkbutton
    @type set_mem: C{Boolean}

    @param n: The dictionary that keeps a memory of which check buttons were checked before open/close grasp was pressed.
    @type n: C{[CheckButton_Widget:Boolean...(x)]}
    
    @param chart: A dictionary of dictionaries that keeps track of where all sliders are in relation to each other.
    @type chart: C{ [Scale_Widget: [Scale_Widget : Double] , [Scale_Widget :  Double]...(1) ]...(3) }
    
    @param active_c: The CheckButton widget that is being pressed
    @type active_c: C{CheckButton_Widget}
    
    @param other1_c: One of the other CheckButton Widgets, can be any of them.
    @type other1_c: C{CheckButton_Widget}
    
    @param other2_c: One of the other CheckButton Widgets, can be any of them.
    @type other2_c: C{CheckButton_Widget}
    
    @param other3_c: One of the other CheckButton Widgets, can be any of them.
    @type other3_c: C{CheckButton_Widget}

    @param canvas: canvas to draw the check box connecting lines.
    @type canvas: C{Canvas_Widget}
    """
    chart["CURRENT_LINKS"].clear()
    update_all_delays(chart,active_c.slide,other1_c.slide,other2_c.slide,other3_c.slide)
    canvas.delete("all")
    if active_c.var.get()==True:
        canvas.create_line(active_c.number[0], active_c.number[1], 0, active_c.number[1], width=4)
        if set_mem==True:
            n[active_c]=True
        if other1_c.var.get()==True and other2_c.var.get()==True and other3_c.var.get()==True:
            canvas.create_line(4, 0, 4, 170, width= 4)
            canvas.create_line(other1_c.number[0], other1_c.number[1], 0, other1_c.number[1], width=4)
            canvas.create_line(other2_c.number[0], other2_c.number[1], 0, other2_c.number[1], width=4)
            canvas.create_line(other3_c.number[0], other3_c.number[1], 0, other3_c.number[1], width=4)
            connect_sliders(chart,active_c.slide,other1_c.slide,other2_c.slide,other3_c.slide)    
        elif other1_c.var.get()==True and other2_c.var.get()==True:
            maxval= max(other1_c.number[1], other2_c.number[1], active_c.number[1])
            minval= min(other1_c.number[1], other2_c.number[1], active_c.number[1])
            canvas.create_line(4, minval, 4, maxval, width= 4)
            canvas.create_line(other1_c.number[0], other1_c.number[1], 0, other1_c.number[1], width=4)
            canvas.create_line(other2_c.number[0], other2_c.number[1], 0, other2_c.number[1], width=4)
            connect_sliders(chart,active_c.slide,other1_c.slide,other2_c.slide)
        elif other2_c.var.get()==True and other3_c.var.get()==True:
            maxval= max(other3_c.number[1], other2_c.number[1], active_c.number[1])
            minval= min(other3_c.number[1], other2_c.number[1], active_c.number[1])
            canvas.create_line(4, minval, 4, maxval, width= 4)
            canvas.create_line(other2_c.number[0], other2_c.number[1], 0, other2_c.number[1], width=4)
            canvas.create_line(other3_c.number[0], other3_c.number[1], 0, other3_c.number[1], width=4)
            connect_sliders(chart,active_c.slide,other2_c.slide,other3_c.slide)
        elif other1_c.var.get()==True and other3_c.var.get()==True:
            maxval= max(other3_c.number[1], other1_c.number[1], active_c.number[1])
            minval= min(other3_c.number[1], other1_c.number[1], active_c.number[1])
            canvas.create_line(4, minval, 4, maxval, width= 4)
            canvas.create_line(other1_c.number[0], other1_c.number[1], 0, other1_c.number[1], width=4)
            canvas.create_line(other3_c.number[0], other3_c.number[1], 0, other3_c.number[1], width=4)
            connect_sliders(chart,active_c.slide,other1_c.slide,other3_c.slide)
        elif other1_c.var.get()==True:
            maxval= max(other1_c.number[1], active_c.number[1])
            minval= min(other1_c.number[1], active_c.number[1])
            canvas.create_line(4, minval, 4, maxval, width= 4)
            canvas.create_line(other1_c.number[0], other1_c.number[1], 0, other1_c.number[1], width=4)
            connect_sliders(chart,active_c.slide,other1_c.slide)
        elif other2_c.var.get()==True:
            maxval= max(other2_c.number[1], active_c.number[1])
            minval= min(other2_c.number[1], active_c.number[1])
            canvas.create_line(4, minval, 4, maxval, width= 4)
            canvas.create_line(other2_c.number[0], other2_c.number[1], 0, other2_c.number[1], width=4)
            connect_sliders(chart,active_c.slide,other2_c.slide)
        elif other3_c.var.get()==True:
            maxval= max(other3_c.number[1], active_c.number[1])
            minval= min(other3_c.number[1], active_c.number[1])
            canvas.create_line(4, minval, 4, maxval, width= 4)
            canvas.create_line(other3_c.number[0], other3_c.number[1], 0, other3_c.number[1], width=4)            
            connect_sliders(chart,active_c.slide,other3_c.slide)
        else:
            active_c.slide.config(command=lambda x:dud(active_c))
    else:
        if set_mem==True:
            n[active_c]=False
        if other1_c.var.get()==True and other2_c.var.get()==True and other3_c.var.get()==True:
            maxval= max(other1_c.number[1], other2_c.number[1], other3_c.number[1])
            minval= min(other1_c.number[1], other2_c.number[1], other3_c.number[1])
            canvas.create_line(4, minval, 4, maxval, width= 4)
            canvas.create_line(other1_c.number[0], other1_c.number[1], 0, other1_c.number[1], width=4)
            canvas.create_line(other2_c.number[0], other2_c.number[1], 0, other2_c.number[1], width=4)
            canvas.create_line(other3_c.number[0], other3_c.number[1], 0, other3_c.number[1], width=4)
            connect_sliders(chart,other1_c.slide,other2_c.slide,other3_c.slide)
##            active_c.slide.config(command=lambda x:dud(active_c))
        elif other1_c.var.get()==True and other2_c.var.get()==True:
            maxval= max(other1_c.number[1], other2_c.number[1])
            minval= min(other1_c.number[1], other2_c.number[1])
            canvas.create_line(4, minval, 4, maxval, width= 4)
            canvas.create_line(other1_c.number[0], other1_c.number[1], 0, other1_c.number[1], width=4)
            canvas.create_line(other2_c.number[0], other2_c.number[1], 0, other2_c.number[1], width=4)
            connect_sliders(chart,other1_c.slide,other2_c.slide)
##            active_c.slide.config(command=lambda x:dud(active_c))
        elif other2_c.var.get()==True and other3_c.var.get()==True:
            maxval= max(other2_c.number[1], other3_c.number[1])
            minval= min(other2_c.number[1], other3_c.number[1])
            canvas.create_line(4, minval, 4, maxval, width= 4)
            canvas.create_line(other2_c.number[0], other2_c.number[1], 0, other2_c.number[1], width=4)
            canvas.create_line(other3_c.number[0], other3_c.number[1], 0, other3_c.number[1], width=4)
            connect_sliders(chart,other2_c.slide,other3_c.slide)
        elif other1_c.var.get()==True and other3_c.var.get()==True:
            maxval= max(other1_c.number[1], other3_c.number[1])
            minval= min(other1_c.number[1], other3_c.number[1])
            canvas.create_line(4, minval, 4, maxval, width= 4)
            canvas.create_line(other1_c.number[0], other1_c.number[1], 0, other1_c.number[1], width=4)
            canvas.create_line(other3_c.number[0], other3_c.number[1], 0, other3_c.number[1], width=4)
            connect_sliders(chart,other1_c.slide,other3_c.slide)
        else:
            other1_c.slide.config(command=lambda x:dud(other1_c))
            other2_c.slide.config(command=lambda x:dud(other2_c))
            other3_c.slide.config(command=lambda x:dud(other3_c))

    if active_c.var.get()==False:
        active_c.slide.config(command=lambda x:dud(active_c))
    else:
        chart["CURRENT_LINKS"].add(active_c.finger)
    if other1_c.var.get()==False:
        other1_c.slide.config(command=lambda x:dud(other1_c))
    else:
        canvas.create_line(other1_c.number[0], other1_c.number[1], 0, other1_c.number[1], width=4)
        chart["CURRENT_LINKS"].add(other1_c.finger)
    if other2_c.var.get()==False:
        other2_c.slide.config(command=lambda x:dud(other2_c))
    else:
        canvas.create_line(other2_c.number[0], other2_c.number[1], 0, other2_c.number[1], width=4)
        chart["CURRENT_LINKS"].add(other2_c.finger)
        #other2_c.config(bg="blue")
    if other3_c.var.get()==False:
        other3_c.slide.config(command=lambda x:dud(other3_c))
    else:
        canvas.create_line(other3_c.number[0], other3_c.number[1], 0, other3_c.number[1], width=4)
        chart["CURRENT_LINKS"].add(other3_c.finger)
##        else:
##            active_c.slide.config(command=lambda x:dud(active_c))
##            other1_c.slide.config(command=lambda x:dud(other1_c))
##            other2_c.slide.config(command=lambda x:dud(other2_c))
            
def link(chart,active,other1,other2=None,other3=None):
    """
    The actual function called when the sliders are linked when they are moved.
    Sets the value of the active slider to the others if they are linked.
    Also updates the entry with the current value.

    @param chart: A dictionary of dictionaries that keeps track of where all sliders are in relation to each other.
    @type chart: C{ [Scale_Widget: [Scale_Widget : Double] , [Scale_Widget :  Double]...(1) ]...(3) }

    @param active: The Scale_Widget currently being moved.
    @type active: C{Scale_Widget}

    @param other1: One of the sliders that is not the current one.
    @type other1: C{Scale_WIdget}

    @param other2: One of the sliders that is not the current one.
    @type other2: C{Scale_WIdget}

    @param other3: One of the sliders that is not the current one.
    @type other3: C{Scale_WIdget}

    """
    #print active.get()
    update_text(active.get(),active.entry)
    other1.set(active.get()-chart[active][other1])
    if other2!=None:
        other2.set(active.get()-chart[active][other2])
    if other3!=None:
        other3.set(active.get()-chart[active][other3])
        
def dud(check):
    """
    When the scales are not linked to other scales, the only update their own entry when moved.
    
    @param check: The Checkbox_Widget whose entry and slider you want to connect.
    @type check: C{Checkbox_Widget}
    """
    update_text(check.slide.get(),check.slide.entry)

def connect_sliders(chart,active,other1,other2=None,other3=None):
    """
    Sets the given sliders' commands to be the correct ones.
    Actually changes the commands as opposed to check(), which just figures out which commands need to be changed.

    @param chart: A dictionary of dictionaries that keeps track of where all sliders are in relation to each other.
    @type chart: C{ [Scale_Widget: [Scale_Widget : Double] , [Scale_Widget :  Double]...(1) ]...(3) }

    @param active: The Scale_Widget currently being moved.
    @type active: C{Scale_Widget}

    @param other1: One of the sliders that is not the current one.
    @type other1: C{Scale_Widget}

    @param other2: One of the sliders that is not the current one.
    @type other2: C{Scale_Widget}

    @param other3: One of the sliders that is not the current one.
    @type other3: C{Scale_Widget}
    """
    active.config(command=lambda x:link(chart,active,other1,other2,other3))
    other1.config(command=lambda x :link(chart,other1, active, other2, other3))
    if other2!=None:
        other2.config(command=lambda x :link(chart,other2, other1, active, other3))
    if other3!=None:
        other3.config(command=lambda x: link(chart,other3, other1, other2 ,active))
        
def call(chart,active,other1,other2,other3):
    """
    Updates the position chart to keep track on where all the sliders are in relation to one another.

    @param chart: A dictionary of dictionaries that keeps track of where all sliders are in relation to each other.
    @type chart: C{ [Scale_Widget: [Scale_Widget : Double] , [Scale_Widget :  Double]...(1) ]...(3) }

    @param active: The Scale_Widget currently being moved.
    @type active: C{Scale_Widget}

    @param other1: One of the sliders that is not the current one.
    @type other1: C{Scale_Widget}

    @param other2: One of the sliders that is not the current one.
    @type other2: C{Scale_Widget}

    @param other3: One of the sliders that is not the current one.
    @type other3: C{Scale_Widget}
    """
    chart[active][other1]=active.get()-other1.get()
    chart[active][other2]=active.get()-other2.get()
    chart[active][other3]=active.get()-other3.get()
    
def update_all_delays(chart,active,other1,other2,other3):
    """
    Calls all combination of arguments so that all sliders deltas in the chart are updated.
    
    @param chart: A dictionary of dictionaries that keeps track of where all sliders are in relation to each other.
    @type chart: C{ [Scale_Widget: [Scale_Widget : Double] , [Scale_Widget :  Double]...(1) ]...(3) }

    @param active: The Scale_Widget currently being moved.
    @type active: C{Scale_Widget}

    @param other1: One of the sliders that is not the current one.
    @type other1: C{Scale_Widget}

    @param other2: One of the sliders that is not the current one.
    @type other2: C{Scale_Widget}

    @param other3: One of the sliders that is not the current one.
    @type other3: C{Scale_Widget}
    """
    call(chart,active,other1,other2,other3)
    call(chart,other1,other2,active,other3)
    call(chart,other2,active,other1,other3)
    call(chart,other3,other2,other1,active)

def select_all_history(n,chart,check1, check2, check3,check4, canvas):
    """
    Selects all the finger check buttons when the grasp button is pressed.
    Also updates all the positions in the chart and saves whether or not the
    check button was check before the grasp button was pressed so that it can return to that value when grasp is pressed again.

    @param n: The dictionary that keeps a memory of which check buttons were checked before open/close grasp was pressed.
    @type n: C{[CheckButton_Widget:Boolean...(x)]}
    
    @param chart: A dictionary of dictionaries that keeps track of where all sliders are in relation to each other.
    @type chart: C{ [Scale_Widget: [Scale_Widget : Double] , [Scale_Widget :  Double]...(1) ]...(3) }
    
    @param check1: The Finger 1 Check_Button
    @type check1: C{CheckButton_Widget}
    
    @param check2: The Finger 2 Check_Button
    @type check2: C{CheckButton_Widget}
    
    @param check3: The Finger 3 Check_Button
    @type check3: C{CheckButton_Widget}
    
    @param check4: The Spread Check_Button
    @type check4: C{CheckButton_Widget}
    """
    check1.select()
    check2.select()
    check3.select()
    check4.deselect()
    #check4.select()

    check(False,n,chart,check1,check2,check3,check4, canvas)
    check(False,n,chart,check2,check1,check3,check4, canvas)
    check(False,n,chart,check3,check2,check1,check4, canvas)
    check(False,n,chart,check4,check1,check2,check3, canvas)
     
def deselect_all_history(n,chart,check1, check2, check3, check4, canvas):
    """
    Deselects all fingers that have been selected from the grasp button.

    @param n: The dictionary that keeps a memory of which check buttons were checked before open/close grasp was pressed.
    @type n: C{[CheckButton_Widget:Boolean...(x)]}
    
    @param chart: A dictionary of dictionaries that keeps track of where all sliders are in relation to each other.
    @type chart: C{ [Scale_Widget: [Scale_Widget : Double] , [Scale_Widget :  Double]...(1) ]...(3) }
    
    @param check1: The Finger 1 Check_Button
    @type check1: C{CheckButton_Widget}
    
    @param check2: The Finger 2 Check_Button
    @type check2: C{CheckButton_Widget}
    
    @param check3: The Finger 3 Check_Button
    @type check3: C{CheckButton_Widget}
    
    @param check4: The Spread Check_Button
    @type check4: C{CheckButton_Widget}

    @param canvas: canvas to draw the check box connecting lines.
    """
    if n[check1] == False:
        check1.deselect()
        check(False,n,chart,check1,check2,check3,check4, canvas)
    if n[check2] == False:
        check2.deselect()
        check(False,n,chart,check2,check1,check3,check4, canvas)
    if n[check3] == False:
        check3.deselect()
        check(False,n,chart,check3,check2,check1,check4, canvas)
    if n[check4] == True:
        check4.select()
        check(False,n,chart,check4,check2,check1,check3, canvas)

def update_text(value, field):
    """
    Tells a entry to update its value to the given one.

    @param value: A string value
    @type value: C{String}

    @param field: A Entry_Widget whose value you are going to change.
    @type field: C{Entry_Widget}
    """
    field.delete(0, END)
    field.insert(0, value)
 
def toggle(n,chart,btn, check1, check2, check3,check4, canvas):
    """
    A toggle function for the grasp button. Can either be pressed or unpressed.

    @param n: The dictionary that keeps a memory of which check buttons were checked before open/close grasp was pressed.
    @type n: C{[CheckButton_Widget:Boolean...(x)]}
    
    @param chart: A dictionary of dictionaries that keeps track of where all sliders are in relation to each other.
    @type chart: C{ [Scale_Widget: [Scale_Widget : Double] , [Scale_Widget :  Double]...(1) ]...(3) }
    
    @param check1: The Finger 1 Check_Button
    @type check1: C{CheckButton_Widget}
    
    @param check2: The Finger 2 Check_Button
    @type check2: C{CheckButton_Widget}
    
    @param check3: The Finger 3 Check_Button
    @type check3: C{CheckButton_Widget}
    
    @param check4: The Spread Check_Button
    @type check4: C{CheckButton_Widget}

    @param canvas: canvas to draw the check box connecting lines.
    @type canvas: C{Canvas_Widget}
    """
    if btn.var.get() == 1:
        select_all_history(n,chart,check1, check2, check3,check4, canvas)
        return
    elif btn.var.get()==0:
        deselect_all_history(n,chart,check1, check2, check3,check4, canvas)
        return
    else:
        print "being stupid"

def set_scale(chart, active_c, other1_c,other2_c,other3_c):
    """
    Sets the scale value to the entry input as long as the input does not equal the empty string.

    @param chart: A dictionary of dictionaries that keeps track of where all sliders are in relation to each other.
    @type chart: C{ [Scale_Widget: [Scale_Widget : Double] , [Scale_Widget :  Double]...(1) ]...(3) }
    
    @param active_c: The CheckButton widget that is being pressed
    @type active_c: C{CheckButton_Widget}
    
    @param other1_c: One of the other CheckButton Widgets, can be any of them.
    @type other1_c: C{CheckButton_Widget}
    
    @param other2_c: One of the other CheckButton Widgets, can be any of them.
    @type other2_c: C{CheckButton_Widget}
    
    @param other3_c: One of the other CheckButton Widgets, can be any of them.
    @type other3_c: C{CheckButton_Widget}
    """
    if active_c.slide.entry.get()!="":
        active_c.slide.set(active_c.slide.entry.get())
        if active_c.var.get()==True:
            if other1_c.var.get()==True:
                other1_c.slide.set(active_c.slide.entry.get())
            if other2_c.var.get()==True:
                other2_c.slide.set(active_c.slide.entry.get())
            if other3_c.var.get()==True:
                other3_c.slide.set(active_c.slide.entry.get())
    else:
        active_c.slide.entry.var.set(active_c.slide.get())

    update_all_delays(chart,active_c.slide,other1_c.slide,other2_c.slide,other3_c.slide)

def tab_selected(nb,chart,slider1,slider2,slider3,slider_spread,handType):
    """
    Gets the current selected tab in the notebook and messes with TSTOP, self preservation, and MODE.

    @param nb: The notebook
    @type nb: C{Notebook_Widget}

    @param slider1: The Finger 1 Scale
    @type slider1: C{Scale_Widget}
    
    @param slider2: The Finger 2 Scale
    @type slider2: C{Scale_Widget}
    
    @param slider3: The Finger 3 Scale
    @type slider3: C{Scale_Widget}
    
    @param slider_spread: The Spread Scale
    @type slider_spread: C{Scale_Widget}

    @param handType: The type of hand, -1 for unknown, 0 for model 282 and 1 for model 280.
    @type handType: C{int}
    """
    if handType!=-1:
        if nb.select()!="":
            current_tab=nb.tab(nb.select(), "text")
            if current_tab=='Control':
                set_sliders_to_hand(chart,slider1,slider2,slider3,slider_spread)
                set_modes_tstop()
            if current_tab =='Sensors':
                set_property(0x405, TSTOP, 50)
                set_property(SPREAD, TSTOP, 150)
                #silences the hand
                set_property(0x405, MODE, MODE_IDLE)
                #Turns self preservation off
                set_property(0x405, HSG, 10000)
            if current_tab == 'Maintenance':
                set_property(0x405, TSTOP, 50)
                set_property(SPREAD, TSTOP, 150)
                set_property(0x405, MODE, MODE_IDLE)
            if current_tab == 'Force/Torque':
                set_property(0x405, TSTOP, 50)
                set_property(SPREAD, TSTOP, 150)
                set_property(0x405, MODE, MODE_IDLE)
            
def set_modes_tstop():
    """
    set the tstop to be 0 and the mode to be velocity for position control to work.
    """
    set_property(FINGER1, TSTOP,0) 
    set_property(FINGER2, TSTOP,0) 
    set_property(FINGER3, TSTOP,0) 
    set_property(SPREAD, TSTOP,0) 
    
    set_mode(FINGER1,MODE_VEL)
    set_mode(FINGER2,MODE_VEL)
    set_mode(FINGER3,MODE_VEL)
    set_mode(SPREAD,MODE_VEL)
    
def constrain(n, minn, maxn):
    """
    Keeps a value n to within minn and maxn and returns that new value.
    
    @param n: A value
    @type n: C{float}

    @param minn: A minimum value
    @type minn: C{float}

    @param maxn: A maximum value
    @type maxn: C{float}

    @return: A value within minn and maxn
    @rtype: C{float}
    """
    return max(min(maxn, n), minn)
def set_sliders_to_hand(chart,slider1,slider2,slider3,slider_spread):
    """
    Moves the sliders to the hand's current position

    @param chart: A dictionary of dictionaries that keeps track of where all sliders are in relation to each other.
    @type chart: C{ [Scale_Widget: [Scale_Widget : Double] , [Scale_Widget :  Double]...(1) ]...(3) }

    @param slider1: The Finger 1 Scale
    @type slider1: C{Scale_Widget}
    
    @param slider2: The Finger 2 Scale
    @type slider2: C{Scale_Widget}
    
    @param slider3: The Finger 3 Scale
    @type slider3: C{Scale_Widget}
    
    @param slider_spread: The Spread Scale
    @type slider_spread: C{Scale_Widget}
    """
    
    cur_pos_1 = get_position(FINGER1)
    cur_pos_2 = get_position(FINGER2)
    cur_pos_3 = get_position(FINGER3)
    cur_pos_spread = get_position(SPREAD)

    per_pos_1=int(cur_pos_1/1950.0)
    per_pos_2=int(cur_pos_2/1950.0)
    per_pos_3=int(cur_pos_3/1950.0)
    per_pos_spread=int(cur_pos_spread/359.0)
    
    slider1.set(int(cur_pos_1/1950.0))
    slider2.set(int(cur_pos_2/1950.0))
    slider3.set(int(cur_pos_3/1950.0))
    slider_spread.set(int(cur_pos_spread/359.0))

    update_all_delays(chart,slider1,slider2,slider3,slider_spread)
    
def flash_button(btn):
    """
    Flashes a given button yellow

    @param btn: A button
    @type btn: C{Button_Widget}
    """
    memory=btn.cget("bg")
    btn.config(bg="yellow")
    btn.after(350,lambda:btn.config(bg=memory))
    btn.after(700,lambda:btn.config(bg="yellow"))
    btn.after(1050,lambda:btn.config(bg=memory))
    btn.after(1400,lambda:btn.config(bg="yellow"))
    btn.after(1750,lambda:btn.config(bg=memory))
    
def close_enough(chart,per_1_int,per_2_int,per_3_int,per_spread_int):
    """
    @param chart: A dictionary of dictionaries that keeps track of where all sliders are in relation to each other.
    @type chart: C{ [Scale_Widget: [Scale_Widget : Double] , [Scale_Widget :  Double]...(1) ]...(3) }

    @param per_1_int: The position of the slider in percentage
    @type per_1_int: C{int}
    
    @param per_2_int: The position of the slider in percentage
    @type per_2_int: C{int}
    
    @param per_3_int: The position of the slider in percentage
    @type per_3_int: C{int}
    
    @param per_spread_int: The position of the slider in percentage
    @type per_spread_int: C{int}
    """
    cur_links=chart["CURRENT_LINKS"]
    delay1_2=abs(per_1_int-per_2_int)
    delay2_3=abs(per_2_int-per_3_int)
    delay1_3=abs(per_1_int-per_3_int)

    ctrl_vel_1=calc_velocity(FINGER1,per_1_int,1950,400.0,-200,200)
    ctrl_vel_2=calc_velocity(FINGER2,per_2_int,1950,400.0,-200,200)
    ctrl_vel_3=calc_velocity(FINGER3,per_3_int,1950,400.0,-200,200)
    ctrl_vel_spread=calc_velocity(SPREAD,per_spread_int,362,400.0,-75,75)


    """
    Special movement mode for when the spread is open.
    Will move all fingers that are checked as one so there is no perceivable lag
    """
    if per_spread_int>=99:
        if delay1_2<4 and delay2_3<4 and (FINGER1 in cur_links) and (FINGER2 in cur_links) and (FINGER3 in cur_links):
            #print "delays are close, fingers are linked"
            former_mailboxes=new_temp_mail([FINGER1,FINGER2,FINGER3])
            maximum_vel=max(ctrl_vel_1,ctrl_vel_2,ctrl_vel_3,key=abs)
            set_property(0x40c, V, maximum_vel)
            set_property(SPREAD, V, ctrl_vel_spread)
            revert_temp_mail([FINGER1,FINGER2,FINGER3],former_mailboxes)
        elif delay1_2<4 and (FINGER1 in cur_links) and (FINGER2 in cur_links):
            former_mailboxes=new_temp_mail([FINGER1,FINGER2])
            maximum_vel=max(ctrl_vel_1,ctrl_vel_2,key=abs)
            set_property(0x40c, V, maximum_vel)
            set_property(FINGER3, V, ctrl_vel_3)
            set_property(SPREAD, V, ctrl_vel_spread)
            revert_temp_mail([FINGER1,FINGER2],former_mailboxes)
        elif delay2_3<4 and (FINGER2 in cur_links) and (FINGER3 in cur_links):
            former_mailboxes=new_temp_mail([FINGER3,FINGER2])
            maximum_vel=max(ctrl_vel_2,ctrl_vel_3,key=abs)
            set_property(0x40c, V, maximum_vel)
            set_property(FINGER1, V, ctrl_vel_1)
            set_property(SPREAD, V, ctrl_vel_spread)
            revert_temp_mail([FINGER3,FINGER2],former_mailboxes)
        elif delay1_3<4 and (FINGER1 in cur_links) and (FINGER3 in cur_links):
            former_mailboxes=new_temp_mail([FINGER1,FINGER3])
            maximum_vel=max(ctrl_vel_1,ctrl_vel_3,key=abs)
            set_property(0x40c, V, maximum_vel )
            set_property(FINGER2, V, ctrl_vel_2)
            set_property(SPREAD, V, ctrl_vel_spread)
            revert_temp_mail([FINGER1,FINGER3],former_mailboxes)
        else:
            set_property(FINGER1, V, ctrl_vel_1)
            set_property(FINGER2, V, ctrl_vel_2)
            set_property(FINGER3, V, ctrl_vel_3)
            set_property(SPREAD, V, ctrl_vel_spread)

    else:
        set_property(FINGER1, V, ctrl_vel_1)
        set_property(FINGER2, V, ctrl_vel_2)
        set_property(FINGER3, V, ctrl_vel_3)
        set_property(SPREAD, V, ctrl_vel_spread)

def calc_velocity(finger,scale_position,encoder_gain,velocity_gain,lower_bound,upper_bound):
    """
    Takes in a ton of arguments and calculates the velocity nessesary to move the finger to the desired position.

    @param finger: The finger to calculate velocity for.
    @type finger: c{int}
    
    @param scale_position: The position that the slider related to the finger is in.
    @type scale_position: c{int}
    
    @param encoder_gain: The gain from percentage to encoder ticks for that specific finger
    @type encoder_gain: c{int}

    @param velocity_gain: The gain from delta encoder ticks to velocity. Can also be thought of as the time for the system to reach desired position
    @type velocity_gain: c{double}

    @param lower_bound: The lower acceptable velocity allowed.
    @type lower_bound: c{int}

    @param upper_bound: The upper acceptable velocity allowed.
    @type upper_bound: c{int}
    """
    new_pos=(scale_position*encoder_gain)#1950
    cur_pos = get_position(finger)
    new_vel = (new_pos - cur_pos) / float(velocity_gain)#400.0
    ctrl_vel=constrain(int(new_vel),lower_bound,upper_bound)#-200,200
    return ctrl_vel
        
def update_positions(chart,nb,e1_var,e2_var,e3_var,e_spread_var):
    """
    Continuously keeps the position of the hand linked to the values of the sliders using velocity control.
    
    @param nb: The notebook
    @type nb: C{Notebook_Widget}
    
    @param e1_var: Finger1's Entry_Widget's StringVar()
    @type e1_var: C{Tcl_StringVar}
    
    @param e2_var: Finger2's Entry_Widget's StringVar()
    @type e2_var: C{Tcl_StringVar}
    
    @param e3_var: Finger3's Entry_Widget's StringVar()
    @type e3_var: C{Tcl_StringVar}
    
    @param e_spread_var: Spread's Entry_Widget's StringVar()
    @type e_spread_var: C{Tcl_StringVar}
    """
##    print "a"
    per_1_str=e1_var.get()
    per_2_str=e2_var.get()
    per_3_str=e3_var.get()
    per_spread_str=e_spread_var.get()
    
    per_1_int=int(per_1_str)
    per_2_int=int(per_2_str)
    per_3_int=int(per_3_str)
    per_spread_int=int(per_spread_str)
    
    if nb.select()!="" and (not demoRunning):
        if nb.tab(nb.select(), "text")=='Control':

            already_moved=close_enough(chart,per_1_int,per_2_int,per_3_int,per_spread_int)
    nb.after(150,lambda:update_positions(chart,nb,e1_var,e2_var,e3_var,e_spread_var))    
    
