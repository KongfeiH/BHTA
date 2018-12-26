#  position_controls_tab.py
#  
#  ~~~~~~~~~~~~
#  
#  pyHand Position Controls Tab
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
from tkFileDialog import *
from PIL import ImageTk
from position_controls_tab_helper import*
from IntegerEntry import *
import tkFont
import threading

k=[]

def create_demo(parent_frame, x, y):
    """
    Writes the demo button to the screen.
    
    @param parent_frame: Where you wnt to add the button
    @type parent_frame: C{Frame_Widget}

    @param x: The grid x position of where the button will go
    @type x: C{int}

    @param y: The grid y position of where the button will go
    @type y: C{int}
    """
    demo_frame = tk.Label(parent_frame)
    customFontDemo = tkFont.Font(size=15)
    
    var=BooleanVar()    
    var.set(0)
    run_stop_b = Button(demo_frame, text="Barrett Hand Demo", bg="#62CC68", font= customFontDemo)
    run_stop_b.var=var
    
    run_stop_b.pack(fill= "both" , anchor= CENTER,ipady=27)
    demo_frame.grid(row= x, column= y, sticky="NESW", pady=(10, 0),padx=10)
    return run_stop_b

#This function takes in a root and creates a Position Control Frame in the 
#Controls tab of the GUI
def position_controls(nb,parent_frame, x,y,demo_btn,handType):
    """
    Creates a position control frame in the specified area.
    This includes binding all the sliders and the grasp button as well as the checkboxes.
    
    @param nb: The notebook
    @type nb: C{Notebook_Widget}

    @param parent_frame: Where you wnt to add the button
    @type parent_frame: C{Frame_Widget}

    @param x: The grid x position of where the frame will go
    @type x: C{int}

    @param y: The grid y position of where the frame will go
    @type y: C{int}
    """
    #position_controls(0,0)
    #keeps track of the nuber of check buttons checked

    #Adding other Gui Elements as well as formatting their 
    #position on window by putting them into frames
    poscon= LabelFrame(parent_frame,text="Position Control")
    selected_frame=Frame(poscon,borderwidth=1)
    selected= Label(selected_frame, text="Selected", fg= "grey")
    canvas= Canvas(poscon, width= 20, height =170)
  
    str_var1=StringVar()
    str_var2=StringVar()
    str_var3=StringVar()
    str_var_spread=StringVar()

    #Position Control Entry Boxes
    e1= IntegerEntry(poscon, width= 5,textvariable=str_var1)
    e2= IntegerEntry(poscon, width= 5,textvariable=str_var2)
    e3= IntegerEntry(poscon, width= 5,textvariable=str_var3)
    e_spread= IntegerEntry(poscon, width= 5,textvariable=str_var_spread)

    cur_symbol=StringVar()
    symbol_options=['%','Rad','Theta','Encoder']
    symbol_menu = OptionMenu(poscon, cur_symbol, *symbol_options)
    symbol_menu.configure(width=7)
    cur_symbol.set(symbol_options[0])
    
    e1.var=str_var1
    e2.var=str_var2
    e3.var=str_var3
    e_spread.var=str_var_spread

    e1.var.set("0")
    e2.var.set("0")
    e3.var.set("0")
    e_spread.var.set("0")

    if handType!=-1:
        set_modes_tstop()

    scale_var_1=IntVar()
    scale_var_2=IntVar()
    scale_var_3=IntVar()
    scale_var_spread=IntVar()

    encode_var_1=IntVar()
    encode_var_2=IntVar()
    encode_var_3=IntVar()
    encode_var_spread=IntVar()

    #Position Control Scales/sliders
    #resolution=.1
    scale1 = Scale( poscon, variable=scale_var_1, showvalue=0,resolution=1 ,orient=HORIZONTAL,length=250, command= lambda x: update_text(scale1.get(),e1))
    scale2 = Scale( poscon, variable=scale_var_2, showvalue=0,resolution=1,orient=HORIZONTAL,length=250, command= lambda x: update_text(scale2.get(),e2))
    scale3 = Scale( poscon, variable=scale_var_3, showvalue=0,resolution=1,orient=HORIZONTAL,length=250, command= lambda x: update_text(scale3.get(),e3)) 
    scale_spread = Scale( poscon, variable=scale_var_spread, showvalue=0,resolution=1,orient=HORIZONTAL, 
        command= lambda x:update_text(scale_spread.get(), e_spread), length= 250)

    
    chart={scale1:{scale2:0,scale3:0,scale_spread:0}, scale2:{scale1:0,scale3:0,scale_spread:0}, scale3:{scale1:0,scale2:0,scale_spread:0},scale_spread:{scale1:0,scale2:0,scale3:0},"CURRENT_LINKS":set()}

    #Variables needed for checkbox buttons
    v1= BooleanVar()
    v2= BooleanVar()
    v3= BooleanVar()
    v_spread=BooleanVar()

    #Position Control Check buttons.   
    #0 is unchecked and 1 is checked
    finger1 = Checkbutton(poscon, text="Finger 1", variable= v1)  
    finger2 = Checkbutton(poscon, text="Finger 2", variable= v2)  
    finger3 = Checkbutton(poscon, text="Finger 3", variable= v3)   
    spread = Checkbutton(poscon, text="Spread",variable=v_spread)

    finger1.number= (30,4)
    finger2.number= (30,58)
    finger3.number= (30, 113)
    spread.number=  (30, 168)

    finger1.finger=FINGER1
    finger2.finger=FINGER2
    finger3.finger=FINGER3
    spread.finger=SPREAD

    scale1.encode_var=encode_var_1
    scale2.encode_var=encode_var_2
    scale2.encode_var=encode_var_3
    scale_spread.encode_var=encode_var_spread

    n={finger1:False,finger2:False,finger3:False,spread:False}

    finger1.slide=scale1
    finger2.slide=scale2
    finger3.slide=scale3
    spread.slide=scale_spread

    scale1.entry=e1
    scale2.entry=e2
    scale3.entry=e3
    scale_spread.entry=e_spread

    finger1.var = v1
    finger2.var = v2
    finger3.var = v3
    spread.var= v_spread
    
    if handType!=-1:
        update_positions(chart,nb,scale_var_1,scale_var_2,scale_var_3,scale_var_spread)

    finger1.config(command=lambda:check(True,n,chart,finger1,finger2,finger3,spread,canvas))
    finger2.config(command=lambda:check(True,n,chart,finger2,finger1,finger3,spread,canvas))
    finger3.config(command=lambda:check(True,n,chart,finger3,finger2,finger1,spread,canvas))
    spread.config(command=lambda:check(True,n,chart,spread,finger1,finger2,finger3,canvas))

    scale1.bind("<Button-1>",lambda x:call(chart,scale1,scale2,scale3,scale_spread))
    scale2.bind("<Button-1>",lambda x:call(chart,scale2,scale1,scale3,scale_spread))
    scale3.bind("<Button-1>",lambda x:call(chart,scale3,scale1,scale2,scale_spread))
    scale_spread.bind("<Button-1>",lambda x:call(chart,scale_spread,scale1,scale2,scale3))

    scale1.bind("<ButtonRelease-1>",lambda x:update_all_delays(chart,scale1,scale2,scale3,scale_spread))
    scale2.bind("<ButtonRelease-1>",lambda x:update_all_delays(chart,scale2,scale1,scale3,scale_spread))
    scale3.bind("<ButtonRelease-1>",lambda x:update_all_delays(chart,scale3,scale1,scale2,scale_spread))
    scale_spread.bind("<ButtonRelease-1>",lambda x:update_all_delays(chart,scale_spread,scale1,scale2,scale3))

    e1.bind('<Return>', lambda x: set_scale(chart,finger1,finger2,finger3,spread))
    e2.bind('<Return>', lambda x: set_scale(chart,finger2,finger1,finger3,spread))
    e3.bind('<Return>', lambda x: set_scale(chart,finger3,finger1,finger2,spread))
    e_spread.bind('<Return>',lambda x:set_scale(chart,spread,finger1,finger2,finger3))

    grasp_var=BooleanVar()
    grasp_var.set(0)

    #Allows user to select all three fingers with just one button

    selectb= Checkbutton(poscon, text= "ALL FINGERS", variable= grasp_var, command= lambda: toggle(n,chart, selectb, finger1, finger2, finger3, spread, canvas))

    selectb.var=grasp_var

    percent_1=Label(poscon,textvariable=cur_symbol)
    percent_2=Label(poscon,textvariable=cur_symbol)
    percent_3=Label(poscon,textvariable=cur_symbol)
    percent_spread=Label(poscon,textvariable=cur_symbol)

    nb.bind_all("<<NotebookTabChanged>>",lambda x:tab_selected(nb,chart,scale1,scale2,scale3,scale_spread,handType))
    demo_btn.config(command = lambda: run_stop_toggle(demo_btn,parent_frame,chart,scale1,scale2,scale3,scale_spread))
    #Open and Close labels to give directionality to slider
    customFont = tkFont.Font(family="Helvetica", size=12)
    canvas_open= Canvas(poscon, width=30, height=200)
    canvas_close= Canvas(poscon, width=35, height=200)

    canvas_open.create_text(17, 100,text = "\n".join("OPEN GRASP"))
    canvas_close.create_text(17, 100,text = "\n".join("CLOSE GRASP"))

    canvas_open.create_line(29, 10,29, 192)
    canvas_open.create_line(5, 10,5, 192)
    canvas_close.create_line(29, 10,29, 192)
    canvas_close.create_line(5, 10,5, 192)    
 
    canvas_open.grid(row=0,column=3, rowspan=4)
    canvas_close.grid(row=0,column=5,rowspan=4)
    
    #Formatting Spacing of all the above components
    finger1.grid(row= 0, column= 2,sticky="w", pady=15)
    e1.grid(row= 0, column= 6,sticky="e")
    percent_1.grid(row=0,column=7)
    scale1.grid(row= 0, column= 4, columnspan= 1,pady=15)

    finger2.grid(row=1 , column=2,sticky="w", pady=15)
    e2.grid(row= 1, column= 6,sticky="e", pady=15)
    percent_2.grid(row=1,column=7, pady=15)
    scale2.grid(row= 1, column= 4, columnspan= 1,pady=15)

    finger3.grid(row= 2, column=2,sticky="w", pady=15)
    e3.grid(row= 2, column=6,sticky="e", pady=15)
    percent_3.grid(row=2,column=7, pady=15)
    scale3.grid(row= 2, column= 4, columnspan=1,pady=15)

    selectb.grid(row= 1, column= 0,pady=10)

    canvas.grid(row=0, column=1, rowspan=4 , pady=(0,0))

    spread.grid(row= 3, column= 2,sticky="w", pady=15)
    e_spread.grid(row= 3, column= 6,sticky="e", pady=15)
    percent_spread.grid(row=3,column=7, pady=15)
    scale_spread.grid(row= 3, column= 4, columnspan=1, pady=15)
        
    poscon.grid(row= y, column= x,rowspan=3,pady=(14,0), sticky="ns")
    create_bottom_pos_frame(poscon, 0, 5,[finger1,finger2,finger3,spread],demo_btn, chart, scale1, scale2, scale3, scale_spread)

