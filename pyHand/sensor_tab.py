#  sensor_tab.py
#  
#  ~~~~~~~~~~~~
#  
#  pyHand Sensor Tab File
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
#  This version of the pyHand is free software: you can 
#  redistribute it and/or modify it under the terms of the GNU General Public
#  License as published by the Free Software Foundation.
#
from Tkinter import *
import ttk as tk
from PIL import ImageTk
from PIL import Image
from sensor_tab_helper import *
import tkFont

from pyHand_API.pyHand_api import *
from pyHand_API.puck_properties_consts import*




def populate_sensor_tab(sensor_tab, x, y, tactile, nb, strain, thermister, handtype):
    '''
    Populates sensor tab with all it's contents.
    Some of which are: Tactile sensor array, tare and start tactile sensor array button,
    puck and motor temp and fingertip torque sensor displays.

    @param sensor_tab: the frame in which everything is created on.

    @param x: the x coordinate to place the fram.

    @param y: the y coordinate to place the frame.

    @param tactile: tells whether or not the hand model has tactile sensors. 1 if yes, 0 if no and -1 if unkown.

    @param nb: the notebook the sensor tab is to be included in.
     '''
    #=======================Class Tactile Sensor ==================================
    class tact_unit():
        '''
        Creates a tact_unit object.

        Availabel attributes are:
        canvas, position coordinates, offset coordinates, width, height,
        fill color, greyscale "transparency value" , and  text.

        @cvar coord: coordinates of rectangle on canvas.
        @type coord: C{(int, int)}

        @cvar offset: values to offset the coordinates of rectangle on canvas by.
        @type offset: C{(int, int)}

        @cvar width: width of rectangle on canvas.
        @type width: C{int}

        @cvar width: length of rectangle on canvas.
        @type width: C{int}

        @cvar fill: fill color of rectangle on canvas.
        @type fill: C{String}

        @cvar stipple: level of transparency of rectangle on canvas.
        @type stipple: C{String}

        @cvar text: text in rectangle on canvas.
        @type text: C{String}
        '''
        def __init__(self, canvas, coord=(0,0),offset=(0,0),width=0,
                     length=0,fill="",stipple="",text="0"):
            self.coord=coord
            self.offset=offset
            self.width=width
            self.length=length
            self.fill=fill
            self.stipple=stipple
            self.text=text
            
            self.make_rect(canvas)

        def make_rect(self, canvas):
            '''
            Creates a rectangle object on a canvas.

            @param canvas: canvas rectangle is to be created on.
            '''
            self.rect=canvas.create_rectangle(
                      self.coord,
                      self.coord[0]+self.width,
                      self.coord[1]+self.length,
                      outline="black",
                      fill=self.fill,
                      stipple=self.stipple)
            canvas.move(self.rect, self.offset[0], self.offset[1])
            self.label= canvas.create_text(zero(self.coord[0], self.coord[1]),
                                           text=self.text)
    #====================== Sensor Tab Functions====================================

    def enable_tabs(nb,tab_list):
        '''
        Enables all tabs previously disabled.

        @param nb: notebook to enable tabs from.

        @param tab_list: list of tabs to be enabled.
        '''
        for tab in tab_list:
            nb.tab(tab,state="normal")

    def disable_tabs(nb,tab_list):
        '''
        Disables all tabs but the one user is on.

        @params nb: notebook to disable tabs from.

        @params tab_list: list of tabs to be disabled.
        '''
        for tab in tab_list:
            if nb.tab(tab,"text")!="Sensors":
                nb.tab(tab,state="disabled")
                
    def zero(x, y):
        '''
        Zeros out coordinates of a canvas object since (0,0) on canvas is not in top left corner.

        @param x: x vlaue of position coordinate (can be int or float).
        @param y: y value of position coordinate (can be int or float).

        @return offsetx: the new x value of position offset with top left corner being (0,0).
        @return offsety: the new y value of position offset with top left corner being (0,0).
        '''
        offsetx=0
        offsety=0
        if x>=0:
            offsetx= -274+x
            offsety= -193+y
        return offsetx, offsety


    def on_puck_temp_call(label, puckID, sat_label_puck, handtype):
        '''
        Gets the pucks temperature and displays it to screen. Also warns user if puck temp is too high.

        @param label: Label widget that is to be updated with new fingertip torque value.
        
        @param puckID: puck ID.
        
        @param sat_label: The saturation warning label.

        @param tactile: tells whether or not the hand model has tactile sensors. 1 if yes, 0 if no and -1 if unkown.
        '''
        if handtype == -1:
            sat_label_puck.config(bg="#B80000",fg="white", text= "Sensor Not Detected" )
        else:
            temp= get_temp(puckID)
            label.config( text= temp,bg="#F0F0F0",fg="black")
            if temp>= 75:
                label.config(text= temp,bg="#B80000",fg="white")

    def on_motor_temp_call(label, puckID, sat_label_motor, thermister):
        '''
        Gets the motor temperature and displays it to screen. Also warns user if motortemp is too high.

        @param label: Label widget that is to be updated with new fingertip torque value.

        @param puckID: puck ID.
        
        @param sat_label: The saturation warning label.

        @param tactile: tells whether or not the hand model has tactile sensors. 1 if yes, 0 if no and -1 if unkown.
        '''
        if thermister == -1:
            sat_label_motor.config(bg="#B80000",fg="white", text= "Sensor Not Detected" )
        else:
            therm= get_therm(puckID)
            label.config(text=therm, bg="#F0F0F0",fg="black")
            if therm >= 75:
               label.config( bg="#B80000", text= therm,fg="white")

    def on_strain_call(w, puckID, sat_label_strain, strain):
        '''
        Gets the fingertip torque sensors and displays it to screen. Also warns user if fingertip torque is too high or too low.

        @param label: Label widget that is to be updated with new fingertip torque value.
        
        @param puckID: puck ID.
        
        @param sat_label_strain: The saturation warning label for fingertip torque sensor.
        @type sat_label_strain: C{Label_Widget}
        
        @param strain: tells whether or not the hand model has strain sensors. 1 if yes, 0 if no and -1 if unkown.
        '''
        if strain == -1 or strain == 0:
            sat_label_strain.config(bg="#B80000",fg="white", text= "Sensor Not Detected" )
        else:
            strain= get_strain(puckID)
            update_bar(w, puckID-11, strain)

    def update_color(canvas,rect,tact_val):
        '''
        Updates the color of the tactile sensor rectangle unit corresponding to the tactile senor's value.

        @param canvas: the canvas the tactile unit rectangle is created on.

        @param rect: the tactile rectangle unit.

        @param tact_val: value of the tactile sensing unit.
        '''
        if tact_val<2.5:
            canvas.itemconfig(rect,stipple="",fill="")
        elif 2.5<tact_val and tact_val<5:
             canvas.itemconfig(rect,stipple="gray25",fill="blue")
        elif 5<tact_val and tact_val<7.5:
             canvas.itemconfig(rect,stipple="gray50",fill="blue")
        elif 7.5<tact_val and tact_val<10:
             canvas.itemconfig(rect,stipple="gray75",fill="blue")
        else:
             canvas.itemconfig(rect,stipple="",fill="blue")

    #NEED TO UPDATE
    def update_color_strain(w, n, strain_val):
        '''
        Updates the color of the fingertip torque sensor bar graph.

        @param w: the canvas the fingertip torque sensor bar graph is created on.

        @param n: the finger number 1,2, 3, or 4 for spread.

        @param strain_val: value of strain from the fingertip force torque sensors in raw encoder format.

        '''
        nm= strain_to_nm(strain_val)
        if nm<=0.32 and nm>=-0.32:
            w.itemconfig(w.rects[n],stipple="",fill="")
        elif (nm<=0.64 and nm > 0.32) or (nm>=-0.64 and nm<-0.32):
            w.itemconfig(w.rects[n],stipple="gray25",fill="blue")
        elif (nm>0.64 and nm<=0.96) or (nm < -0.64 and nm>=-0.96):
            w.itemconfig(w.rects[n],stipple="gray50",fill="blue")
        elif (nm<=1.28 and nm> 0.96) or  (nm>=-1.28 and nm<-0.96):
            w.itemconfig(w.rects[n],stipple="gray75",fill="blue")
        elif (nm>1.28 and nm<=1.6) or (nm<-1.28 and nm>=-1.6):
            w.itemconfig(w.rects[n], stipple= "", fill ="blue")
        else:
             w.itemconfig(w.rects[n],stipple="",fill="red")

    def update(canvas, on_off, matrix,s,label1,label2,label3,puck_labels,motor_labels,sat_label_puck, sat_label_motor, sat_label_strain,counter,nb, w):
        '''
        A single recursive function call that updates the values of each tactile sensing unit as well as the
        puck temp, motor temp, and fingertip torque sensors. This ws done in a single recursive call to eliminate
        time dealys for when  multiple processes occurred simultaniously.

        @param canvas: the canvas the tactile unit rectangle is created on.

        @param on_off: the start tactile array sensor variable which indicates the state of the button (1 is on, 0 is off)
        @type on_off: C{int}

        @param matrix: an array of fingers (and palm) which consist of array of tact_units. 
        @type matrix: C{[[tact_unit]]}

        @param s: HandSensor object

        @param label1: fingertip torque sensor label for Finger1
        @type label1: C{Label_Widget}

        @param label2: fingertip torque sensor label for Finger2
        @type label1: C{Label_Widget}

        @param label3: fingertip torque sensor label for Finger3
        @type label1: C{Label_Widget}

        @param puck_labels: puck temperature label for all fingers
        @type label1: C{[Label_Widget]}

        @param motor_labels: motor temperature label for all fingers
        @type label1: C{[Label_Widget]}

        @param sat_label_puck:  The saturation warning label for puck temperature
        @type label1: C{Label_Widget}

        @param sat_label_motor: The saturation warning label for motor temperature
        @type label1: C{Label_Widget}

        @param sat_label_strain: The saturation warning label for fingertip torque sensor
        @type label1: C{Label_Widget}

        @param counter: parameter to keep track of update/refresh times (int of 0-100)

        @param nb: notebook to enable tabs from.
        
        '''
        update_rate=10
        if nb.select()!="":
            if nb.tab(nb.select(), "text") == "Sensors":
                counter+=1
                if counter>100:
                    counter=0

                if on_off.get()==1:
                    s.get_full_tact()
                    
                    arr=matrix[0] 
                    for i in range(len(s.finger1)):
                        canvas.itemconfig(arr[i].label,text=s.finger1[i])
                        update_color(canvas,arr[i].rect,s.finger1[i])

                    arr2=matrix[1] 
                    for j in range(len(s.finger2)):
                        canvas.itemconfig(arr2[j].label,text=s.finger2[j])
                        update_color(canvas,arr2[j].rect,s.finger2[j])

                    arr3=matrix[2] 
                    for i in range(len(s.finger3)):
                         canvas.itemconfig(arr3[i].label,text=s.finger3[i])
                         update_color(canvas,arr3[i].rect,s.finger3[i])        

                    arr4=matrix[3]
                    for i in range(len(s.spread)):
                         canvas.itemconfig(arr4[i].label,text=s.spread[i])
                         update_color(canvas,arr4[i].rect,s.spread[i])
                     
                if on_off.get()==1:     
                    if counter%10==0:
                        on_strain_call(w,FINGER1,sat_label_strain, strain)
                    if (counter+4)%10==0:
                        on_strain_call(w,FINGER2,sat_label_strain, strain)
                    if (counter+8)%10==0:
                        on_strain_call(w,FINGER3,sat_label_strain, strain)

                    if counter%100==0:
                        #Puck Temperature
                        on_puck_temp_call(puck_labels[0],FINGER1,sat_label_puck, handtype)
                    if (counter+12)%100==0:
                        on_puck_temp_call(puck_labels[1],FINGER2,sat_label_puck,handtype)
                    if (counter+24)%100==0:
                        on_puck_temp_call(puck_labels[2],FINGER3,sat_label_puck,handtype)
                    if (counter+36)%100==0:
                        on_puck_temp_call(puck_labels[3],SPREAD,sat_label_puck,handtype)

                        #Motor Temperature
                    if (counter+48)%100==0:
                        on_motor_temp_call(motor_labels[0],FINGER1,sat_label_motor,thermister)
                    if (counter+60)%100==0:
                        on_motor_temp_call(motor_labels[1],FINGER2,sat_label_motor,thermister)
                    if (counter+72)%100==0:
                        on_motor_temp_call(motor_labels[2],FINGER3,sat_label_motor,thermister)
                    if (counter+84)%100==0:
                        on_motor_temp_call(motor_labels[3],SPREAD,sat_label_motor,thermister)
                        
                if on_off.get()==0:
                    on_strain_call(w,FINGER1,sat_label_strain, strain)
                    on_strain_call(w,FINGER2,sat_label_strain, strain)
                    on_strain_call(w,FINGER3,sat_label_strain, strain)
                    
                    if counter%15==0:
                        #Puck Temperature
                        on_puck_temp_call(puck_labels[0],FINGER1,sat_label_puck, handtype)
                        on_puck_temp_call(puck_labels[1],FINGER2,sat_label_puck, handtype)
                        on_puck_temp_call(puck_labels[2],FINGER3,sat_label_puck, handtype)
                        on_puck_temp_call(puck_labels[3],SPREAD,sat_label_puck, handtype)

                        #Motor Temperature
                        on_motor_temp_call(motor_labels[0],FINGER1,sat_label_motor, thermister)
                        on_motor_temp_call(motor_labels[1],FINGER2,sat_label_motor, thermister)
                        on_motor_temp_call(motor_labels[2],FINGER3,sat_label_motor, thermister)
                        on_motor_temp_call(motor_labels[3],SPREAD,sat_label_motor, thermister)

        canvas.after(update_rate, lambda: update( canvas, on_off, matrix, s,label1,label2,label3,puck_labels,motor_labels,sat_label_puck, sat_label_motor, sat_label_strain,counter,nb, w))

    def toggle(canvas,btn, top_frame,matrix,s,label1,label2,label3):
        '''
        Updates the Start Tactile Sensor Array button to toggle Start/Stop.
        
        @param canvas: the canvas the tactile unit rectangle is created on.

        @param btn: button to be toggled

        @param top_frame: top level frame with widgets on it.
        @type top_frame: C{Frame_Widget}

        @param matrix: an array of fingers (and palm) which consist of array of tact_units. 
        @type matrix: C{[[tact_unit]]}

        @param s: HandSensor object

        @param label1: fingertip torque sensor label for Finger1
        @type label1: C{Label_Widget}

        @param label2: fingertip torque sensor label for Finger2
        @type label1: C{Label_Widget}

        @param label3: fingertip torque sensor label for Finger3
        @type label1: C{Label_Widget}
        '''
        nb= top_frame.master
        tab_list= nb.tabs()
        if btn.var.get() == 0:
            btn.config(text='Stop Tactile Sensor Array', bg="#B80000", fg="black", relief= "sunken")
            btn.var.set(1)
            disable_tabs(nb, tab_list)
        elif btn.var.get()==1:
            btn.config(text='Start Tactile Sensor Array', bg="#62CC68", fg="black",relief="raised")
            btn.var.set(0)
            enable_tabs(nb, tab_list)

    def enable_buttons(sensor_tab, tactile, update_data):
        '''
        Creates button to steam of tactile sensor array data if hand has tactile sensors. Disables button if there are no tactile sensors.

        @param sensor_tab: frame
        @type sensor_tab: C{Frame_Widget}
        
        @param tactile: tells whether or not the hand model has tactile sensors. 1 if yes, 0 if no and -1 if unkown.

        @param update_data: Start Tactile Sensor Array toggle button.
        '''
        if tactile == 1:
            pass
        if tactile == 0 or tactile ==-1:
            update_data.config(state="disabled")
    
    #creates frame for canvas to display tactile sensor array data                                       
    image_frame=tk.LabelFrame(sensor_tab)

    #create canvas object
    canvas = Canvas(image_frame, height='20c', width='17c')
   
    ##==================RESIZES IMAGE ON CANVAS (TACTILE UNITS) BASED ON BASEHIEGHT===========
    #Finger image resizing, saves resized version to Images folder
    baseheight = 370
    img = Image.open("Images/Finger_withgrid_edit.png")
    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, 25+baseheight), Image.ANTIALIAS)
    img.save("Images/Finger_withgrid_edit2.png")

    #palm image resizing, saves resized version to Images folder
    baseheight_p = 350
    img_p = Image.open("Images/Palm_withgrid_edit.png")
    hpercent_p = (baseheight_p / float(img_p.size[1]))
    wsize_p = int((float(img_p.size[0]) * float(hpercent_p)))
    img_p = img_p.resize((wsize_p, baseheight_p), Image.ANTIALIAS)
    img_p.save("Images/Palm_withgrid_edit2.png")

    #creates a photo object
    photo_finger = ImageTk.PhotoImage(file= "Images/Finger_withgrid_edit2.png")
    photo_palm = ImageTk.PhotoImage(file="Images/Palm_withgrid_edit2.png")

    #creates labels with image set to photo object
    photo_label =Label(image_frame, image= photo_finger)
    photo_labelp = Label(image_frame, image= photo_palm)

    #saves refrence to image (this step is necissary or else images wont show on gui)
    photo_label.image = photo_finger 
    photo_labelp.image = photo_palm 

    #adds the images to canvas
    canvas.create_image(25,390,image=photo_palm)
    canvas.create_image(-175,0, image = photo_finger)
    canvas.create_image(225, 0, image= photo_finger)
    canvas.create_image(25,0, image = photo_finger)

    #creating large labels for each finger and adding to canvas
    font1 = tkFont.Font(size = 15, weight= "bold")

    canvas.create_text(-175,-180, text= "Finger1", font=font1)
    canvas.create_text(225, -180,text="Finger3", font=font1)
    canvas.create_text(25,-180,text="Finger2", font= font1)
    canvas.create_text(25,230,text="Palm", font= font1)

    #Because I had this line of code from the begining...
    #All my tactile unit positions require the line of code below :(
    canvas.config(scrollregion=canvas.bbox(ALL))        

    #==============================FINGER1==========================================
    x1= tact_unit(canvas, (57, 330), (-293, -208), 38, 42, text ="1")

    x2= tact_unit(canvas, (100, 330), (-293, -210), 38, 42, text="2") 

    x3= tact_unit(canvas, (142, 330), (-293, -210), 38, 42, text="3") 

    x4= tact_unit(canvas, (57, 284), (-293, -208), 38, 40, fill="blue",stipple="gray12", text="4") 

    x5= tact_unit(canvas, (100, 284), (-293, -208), 38, 40, fill="blue",stipple="gray12", text="5") 

    x6= tact_unit(canvas, (142, 284), (-293, -208), 38, 40, fill="blue",stipple="gray12", text="6")

    x7= tact_unit(canvas, (57, 242), (-293, -212), 38, 43, fill="blue",stipple="gray12", text="7") 

    x8= tact_unit(canvas, (100, 242), (-293, -212), 38, 43, fill="blue",stipple="gray12", text="8") 

    x9= tact_unit(canvas, (142, 242), (-293, -212), 38, 43, fill="blue",stipple="gray12", text="9") 

    x10= tact_unit(canvas, (57, 191), (-293, -210), 38, 44, fill="blue",stipple="gray25", text="10") 

    x11= tact_unit(canvas, (100, 191), (-293, -210), 38, 44, fill="blue",stipple="gray25", text="11")

    x12= tact_unit(canvas, (142, 191), (-293, -210), 38, 44, fill="blue",stipple="gray25", text="12") 

    x13= tact_unit(canvas, (57, 145), (-293, -213), 38, 45, fill="blue",stipple="gray50", text="13") 

    x14= tact_unit(canvas, (100, 145), (-293, -213), 38, 45, fill="blue",stipple="gray50", text="14") 

    x15= tact_unit(canvas, (142, 145), (-293, -213), 39, 45, fill="blue",stipple="gray50", text="15")

    x16= tact_unit(canvas, (57, 107), (-293, -205), 39, 26, fill="blue",stipple="gray75", text="16") 

    x17= tact_unit(canvas, (100, 107), (-293, -205), 39, 26, fill="blue",stipple="gray75", text="17") 

    x18= tact_unit(canvas, (142, 107), (-293, -205), 39, 26, fill="blue",stipple="gray75", text="18")

    x19= tact_unit(canvas, (57, 75), (-293, -204), 38, 26, fill="blue",stipple="gray75", text="19") 

    x20= tact_unit(canvas, (100, 75), (-293, -204), 38, 26, fill="blue",stipple="gray75", text="20") 

    x21= tact_unit(canvas, (142, 75), (-292, -204), 38, 27, fill="blue",stipple="gray75", text="21") 

    x22= tact_unit(canvas, (57, 49), (-293, -201), 38, 20, fill="blue",stipple="", text="22") 

    x23= tact_unit(canvas, (100, 49), (-293, -201), 38, 20, fill="blue",stipple="", text="23") 

    x24= tact_unit(canvas, (142, 49), (-293, -201), 39, 20, fill="blue",stipple="", text="24")

  
    #===============================FINGER2=================================================
    
    y1= tact_unit(canvas, (257, 330), (-293, -208), 38, 42 ,text="1")

    y2= tact_unit(canvas, (300, 330), (-293, -210), 38, 42, text="2") 

    y3= tact_unit(canvas, (342, 330), (-293, -210), 38, 42, text="3") 

    y4= tact_unit(canvas, (257, 284), (-293, -209), 38, 43, fill="blue",stipple="gray12", text="4") 

    y5= tact_unit(canvas, (300, 284), (-293, -209), 38, 43, fill="blue",stipple="gray12", text="5") 

    y6= tact_unit(canvas, (342, 284), (-293, -209), 38, 43, fill="blue",stipple="gray12", text="6")
  
    y7= tact_unit(canvas,  (257, 242), (-293, -213), 38, 44, fill="blue",stipple="gray12", text="7") 

    y8= tact_unit(canvas, (300, 242), (-293, -213), 38, 44, fill="blue",stipple="gray12", text="8") 

    y9= tact_unit(canvas, (342, 242), (-293, -213), 38, 44, fill="blue",stipple="gray12", text="9")
    
    y10= tact_unit(canvas, (257, 191), (-293, -210), 38, 44, fill="blue",stipple="gray25", text="10") 

    y11= tact_unit(canvas, (300, 191), (-293, -210), 38, 44, fill="blue",stipple="gray25", text="11")

    y12= tact_unit(canvas,(342, 191), (-293, -210), 38, 44, fill="blue",stipple="gray25", text="12") 

    y13= tact_unit(canvas, (257, 145), (-293, -213), 38, 45, fill="blue",stipple="gray50", text="13") 

    y14= tact_unit(canvas, (300, 145), (-293, -213), 38, 45, fill="blue",stipple="gray50", text="14") 

    y15= tact_unit(canvas, (342, 145), (-293, -213), 39, 45, fill="blue",stipple="gray50", text="15")

    y16= tact_unit(canvas, (257, 107), (-293, -205), 39, +26, fill="blue",stipple="gray75", text="16") 

    y17= tact_unit(canvas, (300, 107), (-293, -205), 39, 26, fill="blue",stipple="gray75", text="17") 

    y18= tact_unit(canvas, (342, 107), (-293, -205), 39, 26, fill="blue",stipple="gray75", text="18")

    y19= tact_unit(canvas, (257, 75), (-293, -204), 38, 26, fill="blue",stipple="gray75", text="19") 

    y20= tact_unit(canvas, (300, 75), (-293, -204), 38, 26, fill="blue",stipple="gray75", text="20") 

    y21= tact_unit(canvas, (342, 75), (-292, -204), 38, 27, fill="blue",stipple="gray75", text="21") 

    y22= tact_unit(canvas, (257, 49), (-293, -201), 38, 20, fill="blue",stipple="", text="22") 

    y23= tact_unit(canvas, (300, 49), (-293, -201), 38, 20, fill="blue",stipple="", text="23") 

    y24= tact_unit(canvas, (342, 49), (-293, -201), 39, 20, fill="blue",stipple="", text="24")


   #===============================FINGER3=================================================


    z1= tact_unit( canvas, (457, 330), (-293, -208), 38, 42,  text="1")

    z2= tact_unit( canvas, (500, 330), (-293, -210), 38, 42,  text="2") 

    z3= tact_unit( canvas, (542, 330), (-293, -210), 38, 42,  text="3")

    z4= tact_unit( canvas, (457, 284), (-293, -209), 38, 43, fill="blue",stipple="gray12", text="4") 

    z5= tact_unit( canvas, (500, 284), (-293, -209), 38, 43, fill="blue",stipple="gray12", text="5") 

    z6= tact_unit( canvas, (542, 284), (-293, -209), 38, 43, fill="blue",stipple="gray12", text="6")

    z7= tact_unit( canvas, (457, 242), (-293, -213), 38, 44, fill="blue",stipple="gray12", text="7") 

    z8= tact_unit( canvas, (500, 242), (-293, -213), 38, 44, fill="blue",stipple="gray12", text="8") 

    z9= tact_unit( canvas, (542, 242), (-293, -213), 38, 44, fill="blue",stipple="gray12", text="9") 
   
    z10= tact_unit( canvas, (457, 191), (-293, -210), 38, 44, fill="blue",stipple="gray25", text="10") 

    z11= tact_unit( canvas, (500, 191), (-293, -210), 38, 44, fill="blue",stipple="gray25", text="11")

    z12= tact_unit( canvas, (542, 191), (-293, -210), 38, 44, fill="blue",stipple="gray25", text="12") 

    z13= tact_unit( canvas, (457, 145), (-293, -213), 38, 45, fill="blue",stipple="gray50", text="13") 

    z14= tact_unit( canvas, (500, 145), (-293, -213), 38, 45, fill="blue",stipple="gray50", text="14") 

    z15= tact_unit( canvas, (542, 145), (-293, -213), 39, 45, fill="blue",stipple="gray50", text="15")

    z16= tact_unit( canvas, (457, 107), (-293, -205), 39, 26, fill="blue",stipple="gray75", text="16")

    z17= tact_unit( canvas, (500, 107), (-293, -205), 39, 26, fill="blue",stipple="gray75", text="17") 

    z18= tact_unit( canvas, (542, 107), (-293, -205), 39, 26, fill="blue",stipple="gray75", text="18")
    
    z19= tact_unit( canvas, (457, 75), (-293, -204), 38, 26, fill="blue",stipple="gray75", text="19") 

    z20= tact_unit( canvas, (500, 75), (-293, -204), 38, 26, fill="blue",stipple="gray75", text="20") 

    z21= tact_unit( canvas, (542, 75), (-292, -204), 38, 27, fill="blue",stipple="gray75", text="21") 

    z22= tact_unit( canvas, (457, 49), (-293, -201), 38, 20, fill="blue",stipple="", text="22") 

    z23= tact_unit( canvas, (500, 49), (-293, -201), 38, 20, fill="blue",stipple="", text="23") 

    z24= tact_unit( canvas, (542, 49), (-293, -201), 39, 20, fill="blue",stipple="", text="24")
    

   #===============================SPREAD=================================================


    s1= tact_unit( canvas, (402, 525), (-298, -216), 47, 47, text="1")

    s2= tact_unit( canvas, (350, 525), (-298, -216), 47, 47, text="2")
    
    s3= tact_unit( canvas, (298, 525), (-297, -216), 46, 47, text="3") 

    s4= tact_unit( canvas, (245, 525), (-295, -216), 46, 47, text="4") 

    s5= tact_unit( canvas, (193, 525), (-294, -216), 46, 47, text="5") 

    s6= tact_unit( canvas, (452.5, 575), (-298, -215), 46, 47, fill="blue",stipple="gray25", text="6")

    s7= tact_unit( canvas, (402, 575), (-297, -215), 47, 46, fill="blue",stipple="gray25", text="7") 

    s8= tact_unit( canvas, (350, 575), (-296, -215), 47, 46, fill="blue",stipple="gray25", text="8") 

    s9= tact_unit( canvas, (298, 575), (-296, -215), 47, 46, fill="blue",stipple="gray25", text="9") 

    s10= tact_unit( canvas, (245, 575), (-294, -215), 47, 46, fill="blue",stipple="gray25", text="10") 

    s11= tact_unit( canvas, (193, 575), (-293, -215), 47, 46, fill="blue",stipple="gray25", text="11")

    s12= tact_unit( canvas, (140, 575), (-292, -215), 46, 46, fill="blue",stipple="gray25", text="12") 
    
    s13= tact_unit( canvas,  (452.5, 626), (-298, -215), 47, 46, fill="blue",stipple="gray50", text="13") 

    s14= tact_unit( canvas, (402, 626), (-297, -215), 47, 46, fill="blue",stipple="gray50", text="14") 

    s15= tact_unit( canvas, (350, 626), (-296, -215), 47, 46, fill="blue",stipple="gray50", text="15")

    s16= tact_unit( canvas, (298, 626), (-296, -215), 47, 46, fill="blue",stipple="gray50", text="16") 

    s17= tact_unit( canvas,  (245, 626), (-294, -215), 47, 46, fill="blue",stipple="gray50", text="17") 

    s18= tact_unit( canvas, (193, 626), (-294, -215), 47, 46, fill="blue",stipple="gray50", text="18")
    
    s19= tact_unit( canvas, (140, 626), (-293, -215), 46, 46, fill="blue",stipple="gray50", text="19") 

    s20= tact_unit( canvas, (402, 678), (-298, -215), 47, 46, fill="blue",stipple="", text="20") 

    s21= tact_unit( canvas, (350, 678), (-297, -215), 47, 46, fill="blue",stipple="", text="21") 

    s22= tact_unit( canvas, (298, 678), (-296, -215), 47, 46, fill="blue",stipple="", text="22") 

    s23= tact_unit( canvas, (245, 678), (-296, -215), 47, 46, fill="blue",stipple="", text="23") 

    s24= tact_unit( canvas, (193, 678), (-294, -215), 47, 46, fill="blue",stipple="", text="24")


   #===============================FINGER AND SPREAD ARRAYS=================================================

    Fingie1= [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13 ,x14 ,x15, x16, x17, x18, x19, x20, x21, x22, x23, x24]

    Fingie2= [y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13 ,y14 ,y15, y16, y17, y18, y19, y20, y21, y22, y23, y24]

    Fingie3= [z1, z2, z3, z4, z5, z6, z7, z8, z9, z10, z11, z12, z13 ,z14 ,z15, z16, z17, z18, z19, z20, z21, z22, z23, z24]

    Spreadie= [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13 ,s14 ,s15, s16, s17, s18, s19, s20, s21, s22, s23, s24]

    ALL_Fingies= [Fingie1, Fingie2, Fingie3, Spreadie]
    def strain_to_nm(x):
        '''
        Converts from raw encoder unit reading to Newton-meters.

        @param w: the canvas the fingertip torque sensor bar graph is created on.

        @returns nm: the torque value in Newton-meters. 
        '''
        p1 = 2.754e-10
        p2 = -1.708e-06
        p3 = 0.003764
        p4 = -2.85
        nm= p1*x**3 + p2*x**2 + p3*x + p4
        return nm
    def update_bar(w, n, strain_val):
        '''
        Updates the fingertip torque sensor bar graph by redrawing the bars on the gaph, updating
        the hovering value the bars height, and updating the bar's color. 

        @param w: the canvas the fingertip torque sensor bar graph is created on.

        @param n: the finger number 1,2, 3, or 4 for spread.

        @param strain_val: value of strain from the fingertip force torque sensors in raw encoder format.
        '''
        coordie= w.coords(w.rects[n])
        valie= w.coords(w.vals[n])
        nm= strain_to_nm(strain_val)
        maxval=2
        minval=-maxval
        if nm>= 0:
            if nm<maxval:
                w.coords(w.rects[n], coordie[0], 175, coordie[2], 175-nm*(69.375))
                w.coords(w.vals[n], valie[0], 175-nm*69.375- 10)
                w.itemconfig(w.vals[n], text= round(nm, 3))
            else:
                w.coords(w.rects[n], coordie[0], 175, coordie[2], 175-maxval*(69.375))
                w.coords(w.vals[n], valie[0], 175-maxval*69.375- 10)
                w.itemconfig(w.vals[n], text= round(maxval, 3))
        else:
            if nm>minval:
                w.coords(w.rects[n], coordie[0], 175-nm*(69.375), coordie[2], 175)
                w.coords(w.vals[n], valie[0], 175-nm*(69.375)+ 10)
                w.itemconfig(w.vals[n], text= round(nm, 3))
            else:
                w.coords(w.rects[n], coordie[0], 175-minval*(69.375), coordie[2], 175)
                w.coords(w.vals[n], valie[0], 175-minval*(69.375)+ 10)
                w.itemconfig(w.vals[n], text= round(minval, 3))                
        update_color_strain(w, n, strain_val)

    def strainG_plot(w, x, y):
        '''
        Creates the Fingertip Torque bar graph.

        @param x: the x location of the graph on sensor frame.

        @param y: the y location of the graph on sensor frame.

        @param strain_val: value of strain from the fingertip force torque sensors in raw encoder format.

        '''

        #width of axis lines
        wid= 2
        
        #create x axis
        w.create_line(0, y, 550, y, width= wid)

        #create rectangles
        rect1= w.create_rectangle(90, 175, 190, 175)
        line1= w.create_line(190, 175, 0, 175)
        w.create_text(140, 10, text= "Finger1")

        rect2= w.create_rectangle(240, 175, 340, 175)
        line2= w.create_line(340, 175, 0, 175)
        w.create_text(290, 10, text="Finger2")

        rect3= w.create_rectangle(390, 175, 490, 175)
        line3= w.create_line(490, 175, 0, 175)
        w.create_text(440, 10, text="Finger3")

        #create y axis
        w.create_line(30, 20, 30, 325, width= wid)
        w.create_text(40, 10, text= "Torque (N*m)")
        w.create_text(275, 342, text=" When red, value is saturated and reading is no longer reliable. Refer to pyHand Manual." )

        #highest accurate point on graph
        w.create_text(15, 64, text= "1.6")
        w.create_line(30, 64, 39, 64, width= wid)

        #mid point
        w.create_text(15, y-10, text= "0")

        #lowest accurate point on graph
        w.create_text(15, 288, text= "-1.6")
        w.create_line(30, 288, 39, 288, width= wid)

        #initial values for hovering bar graph values
        val1= w.create_text(140, 160, text="0000")
        val2= w.create_text(290, 160, text="0000")
        val3= w.create_text(440, 160, text="0000")

        w.vals= []
        w.vals.append(val1)
        w.vals.append(val2)
        w.vals.append(val3)        

        w.rects= []
        w.rects.append(rect1)
        w.rects.append(rect2)
        w.rects.append(rect3)


    #===========================CREATING STRAIN TEMP SENSOR DISPLAY=====================

    y1=10
    x1=1

    #create a frame for saturation indicators
    sat_frame= Frame(sensor_tab)

    #creates saturation labels
    strain_frame= LabelFrame(sensor_tab, text= "Fingertip Torque Switches", labelanchor= N, font= font1)

    w = Canvas(strain_frame, width=550, height=350)
    w.grid()

    strainG_plot(w, 50, 175)
    sat_frame.grid(row=y1+1, column=x1, padx=(10,0))
         
    #temperature and strain frame
    ts_frame=LabelFrame(sensor_tab, text="Temperature Sensors", font= font1, labelanchor= N)
    location_lbl=Label(ts_frame,text="Location")
    motor_temp_lbl=Label(ts_frame,text="Motor Temperature (" + u"\N{DEGREE SIGN}"+"C)")
    puck_temp_lbl=Label(ts_frame,text="Puck Temperature (" + u"\N{DEGREE SIGN}"+ "C)" )
    strain_lbl=Label(ts_frame,text="Fingertip Torque Switches (kg*mm)")

    finger1_lbl=Label(ts_frame,text="Finger 1")
    finger2_lbl=Label(ts_frame,text="Finger 2")
    finger3_lbl=Label(ts_frame,text="Finger 3")
    spread_lbl=Label(ts_frame,text="Spread")

    x_pad=20
    y_pad=10

    #=======================CREATING THE LABELS FOR FINGERTIP TORQUE/ TEMPERATURES=======================

    motor_temp1=Label(ts_frame)
    motor_temp2=Label(ts_frame)
    motor_temp3=Label(ts_frame)
    motor_tempS=Label(ts_frame)

    puck_temp1=Label(ts_frame)
    puck_temp2=Label(ts_frame)
    puck_temp3=Label(ts_frame)
    puck_tempS=Label(ts_frame)

    strain1=Label(ts_frame)
    strain2=Label(ts_frame)
    strain3=Label(ts_frame)
    strainS=Label(ts_frame, text= "N/A", fg= "gray")

    sat_label_puck= Label(ts_frame)
    sat_label_motor= Label(ts_frame)
    sat_label_strain= Label(ts_frame)

    #==================GRIDDING THE LABELS FOR FINGERTIP TORQUE/ TEMPERATURES=======================

    puck_temp1.grid(column=2, row=1,sticky="ew")
    puck_temp2.grid(column=2, row=2,sticky="ew")
    puck_temp3.grid(column=2, row=3,sticky="ew")
    puck_tempS.grid(column=2, row=4,sticky="ew")

    motor_temp1.grid(column=1, row=1,sticky="ew")
    motor_temp2.grid(column=1, row=2,sticky="ew")
    motor_temp3.grid(column=1, row=3,sticky="ew")
    motor_tempS.grid(column=1, row=4,sticky="ew")
 
    finger1_lbl.grid(row=1, column=0, pady=(0,y_pad),sticky="ew")
    finger2_lbl.grid(row=2, column=0, pady=(0,y_pad),sticky="ew")
    finger3_lbl.grid(row=3, column=0, pady=(0,y_pad),sticky="ew")
    spread_lbl.grid(row=4, column=0, pady=(0,y_pad),sticky="ew")
    
    sat_label_motor.grid(row=5, column=1,sticky="ew",padx=(0,1))
    sat_label_puck.grid(row=5, column=2,sticky="ew",padx=(0,1))

    location_lbl.grid(row=0, column=0)
    motor_temp_lbl.grid(row=0, column=1, padx=(x_pad,0),pady=y_pad)
    puck_temp_lbl.grid(row=0, column=2,padx=x_pad)

    ts_frame.grid(row = y1, column= x1, padx=(40,35))

    strain_frame.grid(column= 1, row=4 )
    
    #=======================Creating the Start Tactile Sensor Array Button===============================================
        
    font1 = tkFont.Font(size = 12, weight="bold")
    update_data= Button(sensor_tab, text="Start Tactile Sensor Array",   bg="#62CC68",font=font1,command=lambda:toggle(canvas, update_data, sensor_tab, ALL_Fingies, s,strain1, strain2, strain3))
    var_update=BooleanVar()    
    var_update.set(0)
    update_data.var=var_update

    units= Label(sensor_tab, text="Tactile sensors are reported in Newtons/cm^2")

    #makes sure there is a hand connected then proceeds to update the tab.
    if handtype != -1:
        s= HandSensor()
        update(canvas,update_data.var,ALL_Fingies,s,strain1,strain2,strain3,[puck_temp1,puck_temp2,puck_temp3,puck_tempS],[motor_temp1,motor_temp2,motor_temp3,motor_tempS],sat_label_puck, sat_label_motor, sat_label_strain,0, nb, w)
    update_data.grid(column=1,row=11, padx=(10,0), pady=(50,0))
    units.grid(column=1, row=12, padx=(10,0), pady=(10, 0))

    enable_buttons(sensor_tab, tactile, update_data)    
     
    canvas.grid(row=0, column=0) 
    image_frame.grid(row=y,column=x, rowspan=25)
    
           
def create_sensor_tab(nb, tactile, strain, thermister, handtype):
    '''
    Wrapper for populate_sensor_tab. Creates the contents of sensor tab in a tk Frame.

    @param nb: notbook to add tab to.

    @param tactile: tells whether or not the hand model has tactile sensors. 1 if yes, 0 if no and -1 if unkown.

    @param strain: tells whether or not the hand model has fingertip torque sensors. 1 if yes, 0 if no and -1 if unkown.

    @param thermister: tells whether or not the hand model has a thermister. 1 if yes, 0 if no and -1 if unkown.

    @param handtype: hand model identifier. 1 if 280, 0 if 282, and -1 if unkown or no communication with any hand.
    '''
    #frame to hold content
    sensor_frame = tk.Frame(nb, name='sensors')
    
    populate_sensor_tab(sensor_frame, 0,0, tactile, nb, strain, thermister, handtype)

    #nb.bind("<<NotebookTabChanged>>", lambda x:sensor_tab_selected(nb))

    #adding tab to notebook
    nb.add(sensor_frame, text='Sensors', underline=0, padding=2)


