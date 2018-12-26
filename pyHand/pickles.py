#  gui_main.py
#  
#  ~~~~~~~~~~~~
#  
#  pyHand Pickle File
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

import pickle

#puck_dic={}
#group_id={}
#puck_command_dic={}

def load_puck_commands():
    """
    Attempts to load puck commands from Memory folder
    """
    
    try:
        #global puck_command_dic
        puck_command_dic=pickle.load(open("Memory/Pickle/puck_commands_dic.p","rb"))
        return puck_command_dic
        
    except:
        print"Error: Puck Commands Pickle File 'puck_commands_dic.p' Not Found"
def load_puck_units():
    """
    Attempts to load all puck properties from Memory folder
    """
    try:
        #global puck_dic
        puck_dic=pickle.load( open( "Memory/Pickle/puck_dic.p", "rb" ) )
        return puck_dic
    except:
        print"Error: Puck Pickle File 'puck_dic.p' Not Found"
def load_group_id():
    """
    Loads all group id's from Memory folder
    """
    try:
        #global group_id
        group_id=pickle.load(open("Memory/Pickle/group_id_dic.p","rb"))
        return group_id
    except:
        print"Error: Group ID Pickle File 'group_id_dic' Not Found"

puck_commands=load_puck_commands() 
puck_units=load_puck_units()   
group_id=load_group_id()