def create_bottom_pos_frame(parent_frame, x, y,check_list, demo_btn, chart, scale1, scale2, scale3, scale_spread):
    """
    Creates a frame that goes at the bottom of the position control section

    @param parent_frame: the frame on which the bottom frame is created
    @type parent_frame: any variation of tkinter frame (ex. LabelFrame)

    @param x: the column that the bottom frame is placed in
    @type x: c{int}

    @param y: the row that the bottom frame is placed in
    @type y: c{int}

    @param check_list: passed to create_load_save function

    @param chart: passed to create_load_save function
    """
    bottom_frame = Frame(parent_frame)
    create_reset_buttons(bottom_frame, 0, 0, parent_frame, demo_btn, chart, scale1, scale2, scale3, scale_spread)
    create_load_save(bottom_frame, 1, 0,check_list,chart)
    bottom_frame.grid(row = y, column = x, columnspan = 7, padx = 5, pady = 5)

def create_reset_buttons(parent_frame, x, y, f, demo_btn, chart, scale1, scale2, scale3, scale_spread):
    """
    Creates a frame that holds all of the buttons that reset individual fingers

    @param parent_frame: the frame on which the reset finger frame is created
    @type parent_frame: any variation of a Tkinter frame (ex. LabelFrame)

    @param x: the column that the reset finger frame is gridded on
    @type x: c{int}

    @param x: the row that the reset finger frame is gridded on
    @type x: c{int}
    """
    toDisable = f._nametowidget(f.winfo_parent())
    reset_frame = tk.LabelFrame(parent_frame, text = "Finger Reset Buttons")
    reset1 = Button(reset_frame, text = "Finger 1", command = lambda: reset_finger(FINGER1, toDisable, demo_btn, chart, scale1, scale2, scale3, scale_spread))
    reset2 = Button(reset_frame, text = "Finger 2", command = lambda: reset_finger(FINGER2, toDisable, demo_btn, chart, scale1, scale2, scale3, scale_spread))
    reset3 = Button(reset_frame, text = "Finger 3", command = lambda: reset_finger(FINGER3, toDisable, demo_btn, chart, scale1, scale2, scale3, scale_spread))
    reset4 = Button(reset_frame, text = "Spread", command = lambda: reset_finger(SPREAD, toDisable, demo_btn, chart, scale1, scale2, scale3, scale_spread))

    reset1.grid(row = 0, column = 0, padx = 5, pady = 5)
    reset2.grid(row = 0, column = 1, padx = 5, pady = 5)
    reset3.grid(row = 1, column = 0, padx = 5, pady = 5)
    reset4.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = E+W)
    reset_frame.grid(row = y, column = x, columnspan = 1, padx = 5, pady = 10, sticky = N+S+E)

