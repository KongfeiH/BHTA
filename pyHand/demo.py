#  demo.py
#  
#  ~~~~~~~~~~~~
#  
#  Barrett Hand Demo Example
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

#imports
from pyHand_API.pyHand_api import *

prevMvs = []
prevAccels = []
prevTstops = []

handType = 0

def wait():
    '''
    waits for 0.23 seconds, used in demo
    '''
    time.sleep(0.23)

def setup():
    '''
    Before the demo starts, puck properties need to be changed. This method stores current puck properties to be reset at the end of the demo,
    then sets new properties 
    '''
    global handType
    global prevMvs
    global prevAccels
    
    prevMvs.append(get_property(FINGER1, MV))
    prevMvs.append(get_property(FINGER2, MV))
    prevMvs.append(get_property(FINGER3, MV))
    prevMvs.append(get_property(SPREAD, MV))

    prevAccels.append(get_property(FINGER1, ACCEL))
    prevAccels.append(get_property(FINGER2, ACCEL))
    prevAccels.append(get_property(FINGER3, ACCEL))
    prevAccels.append(get_property(SPREAD, ACCEL))

    prevTstops.append(get_property(FINGER1, TSTOP))
    prevTstops.append(get_property(FINGER2, TSTOP))
    prevTstops.append(get_property(FINGER3, TSTOP))
    prevTstops.append(get_property(SPREAD, TSTOP))

    handType = get_property(FINGER1, HALLS)

    if(handType == 7):
        set_property(FINGER1, MV, 300)
        set_property(FINGER2, MV, 300)
        set_property(FINGER3, MV, 300)
        set_property(SPREAD, MV, 75)

        set_property(FINGER1, ACCEL, 325)
        set_property(FINGER2, ACCEL, 325)
        set_property(FINGER3, ACCEL, 325)
        set_property(SPREAD, ACCEL, 85)

        set_property(FINGER1, TSTOP, 50)
        set_property(FINGER2, TSTOP, 50)
        set_property(FINGER3, TSTOP, 50)
        set_property(SPREAD, TSTOP, 150)
    else:
        set_property(FINGER1, MV, 250)
        set_property(FINGER2, MV, 250)
        set_property(FINGER3, MV, 250)
        set_property(SPREAD, MV, 60)

        set_property(FINGER1, ACCEL, 250)
        set_property(FINGER2, ACCEL, 250)
        set_property(FINGER3, ACCEL, 250)
        set_property(SPREAD, ACCEL, 250)

        set_property(FINGER1, TSTOP, 60)
        set_property(FINGER2, TSTOP, 60)
        set_property(FINGER3, TSTOP, 60)
        set_property(SPREAD, TSTOP, 100)

