#Class taken partially from effbot.org public examples

#  IntegerEntry.py
#  
#  ~~~~~~~~~~~~
#  
#  Entry Field Accepting Only Integers
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

from Tkinter import *

class IntegerEntry(Entry):
    '''
    Creates an IntegerEntry object

    Attributes are:
    standard tkinter Entry atributes, __value, __variable, maxval, and minval

    @cvar master: parent frame of the IntegerEntry
    @type master: tkinter frame (or any variation, such as labelframe) widget

    @cvar textvariable: the control variable of the IntegerEntry
    @type textvariable: tkinter StringVar() or IntVar()

    @cvar maxval: The maximum value that the IntegerEntry will allow to be entered
    @type maxval: C{int}

    @cvar minval: The minimum value that the IntegerEntry will allow to be entered
    @type minval: C{int}
    '''
    def __init__(self, master, textvariable = StringVar(), maxval = None, minval = None, val = "", **kw):
        apply(Entry.__init__, (self, master), kw)
        self.__value = val
        self.__variable = textvariable
        self.__variable.set(self.__value)
        self.__variable.trace("w", self.__callback)
        self.maxval = maxval
        self.minval = minval
        self.config(textvariable=self.__variable)

    def __callback(self, *dummy):
        '''
        This is called every time a new character is entered into the IntegerEntry
        This method calls a validte method to check if the new character should be allowed to stay

        @param *dummy: takes excessive inputs
        @type *dummy: takes inputs and makes an array
        '''
        value = self.__variable.get()
        isGood = self.validate(value)
        if isGood:
            self.__value = value
        self.__variable.set(self.__value)

    def validate(self, value):
        '''
        Takes in a value and sees if the value is valid. To be valid, value must be an int or an empty string.
        If value is valid, this method returns true, otherwise it returns false

        @param value: the value to be tested for validity based on ability to be parsed as an int
        @type value: C{String}
        '''
        try:
            if(value == ""):
                return True
            a = int(value)
            if(self.maxval != None) and (a > self.maxval):
                return False
            if(self.minval != None) and (a < self.minval):
                return False
            return True
        except:
            return False