def create_load_save(parent_frame, x, y,check_list,chart):
    """
    Makes a load save frame in the specified area.

    @param parent_frame: Where you wnt to add the button
    @type parent_frame: C{Frame_Widget}

    @param x: The grid x position of where the frame will go
    @type x: C{int}

    @param y: The grid y position of where the frame will go
    @type y: C{int}

    @param check_list: A list of all Checkbox Widgets
    @type check_list: C{[CheckBox_Widget...(3)]}

    @param chart: A dictionary of dictionaries that keeps track of where all sliders are in relation to each other.
    @type chart: C{ [Scale_Widget: [Scale_Widget : Double] , [Scale_Widget :  Double]...(1) ]...(3) }

    """
    pos_chart={}
    entry_list=[check_list[0].slide.entry,check_list[1].slide.entry,check_list[2].slide.entry,check_list[3].slide.entry]
    scale_list=[check_list[0].slide,check_list[1].slide,check_list[2].slide,check_list[3].slide]
    
    load_save_frame= tk.LabelFrame(parent_frame,text="User Defined Hand Position")

   
    OPTIONS=load_hand_positions(pos_chart)
    pos_var = StringVar(load_save_frame)
    if len(OPTIONS)>0:
        # default value
        pos_var.set(OPTIONS[0]) 
    else:
        OPTIONS.append("Memory File Cannot be Read or is Empty")

    e= Entry(load_save_frame, textvariable=pos_var, width= 25)
    e.get()
    
    config_opts_frame=Frame(load_save_frame)
    
    save_btn= Button(config_opts_frame, text=" Save Position ", command= lambda:save_hand_positions(chart,pos_chart,e,option,OPTIONS,load_save_frame,pos_var,entry_list,scale_list,load_btn))
    load_btn= Button(config_opts_frame, text=" Load Position ", command=lambda:set_hand_pos(chart,scale_list,pos_var.get(),pos_chart,parent_frame.master))
    del_btn=Button(config_opts_frame,text=" Delete Position ", command =lambda:del_pos(option,OPTIONS,pos_chart,pos_var.get(),pos_var,load_save_frame,load_btn))

    option = OptionMenu(load_save_frame, pos_var, *OPTIONS,command=lambda x:flash_button(load_btn))

    save_btn.grid(row=0,column=0, padx = 2, pady = 2, stick="e")
    load_btn.grid(row=1,column=0, padx = 2, pady = 2, stick="e")
    del_btn.grid(row=2,column=0, padx = 2, pady = 2, stick="e")
    
    e.grid(row= 0, column= 0,padx=5)
    config_opts_frame.grid(row=0,column=1, rowspan=2)
    config_opts_frame.columnconfigure(0,weight=1)
    option.grid(row= 1, column= 0,sticky="ew")
    
    option.grid_rowconfigure(0,weight=1)
    option.grid_rowconfigure(1,weight=1)
    option.grid_columnconfigure(0,weight=1)
    option.grid_columnconfigure(1,weight=1)

    load_save_frame.grid(row= y, column= x, columnspan = 4, pady=10,sticky="NS")


