#  scrollable_frame.py
#  
#  ~~~~~~~~~~~~
#  
#  pyHand Frame with Scrollbars
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
class scrollable_frame(Frame):
    """
    A subclass of Frame that becomes scrollable by having a hidden frame inside of a hidden canvas. 

    @cvar canvas: The hidden internal canvas
    @ctype: C{Canvas_Widget}
    
    @cvar internal_frame: A hidden internal frame
    @ctype: C{Frame_Widget}
    
    @cvar hbar: The horizontal scrollbar
    @ctype: C{Scrollbar_Widget}
    
    @cvar vbar: The vertical scrollbar
    @ctype: C{Scrollbar_Widget}
    """
    def __init__(self,master,**kw):
        """
        Creates a scrollable frame object. This is surprisingly more complicated than expected.

        @param self: A scrollable frame instance.
        @type self: C{scrollable_frame_widget}

        @param master: A master widget.
        @type master: C{Widget}
        """
        Frame.__init__(self,master,**kw)
        
        self.canvas=Canvas(self,scrollregion=(0,0,500,500))#,width=300,height=300,scrollregion=(0,0,500,500))
        self.internal_frame=Frame(self.canvas)
        self.hbar=Scrollbar(self,orient=HORIZONTAL)
        self.vbar=Scrollbar(self,orient=VERTICAL)

        interior_id=self.canvas.create_window((0,0),window=self.internal_frame,anchor="nw")

        
        self.hbar.pack(side=BOTTOM,fill=X)
        self.hbar.config(command=self.canvas.xview)
        
        
        self.vbar.pack(side=RIGHT,fill=Y)
        self.vbar.config(command=self.canvas.yview)
        
##        self.canvas.config(width=300,height=300)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas.bind_all("<MouseWheel>",lambda x:self.on_mouse_wheel(x,self.canvas))
        self.canvas.pack(side=LEFT,expand=True,fill=BOTH)

        def _configure_interior(event):
            """
            Figures out how big the interior frame needs to be
            """
            # update the scrollbars to match the size of the inner frame
            size = (self.internal_frame.winfo_reqwidth(), self.internal_frame.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if self.internal_frame.winfo_reqwidth() != self.canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                self.canvas.config(width=self.internal_frame.winfo_reqwidth())
            if self.internal_frame.winfo_reqheight() != self.canvas.winfo_height():
                # update the canvas's width to fit the inner frame
                self.canvas.config(height=self.internal_frame.winfo_reqheight())
        self.internal_frame.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            """
            Figures out how bid the interior canvas needs to be
            """
            if self.internal_frame.winfo_reqwidth() != self.canvas.winfo_width():
##                print "frame",self.internal_frame.winfo_reqwidth()
##                print "canvas",self.canvas.winfo_width()
                # update the inner frame's width to fill the canvas
##                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())
                self.canvas.config(width=self.internal_frame.winfo_reqwidth())
            if self.internal_frame.winfo_reqheight() != self.canvas.winfo_height():
                # update the inner frame's width to fill the canvas
##                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())
                self.canvas.config(height=self.internal_frame.winfo_reqheight())
        self.canvas.bind('<Configure>', _configure_canvas)
    def on_mouse_wheel(self,event,canvas):
        """
        What gets called when the mouse wheel is scrolled
        """
        canvas.yview("scroll",-1*event.delta/100,"units")
        