def start_demo(var):
    '''
    Runs through a sequence of predetermined hand moves. After the completion of each step, a variable is checked, and if the variable is zero,
    meaning a button has been pressed, the demo will stop, call and exit function, and return.

    @param var: the variable that will be checked after each step of the demo to see if the user has hit the Stop Demo button
    @type var: tkinter IntVar()
    '''
    setup()
    #The commented out commands are in grasper control language and are the equivalent to the API calls below them
    while True:
        if(var.get() == 0):
            return exit()
        ##go
        open_grasp()

        if(var.get() == 0):
            return exit()
        ##so
        open_spread()

        if(var.get() == 0):
            return exit()
        ##gc
        close_grasp()

        if(var.get() == 0):
            return exit()
        ##go
        open_grasp()

        if(var.get() == 0):
            return exit()
        ##sc
        close_spread()

        if(var.get() == 0):
            return exit()
        ##gc
        close_grasp()

        if(var.get() == 0):
            return exit()
        ##go
        open_grasp()

        if(var.get() == 0):
            return exit()
        ##1m 55000
        move_to(FINGER1, 55000)

        if(var.get() == 0):
            return exit()
        ##3m 110000
        move_to(FINGER3, 110000)

        if(var.get() == 0):
            return exit()
        ##2m 165000
        move_to(FINGER2, 165000)

        if(var.get() == 0):
            return exit()
        ##o
        open_all()

        if(var.get() == 0):
            return exit()
        ##sc
        close_spread()

        if(var.get() == 0):
            return exit()
        ##gc
        close_grasp()

        if(var.get() == 0):
            return exit()
        ##1o
        open_finger(FINGER1)

        if(var.get() == 0):
            return exit()
        ##3o
        open_finger(FINGER3)

        if(var.get() == 0):
            return exit()
        ##2o
        open_finger(FINGER2)

        if(var.get() == 0):
            return exit()
        ##sm 18000
        move_to(SPREAD, 18000)

        if(var.get() == 0):
            return exit()
        ##12m 130000
        set_property(FINGER1, DP, 130000)
        set_property(FINGER2, DP, 130000)
        set_property(FINGER3, DP, get_position(FINGER3))
        move_grasp()

        if(var.get() == 0):
            return exit()
        ##3c
        close_finger(FINGER3)

        if(var.get() == 0):
            return exit()
        ##go
        open_grasp()

        if(var.get() == 0):
            return exit()
        ##3fset dp 130000
        set_property(FINGER3, 50, 130000)

        if(var.get() == 0):
            return exit()
        ##1fset dp 130000
        set_property(FINGER1, 50, 130000)

        if(var.get() == 0):
            return exit()
        ##2fset dp 68000
        set_property(FINGER2, 50, 68000)

        if(var.get() == 0):
            return exit()
        ##gm
        move_grasp()

        if(var.get() == 0):
            return exit()
        ##1fset dp 68000
        set_property(FINGER1, 50, 68000)

        if(var.get() == 0):
            return exit()
        ##2fset dp 130000
        set_property(FINGER2, 50, 130000)

        if(var.get() == 0):
            return exit()
        ##gm
        move_grasp()

        if(var.get() == 0):
            return exit()
        ##1fset dp 130000
        set_property(FINGER1, 50, 130000)

        if(var.get() == 0):
            return exit()
        ##2fset dp 68000
        set_property(FINGER2, 50, 68000)

        if(var.get() == 0):
            return exit()
        ##gm
        move_grasp()

        if(var.get() == 0):
            return exit()
        ##1fset dp 68000
        set_property(FINGER1, 50, 68000)

        if(var.get() == 0):
            return exit()
        ##2fset dp 130000
        set_property(FINGER2, 50, 130000)

        if(var.get() == 0):
            return exit()
        ##gm
        move_grasp()

        if(var.get() == 0):
            return exit()
        ##1fset dp 130000
        set_property(FINGER1, 50, 130000)

        if(var.get() == 0):
            return exit()
        ##2fset dp 68000
        set_property(FINGER2, 50, 68000)

        if(var.get() == 0):
            return exit()
        ##gm
        move_grasp()

        if(var.get() == 0):
            return exit()
        ##1fset dp 68000
        set_property(FINGER1, 50, 68000)

        if(var.get() == 0):
            return exit()
        ##2fset dp 130000
        set_property(FINGER2, 50, 130000)

        if(var.get() == 0):
            return exit()
        ##gm
        move_grasp()

        if(var.get() == 0):
            return exit()
        ##gm 120000
        move_grasp(120000)

        if(var.get() == 0):
            return exit()
        ##sc
        close_spread()

        if(var.get() == 0):
            return exit()
        ##gc
        close_grasp()

        if(var.get() == 0):
            return exit()
        ##gm 22800
        move_grasp(22800)

        if(var.get() == 0):
            return exit()
        ##sm 11400
        move_to(SPREAD, 11400)

        if(var.get() == 0):
            return exit()
        ##1m 192000
        move_to(FINGER1, 192000)

        if(var.get() == 0):
            return exit()
        ##2m 160000
        move_to(FINGER2, 160000)

        if(var.get() == 0):
            return exit()
        ##3m 130000
        move_to(FINGER3, 130000)

        if(var.get() == 0):
            return exit()
        ##gm 100000
        move_grasp(100000)

        if(var.get() == 0):
            return exit()
        ##o
        open_all()

        if(var.get() == 0):
            return exit()
        ##c
        close_all()

        if(var.get() == 0):
            return exit()
        ##1m 148500
        move_to(FINGER1, 148500)

        if(var.get() == 0):
            return exit()
        ##3m 148500
        move_to(FINGER3, 148500)

        if(var.get() == 0):
            return exit()
        ##2m 148500
        move_to(FINGER2, 148500)

        if(var.get() == 0):
            return exit()
        ##1m 194200
        move_to(FINGER1, 194200)

        if(var.get() == 0):
            return exit()
        ##3m 194200
        move_to(FINGER3, 194200)

        if(var.get() == 0):
            return exit()
        ##2m 194200
        move_to(FINGER2, 194200)

        if(var.get() == 0):
            return exit()
        ##1m 102000
        move_to(FINGER1, 102000)

        if(var.get() == 0):
            return exit()
        ##3m 102000
        move_to(FINGER3, 102000)

        if(var.get() == 0):
            return exit()
        ##2m 102000
        move_to(FINGER2, 102000)

        if(var.get() == 0):
            return exit()
        ##o
        open_all()

        if(var.get() == 0):
            return exit()
        ##4fset ds 7182
        set_property(SPREAD, 60, 7182)

        if(var.get() == 0):
            return exit()
        ##gm 125000
        move_grasp(125000)

        if(var.get() == 0):
            return exit()
        ##gm 45700
        move_grasp(45700)

        if(var.get() == 0):
            return exit()
        ##sic
        close_spread_step()

        if(var.get() == 0):
            return exit()
        ##gm 125000
        move_grasp(125000)

        if(var.get() == 0):
            return exit()
        ##gm 45700
        move_grasp(45700)

        if(var.get() == 0):
            return exit()
        ##sic
        close_spread_step()

        if(var.get() == 0):
            return exit()
        ##gm 125000
        move_grasp(125000)

        if(var.get() == 0):
            return exit()
        ##gm 45700
        move_grasp(45700)

        if(var.get() == 0):
            return exit()
        ##sic
        close_spread_step()

        if(var.get() == 0):
            return exit()
        ##gm 125000
        move_grasp(125000)

        if(var.get() == 0):
            return exit()
        ##gm 45700
        move_grasp(45700)

        if(var.get() == 0):
            return exit()
        ##sic
        close_spread_step()

        if(var.get() == 0):
            return exit()
        ##gm 125000
        move_grasp(125000)

        if(var.get() == 0):
            return exit()
        ##gm 45700
        move_grasp(45700)

        if(var.get() == 0):
            return exit()
        ##sic
        close_spread_step()

        if(var.get() == 0):
            return exit()
        ##c
        close_spread()
        close_grasp()

        #come hither!!!

        open_grasp()
        close_spread()

        if(handType == 0):
            set_property(FINGER1, MV, 300)
            set_property(FINGER2, MV, 300)
            set_property(FINGER3, MV, 300)
            set_property(SPREAD, MV, 150)

            set_property(FINGER1, ACCEL, 300)
            set_property(FINGER2, ACCEL, 300)
            set_property(FINGER3, ACCEL, 300)
            set_property(SPREAD, ACCEL, 200)

            set_property(FINGER1, TSTOP, 50)
            set_property(FINGER2, TSTOP, 50)
            set_property(FINGER3, TSTOP, 50)
            set_property(SPREAD, TSTOP, 150)
        
        for j in range(4):
            if(var.get() == 0):
                return exit()
            
            set_property(FINGER1, E, 195000)
            set_property(FINGER1, MODE, MODE_TRAP)
            wait()

            set_property(FINGER3, E, 195000)
            set_property(FINGER3, MODE, MODE_TRAP)
            wait()

            set_property(FINGER2, E, 195000)
            set_property(FINGER2, MODE, MODE_TRAP)
            time.sleep(0.4)

            if(var.get() == 0):
                return exit()
        
            set_property(FINGER1, E, 0)
            set_property(FINGER1, MODE, MODE_TRAP)
            wait()

            set_property(FINGER3, E, 0)
            set_property(FINGER3, MODE, MODE_TRAP)
            wait()

            set_property(FINGER2, E, 0)
            set_property(FINGER2, MODE, MODE_TRAP)
            time.sleep(0.6)

        if(handType == 0):
            set_property(FINGER1, MV, 250)
            set_property(FINGER2, MV, 250)
            set_property(FINGER3, MV, 250)
            set_property(SPREAD, MV, 60)

            set_property(FINGER1, ACCEL, 250)
            set_property(FINGER2, ACCEL, 250)
            set_property(FINGER3, ACCEL, 250)
            set_property(SPREAD, ACCEL, 250)

            set_property(FINGER1, TSTOP, 60)
            set_property(FINGER2, TSTOP, 60)
            set_property(FINGER3, TSTOP, 60)
            set_property(SPREAD, TSTOP, 100)

def exit():
    '''
    Resets the properties stored earlier by the setup method, and returns None
    '''
    set_property(FINGER1, MV, prevMvs[0])
    set_property(FINGER1, ACCEL, prevAccels[0])
    set_property(FINGER1, TSTOP, prevTstops[0])
    
    set_property(FINGER2, MV, prevMvs[1])
    set_property(FINGER2, ACCEL, prevAccels[1])
    set_property(FINGER2, TSTOP, prevTstops[1])
    
    set_property(FINGER3, MV, prevMvs[2])
    set_property(FINGER3, ACCEL, prevAccels[2])
    set_property(FINGER3, TSTOP, prevTstops[2])
    
    set_property(SPREAD, MV, prevMvs[3])
    set_property(SPREAD, ACCEL, prevAccels[3])
    set_property(SPREAD, TSTOP, prevTstops[3])
    
    return None