#Takes in a notebook and creates the controls tab
def create_position_control_tab(nb, handType):
    """
    The main function of controls tab.
    Calls all affiliated functions and takes care of highest tab level event handling.

    @param nb: The notebook
    @type nb: C{Notebook_Widget}

    @param handType: The type of hand that is detected by the gui
    @type handType: C{int}
    """
    position_control_frame = tk.Frame(nb, name='control')
    t = "Barrett Hand Model: "
    f = None
    if(handType == 0):
        t += "282"
        f = "Images/BH_282_shiny_smaller.png"
    elif(handType == 1):
        t += "280"
        f = "Images/BH_280_small.png"
    else:
        t += "Unknown"
        f = "Images/BH_282_shiny_smaller.png"
        
    bannerFont = tkFont.Font(size = 30)
    visual_frame= LabelFrame(position_control_frame, font = bannerFont, text=t, relief= "groove", borderwidth=1)
    
    photo= ImageTk.PhotoImage(file= f)
    label = Label(visual_frame,image=photo)
    # keep a reference!
    label.image = photo 

    label.grid(row=0, column=0, pady=(10,0))
    
    visual_frame.grid(row=0, column=0, padx = 10)
    visual_frame.grid_columnconfigure(0,weight=1)
    visual_frame.grid_rowconfigure(0,weight=1)
    
    that_button=create_demo(position_control_frame,2,0)
    position_controls(nb,position_control_frame, 1, 0,that_button,handType)
     
    # add to notebook (underline = index for short-cut character)
    nb.add(position_control_frame, text='Control', underline=0, padding=2)
    if handType !=0 and handType!=1:
        fake_btn=Button(None)
        disable_list(fake_btn,nb.tab_slaves())
        that_button.config(state="disabled")
