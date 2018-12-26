#  auto_resize.py
#  
#  ~~~~~~~~~~~~
#  
#  Overwrite Notebook class, auto-resize capabilities
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
import ttk as tk

class Notebook(tk.Notebook):
    """
    This is a wrapper for the original tk Notebook with the added feature of having a tab_slaves function which makes recursing easier.
    """
    def __init__(self,**kw):
        tk.Notebook.__init__(self,**kw)
        self.tab_slave_list=[]
    def add(self,child,**kw):
        """
        Add was been overwritten to keep track of all children tabs.
        """
        self.tab_slave_list.append(child)
        tk.Notebook.add(self,child,**kw)
    def tab_slaves(self):
        """
        Returns all child tabs
        """
        return self.tab_slave_list
        
def is_container(widget):
    """
    Determines whether a widget is a container or not.
    A widget is a container if it is a frame of any kind or a Notebook.

    @param widget: Any widget
    @type widget: C{Widget}

    @return: True or False if it is a container or not
    @rtype: C{Boolean}
    """
    return (widget.winfo_class()=="TLabelframe" or widget.winfo_class()=="TFrame" or widget.winfo_class()=="Frame" or widget.winfo_class()=="Labelframe" or widget.winfo_class()=="TNotebook")

def auto_resize_list(widget_list,parent_notebook):
    """
    Calls auto_resize_widget on every element in the given widget list.

    @param widget_list: A list of widgets
    @type widget_list: C{[Widget...(x)]}

    @param parent_notebook: The parent notebook
    @type parent_notebook: C{Notebook_Widget}
    """
    for widget in widget_list:
        auto_resize_widget(widget,parent_notebook)

def auto_resize_widget(widget,parent_notebook):
    """
    Recursively stickys all widgets to nesw and configures all columns and rows to resize via weight=1.
    
    @param widget: A widget
    @type widget: C{Widget}

    @param parent_notebook: The parent notebook
    @type parent_notebook: C{Notebook_Widget}
    """
    if widget==None:
        return
    if not parent_notebook:
        widget.grid(sticky="nesw")
    elif is_container(widget):
        maxx,maxy=widget.grid_size()
        for x in range(maxx):
            Grid.columnconfigure(widget,x,weight=1)
        for y in range(maxy):
            Grid.rowconfigure(widget,y,weight=1)
        children=widget.grid_slaves()+widget.pack_slaves()
        if children!=[]:
            auto_resize_list(children,False)
        elif widget.winfo_class()=="TNotebook":
            auto_resize_list(widget.tab_slaves(),True)

